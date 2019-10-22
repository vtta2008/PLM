# -*- coding: utf-8 -*-
"""

Script Name: path.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python

import os

# PLM
from appData.metadatas import __appname__, __groupname__, __envKey__

# -------------------------------------------------------------------------------------------------------------
""" Directory local system """

PROGRAM86                   = os.getenv('PROGRAMFILES(X86)')
PROGRAM64                   = os.getenv('PROGRAMW6432')
LOCALAPPDATA                = os.getenv('LOCALAPPDATA')
PROGRAMDATA                 = os.getenv('PROGRAMDATA')
DESKTOP_DIR                 = os.path.join(os.environ["HOMEPATH"], "desktop")           # Desktop path

# -------------------------------------------------------------------------------------------------------------
""" Name variables """

config                      = 'configuration'
logs                        = 'logs'
cache                       = 'cache'
settings                    = 'settings'
reg                         = 'reg'
nodegraph                   = 'nodegraph'
userPrefs                   = 'userPrefs'
prefs                       = 'prefs'

# -------------------------------------------------------------------------------------------------------------
""" Name variables """

print(os.getenv(__envKey__))

ROOT_DIR                    = os.path.join(os.getenv(__envKey__))

CFG_DIR                     = os.path.join(ROOT_DIR, 'appData', '.config')

CONFIG_LOCAL_DAMG_DIR       = os.path.join(CFG_DIR, __groupname__)                      # DAMG team directory
CONFIG_LOCAL_PLM_DIR        = os.path.join(CFG_DIR, __appname__)                        # Plm directory
CONFIG_DIR                  = os.path.join(CFG_DIR, 'common')                           # Config dir to store config info

SETTING_DIR                 = os.path.join(CONFIG_LOCAL_PLM_DIR, settings)              # Setting dir
LOG_DIR                     = os.path.join(CONFIG_LOCAL_PLM_DIR, logs)                  # Log dir
CACHE_DIR                   = os.path.join(CONFIG_LOCAL_PLM_DIR, cache)                 # Cache dir

NODEGRAPH_DIR               = os.path.join(CONFIG_DIR, nodegraph)                       # Nodegraph dir
PREF_DIR                    = os.path.join(CONFIG_DIR, prefs)                           # Preferences dir
USER_PREF_DIR               = os.path.join(CONFIG_DIR, userPrefs)                       # User preferences dir

# -------------------------------------------------------------------------------------------------------------
""" App (python) """

APP_DATA_DIR                = os.path.join(ROOT_DIR, 'appData')
BUILD_DIR                   = os.path.join(ROOT_DIR, 'build')
IMG_DIR                     = os.path.join(ROOT_DIR, 'imgs')
PLUGIN_DIR                  = os.path.join(ROOT_DIR, 'plugins')
UI_DIR                      = os.path.join(ROOT_DIR, 'ui')
TEST_DIR                    = os.path.join(ROOT_DIR, 't')
DB_DIR                      = APP_DATA_DIR
# -------------------------------------------------------------------------------------------------------------
""" App (Non python) """

BIN_DIR                     = os.path.join(ROOT_DIR, 'bin')
APPS_DIR                    = os.path.join(BIN_DIR, 'apps')
DATA_DIR                    = os.path.join(BIN_DIR, 'data')
DEPENDANCIES_DIR            = os.path.join(BIN_DIR, 'dependencies')
RESOURCES_DIR               = os.path.join(BIN_DIR, 'resources')

SCRIPTS_DIR                 = os.path.join(ROOT_DIR, 'scripts')
QSS_DIR                     = os.path.join(SCRIPTS_DIR, 'qss')
JSON_DIR                    = os.path.join(SCRIPTS_DIR, 'json')


# -------------------------------------------------------------------------------------------------------------
""" Image """

APP_ICON_DIR                = os.path.join(IMG_DIR, 'icons')
WEB_ICON_DIR                = os.path.join(IMG_DIR, 'web')
AVATAR_DIR                  = os.path.join(IMG_DIR, 'avatar')
LOGO_DIR                    = os.path.join(IMG_DIR, 'logo')
PIC_DIR                     = os.path.join(IMG_DIR, 'pics')
TAG_DIR                     = os.path.join(IMG_DIR, 'tags')

ICON_DIR_16                 = os.path.join(APP_ICON_DIR, 'x16')
ICON_DIR_24                 = os.path.join(APP_ICON_DIR, 'x24')
ICON_DIR_32                 = os.path.join(APP_ICON_DIR, 'x32')
ICON_DIR_48                 = os.path.join(APP_ICON_DIR, 'x48')
ICON_DIR_64                 = os.path.join(APP_ICON_DIR, 'x64')

WEB_ICON_16                 = os.path.join(WEB_ICON_DIR, 'x16')
WEB_ICON_24                 = os.path.join(WEB_ICON_DIR, 'x24')
WEB_ICON_32                 = os.path.join(WEB_ICON_DIR, 'x32')
WEB_ICON_48                 = os.path.join(WEB_ICON_DIR, 'x48')
WEB_ICON_64                 = os.path.join(WEB_ICON_DIR, 'x64')
WEB_ICON_128                = os.path.join(WEB_ICON_DIR, 'x128')

DAMG_LOGO_DIR               = os.path.join(LOGO_DIR, 'DAMGteam', 'icons')
PLM_LOGO_DIR                = os.path.join(LOGO_DIR, 'Plm', 'icons')

DAMG_LOGO_32                = os.path.join(DAMG_LOGO_DIR, 'logo32')
PLM_LOGO_32                 = os.path.join(PLM_LOGO_DIR, 'logo32')

# -------------------------------------------------------------------------------------------------------------
""" Documentations """

RAWS_DATA_DIR               = os.path.join(APP_DATA_DIR, 'raws')
DOCUMENTATION_DIR           = os.path.join(APP_DATA_DIR, 'documentations')

# -------------------------------------------------------------------------------------------------------------
""" File path configurations """

cfgFile                     = os.path.join(CFG_DIR, 'PLM.cfg')

appIconCfg                  = os.path.join(CONFIG_DIR, 'appIcon.cfg')                   # Config app icon path
webIconCfg                  = os.path.join(CONFIG_DIR, 'webIcon.cfg')                   # Config Web icon path
logoIconCfg                 = os.path.join(CONFIG_DIR, 'logoIcon.cfg')                  # Config logo icon path

pyEnvCfg                    = os.path.join(CONFIG_DIR, 'envKey.cfg')                    # Config python env variables
appConfig                   = os.path.join(CONFIG_DIR, 'main.cfg')                      # Config pipeline soft package
mainConfig                  = os.path.join(CONFIG_DIR, 'PLM.cfg')                       # Master config

# -------------------------------------------------------------------------------------------------------------
""" Settings """

APP_SETTING                 = os.path.join(SETTING_DIR, 'PLM.ini')                      # Pipeline application setting
USER_SETTING                = os.path.join(SETTING_DIR, 'user.ini')                     # User setting
FORMAT_SETTING              = os.path.join(SETTING_DIR, 'format.ini')
UNIX_SETTING                = os.path.join(SETTING_DIR, 'unix.ini')

SETTING_FILEPTH = dict( app = APP_SETTING, user = USER_SETTING, unix = UNIX_SETTING, format = FORMAT_SETTING)

# -------------------------------------------------------------------------------------------------------------
""" File path """

DB_PTH                      = os.path.join(DB_DIR, 'local.db')                          # Local database
LOG_PTH                     = os.path.join(LOG_DIR, 'PLM.logs')                         # Log file

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 10:45 PM
# Pipeline manager - DAMGteam
