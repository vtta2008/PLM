# -*- coding: utf-8 -*-
"""

Script Name: setup.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This script will build executable file.

"""
# -------------------------------------------------------------------------------------------------------------
""" Setup envronment key to be able to work """

import os
from core.Metadata import __envKey__
ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)))

try:
    os.getenv(__envKey__)
except KeyError:
    os.environ[__envKey__]      = ROOT
else:
    if os.getenv(__envKey__)   != ROOT:
        os.environ[__envKey__]  = ROOT

from core.Configurations import Configurations
cfg                             = Configurations(__envKey__, ROOT)

# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python

import sys
import setuptools
from cx_Freeze import setup, Executable

# PLM
from appData import (LICENCE_MIT, ABOUT, DESKTOP_DIR, __envKey__, __project__, __version__, __plmSlogan__, __website__,
                     __download__, __author1__, __author2__, __email__, __modules__, __pkgsReq__, __classifiers__,
                     __packages_dir__, COPYRIGHT)

print(DESKTOP_DIR)

os.environ['TCL_LIBRARY']   = "C:/ProgramData/Anaconda3/tcl/tcl8.6"
os.environ['TK_LIBRARY']    = "C:/ProgramData/Anaconda3/tcl/tk8.6"

application_title = __project__
main_python_file = "PLM.py"

if not cfg.cfgs:
    print("Configurations has not completed yet!")
else:
    print("Configurations has completed")

if sys.platform == "win32":
    base = "Win32GUI"
else:
    base = None

from core.Loggers import SetLogger
logger = SetLogger(__file__)
report = logger.report

for dir in os.listdir(os.getenv(__envKey__)):
    pltPth = os.path.join(os.getenv(__envKey__), dir)
    if os.path.isdir(pltPth):
        if not pltPth in sys.path:
            sys.path.append(pltPth)
            print(pltPth)

with open('README.rst', 'r') as f:
    readme = f.read()

includes = ['imgs']

excludes = ["tkinter"]

packages = __packages_dir__

build_exe_options = {'includes': includes, 'packages':packages, 'excludes':excludes, }      #'include_files': includefiles,}

setup(  name = application_title,

        version          = __version__     , packages          = setuptools.find_packages(),
        url              = __website__     , download_url      = __download__    , license          = LICENCE_MIT,
        author           = __author1__ + " & " + __author2__                     , author_email     = __email__  ,
        maintainer       = __author1__     , maintainer_email  = __author1__     , description      = ABOUT      ,
        long_description = readme          , py_modules        = __modules__     , install_requires = __pkgsReq__,
        classifiers      = __classifiers__ , package_dir       = {"": "src"}     , zip_safe         = False      ,

        keywords                = __plmSlogan__                     ,
        options                 = {"build_exe" : build_exe_options} ,

        executables = [Executable(main_python_file, base=base, icon=["scr/imgs/logo/Plm/icons/32x32.png"], copyright=COPYRIGHT)],
)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 2:26 AM
# © 2017 - 2018 DAMGteam. All rights reserved