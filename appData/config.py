# -*- coding: utf-8 -*-
"""

Script Name: _data.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import platform, subprocess, json

try:
    from importlib import reload
except ImportError:
    pass

PLATFORM = 'Windows'
API_MINIMUM = 0.64

# PyQt5
from PyQt5                          import __file__ as pyqt_path

from appData                        import metadatas as m
from appData.dirs                   import *
from appData.pths                   import *
from appData.text                   import *
from appData.keys                   import *
from appData.settingFormats         import *
from appData.settingOptions         import *
from bin.data.localSQL              import SQLS

# -------------------------------------------------------------------------------------------------------------
""" Environment configKey """

__envKey__              = m.__envKey__
PLMAPPID                = m.PLMAPPID
VERSION                 = m.VERSION
COPYRIGHT               = m.COPYRIGHT

# -------------------------------------------------------------------------------------------------------------
""" DAMG team """

__copyright__           = m.COPYRIGHT
__organization__        = m.__organization__
__groupname__           = m.__groupname__
__damgSlogan__          = m.__damgSlogan__
__website__             = m.__website__
__author1__             = m.__author1__
__author2__             = m.__author2__
__Founder__             = m.__author1__
__CoFonder1__           = m.__author2__
__email1__              = m.__email1__
__email2__              = m.__email2__

# -------------------------------------------------------------------------------------------------------------
""" PipelineTool """

__project__             = m.__project__
__appname__             = m.__appname__
__appShortcut__         = m.__appShortcut__
__version__             = m.__version__
__versionFull__         = m.VERSION
__cfgVersion__          = m.__cfgVersion__
__verType__             = m.__verType__
__reverType__           = m.__reverType__
__about__               = m.__about__
__homepage__            = m.__homepage__
__plmSlogan__           = m.__plmSlogan__
__plmWiki__             = m.__plmWiki__

# -------------------------------------------------------------------------------------------------------------
""" Server """

__globalServer__        = m.__globalServer__
__globalServerCheck__   = m.__globalServerCheck__
__globalServerAutho__   = m.__globalServerAutho__

__localPort__           = m.__localPort__
__localHost__           = m.__localHost__
__localServer           = m.__localServer__
__localServerCheck__    = m.__localServerCheck__
__localServerAutho__    = m.__localServerAutho__

__google__              = m.__google__
__googleVN__            = m.__googleVN__
__googleNZ__            = m.__googleNZ__

__email__               = m.__email__

__packages_dir__        = m.__packages_dir__
__classifiers__         = m.__classifiers__
__download__            = m.__download__
__description__         = m.__description__
__readme__              = m.__readme__
__modules__             = m.__modules__
__pkgsReq__             = m.__pkgsReq__

# -------------------------------------------------------------------------------------------------------------
""" Config directories """

if not os.path.exists(DB_PTH):
    SQLS(DB_PTH)

allDirs = [APP_DATA_DIR, APP_ICON_DIR, AVATAR_DIR, BASE, BIN_DIR, BODY_DIR, BUILD_DIR, CACHE_DIR,
           CFG_DIR, CONFIG_DAMG_DIR, CONFIG_PLM_DIR, CORES_DIR, CORE_DIR, DAMG_LOGO_DIR, DATA_DIR,
           DB_DIR, DEPENDANCIES_DIR, DESKTOP_DIR, DOCUMENTATION_DIR, FOOTER_DIR, FUNCS_DIR, GUI_DIR,
           HEADER_DIR, HOOK_DIR, HOUDINI_DIR, ICON_DIR_16, ICON_DIR_24, ICON_DIR_32, ICON_DIR_48,
           ICON_DIR_64, IMG_DIR, INFO_DIR, JSON_DIR, LOCALAPPDATA, LOGO_DIR, LOG_DIR, MARI_DIR,
           MAYA_DIR, MAYA_ICON_DIR, MENU_DIR, NETWORK_DIR, NODEGRAPH_DIR, NODE_GRAPH_DIR, NUKE_DIR,
           ORG_DIR, PIC_DIR, PLM_LOGO_DIR, PLUGIN_DIR, PREF_DIR, PRJ_DIR, PROGRAM64, PROGRAM86,
           PROGRAMDATA, PROJECT_DIR, QSS_DIR, RAWS_DATA_DIR, RCS_DIR, RESOURCES_DIR, ROOT_DIR,
           SCRIPTS_DIR, SETTINGS_DIR, SETTING_DIR, SOUND_DIR, SUBUI_DIR, TABS_DIR, TAG_DIR,
           TASK_DIR, TEAM_DIR, TEST_DIR, TMP_DIR, TOOLBAR_DIR, TOOLKIT_DIR, TOOLS_DIR, UI_DIR,
           USER_PREF_DIR, UTILS_DIR, WEB_ICON_128, WEB_ICON_16, WEB_ICON_24, WEB_ICON_32, WEB_ICON_48,
           WEB_ICON_64, WEB_ICON_DIR, WIDGETS_DIR, ZBRUSH_DIR]

allDirs = [i.replace('\\', '/') for i in allDirs]

for p in allDirs:
    if not os.path.exists(p):
        os.makedirs(p, exist_ok=True)

# Set _data folder to invisible (hide)
for d in allDirs:
    if '.' in os.path.basename(d):
        if platform.system() == "Windows":
            subprocess.call(["attrib", "+H", d])
        elif platform.system() == "Darwin":
            subprocess.call(["chflags", "hidden", CFG_DIR])

# -------------------------------------------------------------------------------------------------------------
""" Config qssPths from text file """

def read_file(fileName):

    filePth = os.path.join(RAWS_DATA_DIR, fileName)

    if not os.path.exists(filePth):
        filePth = os.path.join(DOCUMENTATION_DIR, "{}.rst".format(fileName))

    if os.path.exists(filePth):
        with open(filePth, 'r') as f:
            data = f.read()
        return data

QUESTIONS = read_file('QUESTION')
ABOUT = read_file('ABOUT')
CREDIT = read_file('CREDIT')
CODECONDUCT = read_file('CODECONDUCT')
CONTRIBUTING = read_file('CONTRIBUTING')
REFERENCE = read_file('REFERENCE')
LICENCE_MIT = read_file('LICENCE_MIT')

actionTypes = ['DAMGACTION', 'DAMGShowLayoutAction', 'DAMGStartFileAction', 'DAMGExecutingAction', 'DAMGOpenBrowserAction', ]

layoutTypes = ['DAMGUI', 'DAMGWIDGET', ] + actionTypes

with open(mainConfig, 'r') as f:
    mainData = json.load(f)

CONFIG_OFFICE = [k for k in mainData.keys() if k in CONFIG_OFFICE]

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 10:56 PM
# Pipeline manager - DAMGteam
