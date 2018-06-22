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
from appData._meta import __appname__, __groupname__, __envKey__
from appData._name import *
# PyQt5
from PyQt5.QtCore import QSettings

# -------------------------------------------------------------------------------------------------------------
""" Directory local system """

CONFIGLOCALDAMGDIR = os.path.join(os.getenv("LOCALAPPDATA"), __groupname__)        # DAMG team directory
PLMCONFIGLOCAL = os.path.join(CONFIGLOCALDAMGDIR, __appname__)                  # Plm directory

CONFIGDIR = os.path.join(PLMCONFIGLOCAL, config)                              # Config dir to store config info
SETTINGDIR = os.path.join(PLMCONFIGLOCAL, settings)                           # Setting dir to store setting info
LOGDIR = os.path.join(PLMCONFIGLOCAL, logs)                                   # Log dir to store log info
CACHEDIR = os.path.join(PLMCONFIGLOCAL, cache)                                # In case caching something

PREFDIR = os.path.join(CONFIGDIR, nodeBase)
USERPREFDIR = os.path.join(CONFIGDIR, userRef)

# -------------------------------------------------------------------------------------------------------------
""" Directory application """

ROOTDIR = os.getenv(__envKey__)
APPDATADIR = os.path.join(ROOTDIR, appData)
DBDIR = APPDATADIR
BUILDDIR = os.path.join(ROOTDIR, build)
COREDIR = os.path.join(ROOTDIR, core)
IMGDIR = os.path.join(ROOTDIR, imgs)
PLUGINDIR = os.path.join(ROOTDIR, plg_ins)
QSSDIR = os.path.join(ROOTDIR, qss)
UIDIR = os.path.join(ROOTDIR, ui)
TESTDIR = os.path.join(ROOTDIR, test)

# Imgs
APPICONDIR = os.path.join(IMGDIR, icons)
WEBICONDIR = os.path.join(IMGDIR, web)
AVATARDIR = os.path.join(IMGDIR, avatar)
LOGODIR = os.path.join(IMGDIR, logo)
PICDIR = os.path.join(IMGDIR, pics)
TAGDIR = os.path.join(IMGDIR, tags)

ICONDIR16 = os.path.join(APPICONDIR, x16)
ICONDIR24 = os.path.join(APPICONDIR, x24)
ICONDIR32 = os.path.join(APPICONDIR, x32)
ICONDIR48 = os.path.join(APPICONDIR, x48)
ICONDIR64 = os.path.join(APPICONDIR, x64)

WEBICON16 = os.path.join(WEBICONDIR, x16)
WEBICON24 = os.path.join(WEBICONDIR, x24)
WEBICON32 = os.path.join(WEBICONDIR, x32)
WEBICON48 = os.path.join(WEBICONDIR, x48)
WEBICON64 = os.path.join(WEBICONDIR, x64)
WEBICON128 = os.path.join(WEBICONDIR, x128)

DOCDIR = os.path.join(APPDATADIR, docs)

DEPENDANCIESDIR = os.path.join(COREDIR, dependencies)

# -------------------------------------------------------------------------------------------------------------
""" Document pth """

QUESTIONS = os.path.join(DOCDIR, QUESTION)
ABOUT = os.path.join(DOCDIR, ABOUT)
CREDIT = os.path.join(DOCDIR, CREDIT)
from appData._docs import PLM_ABOUT
README = PLM_ABOUT

# -------------------------------------------------------------------------------------------------------------
""" Path """

DAMGLOGOICONDIR = os.path.join(LOGODIR, DAMGteam, icons, )
PLMLOGODIR = os.path.join(LOGODIR, Plm, icons)

DAMGLOGO = os.path.join(DAMGLOGOICONDIR, logo32)
PLMLOGO = os.path.join(PLMLOGODIR, logo32)

APPSETTING = os.path.join(SETTINGDIR, PlmSetting)         # Pipeline application setting
USERSETTING = os.path.join(SETTINGDIR, userSetting)       # User setting
FORMATSETTING = os.path.join(SETTINGDIR, formatSetting)
UNIXSETTING = os.path.join(SETTINGDIR, unixSetting)


appSetting = QSettings(APPSETTING, QSettings.IniFormat)
userSetting = QSettings(USERSETTING, QSettings.IniFormat)
formatSetting = QSettings(FORMATSETTING, QSettings.IniFormat)
unixSetting = QSettings(UNIXSETTING, QSettings.IniFormat)

DBPTH = os.path.join(DBDIR, localDB)                             # Local database
LOGPTH = os.path.join(LOGDIR, appLog)                                                       # Log file

appIconCfg = os.path.join(CONFIGDIR, appIcon)
webIconCfg = os.path.join(CONFIGDIR, webIcon)
logoIconCfg = os.path.join(CONFIGDIR, logoIcon)

pyEnvCfg = os.path.join(CONFIGDIR, pythonCfg)
appConfig = os.path.join(CONFIGDIR, installedAppCfg)
mainConfig = os.path.join(CONFIGDIR, appPackagesCfg)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 10:45 PM
# Pipeline manager - DAMGteam
