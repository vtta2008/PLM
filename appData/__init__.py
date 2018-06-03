#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: __init__.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os
from importlib import reload as r

# Plt
from . import subData as sub
from . import strData as mes

# -------------------------------------------------------------------------------------------------------------
""" Environment Variable """

__envKey__ = sub.__envKey__

# -------------------------------------------------------------------------------------------------------------
""" Reload module """

def reload(module):
    return r(module)

def set_log():
    return sub.set_log()

# -------------------------------------------------------------------------------------------------------------
""" Setup dir, path """

DAMGDIR = sub.CONFIGLOCALDAMGDIR
APPDIR = sub.PLMCONFIGLOCAL

CONFIGDIR = sub.CONFIGDIR                       # Config dir to store config info
SETTINGDIR = sub.SETTINGDIR                     # Setting dir to store setting info
LOGODIR = sub.LOGDIR                             # Log dir to store log info

DBPTH = sub.DBPTH                               # Local database
LOGPTH = sub.LOGPTH                             # Log file

APPICONDIR = sub.APPICONDIR
WEBICONDIR = sub.WEBICONDIR
AVATARDIR = sub.AVATARDIR
PICDIR = sub.PICDIR

ICONDIR16 = sub.ICONDIR16
ICONDIR24 = sub.ICONDIR24
ICONDIR32 = sub.ICONDIR32
ICONDIR48 = sub.ICONDIR48
ICONDIR64 = sub.ICONDIR64

WEBICON16 = sub.WEBICON16
WEBICON24 = sub.WEBICON24
WEBICON32 = sub.WEBICON32
WEBICON48 = sub.WEBICON48
WEBICON64 = sub.WEBICON64
WEBICON128 = sub.WEBICON128

APPSETTING = sub.appSetting
USERSETTING = sub.userSetting

pyEnvCfg = sub.pyEnvCfg
appIconCfg = sub.appIconCfg                     # app icon config
webIconCfg = sub.webIconCfg                     # web icon config
mainConfig = sub.mainConfig                     # pipeline packages config
appConfig = sub.appConfig                       # all app installed config

DAMGLOGO = sub.DAMGLOGO
PLTLOGO = sub.PLTLOGO

# -------------------------------------------------------------------------------------------------------------
""" DAMG team """

__organization__ = "DAMG team"
__damgSlogan__ = "Desire Design"
__website__ = "https://damgteam.com"
__author1__ = "Trinh Do"
__author2__ = "Duong Minh Duc"
__Founder__ = __author1__
__CoFonder1__ = __author2__
__email1__ = "dot@damgteam.com"
__email2__ = "up@damgteam.com"

# -------------------------------------------------------------------------------------------------------------
""" PipelineTool """

__project__ = "Pipeline Tool (Plt)"
__appname__ = "PLT"
__appShortcut__ = "Plt.ink"
__version__ = "13.0.1"
__cfgVersion__ = "0.8.6"
__verType__ = "Dev"
__reverType__ = "2"
__about__ = "About plt"
__homepage__ = "https://pipeline.damgteam.com"
__pltSlogan__ = "Creative solution for problem solving"
__pltWiki__ = "https://github.com/vtta2008/PipelineTool/wiki"

# -------------------------------------------------------------------------------------------------------------
""" Server """

__serverLocal__ = "http://127.0.0.1:8000/"
__serverUrl__ = "https://pipeline.damgteam.com"
__serverCheck__ = "https://pipeline.damgteam.com/check"
__serverAutho__ = "https://pipeline.damgteam.com/auth"

__google__ = "https://google.com.vn"

# -------------------------------------------------------------------------------------------------------------
""" Metadata """

VERSION = "{0} v{1}.{2}-{3}".format(__project__, __version__, __verType__, __reverType__)
COPYRIGHT = "{0} software (c) 2017-2018 {1}. All rights reserved.".format(__appname__, __organization__)
PLUGINVERSION = "{0}.13.cfg.{1}".format(__appname__, __cfgVersion__)
PLTAPPID = u'{0}.{1}.{2}.{3}'.format(__organization__, __project__, __appname__, VERSION)

# --------------------------------------------------------------------------------------------------------------
""" Config data """

KEYDETECT = sub.KEYDETECT

CONFIG_APPUI = sub.CONFIG_APPUI

pVERSION = dict(autodesk=sub.autodeskVer, adobe=sub.adobeVer, foundry=sub.foundryVer, pixologic=sub.pixologiVer,
                sizefx=sub.sizefxVer, office=sub.officeVer, jetbrains=sub.jetbrainsVer)

pPACKAGE = dict(autodesk=sub.autodeskApp, adobe=sub.adobeApp, foundry=sub.foundryApp, pixologic=sub.pixologiApp,
                sizefx=sub.sizefxApp, office=sub.officeApp, jetbrains=sub.jetbrainsApp)

pTRACK = dict(TDS=sub.TRACK_TDS, VFX=sub.TRACK_VFX, ART=sub.TRACK_ART, Office=sub.TRACK_OFFICE, Dev=sub.TRACK_DEV,
              Tools=sub.TRACK_TOOLS, Extra=sub.TRACK_EXTRA, sysTray=sub.TRACK_SYSTRAY, )

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

    return keyPackage + sub.otherApp + sub.anacondaApp + CONFIG_APPUI + ['Word', 'Excel', 'PowerPoint']

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

# ----------------------------------------------------------------------------------------------------------- #
""" Setup.py options """

__email__ = __email1__ + ", " + __email2__

__packages_dir__ = ["", "ui", "appData", "tankers", "docs", "imgs", "utilities"]

__classifiers__ = [
              "Development Status :: 3 - Production/Unstable",
              "Environment :: X11 Applications :: Qt",
              "Environment :: Win64 (MS Windows)",
              "Intended Audience :: Artist :: VFX Company",
              "License :: OSI Approved :: MIT License",
              "Operating System :: Microsoft :: Windows",
              "Programming Language :: Python :: 3.6",
              "Topic :: Software Development :: pipeline-framework :: Application :: vfx :: customization :: optimization :: research-project",
                ]

__download__ = "https://github.com/vtta2008/PipelineTool/releases"

__description__ = "This applications can be used to build, manage, and optimise film making pipelines."

__readme__ = "README.rst"

__modules__ = ["plt", "globals", "_version", "appData.templates.pyTemplate", "utilities.variables", "utilities.utils",
               "utilities.sql_server", "utilities.sql_local", "utilities.message", "ui.ui_acc_setting", "ui.ui_calculator",
               "ui.ui_calendar", "ui.ui_english_dict", "ui.ui_find_files", "ui.ui_image_viewer", "ui.ui_info_template",
               "ui.ui_new_project", "ui.ui_note_reminder", "ui.ui_preference", "ui.ui_pw_reset_form", "ui.ui_screenshot", ]

__pkgsReq__ = [ "deprecated", "jupyter-console", "ipywidgets","pywinauto", "winshell", "pandas", "notebook", "juppyter",
                "opencv-python", "pyunpack", "argparse", "qdarkgraystyle", "asyncio", "websockets", "cx_Freeze", ]

QUESTIONS = sub.read_file(os.path.join(os.getenv(__envKey__), 'appData', 'docs'), 'QUESTION')

ABOUT = sub.read_file(os.path.join(os.getenv(__envKey__), 'appData', 'docs'), 'ABOUT')

CREDIT = sub.read_file(os.path.join(os.getenv(__envKey__), 'appData', 'docs'), 'CREDIT')

README = mes.PLT_ABOUT
# ----------------------------------------------------------------------------------------------------------- #
""" String message """

SYSTRAY_UNAVAI = mes.SYSTRAY_UNAVAI

SIGNUP = mes.SIGNUP

USERBLANK = mes.USER_BLANK

PWBLANK = mes.PW_BLANK
PWWRONG = mes.PW_WRONG
PWCHANGED = mes.PW_CHANGED
PWUNMATCH = mes.PW_UNMATCH


WAITUICOMPLETE = mes.WAIT_LAYOUT_COMPLETE
WAITCOMPLETE = mes.WAIT_TO_COMPLETE

BLANKALERT = mes.SEC_BLANK
USERCHECKREQUIRED = mes.USER_CHECK_REQUIRED

# ----------------------------------------------------------------------------------------------------------- #
""" Global variables setting """

TXT = sub.TXT
WMIN = sub.WMIN
ICONSIZE = sub.ICONSIZE
ICONBTNSIZE = sub.ICONBTNSIZE
BTNICONSIZE = sub.BTNICONSIZE

keepARM = sub.keepARM

SiPoMin = sub.SiPoMin
SiPoExp = sub.SiPoExp
SiPoPre = sub.SiPoPre

left = sub.left
right = sub.right
center = sub.center

# Docking area
dockL = sub.dockL
dockR = sub.dockR
dockT = sub.dockT
dockB = sub.dockB

datetTimeStamp = sub.datetTimeStamp
# ----------------------------------------------------------------------------------------------------------- #