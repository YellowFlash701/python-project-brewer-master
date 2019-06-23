#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Setup script for python-brewer: a Homebrew formula template generator for Python packages.
"""

import re
from io import open
import os.path
from setuptools import setup


def read_file(filename):
    full_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)
    with open(full_path, "rt", encoding="utf-8") as f:
        lines = f.readlines()
    return lines


def get_version():
    pattern = re.compile(r"__version__ = \"(?P<version>[0-9.a-zA-Z-]+)\"")
    for line in read_file(os.path.join("pythonbrewer", "__init__.py")):
        m = pattern.match(line)
        if m is not None:
            return m.group('version')
    raise ValueError("Cannot extract version number for python-brewer")


setup(
    name="python-brewer",
    version=get_version(),
    description="A Homebrew formula template generator for Python packages",
    long_description="".join(read_file("README.rst")),
    author="Thane Thomson",
    author_email="connect@thanethomson.com",
    url="https://github.com/thanethomson/python-brewer",
    install_requires=[r.strip() for r in read_file("requirements.txt") if len(r.strip()) > 0],
    entry_points={
        'console_scripts': [
            'pybrew = pythonbrewer.cmdline:main',
        ]
    },
    license='MIT',
    packages=["pythonbrewer"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities"
    ]
)
