#!/usr/bin/env python
from pathlib import Path

from setuptools import setup


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


setup(version=get_version())
