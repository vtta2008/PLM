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

# PyQt5
from PyQt5.QtCore import QSettings

# -------------------------------------------------------------------------------------------------------------
""" Environment variable """

# Plt environment key:
__envKey__ = "PIPELINE_MANAGER"

# -------------------------------------------------------------------------------------------------------------
""" File name """

localDB = "local.db"
appLog = "plm.log"
appIcon = "appIcon.cfg"
webIcon = "webIcon.cfg"
logoIcon = "logoIcon.cfg"

pythonCfg = "envKey.cfg"
installedAppCfg = "app.cfg"
appPackagesCfg = "main.cfg"

# -------------------------------------------------------------------------------------------------------------
""" Directory """

CONFIGLOCALDAMGDIR = os.path.join(os.getenv("LOCALAPPDATA"), 'DAMGteam')   # DAMG team directory
PLMCONFIGLOCAL = os.path.join(CONFIGLOCALDAMGDIR, 'PipelineManager')          # Plt directory
CONFIGDIR = os.path.join(PLMCONFIGLOCAL, "config")                      # Config dir to store config info
SETTINGDIR = os.path.join(PLMCONFIGLOCAL, "settings")                   # Setting dir to store setting info
LOGDIR = os.path.join(PLMCONFIGLOCAL, "logs")                           # Log dir to store log info

IMGDIR = os.path.join(os.getenv(__envKey__), 'imgs')
APPICONDIR = os.path.join(IMGDIR, 'icons')
WEBICONDIR = os.path.join(IMGDIR, 'web')
AVATARDIR = os.path.join(IMGDIR, 'avatar')
LOGODIR = os.path.join(IMGDIR, 'logo')
PICDIR = os.path.join(IMGDIR, 'pics')

ICONDIR16 = os.path.join(APPICONDIR, 'x16')
ICONDIR24 = os.path.join(APPICONDIR, 'x24')
ICONDIR32 = os.path.join(APPICONDIR, 'x32')
ICONDIR48 = os.path.join(APPICONDIR, 'x48')
ICONDIR64 = os.path.join(APPICONDIR, 'x64')

WEBICON16 = os.path.join(WEBICONDIR, 'x16')
WEBICON24 = os.path.join(WEBICONDIR, 'x24')
WEBICON32 = os.path.join(WEBICONDIR, 'x32')
WEBICON48 = os.path.join(WEBICONDIR, 'x48')
WEBICON64 = os.path.join(WEBICONDIR, 'x64')
WEBICON128 = os.path.join(WEBICONDIR, 'x128')

# -------------------------------------------------------------------------------------------------------------
""" Path """

DAMGLOGO = os.path.join(LOGODIR, 'DAMGteam', 'icons', '32x32.png')
PLTLOGO = os.path.join(LOGODIR, 'Plm', 'icons', '32x32.png')

APPSETTING = os.path.join(SETTINGDIR, "PlmSetting.ini")         # Pipeline tool setting
USERSETTING = os.path.join(SETTINGDIR, "UserSetting.ini")       # User setting

appSetting = QSettings(APPSETTING, QSettings.IniFormat)
userSetting = QSettings(USERSETTING, QSettings.IniFormat)

DBPTH = os.path.join(os.getenv(__envKey__), 'appData', localDB)                             # Local database
LOGPTH = os.path.join(LOGDIR, appLog)                                                       # Log file

appIconCfg = os.path.join(CONFIGDIR, appIcon)
webIconCfg = os.path.join(CONFIGDIR, webIcon)
logoIconCfg = os.path.join(CONFIGDIR, logoIcon)

pyEnvCfg = os.path.join(CONFIGDIR, pythonCfg)
appConfig = os.path.join(CONFIGDIR, installedAppCfg)
mainConfig = os.path.join(CONFIGDIR, appPackagesCfg)

# -------------------------------------------------------------------------------------------------------------
"""

Created by panda on 3/06/2018 - 10:45 PM
Pipeline manager - DAMGteam

"""