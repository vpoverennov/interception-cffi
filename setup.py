#!/usr/bin/env python
import sys

from setuptools import setup

import build_interception
import build_utils

setup(
    ext_modules=[
        build_interception.ffibuilder.distutils_extension(),
        build_utils.ffibuilder.distutils_extension(),
    ],
)
