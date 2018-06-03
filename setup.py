# -*- coding: utf-8 -*-
"""

Script Name: setup.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This script will build executable file.

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
import os
import sys
import setuptools
from cx_Freeze import setup, Executable

import appData as app
from utilities import utils as func

base = None

if sys.platform == "win32":
    base = "Win32GUI"

os.environ[app.__envKey__] = os.getcwd()

for dir in os.listdir(os.getenv(app.__envKey__)):
    pltPth = os.path.join(os.getenv(app.__envKey__), dir)
    if os.path.isdir(pltPth):
        if not pltPth in sys.path:
            sys.path.append(pltPth)

with open('README.rst', 'r') as f:
    readme = f.read()

includes = ["atexit", "re"]

setup(
    name = app.__project__,
    version = app.__version__,
    packages = setuptools.find_packages(),
    package_dir = app.__packages_dir__,
    url = app.__website__,
    download_url = app.__download__,
    license = func.query_metadata("__licence__"),
    author = func.query_metadata("__author__"),
    author_email= func.query_metadata("__email__"),
    maintainer = func.query_metadata("__author__"),
    maintainer_email = func.query_metadata("__email__"),
    description = func.query_metadata("__description__"),
    long_description = readme,
    py_modules = func.query_metadata("__modules__"),
    install_requires =func.query_metadata("__description__"),
    classifiers = func.query_metadata("__classifiers__"),
    options = {"build_exe" : {"includes" : includes }},
    executables = [Executable("Plt.py", base = base)],
)
