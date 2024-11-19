# ------------------------------------------------------------------------------
# Copyright (c) Acoular Development Team.
# ------------------------------------------------------------------------------
"""Implements snapshot testing of frequency beamformers."""

import acoular as ac
import pytest
from pytest_cases import parametrize_with_cases

from tests.cases.test_fbeamform_cases import Beamformer

TEST_PARAMS_F_NUM = [pytest.param(8000, 3, id='8kHz-3rd-oct')]


@pytest.mark.parametrize(('f', 'num'), TEST_PARAMS_F_NUM)
@parametrize_with_cases('beamformer', cases=Beamformer)
def test_beamformer(snapshot, beamformer, f, num):
    """Performs snapshot testing with snapshot fixture from pytest-regtest.

    Uses the beamformer cases defined in class Beamformer from test_fbeamform_cases.py

    To overwrite all snapshots produced by this test, run:
    ```bash
    pytest -v --regtest-reset tests/regression/test_fbeamform.py::test_beamformer
    ```

    To overwrite a specific snapshot, run:
    ```bash
    pytest -v --regtest-reset tests/regression/test_fbeamform.py::test_beamformer[<node_id>]
    ```

    Parameters
    ----------
    snapshot : pytest-regtest snapshot fixture
        Snapshot fixture to compare results
    beamformer : instance of acoular.fbeamform.BeamformerBase
        Beamformer instance to be tested (cases from Beamformer)
    f : int
        Frequency to test
    num : int
        Bandwidth to test (1: octave)

    """
    if isinstance(beamformer, ac.BeamformerCMF) and beamformer.method == 'Split_Bregman':
        pytest.xfail("ImportError: cannot import name 'SplitBregman' from 'pylops'")

    if isinstance(beamformer, ac.BeamformerCMF) and beamformer.method == 'FISTA':
        pytest.xfail("'ImportError: cannot import name 'FISTA' from 'pylops'")

    if isinstance(beamformer, ac.BeamformerGIB) and beamformer.method == 'NNLS':
        pytest.xfail('RuntimeError: Maximum number of iterations reached')

    if isinstance(beamformer, ac.BeamformerGIB) and beamformer.method == 'LassoLarsBIC':
        # Requires number of samples (eigenvalues) to be greater than number of features (grid
        # points). Otherwise noise variance estimate is needed.
        pytest.xfail('ValueError: The number of samples must be larger than the number of features with LassoLarsBIC.')

    beamformer.cached = False
    result = beamformer.synthetic(f, num)
    assert ac.L_p(result.sum()) > 0
    snapshot.check(result, rtol=5e-5, atol=5e-8)  # uses numpy.testing.assert_allclose