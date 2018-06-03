#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: __init__.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" import """

from . import config as c

# -------------------------------------------------------------------------------------------------------------
""" Environment variables """

__envKey__ = c.__envKey__

# -------------------------------------------------------------------------------------------------------------
""" Reload module """

def reload(module):
    return c.reload_module(module)

# -------------------------------------------------------------------------------------------------------------
""" DAMG team """

__organization__ = c.__organization__
__damgSlogan__ = c.__damgSlogan__
__website__ = c.__website__
__author1__ = c.__author1__
__author2__ = c.__author2__
__Founder__ = c.__author1__
__CoFonder1__ = c.__author2__
__email1__ = c.__email1__
__email2__ = c.__email2__

# -------------------------------------------------------------------------------------------------------------
""" PipelineTool """

__project__ = c.__project__
__appname__ = c.__appname__
__appShortcut__ = c.__appShortcut__
__version__ = c.__version__
__cfgVersion__ = c.__cfgVersion__
__verType__ = c.__verType__
__reverType__ = c.__reverType__
__about__ = c.__about__
__homepage__ = c.__homepage__
__pltSlogan__ = c.__pltSlogan__
__pltWiki__ = c.__pltWiki__

# -------------------------------------------------------------------------------------------------------------
""" Server """

__serverLocal__ = c.__serverLocal__
__serverUrl__ = c.__serverUrl__
__serverCheck__ = c.__serverCheck__
__serverAutho__ = c.__serverAutho__

__google__ = c.__google__

# -------------------------------------------------------------------------------------------------------------
""" Metadata """

VERSION = c.VERSION
COPYRIGHT = c.COPYRIGHT
PLUGINVERSION = c.PLUGINVERSION
PLTAPPID = c.PLTAPPID

# ----------------------------------------------------------------------------------------------------------- #
""" Setuc.py options """

__email__ = c.__email__
__packages_dir__ = c.__packages_dir__
__classifiers__ = c.__classifiers__
__download__ = c.__download__
__description__ = c.__description__
__readme__ = c.__readme__
__modules__ = c.__modules__
__pkgsReq__ = c.__pkgsReq__

QUESTIONS = c.QUESTIONS
ABOUT = c.ABOUT
CREDIT = c.CREDIT
README = c.README

# -------------------------------------------------------------------------------------------------------------
""" Name """

localDB = c.localDB
appLog = c.appLog
appIcon = c.appIcon
webIcon = c.webIcon
logoIcon = c.logoIcon

pythonCfg = c.pythonCfg
installedAppCfg = c.installedAppCfg
appPackagesCfg = c.appPackagesCfg

# -------------------------------------------------------------------------------------------------------------
""" Directory """

CONFIGLOCALDAMGDIR = c.CONFIGLOCALDAMGDIR
PLMCONFIGLOCAL = c.PLMCONFIGLOCAL
CONFIGDIR = c.CONFIGDIR
SETTINGDIR = c.SETTINGDIR
LOGDIR = c.LOGDIR

IMGDIR = c.IMGDIR
APPICONDIR = c.APPICONDIR
WEBICONDIR = c.WEBICONDIR
AVATARDIR = c.AVATARDIR
LOGODIR = c.LOGODIR
PICDIR = c.PICDIR

ICONDIR16 = c.ICONDIR16
ICONDIR24 = c.ICONDIR24
ICONDIR32 = c.ICONDIR32
ICONDIR48 = c.ICONDIR48
ICONDIR64 = c.ICONDIR64

WEBICON16 = c.WEBICON16
WEBICON24 = c.WEBICON24
WEBICON32 = c.WEBICON32
WEBICON48 = c.WEBICON48
WEBICON64 = c.WEBICON64
WEBICON128 = c.WEBICON128

# -------------------------------------------------------------------------------------------------------------
""" Log format setting """

def set_log():
    return c.set_log()

# -------------------------------------------------------------------------------------------------------------
""" Path """

DAMGLOGO = c.DAMGLOGO
PLTLOGO = c.PLTLOGO

APPSETTING = c.APPSETTING
USERSETTING = c.USERSETTING

appSetting = c.appSetting
userSetting = c.userSetting

DBPTH = c.DBPTH
LOGPTH = c.LOGPTH

appIconCfg = c.appIconCfg
webIconCfg = c.webIconCfg
logoIconCfg = c.logoIconCfg

pyEnvCfg = c.pyEnvCfg
appConfig = c.appConfig
mainConfig = c.mainConfig

# ----------------------------------------------------------------------------------------------------------- #
""" PyQt5 setting """

# String
TXT = c.TXT
UNIT = c.UNIT
MARG = c.MARG
BUFF = c.BUFF
SCAL = c.SCAL
STEP = c.STEP
VAL = c.VAL
MIN = c.MIN
MAX = c.MAX
WMIN = c.WMIN
HMIN = c.HMIN
HFIX = c.HFIX
ICONSIZE = c.ICONSIZE
ICONBUFFER = c.ICONBUFFER
BTNICONSIZE = c.BTNICONSIZE
ICONBTNSIZE = c.ICONBTNSIZE

keepARM = c.keepARM
ignoreARM = c.ignoreARM

scrollAsNeed = c.scrollAsNeed
scrollOff = c.scrollOff
scrollOn = c.scrollOn

# Size policy
SiPoMin = c.SiPoMin
SiPoMax = c.SiPoMax
SiPoExp = c.SiPoExp
SiPoPre = c.SiPoPre

frameStyle = c.frameStyle

# Alignment
center = c.frameStyle
right = c.right
left = c.left
hori = c.hori
vert = c.vert

# Docking area
dockL = c.dockL
dockR = c.dockR
dockT = c.dockT
dockB = c.dockB

# datestamp
datetTimeStamp = c.datetTimeStamp
__imgExt = c.__imgExt

# -------------------------------------------------------------------------------------------------------------
""" String """

PLM_ABOUT = c.PLM_ABOUT
WAIT_FOR_UPDATE = c.WAIT_FOR_UPDATE
WAIT_TO_COMPLETE = c.WAIT_TO_COMPLETE
WAIT_LAYOUT_COMPLETE = c.WAIT_LAYOUT_COMPLETE
PASSWORD_FORGOTTON = c.PASSWORD_FORGOTTON
SIGNUP = c.SIGNUP
DISALLOW = c.DISALLOW
TIT_BLANK = c.TIT_BLANK
PW_BLANK = c.PW_BLANK
PW_WRONG = c.PW_WRONG
PW_UNMATCH = c.PW_UNMATCH
PW_CHANGED = c.PW_CHANGED
FN_BLANK = c.FN_BLANK
LN_BLANK = c.LN_BLANK
SEC_BLANK = c.SEC_BLANK
USER_CHECK_REQUIRED = c.USER_CHECK_REQUIRED
USER_NOT_CHECK = c.USER_NOT_CHECK
USER_BLANK = c.USER_BLANK
USER_CHECK_FAIL = c.USER_CHECK_FAIL
USER_NOT_EXSIST = c.USER_NOT_EXSIST
USER_CONDITION = c.USER_CONDITION
SYSTRAY_UNAVAI = c.SYSTRAY_UNAVAI
PTH_NOT_EXSIST = c.PTH_NOT_EXSIST
ERROR_OPENFILE = c.ERROR_OPENFILE
ERROR_QIMAGE = c.ERROR_QIMAGE

APPINFO = c.APPINFO
ICONINFO = c.ICONINFO

# --------------------------------------------------------------------------------------------------------------
""" Autodesk config """

autodeskVer = c.autodeskVer
autodeskApp = c.autodeskApp
userMayaDir = c.userMayaDir

# --------------------------------------------------------------------------------------------------------------
""" Adobe config """

adobeVer = c.adobeVer
adobeApp = c.adobeApp

# --------------------------------------------------------------------------------------------------------------
""" Foundry config """

foundryVer = c.foundryVer
foundryApp = c.foundryApp

# --------------------------------------------------------------------------------------------------------------
""" Pixologic config """

pixologiVer = c.pixologiVer
pixologiApp = c.pixologiApp

# --------------------------------------------------------------------------------------------------------------
""" Allegorithmic config """

allegorithmicVer = c.allegorithmicVer
allegorithmicApp = c.allegorithmicApp

# --------------------------------------------------------------------------------------------------------------
""" SideFX config """

sizefxVer = c.sizefxVer
sizefxApp = c.sizefxApp

# --------------------------------------------------------------------------------------------------------------
""" Microsoft Office config """

officeVer = c.officeVer
officeApp = c.officeApp

# --------------------------------------------------------------------------------------------------------------
""" JetBrains config """

jetbrainsVer = c.jetbrainsVer
jetbrainsApp = c.jetbrainsApp

# --------------------------------------------------------------------------------------------------------------
""" another app config """

anacondaApp = c.anacondaApp
otherApp = c.otherApp
CONFIG_APPUI = c.CONFIG_APPUI

# --------------------------------------------------------------------------------------------------------------
""" Tracking key """

TRACK_TDS = c.TRACK_TDS
TRACK_VFX = c.TRACK_VFX
TRACK_ART = c.TRACK_ART
TRACK_OFFICE = c.TRACK_OFFICE
TRACK_DEV = c.TRACK_DEV
TRACK_TOOLS = c.TRACK_TOOLS
TRACK_EXTRA = c.TRACK_EXTRA
TRACK_SYSTRAY = c.TRACK_SYSTRAY
KEYDETECT = c.KEYDETECT

# --------------------------------------------------------------------------------------------------------------
""" Store config data """

KEYPACKAGE = c.KEYPACKAGE

# Toolbar config
CONFIG_TDS = c.CONFIG_TDS
CONFIG_VFX = c.CONFIG_VFX
CONFIG_ART = c.CONFIG_ART

# Tab 1 sections config
CONFIG_OFFICE = c.CONFIG_OFFICE
CONFIG_DEV = c.CONFIG_DEV
CONFIG_TOOLS = c.CONFIG_TOOLS
CONFIG_EXTRA = c.CONFIG_EXTRA
CONFIG_SYSTRAY = c.CONFIG_SYSTRAY

# --------------------------------------------------------------------------------------------------------------