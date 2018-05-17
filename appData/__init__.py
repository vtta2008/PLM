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
import os

# -------------------------------------------------------------------------------------------------------------
""" Global variables """

__envKey__ = "PIPELINE_TOOL"

__project__ = "Pipeline Tool"

__version__ = "13.0.1"

__appname__ = "Pipeline Tool (Plt)"

__about__ = "About plt"

__organization__ = "DAMG team"

__website__ = "https://pipeline.damgteam.com"

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

__server__ = "https://pipeline.damgteam.com"

__serverCheck__ = "https://pipeline.damgteam.com/check"

__serverAutho__ = "https://pipeline.damgteam.com/auth"

VERSION = "{0} v{1}".format(__project__, __version__)

UDP_IP = "192.168.1.1"

UDP_PORT = 20118

KEY_PKGS = ["Maya", "3ds Max", "Mudbox", "Houdini FX", "ZBrush", "Mari", "Substance Painter", "NukeX", "Hiero",
            "After Effects", "Premiere Pro", "Photoshop", "Illustrator", "Word", "Excel", "Snipping Tool", "UVLayout",
            "Audition", "Git Bash", "Git CMD", "Advance Rename", "PyCharm", "Sublime Text", "QtDesigner", "Katana",]

KEY_DETECT = ["Non-commercial", "Uninstall", "Verbose", "License", "Skype"]

CONFIG_ART = ['Adobe Photoshop CC 2018', 'Adobe Illustrator CC 2018']

CONFIG_VFX = ['NukeX11.1v1', 'Davinci Resolve', 'Hiero11.1v1', 'HieroPlayer11.1v1', 'Adobe After Effects CC 2018',
              'Adobe Premiere Pro CC 2018']

CONFIG_TDS = ['Autodesk Maya 2017', 'ZBrush 4R8', 'Mari 4.0v1', 'Houdini FX', 'Substance Painter']

CONFIG_DEV = ['JetBrains PyCharm 2017.3.3', 'Sublime Text 3', 'QtDesigner']

CONFIG_CMD = ['Git CMD', 'Git Bash', 'Command Prompt']

CONFIG_MAIN = ['Calculator', 'Calendar', 'EnglishDictionary', 'FindFiles', 'ForgotPassword', 'ImageViewer',
               'InfoTemplate', 'NewProject', 'NoteReminder', 'Preference', 'Screenshot', 'SignIn', 'SignUp',
               'TextEditor', 'UserSetting', 'WebBrowser', ]

CONFIG_TAB1 = ['NoteReminder', 'TextEditor', 'EnglishDictionary', 'Screenshot', 'Calculator',
               'Calendar', 'FindFiles', 'ImageViewer', 'WebBrowser']

CONFIG_TRAY1 = ['FM', 'ViewSplit', 'Mute', 'VolumeUp', 'VolumeDown', 'ChannelUp', 'ChannelDown']

CONFIG_TRAY2 = ['Snipping Tool', 'Screenshot']

CONFIGPTH = os.path.join(os.getenv(__envKey__), 'appData', 'config')

LOGPTH = os.path.join(os.getenv(__envKey__), 'appData', 'logs')

SETTINGPTH = os.path.join(os.getenv(__envKey__), 'appData', 'settings')