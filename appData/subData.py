#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: subData.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, logging

# PyQt5
from PyQt5.QtCore import Qt, QSize, QSettings, QDateTime
from PyQt5.QtWidgets import QSizePolicy, QFrame

# -------------------------------------------------------------------------------------------------------------
""" Setup directory """

# Plt environment key:
__envKey__ = "PIPELINE_TOOL"

CONFIGLOCALDAMGDIR = os.path.join(os.getenv("LOCALAPPDATA"), 'DAMGteam')   # DAMG team directory
PLMCONFIGLOCAL = os.path.join(CONFIGLOCALDAMGDIR, 'PipelineTool')          # Plt directory
CONFIGDIR = os.path.join(PLMCONFIGLOCAL, "config")                      # Config dir to store config info
SETTINGDIR = os.path.join(PLMCONFIGLOCAL, "settings")                   # Setting dir to store setting info
LOGDIR = os.path.join(PLMCONFIGLOCAL, "logs")                           # Log dir to store log info

APPSETTING = os.path.join(SETTINGDIR, "PltSetting.ini")         # Pipeline tool setting
USERSETTING = os.path.join(SETTINGDIR, "UserSetting.ini")       # User setting

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

DAMGLOGO = os.path.join(LOGODIR, 'DAMGteam', 'icons', '32x32.png')
PLTLOGO = os.path.join(LOGODIR, 'plt', 'icons', '32x32.png')

# -------------------------------------------------------------------------------------------------------------
""" file name """

localDB = "local.db"
appLog = "Plt.log"
appIcon = "appIcon.cfg"
webIcon = "webIcon.cfg"
logoIcon = "logoIcon.cfg"

pythonCfg = "envKey.cfg"
installedAppCfg = "app.cfg"
appPackagesCfg = "main.cfg"

# -------------------------------------------------------------------------------------------------------------
""" Setup config file path """

DBPTH = os.path.join(os.getenv(__envKey__), 'appData', localDB)                             # Local database
LOGPTH = os.path.join(LOGDIR, appLog)                                                       # Log file

appIconCfg = os.path.join(CONFIGDIR, appIcon)
webIconCfg = os.path.join(CONFIGDIR, webIcon)
logoIconCfg = os.path.join(CONFIGDIR, logoIcon)

pyEnvCfg = os.path.join(CONFIGDIR, pythonCfg)
appConfig = os.path.join(CONFIGDIR, installedAppCfg)
mainConfig = os.path.join(CONFIGDIR, appPackagesCfg)

# -------------------------------------------------------------------------------------------------------------
""" Log format setting """

logFormat1 = "%(asctime)s %(levelname)s %(message)s",
logFormat2 = "%(asctime)-15s: %(name)-18s - %(levelname)-8s - %(module)-15s - %(funcName)-20s - %(lineno)-6d - %(message)s"

def set_log(name=__name__, format=logFormat1):
    handler = logging.FileHandler(LOGPTH)
    handler.setFormatter(logging.Formatter(format))
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

def read_file(pth, fileName):
    with open(os.path.join(pth, fileName), 'r') as f:
        data = f.read()
    return data

# ----------------------------------------------------------------------------------------------------------- #
""" PyQt5 setting """

appSetting = QSettings(APPSETTING, QSettings.IniFormat)
userSetting = QSettings(USERSETTING, QSettings.IniFormat)

keepARM = Qt.KeepAspectRatio
ignoreARM = Qt.IgnoreAspectRatio

scrollAsNeed = Qt.ScrollBarAsNeeded
scrollOff = Qt.ScrollBarAlwaysOff
scrollOn = Qt.ScrollBarAlwaysOn

# Size policy
SiPoMin = QSizePolicy.Minimum
SiPoMax = QSizePolicy.Maximum
SiPoExp = QSizePolicy.Expanding
SiPoPre = QSizePolicy.Preferred

frameStyle = QFrame.Sunken | QFrame.Panel

# Alignment
center = Qt.AlignCenter
right = Qt.AlignRight
left = Qt.AlignLeft
hori = Qt.Horizontal
vert = Qt.Vertical

# Docking area
dockL = Qt.LeftDockWidgetArea
dockR = Qt.RightDockWidgetArea
dockT = Qt.TopDockWidgetArea
dockB = Qt.BottomDockWidgetArea

# datestamp

datetTimeStamp = QDateTime.currentDateTime().toString("hh:mm - dd MMMM yy")

__imgExt = "All Files (*);;Img Files (*.jpg);;Img Files (*.png)"

# String
TXT = "No Text" # String by default

# Value, Nummber, Float, Int ...
UNIT = 60   # Base Unit
MARG = 5    # Content margin
BUFF = 10   # Buffer size
SCAL = 1    # Scale value
STEP = 1    # Step value changing
VAL = 1     # Default value
MIN = 0     # Minimum value
MAX = 1000  # Maximum value
WMIN = 50   # Minimum width
HMIN = 20   # Minimum height
HFIX = 80
ICONSIZE = 32
ICONBUFFER = -1
BTNICONSIZE = QSize(ICONSIZE, ICONSIZE)
ICONBTNSIZE = QSize(ICONSIZE+ICONBUFFER, ICONSIZE+ICONBUFFER)

# --------------------------------------------------------------------------------------------------------------
""" Autodesk config """

autodeskVer = ["2017", "2018", "2019", "2020"]

autodeskApp = ["Autodesk Maya", "Autodesk MudBox", "Autodesk 3ds Max", "Autodesk AutoCAD"]

userMayaDir = os.path.expanduser(r"~/Documents/maya")

# --------------------------------------------------------------------------------------------------------------
""" Adobe config """

adobeVer = ["CC 2017", "CC 2018", "CC 2019", ]

adobeApp = ["Adobe Photoshop", "Adobe Illustrator", "Adobe Audition", "Adobe After Effects", "Adobe Premiere Pro",
            "Adobe Media Encoder"]

# --------------------------------------------------------------------------------------------------------------
""" Foundry config """

foundryVer = ["11.1v1", "4.0v1", "2.6v3"]

foundryApp = ['Hiero', 'HieroPlayer', 'Mari', 'NukeX', 'Katana',]

# --------------------------------------------------------------------------------------------------------------
""" Pixologic config """

pixologiVer = ["4R6", "4R7", "4R8"]

pixologiApp = ['ZBrush', ]

# --------------------------------------------------------------------------------------------------------------
""" Allegorithmic config """

allegorithmicVer = []

allegorithmicApp = ['Substance Painter', ]

# --------------------------------------------------------------------------------------------------------------
""" SideFX config """

sizefxVer = ['15.0', '15.5', '16.0']

sizefxApp = ['Houdini FX', ]

# --------------------------------------------------------------------------------------------------------------
""" Microsoft Office config """

officeVer = ['2013', '2015', '2016', '2017']

officeApp = ['Word', 'Excel', 'PowerPoint', 'Wordpad', 'TextEditor', 'NoteReminder']

# --------------------------------------------------------------------------------------------------------------
""" JetBrains config """

jetbrainsVer = ['2017.3.3', '2018.1', ]

jetbrainsApp = ['JetBrains PyCharm', ]

# --------------------------------------------------------------------------------------------------------------
""" another app config """

anacondaApp = ['Spyder', 'QtDesigner', 'Git Bash']

otherApp = ['Sublime Text 2', 'Sublime Text 3', 'Wordpad', 'Headus UVLayout', 'Snipping Tool', ]

CONFIG_APPUI = ['AboutPlt', 'Calculator', 'Calendar', 'Credit', 'EnglishDictionary', 'FindFiles', 'ForgotPassword',
                'ImageViewer', 'NewProject', 'Preferences', 'Screenshot', 'UserSetting', 'PltBrowser', 'NoteReminder',
                'TextEditor']

# --------------------------------------------------------------------------------------------------------------
""" Tracking key """

TRACK_TDS = ['Maya', 'ZBrush', 'Mari', 'Houdini', 'Substance', ]

TRACK_VFX = ['NukeX', 'Davinci Resolve', 'Hiero', 'HieroPlayer', 'After Effects', 'Premiere Pro', 'Media Encoder', ]

TRACK_ART = ['Photoshop', 'Illustrator', ]

TRACK_OFFICE = ['Word', 'Excel', 'PowerPoint', 'Wordpad']

TRACK_DEV = ['PyCharm', 'Sublime Text', 'QtDesigner', 'Git Bash', 'Command Prompt', 'Spyder']

TRACK_TOOLS = ['Calculator', 'Calendar', 'EnglishDictionary', 'FindFiles', 'ImageViewer', 'Screenshot', ]

TRACK_EXTRA = ['3Ds Max', 'Mudbox', 'BLender', ]

TRACK_SYSTRAY = ['Snipping Tool', 'Screenshot', 'Maximize', 'Minimize', 'Restore', 'Quit', ]

KEYDETECT = ["Non-commercial", "Uninstall", "Verbose", "License", "Skype"]

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 31/05/2018 - 9:47 AM