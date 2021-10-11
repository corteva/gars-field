#!/usr/bin/env python
from itertools import chain
from pathlib import Path

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()


def get_version():
    """
    retreive gars_field version information in version variable
    (taken from pyproj)
    """
    with open(Path("gars_field", "_version.py")) as vfh:
        for line in vfh:
            if line.find("__version__") >= 0:
                # parse __version__ and remove surrounding " or '
                return line.split("=")[1].strip()[1:-1]
    raise SystemExit("ERROR: gars_field version not found.")


test_requirements = ["pytest-cov"]
extras_require = {"dev": test_requirements}
extras_require["all"] = list(chain.from_iterable(extras_require.values()))

setup(
    name="gars_field",
    author="gars-field Contributors",
    author_email="alansnow21@gmail.com",
    version=get_version(),
    url="https://github.com/corteva/gars-field",
    packages=find_packages(),
    long_description=readme,
    tests_require=test_requirements,
    install_requires=[
        "shapely",
        "pyproj>=3.0.0",
    ],
    extras_require=extras_require,
    python_requires=">=3.8",
)
