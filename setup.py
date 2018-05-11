#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Script Name: setup.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This script will build executable file.

"""
# -------------------------------------------------------------------------------------------------------------
""" Check data flowing """
# print("Import from modules: {file}".format(file=__name__))
# print("Directory: {path}".format(path=__file__.split(__name__)[0]))
__root__ = "PLT_RT"
# -------------------------------------------------------------------------------------------------------------
""" Import """
import os
import sys

from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

os.environ[__root__] = os.getcwd()
from __init__ import (__pkgsReq__, __readme__, __appname__, __version__, __licence__, __author__, __modules__,
                      __classifiers__, __description__, __download__, __email__, __packages__, __pkgsDir__, __website__)

for dir in os.listdir(os.getenv(__root__)):
    pltPth = os.path.join(os.getenv(__root__), dir)
    if os.path.isdir(pltPth):
        if not pltPth in sys.path:
            sys.path.append(pltPth)

with open(__readme__, 'r') as f:
    readme = f.read()

includes = ["atexit", "re"]

setup(
    name = __appname__,
    version = __version__,
    packages = __packages__,
    package_dir = __pkgsDir__,
    url = __website__,
    download_url = __download__,
    license = __licence__,
    author = __author__,
    author_email=__email__,
    maintainer = __author__,
    maintainer_email = __author__,
    description = __description__,
    long_description = readme,
    py_modules = __modules__,
    install_requires = __pkgsReq__,
    classifiers = __classifiers__,
    options = {"build_exe" : {"includes" : includes }},
    executables = [Executable("Plt.py", base = base)]
)
