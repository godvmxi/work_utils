#!/usr/bin/env python3
from distutils.core import setup, Extension
from Cython.Build import cythonize
setup(
    name = "diags_utils",
    version = '0.1.0',
    author="Bright Jiang",
    ext_modules = cythonize(["email_utils.py"])

)