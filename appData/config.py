# -*- coding: utf-8 -*-
"""

Script Name: config.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python

from platform import system
import json

from importlib import reload as r

from appData.scr._path import *

dirLst = [CONFIG_LOCAL_DAMG_DIR, CONFIG_LOCAL_PLM_DIR, CONFIG_DIR, SETTING_DIR, LOG_DIR, REG_DIR, CACHE_DIR, PREF_DIR, USER_PREF_DIR]

for pth in dirLst:
    if not os.path.exists(pth):
        os.mkdir(pth)

from appData.LocalCfg import LocalCfg

localCfg = LocalCfg()

from appData.scr._docs import *
from appData.scr._keys import *
from appData.scr._layout import *
from appData.scr._format import *
from appData.scr._pref import *
from appData.scr._rcSQL import *
from appData.scr._meta import *

PLATFORM = 'Windows'
API_MINIMUM = 0.64

from appData.scr import _path as p
from appData.scr import _meta as m

__envKey__ = p.__envKey__

# -------------------------------------------------------------------------------------------------------------
""" DAMG team """

__organization__ = m.__organization__
__damgSlogan__ = m.__damgSlogan__
__website__ = m.__website__
__author1__ = m.__author1__
__author2__ = m.__author2__
__Founder__ = m.__author1__
__CoFonder1__ = m.__author2__
__email1__ = m.__email1__
__email2__ = m.__email2__

# -------------------------------------------------------------------------------------------------------------
""" PipelineTool """

__project__ = m.__project__
__appname__ = m.__appname__
__appShortcut__ = m.__appShortcut__
__version__ = m.__version__
__cfgVersion__ = m.__cfgVersion__
__verType__ = m.__verType__
__reverType__ = m.__reverType__
__about__ = m.__about__
__homepage__ = m.__homepage__
__plmSlogan__ = m.__plmSlogan__
__plmWiki__ = m.__plmWiki__

# -------------------------------------------------------------------------------------------------------------
""" Server """

__serverLocal__ = m.__serverLocal__
__serverUrl__ = m.__serverUrl__
__serverCheck__ = m.__serverCheck__
__serverAutho__ = m.__serverAutho__

__google__ = m.__google__

__email__ = m.__email__

__packages_dir__ = m.__packages_dir__
__classifiers__ = m.__classifiers__
__download__ = m.__download__
__description__ = m.__description__
__readme__ = m.__readme__
__modules__ = m.__modules__
__pkgsReq__ = m.__pkgsReq__

# ----------------------------------------------------------------------------------------------------------- #

def reload_module(module):
    return r(module)

def read_file(filePth):
    with open(filePth, 'r') as f:
        data = f.read()
    return data

QUESTIONS = read_file(QUESTIONS)
ABOUT = read_file(ABOUT)
CREDIT = read_file(CREDIT)
CODECONDUCT = read_file(CODECONDUCT)
CONTRIBUTING = read_file(CONTRIBUTING)
REFERENCE = read_file(REFERENCE)
LICENSE_MIT = read_file(LICENSE_MIT)

if not os.path.exists(DB_PTH):
    GenerateResource()

def fix_environment():
    """Add enviroment variable on Windows systems."""
    from PyQt5 import __file__ as pyqt_path
    if system() == "Windows":
        pyqt = os.path.dirname(pyqt_path)
        qt_platform_plugins_path = os.path.join(pyqt, "plugins")
        os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qt_platform_plugins_path

def load_appInfo():
    if not os.path.exists(mainConfig):
        from appData.LocalCfg import LocalCfg
        # logger.info("Storing local config")
        LocalCfg()
    # Load info from file

    # logger.info("Loading local config")
    with open(mainConfig, 'r') as f:
        appInfo = json.load(f)
    return appInfo

def load_iconInfo():
    if not os.path.exists(mainConfig):
        from appData.LocalCfg import LocalCfg
        LocalCfg()
    with open(appIconCfg, 'r') as f:
        iconInfo = json.load(f)
    return iconInfo

fix_environment()
APPINFO = load_appInfo()
ICONINFO = load_iconInfo()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 10:56 PM
# Pipeline manager - DAMGteam
