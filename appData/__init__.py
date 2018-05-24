#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: __init__.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Check data flowing """
# print("Import from modules: {file}".format(file=__name__))
# print("Directory: {path}".format(path=__file__.split(__name__)[0]))
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os
from importlib import reload as r

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QSizePolicy, QFrame

# -------------------------------------------------------------------------------------------------------------
""" Global variables """

__envKey__ = "PIPELINE_TOOL"

__project__ = "Pipeline Tool"

__version__ = "13.0.1"

__verType__ = "Dev"

__reverType__ = "1"

__appname__ = "Pipeline Tool"

__slogan__ = "Creative solution for problem solving"

__about__ = "About plt"

__organization__ = "DAMG team"

__website__ = "https://pipeline.damgteam.com"

__pltWiki__ = "https://github.com/vtta2008/PipelineTool/wiki"

__download__ = "https://github.com/vtta2008/pipelineTool"

__email__ = "dot@damgteam.com, up@damgteam.com"

__author__ = "Trinh Do, Duong Minh Duc"

__description__ = "This applications can be used to build, manage, and optimise film making pipelines."

__readme__ = "README.rst"

__modules__ = ["plt", "globals", "_version", "appData.templates.pyTemplate", "utilities.variables", "utilities.utils",
               "utilities.sql_server", "utilities.sql_local", "utilities.message", "ui.ui_acc_setting", "ui.ui_calculator",
               "ui.ui_calendar", "ui.ui_english_dict", "ui.ui_find_files", "ui.ui_image_viewer", "ui.ui_info_template",
               "ui.ui_new_project", "ui.ui_note_reminder", "ui.ui_preference", "ui.ui_pw_reset_form", "ui.ui_screenshot", ]
__pkgsReq__ = [ "deprecated", "jupyter-console", "ipywidgets","pywinauto", "winshell", "pandas", "notebook", "juppyter",
                "opencv-python", "pyunpack", "argparse", "qdarkgraystyle", "asyncio", "websockets", "cx_Freeze", ]

__packages_dir__ = ["", "ui", "appData", "appPackages", "docs", "imgs", "utilities"]


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

__homepage__ = "https://pipeline.damgteam.com"

__server__ = "https://pipeline.damgteam.com"

__serverCheck__ = "https://pipeline.damgteam.com/check"

__serverAutho__ = "https://pipeline.damgteam.com/auth"

VERSION = "{0} v{1}.{2}-{3}".format(__project__, __version__, __verType__, __reverType__)

COPYRIGHT = "Copyright (C) 2017 - 2018 by DAMG team."

KEY_PKGS = ['3ds Max', 'Advance Rename', 'After Effects', 'Audition', 'Git Bash', 'Hiero', 'Houdini FX',
            'Illustrator', 'Katana', 'Mari', 'Maya', 'McWord', 'McExcel', 'McPowerPoint', 'Mudbox', 'NukeX', 'Photoshop', 'Premiere Pro', 'PyCharm',
            'QtDesigner', 'Snipping Tool', 'Sublime Text', 'Substance Painter', 'UVLayout', 'Wordpad', 'ZBrush']

KEY_DETECT = ["Non-commercial", "Uninstall", "Verbose", "License", "Skype"]

CONFIG_ART = ['Adobe Photoshop CC 2018', 'Adobe Illustrator CC 2018']

CONFIG_VFX = ['NukeX11.1v1', 'Davinci Resolve', 'Hiero11.1v1', 'HieroPlayer11.1v1', 'Adobe After Effects CC 2018',
              'Adobe Premiere Pro CC 2018']

CONFIG_TDS = ['Autodesk Maya 2017', 'ZBrush 4R8', 'Mari 4.0v1', 'Houdini FX', 'Substance Painter']

CONFIG_DEV = ['JetBrains PyCharm 2017.3.3', 'Sublime Text 3', 'QtDesigner', 'Git Bash', 'Command Prompt']

CONFIG_EXTRA = ['Autodesk 3Ds Max 2017', 'Autodesk 3Ds Max 2018', 'Autodesk Mudbox 2017', 'Autodesk Mudbox 2018']

CONFIG_OFFICE = ['McWord', 'McExcel', 'McPowerPoint', 'Wordpad']

CONFIG_PQUI = ['AboutPlt', 'Calculator', 'Calendar', 'Credit', 'EnglishDictionary', 'FindFiles', 'ForgotPassword', 'ImageViewer',
               'NewProject', 'NoteReminder', 'Preferences', 'Screenshot', 'TextEditor', 'UserSetting']

CONFIG_PQUIP1 = ['Calculator', 'Calendar', 'EnglishDictionary', 'FindFiles', 'ImageViewer', 'NoteReminder', 'PltBrowser',
                 'Screenshot', 'TextEditor', ]

CONFIG_TRAY1 = ['Mute', 'VolumeUp', 'VolumeDown', 'ChannelUp', 'ChannelDown']

CONFIG_TRAY2 = ['Snipping Tool', 'Screenshot']

# -------------------------------------------------------------------------------------------------------------
""" Global setting """

__imgExt = "All Files (*);;Img Files (*.jpg);;Img Files (*.png)"

keepARM = Qt.KeepAspectRatio
ignoreARM = Qt.IgnoreAspectRatio

scrollAsNeed = Qt.ScrollBarAsNeeded
scrollOff = Qt.ScrollBarAlwaysOff
scrollOn = Qt.ScrollBarAlwaysOn

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
ICON_SIZE = 30
ICON_BUFFRATE = 10
ICON_BUFFREGION = -1
ICON_BUFF = ICON_BUFFREGION*(ICON_SIZE*ICON_BUFFRATE/100)
ICON_SET_SIZE = QSize(ICON_SIZE+ICON_BUFF, ICON_SIZE+ICON_BUFF)

# ----------------------------------------------------------------------------------------------------------- #
""" Check plt scripts runable """

try:
    pth = os.path.join(os.getenv(__envKey__))
except TypeError:
    raise KeyError("We need environment variable to run.")
else:
    CONFIGPTH = os.path.join(os.getenv(__envKey__), 'appData', 'config')
    LOGPTH = os.path.join(os.getenv(__envKey__), 'appData', 'logs', 'Plt.log')
    SETTINGPTH = os.path.join(os.getenv(__envKey__), 'appData', 'settings')

def reload(module):
    return r(module)