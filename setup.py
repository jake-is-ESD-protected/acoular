from setuptools import setup, find_packages

setup(
    name="acoular",
    version="24.07",
    description="Python library for acoustic beamforming",
    long_description="README.md",
    author="Acoular Development Team",
    author_email="info@acoular.org",
    url="https://acoular.org",
    download_url="https://github.com/acoular/acoular",
    license="BSD License",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.6"
    ],
    keywords="acoustics beamforming microphone array",
    packages=find_packages(),
    install_requires=[
        "numba",
        "numpy<2.0",
        "scipy>=1.1.0",
        "scikit-learn",
        "tables>=3.4.4",
        "traits>=6.0"
    ]
)