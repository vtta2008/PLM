# -*- coding: utf-8 -*-
"""

Script Name: __init__.py.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

    This is our source code directory, which should be named by your application or package you are working on.
    Inside we have the usual __init__.py file signifying that it's a Python package, next there is __main__.py
    which is used when we want to run our application directly with python -m blueprint. Last source file here
    is the app.py which is here really just for demonstration purposes. In real project instead of this app.py
    you would have few top level source files and more directories (internal packages). We will get to contents
    of these files a little later. Finally, we also have resources directory here, which is used for any static
    content your application might need, e.g. images, keystore, etc.

"""

# -------------------------------------------------------------------------------------------------------------
""" Import """
# Python
import os, sys, subprocess
from termcolor                      import cprint
from pyjavaproperties               import Properties

# PLM
from .globalSettings                import GlobalSettings
from PLM.api.version                import Version


# -------------------------------------------------------------------------------------------------------------
""" Metadatas """

__envKey__                          = "PLM"
__appName__                         = "Pipeline Manager (PLM)"
__version__                         = Version()
__organization__                    = "DAMGTEAM"
__apiName__                         = "DAMG API"
__apiVersion__                      = Version(0, 0, 1)

TRADE_MARK                          = '™'

RAM_TYPE                         = {0: 'Unknown', 1: 'Other', 2: 'DRAM', 3: 'Synchronous DRAM', 4: 'Cache DRAM',
                                    5: 'EDO', 6: 'EDRAM', 7: 'VRAM', 8: 'SRAM', 9: 'RAM', 10: 'ROM', 11: 'Flash',
                                    12: 'EEPROM', 13: 'FEPROM', 14: 'EPROM', 15: 'CDRAM', 16: '3DRAM', 17: 'SDRAM',
                                    18: 'SGRAM', 19: 'RDRAM', 20: 'DDR', 21: 'DDR2', 22: 'DDR2 FB-DIMM', 24: 'DDR3',
                                    25: 'FBD2', }

FORM_FACTOR                      = {0: 'Unknown', 1: 'Other', 2: 'SIP', 3: 'DIP', 4: 'ZIP', 5: 'SOJ', 6: 'Proprietary',
                                    7: 'SIMM', 8: 'DIMM', 9: 'TSOP', 10: 'PGA', 11: 'RIMM', 12: 'SODIMM', 13: 'SRIMM',
                                    14: 'SMD', 15: 'SSMP', 16: 'QFP', 17: 'TQFP', 18: 'SOIC', 19: 'LCC', 20: 'PLCC',
                                    21: 'BGA', 22: 'FPBGA', 23: 'LGA', 24: 'FB-DIMM', }

CPU_TYPE                         = {1: 'Other', 2: 'Unknown', 3: 'Central Processor', 4: 'Math Processor', 5: 'DSP Processor',
                                    6: 'Video Processor', }

DRIVE_TYPE                       = {0 : "Unknown", 1 : "No Root Directory", 2 : "Removable Disk", 3 : "Local Disk",
                                    4 : "Network Drive", 5 : "Compact Disc", 6 : "RAM Disk", }

DB_ATTRIBUTE_TYPE               = { 'int_auto_increment'    : 'INTERGER PRIMARY KEY AUTOINCREMENT, ',
                                    'int_primary_key'       : 'INT PRIMARY KEY, ',
                                    'text_not_null'         : 'TEXT NOT NULL, ',
                                    'text'                  : 'TEXT, ',
                                    'bool'                  : 'BOOL, ',
                                    'varchar'               : 'VARCHAR, ',
                                    'varchar_20'            : 'VACHAR(20,)  ', }

CMD_VALUE_TYPE                  = { 'dir'                   : 'directory',
                                    'pth'                   : 'path',
                                    'url'                   : 'link',
                                    'func'                  : 'function',
                                    'cmd'                   : 'commandPrompt',
                                    'event'                 : 'PLM Event',
                                    'stylesheet'            : 'PLMstylesheet',
                                    'shortcut'              : 'shortcut',
                                    'uiKey'                 : 'PLM Layout Key', }

actionTypes                    = ['DAMGACTION', 'DAMGShowLayoutAction', 'DAMGStartFileAction', 'DAMGExecutingAction',
                                  'DAMGOpenBrowserAction', 'DAMGWIDGETACTION']
buttonTypes                     = ['DAMGBUTTON', 'DAMGTOOLBUTTON']
urlTypes                        = ['DAMGURL', 'Url', 'url']
layoutTypes                     = ['DAMGUI', 'DAMGWIDGET', ] + actionTypes

def __copyright__():
    return 'Copyright (C) DAMGTEAM. All right reserved.'

def path_exists(path):
    if not os.path.exists(path):
        cprint("PathNotExistsed: {0}".format(path), 'red', attrs=['blink'])
    return os.path.exists(path)

def create_path(*args):
    path                            = os.path.abspath(os.path.join(*args)).replace('\\', '/')
    path_exists(path)
    return path

def current_directory():
    path                            = os.path.abspath(os.getcwd()).replace('\\', '/')
    path_exists(path)
    return path

def parent_dir(path):
    path                            = os.path.abspath(os.path.join(path, os.pardir)).replace('\\', '/')
    path_exists(path)
    return path

def directory_name(path):
    return os.path.basename(path)

# get current directory path
cwd                                 = current_directory()

if directory_name(cwd) == directory_name(parent_dir(cwd)) == __envKey__:
    ROOT_APP                        = parent_dir(cwd)
    ROOT                            = cwd
else:
    if directory_name(cwd) == __envKey__:
        ROOT_APP                    = cwd
        ROOT                        = create_path(ROOT_APP, __envKey__)
    else:
        try:
            os.getenv(__envKey__)
        except KeyError:
            cprint("Wrong root path. Current directory: {0}".format(cwd), 'red', attrs=['underline', 'blink'])
            sys.exit(__copyright__())
        else:
            ROOT                    = os.getenv(__envKey__)
            ROOT_APP                = parent_dir(ROOT)

glbSettings                         = GlobalSettings()
qtBinding                           = glbSettings.qtBinding

textProp                                = create_path(ROOT_APP, 'bin', 'text.properties')
glbProp                                 = create_path(ROOT_APP, 'bin', 'global.properties')

prop1                                   = Properties()
prop1.load(open(textProp))

prop2                                   = Properties()
prop2.load(open(glbProp))


LOCALAPPDATA                            = os.getenv('LOCALAPPDATA')
USER_DIR                                = parent_dir(os.getenv('HOME'))

APPDATA_DAMG                            = create_path(LOCALAPPDATA, __organization__)
APPDATA_PLM                             = create_path(APPDATA_DAMG, __appName__)

CFG_DIR                                 = create_path(APPDATA_PLM, '.configs')
TMP_DIR                                 = create_path(APPDATA_PLM, '.tmp')
CACHE_DIR                               = create_path(APPDATA_PLM, '.cache')
PREF_DIR                                = create_path(APPDATA_PLM, 'preferences')

SETTING_DIR                             = CFG_DIR
DB_DIR                                  = APPDATA_PLM
LOG_DIR                                 = CFG_DIR

APP_SETTING                             = create_path(SETTING_DIR, 'PLM.ini')
USER_SETTING                            = create_path(SETTING_DIR, 'user.ini')
FORMAT_SETTING                          = create_path(SETTING_DIR, 'format.ini')
UNIX_SETTING                            = create_path(SETTING_DIR, 'unix.ini')

APPDATA_DAMG                            = create_path(LOCALAPPDATA, __organization__)
APPDATA_PLM                             = create_path(APPDATA_DAMG, __appName__)

CFG_DIR                                 = create_path(APPDATA_PLM, '.configs')

SETTING_DIR                             = CFG_DIR

LOCAL_LOG                               = create_path(LOG_DIR, 'PLM.logs')

RESOURCES_DIR                           = create_path(ROOT, 'resources')

ICON_DIR                                = create_path(RESOURCES_DIR, 'icons')

TAG_ICON_DIR                            = create_path(ICON_DIR, 'tags')

NODE_ICON_DIR                           = create_path(ICON_DIR, 'nodes')

WEB_ICON_DIR                            = create_path(ICON_DIR, 'web')
WEB_ICON_16                             = create_path(WEB_ICON_DIR, 'x16')
WEB_ICON_24                             = create_path(WEB_ICON_DIR, 'x24')
WEB_ICON_32                             = create_path(WEB_ICON_DIR, 'x32')
WEB_ICON_48                             = create_path(WEB_ICON_DIR, 'x48')
WEB_ICON_64                             = create_path(WEB_ICON_DIR, 'x64')
WEB_ICON_128                            = create_path(WEB_ICON_DIR, 'x128')

ICON_DIR_12                             = create_path(ICON_DIR, 'x12')
ICON_DIR_16                             = create_path(ICON_DIR, 'x16')
ICON_DIR_24                             = create_path(ICON_DIR, 'x24')
ICON_DIR_32                             = create_path(ICON_DIR, 'x32')
ICON_DIR_48                             = create_path(ICON_DIR, 'x48')
ICON_DIR_64                             = create_path(ICON_DIR, 'x64')

IMAGE_DIR                               = create_path(RESOURCES_DIR, 'images')

LOGO_DIR                                = create_path(RESOURCES_DIR, 'logo')
ORG_LOGO_DIR                            = create_path(LOGO_DIR, 'DAMGTEAM')
APP_LOGO_DIR                            = create_path(LOGO_DIR, 'PLM')

SCRIPTS_DIR                             = create_path(ROOT, 'scripts')

QSS_DIR                                 = create_path(SCRIPTS_DIR, 'qss')

FONT_DIR                                = create_path(RESOURCES_DIR, 'fonts')

TASK_DIR                                = create_path(CFG_DIR, 'task')
TEAM_DIR                                = create_path(CFG_DIR, 'team')
PRJ_DIR                                 = create_path(CFG_DIR, 'project')
ORG_DIR                                 = create_path(CFG_DIR, 'organisation')
USER_LOCAL_DATA                         = create_path(CFG_DIR, 'userLocal')

LIBRARY_DIR                             = create_path(USER_DIR, 'UserLibraries')

BIN_DIR                                 = create_path(ROOT_APP, 'bin')

DOCS_DIR                                = create_path(ROOT_APP, 'docs')
RAWS_DIR                                = create_path(DOCS_DIR, 'raws')
DOCS_READING_DIR                        = create_path(DOCS_DIR, 'reading')
TEMPLATE_DIR                            = create_path(DOCS_DIR, 'template')
TEMPLATE_LICENSE                        = create_path(TEMPLATE_DIR, 'LICENSE')

INTERGRATIONS_DIR                       = create_path(ROOT_APP, 'intergrations')
BLENDER_DIR                             = create_path(INTERGRATIONS_DIR, 'Blender')
HOUDINI_DIR                             = create_path(INTERGRATIONS_DIR, 'Houdini')
MARI_DIR                                = create_path(INTERGRATIONS_DIR, 'Mari')
MAYA_DIR                                = create_path(INTERGRATIONS_DIR, 'Maya')
MUDBOX_DIR                              = create_path(INTERGRATIONS_DIR, 'Mudbox')
NUKE_DIR                                = create_path(INTERGRATIONS_DIR, 'Nuke')
SUBSTANCES_DIR                          = create_path(INTERGRATIONS_DIR, 'Substances')
ZBRUSH_DIR                              = create_path(INTERGRATIONS_DIR, 'ZBrush')
Others_DIR                              = create_path(INTERGRATIONS_DIR, 'Others')

API_DIR                                 = create_path(ROOT, 'api')
CORE_DIR                                = create_path(API_DIR, 'Core')
DAMG_DIR                                = create_path(API_DIR, 'damg')
GUI_DIR                                 = create_path(API_DIR, 'Gui')
NETWORK_DIR                             = create_path(API_DIR, 'Network')
WIDGET_DIR                              = create_path(API_DIR, 'Widgets')

CONFIGS_DIR                             = create_path(ROOT, 'configs')

CORES_DIR                               = create_path(ROOT, 'cores')
CORES_BASE_DIR                          = create_path(CORES_DIR, 'base')
CORES_DATA_DIR                          = create_path(CORES_DIR, 'data')
CORES_HANDLERS_DIR                      = create_path(CORES_DIR, 'handlers')
CORES_MODELS_DIR                        = create_path(CORES_DIR, 'models')
CORES_SETTINGS_DIR                      = create_path(CORES_DIR, 'settings')

LOGGER_DIR                              = create_path(ROOT, 'loggers')
PLUGINS_DIR                             = create_path(ROOT, 'plugins')

RESOURCES_DIR                           = create_path(ROOT, 'resources')

AVATAR_DIR                              = create_path(RESOURCES_DIR, 'avatar')

DESIGN_DIR                              = create_path(RESOURCES_DIR, 'design')


JSON_DIR                                = create_path(RESOURCES_DIR, 'json')


SOUND_DIR                               = create_path(BIN_DIR, 'sound')

SCRIPTS_DIR                             = create_path(ROOT, 'scripts')
CSS_DIR                                 = create_path(SCRIPTS_DIR, 'css')
HTML_DIR                                = create_path(SCRIPTS_DIR, 'html')
JS_DIR                                  = create_path(SCRIPTS_DIR, 'js')

SETTINGS_DIR                            = create_path(ROOT, 'settings')
TYPES_DIR                               = create_path(ROOT, 'types')

UI_DIR                                  = create_path(ROOT, 'ui')
UI_BASE_DIR                             = create_path(UI_DIR, 'base')
UI_COMPONENTS_DIR                       = create_path(UI_DIR, 'components')
UI_LAYOUTS_DIR                          = create_path(UI_DIR, 'layouts')
UI_MODELS_DIR                           = create_path(UI_DIR, 'models')
UI_RCS_DIR                              = create_path(UI_DIR, 'rcs')
UI_TOOLS_DIR                            = create_path(UI_DIR, 'tools')

UTILS_DIR                               = create_path(ROOT, 'utils')

TESTS_DIR                               = create_path(ROOT_APP, 'tests')

evnInfoCfg                              = create_path(CFG_DIR, 'envs.cfg')

avatarCfg                               = create_path(CFG_DIR, 'avatars.cfg')
webIconCfg                              = create_path(CFG_DIR, 'webIcon.cfg')
nodeIconCfg                             = create_path(CFG_DIR, 'nodeIcons.cfg')
imageCfg                                = create_path(CFG_DIR, 'images.cfg')
tagCfg                                  = create_path(CFG_DIR, 'tags.cfg')
envVarCfg                               = create_path(CFG_DIR, 'envVar.cfg')
userCfg                                 = create_path(CFG_DIR, 'user.cfg')
PLMconfig                               = create_path(CFG_DIR, 'PLM.cfg')
sceneGraphCfg                           = create_path(CFG_DIR, 'sceneGraph.cfg')
splashImagePth                          = create_path(IMAGE_DIR, 'splash.png')
serverCfg                               = create_path(CFG_DIR, 'server.cfg')

LOCAL_DB                                = create_path(DB_DIR, 'local.db')


ks                                      = ['icon12', 'icon16', 'icon24', 'icon32', 'icon48', 'icon64', 'node', 'tag',
                                           'web16', 'web24', 'web32', 'web48', 'web64', 'web128']

ds                                      = [ICON_DIR_12, ICON_DIR_16, ICON_DIR_24, ICON_DIR_32, ICON_DIR_48, ICON_DIR_64,
                                           NODE_ICON_DIR, TAG_ICON_DIR, WEB_ICON_16, WEB_ICON_24, WEB_ICON_32,
                                           WEB_ICON_48, WEB_ICON_64, WEB_ICON_128]

IMAGE_ext                               = "All Files (*);;Img Files (*.jpg);;Img Files (*.png)"

cprint("{0} v{1}".format(__appName__, __version__), 'cyan')

PIPE                                = subprocess.PIPE

try:
    os.getenv(__envKey__)
except KeyError:
    process = subprocess.Popen('SetX {0} {1}'.format(__envKey__, ROOT), stdout=PIPE, stderr=PIPE, shell=True).wait()
else:
    if os.getenv(__envKey__) != ROOT:
        subprocess.Popen('SetX {0} {1}'.format(__envKey__, ROOT), stdout=PIPE, stderr=PIPE, shell=True).wait()
finally:
    glbSettings.cfgable = True


if glbSettings.qtBinding == 'PyQt5':
    try:
        import PyQt5
    except ImportError:
        subprocess.Popen('python -m pip install {0}={1} --user'.format(glbSettings.qtBinding, glbSettings.qtVersion), shell=True).wait()
    finally:
        from PyQt5.QtCore import pyqtSlot as Slot, pyqtSignal as Signal, pyqtProperty as Property
elif glbSettings.qtBinding == 'PySide2':
    try:
        import PySide2
    except ImportError:
        subprocess.Popen('python -m pip install {0}={1} --user'.format(glbSettings.qtBinding, glbSettings.qtVersion), shell=True).wait()
    finally:
        from PySide2.QtCore import Slot, Signal, Property


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/16/2020 - 2:15 AM
# © 2017 - 2019 DAMGteam. All rights reserved