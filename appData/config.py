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
import logging
import json

from importlib import reload as r

# Plm
from appData import _path as p
from appData import _docs as d
from appData import _keys as k
from appData import _meta as m
from appData import _style as s

# -------------------------------------------------------------------------------------------------------------
""" Environment variables """

__envKey__ = p.__envKey__

# -------------------------------------------------------------------------------------------------------------
""" Reload module """

def reload_module(module):
    return r(module)

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
__pltSlogan__ = m.__pltSlogan__
__pltWiki__ = m.__pltWiki__

# -------------------------------------------------------------------------------------------------------------
""" Server """

__serverLocal__ = m.__serverLocal__
__serverUrl__ = m.__serverUrl__
__serverCheck__ = m.__serverCheck__
__serverAutho__ = m.__serverAutho__

__google__ = m.__google__

# -------------------------------------------------------------------------------------------------------------
""" Metadata """

VERSION = m.VERSION
COPYRIGHT = m.COPYRIGHT
PLUGINVERSION = m.PLUGINVERSION
PLTAPPID = m.PLTAPPID

# ----------------------------------------------------------------------------------------------------------- #
""" Setup.py options """

def read_file(pth, fileName):
    with open(os.path.join(pth, fileName), 'r') as f:
        data = f.read()
    return data

__email__ = m.__email__
__packages_dir__ = m.__packages_dir__
__classifiers__ = m.__classifiers__
__download__ = m.__download__
__description__ = m.__description__
__readme__ = m.__readme__
__modules__ = m.__modules__
__pkgsReq__ = m.__pkgsReq__

QUESTIONS = read_file(os.path.join(os.getenv(__envKey__), 'appData', 'docs'), 'QUESTION')
ABOUT = read_file(os.path.join(os.getenv(__envKey__), 'appData', 'docs'), 'ABOUT')
CREDIT = read_file(os.path.join(os.getenv(__envKey__), 'appData', 'docs'), 'CREDIT')
README = d.PLM_ABOUT

# -------------------------------------------------------------------------------------------------------------
""" Name """

localDB = p.localDB
appLog = p.appLog
appIcon = p.appIcon
webIcon = p.webIcon
logoIcon = p.logoIcon

pythonCfg = p.pythonCfg
installedAppCfg = p.installedAppCfg
appPackagesCfg = p.appPackagesCfg

# -------------------------------------------------------------------------------------------------------------
""" Directory """

CONFIGLOCALDAMGDIR = p.CONFIGLOCALDAMGDIR
PLMCONFIGLOCAL = p.PLMCONFIGLOCAL
CONFIGDIR = p.CONFIGDIR
SETTINGDIR = p.SETTINGDIR
LOGDIR = p.LOGDIR

for pth in [CONFIGLOCALDAMGDIR, PLMCONFIGLOCAL, CONFIGDIR, SETTINGDIR, LOGDIR]:
    if not os.path.exists(pth):
        os.mkdir(pth)

IMGDIR = p.IMGDIR
APPICONDIR = p.APPICONDIR
WEBICONDIR = p.WEBICONDIR
AVATARDIR = p.AVATARDIR
LOGODIR = p.LOGODIR
PICDIR = p.PICDIR

ICONDIR16 = p.ICONDIR16
ICONDIR24 = p.ICONDIR24
ICONDIR32 = p.ICONDIR32
ICONDIR48 = p.ICONDIR48
ICONDIR64 = p.ICONDIR64

WEBICON16 = p.WEBICON16
WEBICON24 = p.WEBICON24
WEBICON32 = p.WEBICON32
WEBICON48 = p.WEBICON48
WEBICON64 = p.WEBICON64
WEBICON128 = p.WEBICON128



# -------------------------------------------------------------------------------------------------------------
""" Path """

DAMGLOGO = p.DAMGLOGO
PLTLOGO = p.PLTLOGO

APPSETTING = p.APPSETTING
USERSETTING = p.USERSETTING

appSetting = p.appSetting
userSetting = p.userSetting

DBPTH = p.DBPTH
LOGPTH = p.LOGPTH

if not os.path.exists(DBPTH):
    from appData import _rcSQL as r
    r.GenerateResource()

appIconCfg = p.appIconCfg
webIconCfg = p.webIconCfg
logoIconCfg = p.logoIconCfg

pyEnvCfg = p.pyEnvCfg
appConfig = p.appConfig
mainConfig = p.mainConfig

# -------------------------------------------------------------------------------------------------------------
""" Log format setting """

from logging import getLogger, INFO, WARN, DEBUG, ERROR, FATAL

__all__ = ['getLogger', 'INFO', 'WARN', 'DEBUG', 'TRACE', 'ERROR', 'FATAL']

levels = ['TRACE', 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL']

logFormat1 = "%(relativeCreated)d %(levelname)s: %(message)s"
logFormat2 = "%(asctime)-15s: %(name)-18s - %(levelname)-8s - %(module)-15s - %(funcName)-20s - %(lineno)-6d - %(message)s"
logFormat3 = "%(asctime)s %(levelname)s %(message)s",

TRACE = logging.TRACE = DEBUG - 5

def get_logger(name):

    logging.addLevelName(TRACE, 'TRACE')
    logger = logging.getLogger(name)
    return logger

def get_handler(logPth, format):
    handler = logging.FileHandler(logPth)
    handler.setFormatter(logging.Formatter(format))
    return handler

def get_level(opts="DEBUG"):
    try:
        level = getattr(logging, opts.loglevel.upper())
        print(level)
    except AttributeError:
        return logging.DEBUG
    else:
        return level

def set_log(name=__name__, logPth=LOGPTH, format=logFormat1):

    handler = get_handler(logPth, format)
    level = get_level()
    logger = get_logger(name)

    logger.addHandler(handler)
    logger.setLevel(level)

    return logger

# ----------------------------------------------------------------------------------------------------------- #
""" PyQt5 setting """

# String
TXT = s.TXT
UNIT = s.UNIT
MARG = s.MARG
BUFF = s.BUFF
SCAL = s.SCAL
STEP = s.STEP
VAL = s.VAL
MIN = s.MIN
MAX = s.MAX
WMIN = s.WMIN
HMIN = s.HMIN
HFIX = s.HFIX
ICONSIZE = s.ICONSIZE
ICONBUFFER = s.ICONBUFFER
BTNICONSIZE = s.BTNICONSIZE
ICONBTNSIZE = s.ICONBTNSIZE

keepARM = s.keepARM
ignoreARM = s.ignoreARM

scrollAsNeed = s.scrollAsNeed
scrollOff = s.scrollOff
scrollOn = s.scrollOn

# Size policy
SiPoMin = s.SiPoMin
SiPoMax = s.SiPoMax
SiPoExp = s.SiPoExp
SiPoPre = s.SiPoPre
SiPoIgn = s.SiPoIgn

frameStyle = s.frameStyle

# Alignment
center = s.frameStyle
right = s.right
left = s.left
hori = s.hori
vert = s.vert

# Docking area
dockL = s.dockL
dockR = s.dockR
dockT = s.dockT
dockB = s.dockB

# datestamp
datetTimeStamp = s.datetTimeStamp
__imgExt = s.__imgExt

# -------------------------------------------------------------------------------------------------------------
""" String """

PLM_ABOUT = d.PLM_ABOUT
WAIT_FOR_UPDATE = d.WAIT_FOR_UPDATE
WAIT_TO_COMPLETE = d.WAIT_TO_COMPLETE
WAIT_LAYOUT_COMPLETE = d.WAIT_LAYOUT_COMPLETE
PASSWORD_FORGOTTON = d.PASSWORD_FORGOTTON
SIGNUP = d.SIGNUP
DISALLOW = d.DISALLOW
TIT_BLANK = d.TIT_BLANK
PW_BLANK = d.PW_BLANK
PW_WRONG = d.PW_WRONG
PW_UNMATCH = d.PW_UNMATCH
PW_CHANGED = d.PW_CHANGED
FN_BLANK = d.FN_BLANK
LN_BLANK = d.LN_BLANK
SEC_BLANK = d.SEC_BLANK
USER_CHECK_REQUIRED = d.USER_CHECK_REQUIRED
USER_NOT_CHECK = d.USER_NOT_CHECK
USER_BLANK = d.USER_BLANK
USER_CHECK_FAIL = d.USER_CHECK_FAIL
USER_NOT_EXSIST = d.USER_NOT_EXSIST
USER_CONDITION = d.USER_CONDITION
SYSTRAY_UNAVAI = d.SYSTRAY_UNAVAI
PTH_NOT_EXSIST = d.PTH_NOT_EXSIST
ERROR_OPENFILE = d.ERROR_OPENFILE
ERROR_QIMAGE = d.ERROR_QIMAGE

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
""" Autodesk config """

autodeskVer = k.autodeskVer
autodeskApp = k.autodeskApp
userMayaDir = k.userMayaDir

# --------------------------------------------------------------------------------------------------------------
""" Adobe config """

adobeVer = k.adobeVer
adobeApp = k.adobeApp

# --------------------------------------------------------------------------------------------------------------
""" Foundry config """

foundryVer = k.foundryVer
foundryApp = k.foundryApp

# --------------------------------------------------------------------------------------------------------------
""" Pixologic config """

pixologiVer = k.pixologiVer
pixologiApp = k.pixologiApp

# --------------------------------------------------------------------------------------------------------------
""" Allegorithmic config """

allegorithmicVer = k.allegorithmicVer
allegorithmicApp = k.allegorithmicApp

# --------------------------------------------------------------------------------------------------------------
""" SideFX config """

sizefxVer = k.sizefxVer
sizefxApp = k.sizefxApp

# --------------------------------------------------------------------------------------------------------------
""" Microsoft Office config """

officeVer = k.officeVer
officeApp = k.officeApp

# --------------------------------------------------------------------------------------------------------------
""" JetBrains config """

jetbrainsVer = k.jetbrainsVer
jetbrainsApp = k.jetbrainsApp

# --------------------------------------------------------------------------------------------------------------
""" another app config """

anacondaApp = k.anacondaApp
otherApp = k.otherApp
CONFIG_APPUI = k.CONFIG_APPUI

# --------------------------------------------------------------------------------------------------------------
""" Tracking key """

TRACK_TDS = k.TRACK_TDS
TRACK_VFX = k.TRACK_VFX
TRACK_ART = k.TRACK_ART
TRACK_OFFICE = k.TRACK_OFFICE
TRACK_DEV = k.TRACK_DEV
TRACK_TOOLS = k.TRACK_TOOLS
TRACK_EXTRA = k.TRACK_EXTRA
TRACK_SYSTRAY = k.TRACK_SYSTRAY
KEYDETECT = k.KEYDETECT

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

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 10:56 PM
# Pipeline manager - DAMGteam
