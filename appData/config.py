# -*- coding: utf-8 -*-
"""

Script Name: config.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os
import json
import pickle

from importlib import reload as r

# Plm
from appData import logger as l

logger = l.online_exception_logging()

from appData._path import *
from appData._docs import *
from appData._keys import *
from appData._meta import *
from appData._layout import *
from appData._format import *
from appData._pref import *
from appData._rcSQL import *

from utilities import utils as func
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

dirLst = [CONFIGLOCALDAMGDIR, PLMCONFIGLOCAL, CONFIGDIR, SETTINGDIR, LOGDIR, FORMATDIR, CACHEDIR, PREFDIR, USERPREFDIR]

for pth in dirLst:
    if not os.path.exists(pth):
        os.mkdir(pth)

if not os.path.exists(DBPTH):
    GenerateResource()

def load_appInfo():
    if not os.path.exists(mainConfig):
        from appData import LocalCfg
        cfg = reload_module(LocalCfg)
        cfg.LocalCfg()
    # Load info from file
    with open(mainConfig, 'r') as f:
        appInfo = json.load(f)
    return appInfo

def load_iconInfo():
    with open(appIconCfg, 'r') as f:
        iconInfo = json.load(f)
    return iconInfo

APPINFO = load_appInfo()
ICONINFO = load_iconInfo()

# --------------------------------------------------------------------------------------------------------------
""" Combine config data """

pVERSION = dict(autodesk=autodeskVer, adobe=adobeVer, foundry=foundryVer, pixologic=pixologiVer,
                sizefx=sizefxVer, office=officeVer, jetbrains=jetbrainsVer)

pPACKAGE = dict(autodesk=autodeskApp, adobe=adobeApp, foundry=foundryApp, pixologic=pixologiApp,
                sizefx=sizefxApp, office=officeApp, jetbrains=jetbrainsApp)

pTRACK = dict(TDS=TRACK_TDS, VFX=TRACK_VFX, ART=TRACK_ART, Office=TRACK_OFFICE, Dev=TRACK_DEV,
              Tools=TRACK_TOOLS, Extra=TRACK_EXTRA, sysTray=TRACK_SYSTRAY, )

# --------------------------------------------------------------------------------------------------------------
""" Store config data """

def generate_key_packages(*args):
    keyPackage = []
    for k in pPACKAGE:
        for name in pPACKAGE[k]:
            for ver in pVERSION[k]:
                if name == 'Hiero' or name == 'HieroPlayer':
                    key = name + ver
                else:
                    key = name + " " + ver
                keyPackage.append(key)

    return keyPackage + otherApp + anacondaApp + CONFIG_APPUI + ['Word', 'Excel', 'PowerPoint']

def generate_config(key, *args):
    keyPackages = generate_key_packages()
    keys = []
    for k in keyPackages:
        for t in pTRACK[key]:
            if t in k:
                keys.append(k)
    return list(sorted(set(keys)))

KEYPACKAGE = generate_key_packages()

# Toolbar config
CONFIG_TDS = generate_config('TDS')
CONFIG_VFX = generate_config('VFX')
CONFIG_ART = generate_config('ART')

# Tab 1 sections config
CONFIG_OFFICE = generate_config('Office')
CONFIG_DEV = generate_config('Dev') + ['Command Prompt']
CONFIG_TOOLS = generate_config('Tools')
CONFIG_EXTRA = generate_config('Extra')
CONFIG_SYSTRAY = generate_config('sysTray')

FILEPATH = os.path.join(CONFIGDIR, "PLM.cfg")

class _Config(object):
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

        if not os.path.exists(FILEPATH):
            # default to an empty dict
            logger.debug("File not found, starting empty")
            self._data = {}
            return

        with open(FILEPATH, 'rb') as fh:
            self._data = pickle.load(fh)
        logger.debug("Loaded: %s", self._data)

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

    def save(self):
        """Save the config to disk."""
        if self._needs_save:
            logger.debug("Saving: %s", self._data)
            with func.SafeSaver(FILEPATH) as fh:
                pickle.dump(self._data, fh)
                self._needs_save = 0


config = _Config

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 10:56 PM
# Pipeline manager - DAMGteam
