#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Setup requirements

try:
    from setuptools import find_packages, setup
    from setuptools.command.install import install
except ImportError:
    print(
        "setuptools is needed in order to build. Install it using your package manager (usually python-setuptools) or via pip (pip install setuptools)."
    )
    sys.exit(1)

# Extra requirements installable using pip -e '.[<extra>]'
EXTRAS_REQUIRE = {
    "tests": [
        "tox",
        "black>=20.8b1,<21",
        "flake8>=3.7.9",
        "isort>=5.6.0,<5.7.0",
        "pytest-cov>=2.8.1",
        "pytest-datafiles>=2.0",
        "pytest-env>=0.6.2",
        "pytest-logger>=0.5.1",
        "pytest-mock>=2.0.0",
        "pytest-runner>=5.2",
        "pytest-xdist>=1.31.0",
        "pytest>=5.2.2",
    ],
}

# Development requirements
EXTRAS_REQUIRE["dev"] = EXTRAS_REQUIRE["tests"] + ["pre-commit", "twine"]

setup(
    name="vshot",
    author="Florian Dambrine",
    url="https://github.com/Lowess/vshot",
    author_email="android.florian@gmail.com",
    long_description_content_type="text/markdown",
    long_description="# VShot - Take Visual screenshots on the Web",
    version="0.0.1",
    install_requires=["Pillow", "boto3", "selenium>=3.141.0,<3.142.0"],
    package_dir={"": "lib"},
    packages=find_packages("lib"),
    package_data={},
    scripts=["bin/vshot"],
    zip_safe=False,
    extras_require=EXTRAS_REQUIRE,
)
