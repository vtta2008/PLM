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
from appData.scr._meta import __appname__, __groupname__, __envKey__
from appData.scr._name import *
# -------------------------------------------------------------------------------------------------------------
""" Directory local system """

CONFIG_LOCAL_DAMG_DIR = os.path.join(os.getenv("LOCALAPPDATA"), __groupname__)       # DAMG team directory
CONFIG_LOCAL_PLM_DIR = os.path.join(CONFIG_LOCAL_DAMG_DIR, __appname__)              # Plm directory

CONFIG_DIR = os.path.join(CONFIG_LOCAL_PLM_DIR, config)                              # Config dir to store config info
SETTING_DIR = os.path.join(CONFIG_LOCAL_PLM_DIR, settings)                           # Setting dir to store setting info
LOG_DIR = os.path.join(CONFIG_LOCAL_PLM_DIR, logs)                                   # Log dir to store log info
CACHE_DIR = os.path.join(CONFIG_LOCAL_PLM_DIR, cache)                                # In case caching something
REG_DIR = os.path.join(CONFIG_LOCAL_PLM_DIR, reg)

PREF_DIR = os.path.join(CONFIG_DIR, nodeBase)
USER_PREF_DIR = os.path.join(CONFIG_DIR, userRef)

DESKTOP_DIR = os.path.join(os.environ["HOMEPATH"], "desktop")                       # Desktop path

# -------------------------------------------------------------------------------------------------------------
""" Directory application """

ROOT_DIR = os.getenv(__envKey__)

APP_DATA_DIR = os.path.join(ROOT_DIR, appData)
DB_DIR = APP_DATA_DIR
NODEGRAPH_CONFIG_DIR = APP_DATA_DIR
BUILD_DIR = os.path.join(ROOT_DIR, build)
CORE_DIR = os.path.join(ROOT_DIR, core)
IMG_DIR = os.path.join(ROOT_DIR, imgs)
PLUGIN_DIR = os.path.join(ROOT_DIR, plg_ins)
QSS_DIR = os.path.join(ROOT_DIR, qss)
UI_DIR = os.path.join(ROOT_DIR, ui)
TEST_DIR = os.path.join(ROOT_DIR, test)

# Imgs
APP_ICON_DIR = os.path.join(IMG_DIR, icons)
WEB_ICON_DIR = os.path.join(IMG_DIR, web)
AVATAR_DIR = os.path.join(IMG_DIR, avatar)
LOGO_DIR = os.path.join(IMG_DIR, logo)
PIC_DIR = os.path.join(IMG_DIR, pics)
TAG_DIR = os.path.join(IMG_DIR, tags)

ICON_DIR_16 = os.path.join(APP_ICON_DIR, x16)
ICON_DIR_24 = os.path.join(APP_ICON_DIR, x24)
ICON_DIR_32 = os.path.join(APP_ICON_DIR, x32)
ICON_DIR_48 = os.path.join(APP_ICON_DIR, x48)
ICON_DIR_64 = os.path.join(APP_ICON_DIR, x64)

WEB_ICON_16 = os.path.join(WEB_ICON_DIR, x16)
WEB_ICON_24 = os.path.join(WEB_ICON_DIR, x24)
WEB_ICON_32 = os.path.join(WEB_ICON_DIR, x32)
WEB_ICON_48 = os.path.join(WEB_ICON_DIR, x48)
WEB_ICON_64 = os.path.join(WEB_ICON_DIR, x64)
WEB_ICON_128 = os.path.join(WEB_ICON_DIR, x128)

DOC_DIR = os.path.join(APP_DATA_DIR, docs)

DEPENDANCIES_DIR = os.path.join(CORE_DIR, dependencies)

# -------------------------------------------------------------------------------------------------------------
""" Document pth """

QUESTIONS = os.path.join(DOC_DIR, QUESTION)
ABOUT = os.path.join(DOC_DIR, ABOUT)
CREDIT = os.path.join(DOC_DIR, CREDIT)
CODECONDUCT = os.path.join(DOC_DIR, CODECONDUCT)
CONTRIBUTING = os.path.join(DOC_DIR, CONTRIBUTING)
REFERENCE = os.path.join(DOC_DIR, REFERENCE)

from appData.scr._docs import PLM_ABOUT
README = PLM_ABOUT

# -------------------------------------------------------------------------------------------------------------
""" Path """

DAMG_LOGO_DIR = os.path.join(LOGO_DIR, DAMGteam, icons, )
PLM_LOGO_DIR = os.path.join(LOGO_DIR, Plm, icons)

DAMG_LOGO_32 = os.path.join(DAMG_LOGO_DIR, logo32)
PLM_LOGO_32 = os.path.join(PLM_LOGO_DIR, logo32)

APP_SETTING = os.path.join(SETTING_DIR, appSettingFile)         # Pipeline application setting
USER_SETTING = os.path.join(SETTING_DIR, userSettingFile)       # User setting
FORMAT_SETTING = os.path.join(SETTING_DIR, formatSettingFile)
UNIX_SETTING = os.path.join(SETTING_DIR, unixSettingFile)

DB_PTH = os.path.join(DB_DIR, localDatabaseFile)                             # Local database
LOG_PTH = os.path.join(LOG_DIR, appLogFile)                                                       # Log file

appIconCfg = os.path.join(CONFIG_DIR, appIcon)
webIconCfg = os.path.join(CONFIG_DIR, webIcon)
logoIconCfg = os.path.join(CONFIG_DIR, logoIcon)

pyEnvCfg = os.path.join(CONFIG_DIR, pythonCfg)
appConfig = os.path.join(CONFIG_DIR, installedAppCfg)
mainConfig = os.path.join(CONFIG_DIR, appPackagesCfg)
nodeGraphConfig = os.path.join(NODEGRAPH_CONFIG_DIR)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 10:45 PM
# Pipeline manager - DAMGteam
