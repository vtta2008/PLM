# -*- coding: utf-8 -*-
"""

Script Name: Metadata.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" DAMG team """

__envKey__          = "PIPELINE_MANAGER"

__organization__    = "DAMGteam"
__groupname__       = "DAMGteam"
__damgSlogan__      = "Comprehensive Solution Design"
__website__         = "https://damgteam.com"
__author1__         = "Trinh Do"
__author2__         = "Duong Minh Duc"
__Founder__         = __author1__
__CoFonder1__       = __author2__
__email1__          = "dot@damgteam.com"
__email2__          = "up@damgteam.com"

# -------------------------------------------------------------------------------------------------------------
""" PipelineTool """

__project__             = "Pipeline Manager (Plm)"
__appname__             = "PLM"
__appShortcut__         = "Plm.ink"
__version__             = "13.0.1"
__cfgVersion__          = "0.8.6"
__verType__             = "Dev"
__reverType__           = "2"
__about__               = "About Pipeline Manager"
__homepage__            = "https://pipeline.damgteam.com"
__plmSlogan__           = "Creative your own pipeline"
__plmWiki__             = "https://github.com/vtta2008/PipelineTool/wiki"

# -------------------------------------------------------------------------------------------------------------
""" Server """

__serverLocal__         = "http://127.0.0.1:8000/"
__serverUrl__           = "https://pipeline.damgteam.com"
__serverCheck__         = "https://pipeline.damgteam.com/check"
__serverAutho__         = "https://pipeline.damgteam.com/auth"
__google__              = "https://google.com.vn"

# -------------------------------------------------------------------------------------------------------------
""" Metadata """

VERSION                 = "{0} v{1}.{2}-{3}".format(__project__, __version__, __verType__, __reverType__)
COPYRIGHT               = "{0} software (c) 2017-2018 {1}. All rights reserved.".format(__appname__, __organization__)
PLUGINVERSION           = "{0}.13.cfg.{1}".format(__appname__, __cfgVersion__)
PLMAPPID                = "{0}.{1}.{2}.{3}".format(__organization__, __project__, __appname__, VERSION)

API_MAJOR_VERSION       = 0.69
API_REVISION            = 0
API_VERSION             = float('%s%s' % (API_MAJOR_VERSION, API_REVISION))
API_VERSION_AS_STRING   = '%.02f.%d' % (API_MAJOR_VERSION, API_REVISION)
PLATFORM                = 'Windows'
API_MINIMUM             = 0.64

# ----------------------------------------------------------------------------------------------------------- #
""" Setup.py options """

__email__               = __email1__ + ", " + __email2__
__packages_dir__        = ["", 'appData', 'bin', 'core', 'imgs', 'plg_ins', 'ui', 'utilities']
__download__            = "https://github.com/vtta2008/PipelineTool/releases"
__description__         = "This applications can be used to build, manage, and optimise film making pipelines."
__readme__              = "README.rst"
__pkgsReq__             = ['appdirs', 'deprecate', 'msgpack', 'winshell', 'pandas', 'wheel', 'argparse', 'green']
__modules__             = []
__classifiers__         = [

    "Development Status :: 3 - Production/Unstable" , "Environment :: X11 Applications :: Qt"                       ,
    "Environment :: Win64 (MS Windows)"             , "Intended Audience :: Freelance Artist :: small VFX studio"   ,
    "License :: OSI Approved :: MIT License"        , "Operating System :: Microsoft :: Windows"                    ,
    "Programming Language :: Python :: 3.6"         ,

    "Topic :: Software Development :: pipeline-framework :: Application :: vfx :: customization :: optimization :: research-project",
                    ]

# __modules__             = [
#
#     "PLM", "appData/scr/_docs", "appData/config", "appData/ServerCfg", "appData/__init__",
#     "core/Attributes", "core/Configurations", "core/Cores", "core/Errors", "core/EventHandler", "core/keys",
#     "core/Loggers", "core/Metadata", "core/paths", "core/Settings", "core/SQLS", "core/Storage","core/StyleSheets",
#     "core/vlogging", "core/Worker", "bin/resources/pyqt5_style_rc", "plg_ins/Qt", "bin/resources/tooltips_rc", "ui/AppToolbar/DockToolBar",
#     "ui/AppToolbar/MainToolBar", "ui/Funcs/ForgotPassword", "ui/Funcs/SignIn", "ui/Funcs/SignUp", "ui/Info/About",
#     "ui/Info/CodeConduct", "ui/Info/Contributing", "ui/Info/Credit", "ui/Info/LicenceMIT", "ui/Info/Reference",
#     "ui/Info/Version", "ui/Menus/config/config_rc", "ui/Menus/config/Configuration", "ui/Menus/config/Preferences",
#     "ui/Menus/MainMenuBar", "ui/Menus/SubMenuBar", "ui/Network/ServerMonitor", "ui/Network/ServerStatus",
#     "ui/Network/connector/mainwindow", "ui/Network/connector/resources", "ui/Network/connector/server",
#     "ui/NodeGraph/MenuBar",  "ui/NodeGraph/Node",  "ui/NodeGraph/NodeGraph", "ui/NodeGraph/Scene",  "ui/NodeGraph/View",
#     "ui/Projects/NewProject", "ui/Settings/SettingUI", "ui/Settings/UserSetting", "ui/Tools/TextEditor/TextEditor",
#     "ui/Tools/TextEditor/TextEditor_rc", "ui/Tools/Calculator", "ui/Tools/Calendar", "ui/Tools/EnglishDictionary",
#     "ui/Tools/FindFiles", "ui/Tools/ImageViewer", "ui/Tools/NoteReminder", "ui/Tools/Screenshot", "ui/uikits/Action",
#     "ui/uikits/Button", "ui/uikits/DockWidget", "ui/uikits/GridLayout", "ui/uikits/GroupBox", "ui/uikits/node_widgets",
#     "ui/uikits/TabWidget", "ui/uikits/ToolBar", "ui/uikits/UiPreset", "ui/uikits/Widget", "ui/Web/PLMBrowser",
#     "ui/Web/PLMBrowser_rc", "ui/BotTab", "ui/Debugger", "ui/Footer", "ui/GeneralSetting", "ui/PipelineManager",
#     "ui/StatusBar", "ui/SysTrayIcon", "ui/TopTab", "ui/TopTab1", "ui/TopTab2", "ui/TopTab3", "ui/TopTab4", "ui/TopTab5",
#     "utilities/localSQL", "utilities/utils", ]

# includefiles = [
#     ["appData/docs/ABOUT", "appData/docs/CODECONDUCT", "appData/docs/CONTRIBUTING", "appData/docs/CREDIT",
#      "appData/docs/LICENCE_MIT", "appData/docs/QUESTION", "appData/docs/REFERENCE", "appData/ED.json",
#      "preSetup/krita-x64-4.1.1-setup.exe", "preSetup/storyboarder-setup-1.7.1.exe", "qss/darkstyle.qss",
#      "qss/nuke.qss", "qss/stylesheet.qss", "LICENSE", "README.rst"],
#
#     ["build/appData/docs/ABOUT", "build/appData/docs/CODECONDUCT", "build/appData/docs/CONTRIBUTING", "build/appData/docs/CREDIT",
#      "build/appData/docs/LICENCE_MIT", "appData/docs/QUESTION", "build/appData/docs/REFERENCE", "build/appData/ED.json",
#      "build/preSetup/krita-x64-4.1.1-setup.exe", "build/preSetup/storyboarder-setup-1.7.1.exe", "build/qss/darkstyle.qss",
#      "build/qss/nuke.qss", "build/qss/stylesheet.qss", "build/LICENSE", "build/README.rst"],
# ]

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/07/2018 - 12:41 AM
# © 2017 - 2018 DAMGteam. All rights reserved