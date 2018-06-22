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
import pickle

from importlib import reload as r

import platform
from PyQt5 import QtCore

from appData._path import *
from appData._docs import *
from appData._keys import *
from appData._layout import *
from appData._format import *
from appData._pref import *
from appData._rcSQL import *
from appData._meta import *
PLATFORM = 'Windows'
API_MINIMUM = 0.64

from appData import _path as p
from appData import _meta as m

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
README = PLM_ABOUT

dirLst = [CONFIGLOCALDAMGDIR, PLMCONFIGLOCAL, CONFIGDIR, SETTINGDIR, LOGDIR, CACHEDIR, PREFDIR, USERPREFDIR]

for pth in dirLst:
    if not os.path.exists(pth):
        os.mkdir(pth)

if not os.path.exists(DBPTH):
    GenerateResource()

class SafeSaver(object):
    """A safe saver to disk.
    It saves to a .tmp and moves into final destination, and other
    considerations.
    """

    def __init__(self, fname):
        self.fname = fname
        self.tmp = fname + ".tmp"
        self.fh = None

    def __enter__(self):
        self.fh = open(self.tmp, 'wb')
        return self.fh

    def __exit__(self, *exc_data):
        self.fh.close()

        # only move into final destination if all went ok
        if exc_data == (None, None, None):
            if os.path.exists(self.fname):
                # in Windows we need to remove the old file first
                os.remove(self.fname)
            os.rename(self.tmp, self.fname)

def load_appInfo():
    if not os.path.exists(mainConfig):
        from appData.LocalCfg import LocalCfg
        logger.info("Storing local config")
        LocalCfg()
    # Load info from file

    logger.info("Loading local config")
    with open(mainConfig, 'r') as f:
        appInfo = json.load(f)
    return appInfo

def load_iconInfo():
    if not os.path.exists(mainConfig):
        from appData.LocalCfg import LocalCfg
        logger.info("Storing local icon")
        LocalCfg()
    logger.info("Loading local icon")
    with open(appIconCfg, 'r') as f:
        iconInfo = json.load(f)
    return iconInfo

APPINFO = load_appInfo()
ICONINFO = load_iconInfo()

class Configurations(object):
    """The configuration."""

    # config options, with their default
    _config_options = {
        'BOT_AUTH_TOKEN': '',
        'POLLING_TIME': 30,
        'USER_ALLOWED': None,
        'COL_ORDER': []
    }

    def __init__(self):
        self._needs_save = 0
        FILEPATH = os.path.join(CONFIGDIR, 'PLM.cfg')

        if not os.path.exists(FILEPATH):
            # default to an empty dict
            logger.debug("File not found, starting empty")
            self._data = {}
            return

        with open(FILEPATH, 'rb') as fh:
            self._data = pickle.load(fh)
        logger.debug("Loaded: %s", self._data)

        self.fix_environment()
        self.setup_dependancies()

    def __getattr__(self, key):
        return self._data.get(key, self._config_options[key])

    def __setattr__(self, key, value):
        if key in self._config_options:
            if key not in self._data or self._data[key] != value:
                self._data[key] = value
                self._needs_save += 1
        else:
            if key.startswith('_'):
                super().__setattr__(key, value)
            else:
                raise AttributeError

    def fix_environment(self):
        """Add enviroment variable on Windows systems."""
        from PyQt5 import __file__ as pyqt_path
        if system() == "Windows":
            pyqt = os.path.dirname(pyqt_path)
            qt_platform_plugins_path = os.path.join(pyqt, "plugins")
            os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qt_platform_plugins_path

    def setup_dependancies(self):
        dpc = ['nodegraph', 'lauescript']
        for i in dpc:
            pth = os.path.join(p.COREDIR, i)
            pths = os.getenv('PYTHONPATH') + ';' + pth
            os.environ['PYTHONPATH'] = pths
            print(os.getenv('PYTHONPATH'))

    def save(self):
        """Save the config to disk."""
        if self._needs_save:
            logger.debug("Saving: %s", self._data)
            with SafeSaver(FILEPATH) as fh:
                pickle.dump(self._data, fh)
                self._needs_save = 0

Configurations()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 10:56 PM
# Pipeline manager - DAMGteam
