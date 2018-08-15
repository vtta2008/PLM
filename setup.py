# -*- coding: utf-8 -*-
"""

Script Name: setup.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This script will build executable file.

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os
import sys
import pprint
import setuptools
from cx_Freeze import setup, Executable

# PLM
from core.Metadata import (appKey, __project__, __version__, __packages_dir__, __website__, __download__,
                           __author1__, __author2__, __email__, __modules__, __pkgsReq__, __classifiers__)
from core.Configurations import Configurations
from appData import LICENCE_MIT, ABOUT

key = appKey
ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)))

try:
    os.getenv(key)
except KeyError:
    os.environ[key] = ROOT
else:
    if os.getenv(key) != ROOT:
        os.environ[key] = ROOT

cfg = Configurations(key, ROOT)

if not cfg.cfgs:
    print("Configurations has not completed yet!")
else:
    print("Configurations has completed")

if sys.platform == "win32":
    base = "Win32GUI"
else:
    base = None

for dir in os.listdir(os.getenv(appKey)):
    pltPth = os.path.join(os.getenv(appKey), dir)
    if os.path.isdir(pltPth):
        if not pltPth in sys.path:
            sys.path.append(pltPth)

with open('README.rst', 'r') as f:
    readme = f.read()

includefiles = ["appData.docs.ABOUT", "appData.docs.CODECONDUCT", "appData.docs.CONTRIBUTING", "appData.docs.CREDIT",
                "appData.docs.LICENCE_MIT", "appData.docs.QUESTION", "appData.docs.REFERENCE", "appData.ED.json",
                "preSetup.krita-x64-4.1.1-setup.exe", "preSetup.storyboarder-setup-1.7.1.exe", "qss.darkstyle.qss",
                "qss.nuke.qss", "qss.stylessheet.qss"]
includes = ["PyQt5", "tankers"]
excludes = ["Tkinter"]
packages = ['os', 'sys', 'subprocess', 'logging', 'requests', 'ctypes', 'pprint', 're', 'platform', 'winshell', 'json',
            'yaml', 'linecache', 'datetime', 'time', 'uuid', 'win32api', 'traceback', 'unittest', 'pbd', 'sqlite3',
            'types', 'shutil', 'enum', 'pkg_resources', '__future__', 'random', 'importlib']

build_exe_options = {'includes':includes, 'packages':packages, 'excludes':excludes, 'include_files':includefiles}

setup(
    name = __project__,
    version = __version__,
    packages = setuptools.find_packages(),
    package_dir = __packages_dir__,
    url = __website__,
    download_url = __download__,
    license = LICENCE_MIT,
    author = __author1__ + "&" + __author2__,
    author_email= __email__,
    maintainer = __author1__,
    maintainer_email = __author1__,
    description = ABOUT,
    long_description = readme,
    py_modules = __modules__,
    install_requires = __pkgsReq__,
    classifiers = __classifiers__,
    options = {"build_exe" : build_exe_options},
    executables = [Executable("PLM.py", base=base)],
)
