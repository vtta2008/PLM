# -*- coding: utf-8 -*-
'''

Script Name: path.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

'''
# -------------------------------------------------------------------------------------------------------------

# Python
import os
import re
import sys
import subprocess
import platform
import pkg_resources
import winshell
import socket
import uuid
import wmi
import pprint
from collections                    import OrderedDict

# PLM
from PLM                            import globalSetting, ROOT, ROOT_APP, save_data

from .metadatas                     import (__appname__, __organizationName__, __localServer__, __globalServer__,
                                            __homepage__, __plmWiki__, __google__, __googleNZ__, __googleVN__,
                                            __plmWiki__, __localServer__, __pkgsReq__, __homepage__, __appname__,
                                            __organization__, __organizationID__, __organizationName__, __globalServer__,
                                            __google__, __appSlogan__, __localServerAutho__, __version__, __website__,
                                            VERSION, PLMAPPID)
# PyQt5
from PyQt5.QtCore                   import Qt, QSize, QEvent, QSettings, QDateTime
from PyQt5.QtGui                    import QPainter, QFont
from PyQt5.QtWidgets                import (QGraphicsItem, QGraphicsView, QGraphicsScene, QRubberBand, QFrame, QSizePolicy,
                                            QLineEdit, QPlainTextEdit, QAbstractItemView, QStyle, QApplication)


TRADE_MARK = '™'

PLM_ABOUT = """

    PIPELINE MANAGER TO MAKE A SHORT FILM

    This application is built to handle and manage productions as a pipeline tool.
    Currently, it is working with software package: maya, ZBrush, mari, nuke with V-ray plugin.

    The largest version of Python is Python 3.5, however Python 3.x has introduced many breaking changes to Python. 
    These changes are for the better but due to large investment into Python 2 code, maya will continue to be on 
    Python 2 for a while longer.

    You can see the details off platforms that is agreed by industry: www.vfxplatform.com.

    For feedback or questions, feel free to email me: damgteam@gmail.com or dot@damgteam.com

"""


WAIT_FOR_UPDATE = """

this function is currenly under construction, please wait for next update.             
JimJim  

"""

WAIT_TO_COMPLETE = "This function is not completed yet. Please try again later"

WAIT_LAYOUT_COMPLETE = "Udating..."

PASSWORD_FORGOTTON = """

How the hell you forgot your password? Make a showLayout_new one now!!!
(This function will be update soon.)

"""

SIGNUP = "Do not have account?"

DISALLOW = "Sorry, but only Admin can do this function, please contact JimJim for details."
TIT_BLANK = 'Blank title will be set to "Tester"'

PW_BLANK = "Password must not be blank."
PW_WRONG = "Wrong username or password."
PW_UNMATCH = "Password doesn't match"
PW_CHANGED = "Your password has changed"

FN_BLANK = "Firstname must not be blank"
LN_BLANK = "Lastname must not be blank"
SEC_BLANK = " section should not be blank."

USER_CHECK_REQUIRED = "I agree to the DAMG Terms of Service"

USER_NOT_CHECK = "You must agree with DAMG team term of service"

USER_BLANK = "Username must not be blank."

USER_CHECK_FAIL = "Wrong username or password"

USER_NOT_EXSIST = "The username does not exists"

USER_CONDITION = "This username is under condition and can not log in, please contact to admin."

SYSTRAY_UNAVAI = "Systray could not detect any system tray on this system"

PTH_NOT_EXSIST = "Could not find directory path specific"

ERROR_OPENFILE = "There was an error opening the file"

ERROR_QIMAGE = "ImageViewer.setImage: Argument must be a QImage or QPixmap."

# what to present when the user hovers the cells
tooltips_present = [ "When the message was sent", "The text of the message (double click to copy to the clipboard)",
                     "The media (image, audio, etc) included in the message",
                     "Select to remove the message from the system", ]

tooltips_missing = [
    None,
    "No text included in the message",
    "No media included in the message",
    None,
]

N_MESSAGES_TEXT = "{quantity} showLayout_new messages"

SERVER_CONNECT_FAIL = "Connection to server failed. PLM can not run without connecting to server. Please try again "

TEMPLATE_QRC_HEADER = '''
<RCC warning="File created programmatically. All changes made in this file will be lost!">
  <qresource prefix="{resource_prefix}">
'''

TEMPLATE_QRC_FILE = '    <file>rc/{fname}</file>'

TEMPLATE_QRC_FOOTER = '''
  </qresource>
  <qresource prefix="{style_prefix}">
      <file>dark.qss</file>
  </qresource>
</RCC>
'''

HEADER_SCSS = '''// ---------------------------------------------------------------------------
//
//    File created programmatically
//
//    WARNING! All changes made in this file will be lost!
//
//----------------------------------------------------------------------------
'''

HEADER_QSS = '''/* ---------------------------------------------------------------------------

    Created by the qtsass compiler

    WARNING! All changes made in this file will be lost!

--------------------------------------------------------------------------- */
'''

PIPE                                = subprocess.PIPE
STDOUT                              = subprocess.STDOUT

VANILA_LOCAL                        = __localServer__
AWS_GLOBAL                          = __globalServer__

PYTHON_TAG                          = 'https://docs.anaconda.com/anaconda/reference/release-notes/'
LICENCE_TAG                         = 'https://github.com/vtta2008/damgteam/blob/master/LICENCE'
VERSION_TAG                         = 'https://github.com/vtta2008/damgteam/blob/master/bin/docs/rst/version.rst'

# -------------------------------------------------------------------------------------------------------------
''' configs '''
LOCALAPPDATA        = os.getenv('LOCALAPPDATA')

APPDATA_DAMG        = os.path.join(LOCALAPPDATA, __organizationName__).replace('\\', '/')
APPDATA_PLM         = os.path.join(APPDATA_DAMG, __appname__).replace('\\', '/')
CFG_DIR             = os.path.join(APPDATA_PLM, '.configs').replace('\\', '/')
TMP_DIR             = os.path.join(APPDATA_PLM, '.tmp').replace('\\', '/')
CACHE_DIR           = os.path.join(APPDATA_PLM, '.cache').replace('\\', '/')
PREF_DIR            = os.path.join(APPDATA_PLM, 'preferences').replace('\\', '/')

SETTING_DIR         = CFG_DIR
LOG_DIR             = CFG_DIR
TASK_DIR            = os.path.join(CFG_DIR, 'task').replace('\\', '/')
TEAM_DIR            = os.path.join(CFG_DIR, 'team').replace('\\', '/')
PRJ_DIR             = os.path.join(CFG_DIR, 'project').replace('\\', '/')
ORG_DIR             = os.path.join(CFG_DIR, 'organisation').replace('\\', '/')
USER_LOCAL_DATA     = os.path.join(CFG_DIR, 'userLocal').replace('\\', '/')

DB_DIR              = APPDATA_PLM

# -------------------------------------------------------------------------------------------------------------
''' docs '''

DOCS_DIR            = os.path.join(ROOT_APP, 'docs').replace('\\', '/')
TEMPLATE_DIR        = os.path.join(DOCS_DIR, 'template').replace('\\', '/')
TEMPLATE_LICENSE    = os.path.join(TEMPLATE_DIR, 'LICENSE').replace('\\', '/')

# -------------------------------------------------------------------------------------------------------------
''' integrations '''

INTERGRATIONS_DIR   = os.path.join(ROOT_APP, 'intergrations').replace('\\', '/')

# -------------------------------------------------------------------------------------------------------------
''' common '''

COMMONS_DIR         = os.path.join(ROOT, 'commons').replace('\\', '/')
CORE_DIR            = os.path.join(COMMONS_DIR, 'Core').replace('\\', '/')
DAMG_DIR            = os.path.join(COMMONS_DIR, 'damg').replace('\\', '/')
GUI_DIR             = os.path.join(COMMONS_DIR, 'Gui').replace('\\', '/')
WIDGET_DIR          = os.path.join(COMMONS_DIR, 'Widgets').replace('\\', '/')

# -------------------------------------------------------------------------------------------------------------
''' cores '''

CORES_DIR           = os.path.join(ROOT, 'cores').replace('\\', '/')
BASE_DIR            = os.path.join(CORES_DIR, 'base').replace('\\', '/')
LOGGER_DIR          = os.path.join(CORES_DIR, 'Loggers').replace('\\', '/')
MODELS_DIR          = os.path.join(CORES_DIR, 'models').replace('\\', '/')

# -------------------------------------------------------------------------------------------------------------
''' resources '''

RESOURCES_DIR       = os.path.join(ROOT, 'resources').replace('\\', '/')
AVATAR_DIR          = os.path.join(RESOURCES_DIR, 'avatar').replace('\\', '/')
DESIGN_DIR          = os.path.join(RESOURCES_DIR, 'design').replace('\\', '/')
FONT_DIR            = os.path.join(RESOURCES_DIR, 'fonts').replace('\\', '/')

ICON_DIR            = os.path.join(RESOURCES_DIR, 'icons').replace('\\', '/')
TAG_ICON_DIR        = os.path.join(ICON_DIR, 'tags').replace('\\', '/')

NODE_ICON_DIR       = os.path.join(ICON_DIR, 'nodes').replace('\\', '/')

WEB_ICON_DIR        = os.path.join(ICON_DIR, 'web').replace('\\', '/')
WEB_ICON_16         = os.path.join(WEB_ICON_DIR, 'x16').replace('\\', '/')
WEB_ICON_24         = os.path.join(WEB_ICON_DIR, 'x24').replace('\\', '/')
WEB_ICON_32         = os.path.join(WEB_ICON_DIR, 'x32').replace('\\', '/')
WEB_ICON_48         = os.path.join(WEB_ICON_DIR, 'x48').replace('\\', '/')
WEB_ICON_64         = os.path.join(WEB_ICON_DIR, 'x64').replace('\\', '/')
WEB_ICON_128        = os.path.join(WEB_ICON_DIR, 'x128').replace('\\', '/')

ICON_DIR_12         = os.path.join(ICON_DIR, 'x12').replace('\\', '/')
ICON_DIR_16         = os.path.join(ICON_DIR, 'x16').replace('\\', '/')
ICON_DIR_24         = os.path.join(ICON_DIR, 'x24').replace('\\', '/')
ICON_DIR_32         = os.path.join(ICON_DIR, 'x32').replace('\\', '/')
ICON_DIR_48         = os.path.join(ICON_DIR, 'x48').replace('\\', '/')
ICON_DIR_64         = os.path.join(ICON_DIR, 'x64').replace('\\', '/')

IMAGE_DIR           = os.path.join(RESOURCES_DIR, 'images').replace('\\', '/')

JSON_DIR            = os.path.join(RESOURCES_DIR, 'json').replace('\\', '/')

LOGO_DIR            = os.path.join(RESOURCES_DIR, 'logo').replace('\\', '/')
DAMG_LOGO_DIR       = os.path.join(LOGO_DIR, 'DAMGTEAM').replace('\\', '/')
PLM_LOGO_DIR        = os.path.join(LOGO_DIR, 'PLM').replace('\\', '/')

SOUND_DIR           = os.path.join(RESOURCES_DIR, 'sound').replace('\\', '/')

# -------------------------------------------------------------------------------------------------------------
''' ui '''

UI_DIR              = os.path.join(ROOT, 'ui').replace('\\', '/')
UI_BASE_DIR         = os.path.join(UI_DIR, 'base').replace('\\', '/')
UI_COMPONENTS_DIR   = os.path.join(UI_DIR, 'components').replace('\\', '/')
UI_LAYOUTS_DIR      = os.path.join(UI_DIR, 'layouts').replace('\\', '/')
UI_MODELS_DIR       = os.path.join(UI_DIR, 'models').replace('\\', '/')
UI_RCS_DIR          = os.path.join(UI_DIR, 'rcs').replace('\\', '/')
UI_TOOLS_DIR        = os.path.join(UI_DIR, 'tools').replace('\\', '/')

# -------------------------------------------------------------------------------------------------------------
''' utils '''

UTILS_DIR           = os.path.join(ROOT, 'utils').replace('\\', '/')

# -------------------------------------------------------------------------------------------------------------
''' scripts '''

REQUIREMENTS_DIR    = os.path.join(ROOT_APP, 'requirements').replace('\\', '/')

# -------------------------------------------------------------------------------------------------------------
''' scripts '''

SCRIPTS_DIR         = os.path.join(ROOT, 'scripts').replace('\\', '/')
CSS_DIR             = os.path.join(SCRIPTS_DIR, 'css').replace('\\', '/')
HTML_DIR            = os.path.join(SCRIPTS_DIR, 'html').replace('\\', '/')
JS_DIR              = os.path.join(SCRIPTS_DIR, 'js').replace('\\', '/')
QSS_DIR             = os.path.join(SCRIPTS_DIR, 'qss').replace('\\', '/')

# -------------------------------------------------------------------------------------------------------------
''' plugins '''

PLUGIN_DIR          = os.path.join(ROOT, 'plugins').replace('\\', '/')

# -------------------------------------------------------------------------------------------------------------
''' test '''

TEST_DIR            = os.path.join(ROOT_APP, 'tests').replace('\\', '/')

# -------------------------------------------------------------------------------------------------------------
""" config file """

evnInfoCfg                          = os.path.join(CFG_DIR, 'envs.cfg')
iconCfg                             = os.path.join(CFG_DIR, 'icons.cfg')
avatarCfg                           = os.path.join(CFG_DIR, 'avatars.cfg')
logoCfg                             = os.path.join(CFG_DIR, 'logo.cfg')
webIconCfg                          = os.path.join(CFG_DIR, 'webIcon.cfg')
nodeIconCfg                         = os.path.join(CFG_DIR, 'nodeIcons.cfg')
imageConfig                         = os.path.join(CFG_DIR, 'images.cfg')
tagCfg                              = os.path.join(CFG_DIR, 'tags.cfg')
pythonCfg                           = os.path.join(CFG_DIR, 'python.cfg')
plmCfg                              = os.path.join(CFG_DIR, 'pipeline.cfg')
appsCfg                             = os.path.join(CFG_DIR, 'installed.cfg')
envVarCfg                           = os.path.join(CFG_DIR, 'envVar.cfg')
dirCfg                              = os.path.join(CFG_DIR, 'dirs.cfg')
pthCfg                              = os.path.join(CFG_DIR, 'paths.cfg')
pcCfg                               = os.path.join(CFG_DIR, 'pc.cfg')
urlCfg                              = os.path.join(CFG_DIR, 'url.cfg')
typeCfg                             = os.path.join(CFG_DIR, 'types.cfg')
userCfg                             = os.path.join(CFG_DIR, 'user.cfg')
serverCfg                           = os.path.join(CFG_DIR, 'server.cfg')
fmtCfg                              = os.path.join(CFG_DIR, 'formats.cfg')
PLMconfig                           = os.path.join(CFG_DIR, 'PLM.cfg')
sceneGraphCfg                       = os.path.join(CFG_DIR, 'sceneGraph.cfg')

splashImagePth                      = os.path.join(IMAGE_DIR, 'splash.png')

# -------------------------------------------------------------------------------------------------------------
""" setting file """

APP_SETTING                         = os.path.join(SETTING_DIR, 'PLM.ini')
USER_SETTING                        = os.path.join(SETTING_DIR, 'user.ini')
FORMAT_SETTING                      = os.path.join(SETTING_DIR, 'format.ini')
UNIX_SETTING                        = os.path.join(SETTING_DIR, 'unix.ini')

LOCAL_DB                            = os.path.join(DB_DIR, 'local.db')
LOCAL_LOG                           = os.path.join(LOG_DIR, 'PLM.logs')

QSS_PATH                            = os.path.join(QSS_DIR, 'dark.qss')
MAIN_SCSS_PTH                       = os.path.join(QSS_DIR, 'main.scss')
STYLE_SCSS_PTH                      = os.path.join(QSS_DIR, '_styles.scss')
VAR_SCSS_PTH                        = os.path.join(QSS_DIR, '_variables.scss')

SETTING_FILEPTH = dict(app          = APP_SETTING,
                       user         = USER_SETTING,
                       unix         = UNIX_SETTING,
                       format       = FORMAT_SETTING)

actionTypes = ['DAMGACTION', 'DAMGShowLayoutAction', 'DAMGStartFileAction', 'DAMGExecutingAction', 'DAMGOpenBrowserAction', ]

layoutTypes = ['DAMGUI', 'DAMGWIDGET', ] + actionTypes

DB_ATTRIBUTE_TYPE = {

    'int_auto_increment'    : 'INTERGER PRIMARY KEY AUTOINCREMENT, ',
    'int_primary_key'       : 'INT PRIMARY KEY, ',
    'text_not_null'         : 'TEXT NOT NULL, ',
    'text'                  : 'TEXT, ',
    'bool'                  : 'BOOL, ',
    'varchar'               : 'VARCHAR, ',
    'varchar_20'            : 'VACHAR(20,)  ',

}


CMD_VALUE_TYPE = {

    'dir'                   : 'directory',
    'pth'                   : 'path',
    'url'                   : 'link',
    'func'                  : 'function',
    'cmd'                   : 'commandPrompt',
    'event'                 : 'PLM Event',
    'stylesheet'            : 'PLMstylesheet',
    'shortcut'              : 'shortcut',
    'uiKey'                 : 'PLM Layout Key',
}


RAMTYPE = {
    0: 'Unknown',
    1: 'Other',
    2: 'DRAM',
    3: 'Synchronous DRAM',
    4: 'Cache DRAM',
    5: 'EDO',
    6: 'EDRAM',
    7: 'VRAM',
    8: 'SRAM',
    9: 'RAM',
    10: 'ROM',
    11: 'Flash',
    12: 'EEPROM',
    13: 'FEPROM',
    14: 'EPROM',
    15: 'CDRAM',
    16: '3DRAM',
    17: 'SDRAM',
    18: 'SGRAM',
    19: 'RDRAM',
    20: 'DDR',
    21: 'DDR2',
    22: 'DDR2 FB-DIMM',
    24: 'DDR3',
    25: 'FBD2',
}

FORMFACTOR = {
    0: 'Unknown',
    1: 'Other',
    2: 'SIP',
    3: 'DIP',
    4: 'ZIP',
    5: 'SOJ',
    6: 'Proprietary',
    7: 'SIMM',
    8: 'DIMM',
    9: 'TSOP',
    10: 'PGA',
    11: 'RIMM',
    12: 'SODIMM',
    13: 'SRIMM',
    14: 'SMD',
    15: 'SSMP',
    16: 'QFP',
    17: 'TQFP',
    18: 'SOIC',
    19: 'LCC',
    20: 'PLCC',
    21: 'BGA',
    22: 'FPBGA',
    23: 'LGA',
    24: 'FB-DIMM',
}

CPUTYPE = {

    1: 'Other',
    2: 'Unknown',
    3: 'Central Processor',
    4: 'Math Processor',
    5: 'DSP Processor',
    6: 'Video Processor',
}

DRIVETYPE = {
  0 : "Unknown",
  1 : "No Root Directory",
  2 : "Removable Disk",
  3 : "Local Disk",
  4 : "Network Drive",
  5 : "Compact Disc",
  6 : "RAM Disk"
}

# --------------------------------------------------------------------------------------------------------------
""" Autodesk _data """

autodeskVer         = ["2017", "2018", "2019", "2020", "2021"]
autodeskApp         = ["Autodesk Maya", "Autodesk Mudbox", "Maya", "Mudbox", "3ds Max", "AutoCAD"]

# --------------------------------------------------------------------------------------------------------------
""" Adobe _data """

adobeVer            = ["CC 2017", "CC 2018", "CC 2019", "CC 2020", "CC 2021"]
adobeApp            = ["Adobe Photoshop", "Adobe Illustrator", "Adobe Audition", "Adobe After Effects",
                       "Adobe Premiere Pro", "Adobe Media Encoder", ]

# --------------------------------------------------------------------------------------------------------------
""" Foundry _data """

foundryVer          = ["11.1v1", "11.2v1", "4.0v1", "4.1v1", "2.6v3", "4.6v1", "12.0v1", '3.5v2', '3.2v4', '2.6v3']
foundryApp          = ['Hiero', 'Mari', 'NukeStudio', 'NukeX', 'Katana',]

# --------------------------------------------------------------------------------------------------------------
""" Pixologic _data """

pixologiVer         = ["4R6", "4R7", "4R8", '2018', '2019', '2020', '2021']
pixologiApp         = ['ZBrush' ]

# --------------------------------------------------------------------------------------------------------------
""" Allegorithmic _data """

allegorithmicVer    = [ ]
allegorithmicApp    = ['Substance Painter', 'Substance Designer']

# --------------------------------------------------------------------------------------------------------------
""" SideFX _data """

sizefxVer           = ['16.5.439', '16.5.496', '17.5.425', '18.0.327']
sizefxApp           = ['Houdini FX', ]

# --------------------------------------------------------------------------------------------------------------
""" Microsoft Office _data """

officeVer           = ['2017', "2018", "2019", "2020"]
officeApp           = ['Word', 'Excel', 'PowerPoint', 'Wordpad']

# --------------------------------------------------------------------------------------------------------------
""" JetBrains _data """

jetbrainsVer        = ['2017.3.3', '2018.1', ]
jetbrainsApp        = ['JetBrains PyCharm', ]

# --------------------------------------------------------------------------------------------------------------
""" Wonder Unit """

wonderUnitVer       = [ ]
wonderUniApp        = ['Storyboarder', 'Krita (x64)', 'Krita (x32)' ]

# --------------------------------------------------------------------------------------------------------------
""" another app _data """

anacondaApps        = ['Spyder', 'QtDesigner', 'Git Bash']
mcOfficeApps        = ['Word', 'Excel', 'PowerPoint']
windowApps          = ['Sublime Text 2', 'Sublime Text 3', 'Wordpad', 'Headus UVLayout', 'Snipping Tool', ] + anacondaApps + mcOfficeApps

# --------------------------------------------------------------------------------------------------------------
""" Combine data package """

pVERSION = dict(adobe=adobeVer, autodesk=autodeskVer, allegorithmic = allegorithmicVer, foundry=foundryVer,
                pixologic=pixologiVer, sizefx=sizefxVer, office=officeVer, jetbrains=jetbrainsVer, wonderUnit=wonderUnitVer, )

pPACKAGE = dict(adobe=adobeApp, autodesk=autodeskApp, allegorithmic = allegorithmicApp, foundry=foundryApp,
                pixologic=pixologiApp, sizefx=sizefxApp, office=officeApp, jetbrains=jetbrainsApp, wonderUnit=wonderUniApp,)

# --------------------------------------------------------------------------------------------------------------
""" Tracking configKey """

TRACK_TDS           = ['Maya', 'ZBrush', 'Houdini', '3Ds Max', 'Mudbox', 'BLender']

TRACK_VFX           = ['NukeX', 'After Effects', 'Katana']

TRACK_ART           = ['Photoshop', 'Illustrator', 'Krita (x64)', 'Krita (x32)']

TRACK_PRE           = ['Storyboarder', 'Illustrator']

TRACK_TEX           = ['Mari', 'Substance Painter'] + TRACK_ART

TRACK_POST          = ['Davinci Resolve', 'Hiero', 'HieroPlayer', 'Premiere Pro', 'NukeStudio']

TRACK_OFFICE        = ['Word', 'Excel', 'PowerPoint', 'Wordpad']

TRACK_DEV           = ['Sublime Text', 'QtDesigner', 'Git Bash', 'Command Prompt']

TRACK_TOOLS         = ['Calculator', 'Calendar', 'ContactUs', 'EnglishDictionary', 'FeedBack', 'ReportBug', 'FindFiles',
                       'ImageViewer', 'InviteFriend', 'Messenger', 'NoteReminder', 'ScreenShot', 'TextEditor',
                       'PluginManager', 'NodeGraph', 'Browser', ]

TRACK_EXTRA         = ['ReConfig', 'CleanPyc', 'Debug', 'Snipping Tool']

TRACK_SYSTRAY       = ['Snipping Tool', 'ScreenShot', 'Maximize', 'Minimize', 'Restore', 'Exit', ]

KEYDETECT           = ["Non-commercial", "Uninstall", "Verbose", "License", "Skype", ".url", "Changelog", "Settings"]

# --------------------------------------------------------------------------------------------------------------
""" Combine Tracking configKey """

pTRACK = dict(TDS=TRACK_TDS, VFX=TRACK_VFX, ART=TRACK_ART, PRE = TRACK_PRE, TEXTURE = TRACK_TEX, POST = TRACK_POST,
              Office=TRACK_OFFICE, Dev=TRACK_DEV, Tools=TRACK_TOOLS, Extra=TRACK_EXTRA, sysTray=TRACK_SYSTRAY, )

# --------------------------------------------------------------------------------------------------------------
""" PLM Layout Key """

UI_ELEMENT_KEYS     = ['BotTab', 'ConnectStatus', 'GridLayout', 'MainMenuSection', 'MainToolBar', 'MainToolBarSection',
                       'Notification','StatusBar', 'TopTab', 'TopTab1', 'TopTab2', 'TopTab3', 'UserSetting', ]

MAIN_UI_KEYS        = ['SysTray', 'PipelineManager', 'ForgotPassword', 'SignIn', 'SignUp', 'SignOut', 'CommandUI', ]

INFO_UI_KEYS        = ['About', 'CodeOfConduct', 'Contributing', 'Credit', 'Version', 'AppLicence', 'PythonLicence',
                       'OrgInfo', 'References', ]

PROJ_UI_KEYS        = ['ProjectManager', 'PreProductionProj', 'ProductionProj', 'PostProductionPrj', 'VFXProj',
                       'ResearchProject', ]

ORG_UI_KEYS         = ['OrganisationManager', ]

TASK_UI_KEYS        = ['TaskManager', ]

TEAM_UI_KEYS        = ['TeamManager', ]

DEPA_UI_KEYS        = ['DepartmentManager']

SETTING_UI_KEYS     = ['Configurations', 'Preferences', 'AppSetting', 'GlobalSetting', 'UserSetting', 'BrowserSetting',
                       'ProjSetting', 'OrgSetting', 'TaskSetting', 'TeamSetting']

LIBRARY_UI_KEYS     = ['UserLibrary', 'HDRILibrary', 'TextureLibrary', 'AlphaLibrary', ]

TOOL_UI_KEYS        = ['Calculator', 'Calendar', 'EnglishDictionary', 'FindFiles', 'ImageViewer', 'NoteReminder',
                       'ScreenShot', 'TextEditor', ]

PLUGIN_UI_KEY       = ['PluginManager', 'NodeGraph', 'Browser', 'Messenger', 'QtDesigner']

FORM_KEY            = ['ContactUs', 'InviteFriend', 'ReportBug', ]

APP_UI_KEYS         = MAIN_UI_KEYS + INFO_UI_KEYS + PROJ_UI_KEYS + ORG_UI_KEYS + TASK_UI_KEYS + TEAM_UI_KEYS + \
                      SETTING_UI_KEYS + LIBRARY_UI_KEYS + TOOL_UI_KEYS + PLUGIN_UI_KEY + FORM_KEY

# --------------------------------------------------------------------------------------------------------------
""" PLM Function key """

factors             = ['Organisation', 'Project', 'Department', 'Team', 'Task', ]
factorActs          = ['New', 'Config', 'Edit', 'Remove']

FACTOR_KEYS         = []
for f in factors:
    FACTOR_KEYS.append(f)
    for act in factorActs:
        FACTOR_KEYS.append('{0} {1}'.format(act, f))

APP_EVENT_KEYS      = ['ShowAll', 'HideAll', 'CloseAll', 'SwitchAccount', 'LogIn', 'LogOut', 'Quit', 'Exit',
                       'ChangePassword', 'UpdateAvatar',]

STYLESHEET_KEYS     = ['bright', 'dark', 'charcoal', 'nuker', ]

STYLE_KEYS          = []

OPEN_DIR_KEYS       = ['ConfigFolder', 'IconFolder', 'SettingFolder', 'AppDataFolder', 'PreferenceFolder', ]

OPEN_URL_KEYS       = ['pythonTag', 'licenceTag', 'versionTag', 'PLM wiki']

SYS_CMD_KEYS        = ['Command Prompt', 'cmd', ]

SHORTCUT_KEYS       = ['Copy', 'Cut', 'Paste', 'Delete', 'Find', 'Rename']

APP_FUNCS_KEYS      = ['ReConfig', 'CleanPyc', 'Debug', 'Maximize', 'Minimize', 'Restore', ] + FACTOR_KEYS + \
                      APP_EVENT_KEYS + STYLESHEET_KEYS + STYLE_KEYS + OPEN_DIR_KEYS + OPEN_URL_KEYS + SYS_CMD_KEYS + \
                      SHORTCUT_KEYS

# --------------------------------------------------------------------------------------------------------------
""" Store key data """

def generate_key_packages(*args):
    keyPackage = []
    for k in pPACKAGE:
        for name in pPACKAGE[k]:
            if len(pVERSION[k]) == 0:
                key = name
                keyPackage.append(key)
            else:
                for ver in pVERSION[k]:
                    if name == 'Hiero' or name == 'HieroPlayer' or name == 'NukeX':
                        key = name + " " + ver
                    else:
                        if not ver or ver == []:
                            key = name
                        else:
                            key = name + " " + ver
                    keyPackage.append(key)

    args = keyPackage + windowApps
    return args

KEYPACKAGE      = generate_key_packages()

def generate_config(key, *args):
    keys = []
    for k in KEYPACKAGE:
        for t in pTRACK[key]:
            if t in k:
                keys.append(k)
    return list(sorted(set(keys)))

# Toolbar _data
CONFIG_TDS      = generate_config('TDS')                            # TD artist
CONFIG_VFX      = generate_config('VFX')                            # VFX artist
CONFIG_ART      = generate_config('ART')                            # 2D artist
CONFIG_PRE      = generate_config('PRE')                            # Preproduction
CONFIG_TEX      = generate_config('TEXTURE')                        # ShadingTD artist
CONFIG_POST     = generate_config('POST')                           # Post production

# Tab 1 sections _data
CONFIG_OFFICE   = generate_config('Office')                         # Paper work department
CONFIG_DEV      = generate_config('Dev') + ['Command Prompt']       # Rnd - Research and development
CONFIG_TOOLS    = generate_config('Tools') + TOOL_UI_KEYS           # useful/custom tool supporting for the whole pipeline
CONFIG_EXTRA    = generate_config('Extra')                          # Extra tool may be considering to use
CONFIG_SYSTRAY  = generate_config('sysTray') + ['Exit', 'SignIn']

ACTIONS_DATA = dict(TD                  = CONFIG_TDS,
                    VFX                 = CONFIG_VFX,
                    ART                 = CONFIG_ART,
                    PRE                 = CONFIG_PRE,
                    TEXTURE             = CONFIG_TEX,
                    POST                = CONFIG_POST,
                    OFFICE              = CONFIG_OFFICE,
                    DEV                 = CONFIG_DEV,
                    TOOLS               = CONFIG_TOOLS,
                    EXTRA               = CONFIG_EXTRA,
                    SYSTRAY             = CONFIG_SYSTRAY, )

# Binding config
QT_BINDINGS             = ['PyQt5', 'PySide2', 'pyqt']
QT_ABSTRACTIONS         = ['qtpy', 'pyqtgraph', 'Qt']
QT5_IMPORT_API          = ['QtCore', 'QtGui', 'QtWidgets', 'QtWebEngineWidgets', 'QtWebKitWidgets']
QT_API_VALUES           = ['pyqt', 'pyqt5', 'pyside2']
QT_LIB_VALUES           = ['PyQt', 'PyQt5', 'PySide2']
QT_BINDING              = 'Not set or nonexistent'
QT_ABSTRACTION          = 'Not set or nonexistent'
IMAGE_BLACKLIST         = ['base_palette']

PY2 = sys.version[0] == '2'

SYS_OPTS = ["Host Name", "OS Name", "OS Version", "Product ID", "System Manufacturer", "System Model",
            "System type", "BIOS Version", "Domain", "Windows Directory", "Total Physical Memory",
            "Available Physical Memory", "Logon Server"]

notKeys = ['__name__', '__doc__', '__package__', '__loader__', '__spec__', '__file__', '__cached__',
           '__builtins__', 'os', '__envKey__', 'cfgdir', 'CFG_DIR', 'SETTING_DIR', 'DB_DIR', 'LOG_DIR',
           'QSS_DIR', 'RCS_DIR', 'SCSS_DIR', '__appname__', 'subprocess', 'unicode_literals', 'absolute_import',
           '__organization__']

IGNORE_ICONS = ['Widget', 'bright', 'dark', 'charcoal', 'nuker', 'TopTab1', 'TopTab2', 'Organisation', 'Project',
                'Team', 'Task', 'ShowAll','ItemWidget', 'BaseManager', 'SettingInput', 'QueryPage', 'SysTray', 'Footer',
                'BotTab1', 'BotTab2', 'Cmd', 'User', 'Tracking']

INI                         = QSettings.IniFormat
NATIVE                      = QSettings.NativeFormat
INVALID                     = QSettings.InvalidFormat

# -------------------------------------------------------------------------------------------------------------
""" Format """

LOG_FORMAT = dict(

    fullOpt                 = "%(levelname)s: %(asctime)s %(name)s, line %(lineno)s: %(message)s",
    rlm                     = "(relativeCreated:d) (levelname): (message)",
    tlm1                    = "{asctime:[{lvelname}: :{message}",
    tnlm1                   = "%(asctime)s  %(name)-22s  %(levelname)-8s %(message)s",
    tlm2                    = '%(asctime)s|%(levelname)s|%(message)s|',
    tnlm2                   = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
)

DT_FORMAT = dict(

    dmyhms                  = "%d/%m/%Y %H:%M:%S",
    mdhm                    = "'%m-%d %H:%M'",
    fullOpt                 = '(%d/%m/%Y %H:%M:%S)',
)

ST_FORMAT = dict(

    ini                     = INI,
    native                  = NATIVE,
    invalid                 = INVALID,
)

datetTimeStamp = QDateTime.currentDateTime().toString("hh:mm - dd MMMM yy")             # datestamp


IMGEXT = "All Files (*);;Img Files (*.jpg);;Img Files (*.png)"


# -------------------------------------------------------------------------------------------------------------
""" Font """

BOLD                        = QFont.Bold
NORMAL                      = QFont.Normal

# -------------------------------------------------------------------------------------------------------------
""" Event """

NO_WRAP                     = QPlainTextEdit.NoWrap
NO_FRAME                    = QPlainTextEdit.NoFrame
ELIDE_RIGHT                 = Qt.ElideRight
KEY_PRESS                   = QEvent.KeyPress
KEY_RELEASE                 = QEvent.KeyRelease

# -------------------------------------------------------------------------------------------------------------
""" Window state """

StateNormal                 = Qt.WindowNoState
StateMax                    = Qt.WindowMaximized
StateMin                    = Qt.WindowMinimized
State_Selected              = QStyle.State_Selected

# -------------------------------------------------------------------------------------------------------------
""" Nodegraph setting variables """

ASPEC_RATIO                 = Qt.KeepAspectRatio
SMOOTH_TRANS                = Qt.SmoothTransformation
SCROLLBAROFF                = Qt.ScrollBarAlwaysOff                                     # Scrollbar
SCROLLBARON                 = Qt.ScrollBarAlwaysOn
SCROLLBARNEED               = Qt.ScrollBarAsNeeded

WORD_WRAP                   = Qt.TextWordWrap
INTERSECT_ITEM_SHAPE        = Qt.IntersectsItemShape
CONTAIN_ITEM_SHAPE          = Qt.ContainsItemShape
MATCH_EXACTLY               = Qt.MatchExactly
DRAG_ONLY                   = QAbstractItemView.DragOnly

# -------------------------------------------------------------------------------------------------------------
""" UI flags """

ITEMENABLE                  = Qt.ItemIsEnabled
ITEMMOVEABLE                = QGraphicsItem.ItemIsMovable
ITEMSENDGEOCHANGE           = QGraphicsItem.ItemSendsGeometryChanges
ITEMSCALECHANGE             = QGraphicsItem.ItemScaleChange
ITEMPOSCHANGE               = QGraphicsItem.ItemPositionChange
DEVICECACHE                 = QGraphicsItem.DeviceCoordinateCache
SELECTABLE                  = QGraphicsItem.ItemIsSelectable
MOVEABLE                    = QGraphicsItem.ItemIsMovable
FOCUSABLE                   = QGraphicsItem.ItemIsFocusable
PANEL                       = QGraphicsItem.ItemIsPanel

NOINDEX                     = QGraphicsScene.NoIndex                                    # Scene

RUBBER_DRAG                 = QGraphicsView.RubberBandDrag                              # Viewer
RUBBER_REC                  = QRubberBand.Rectangle
POS_CHANGE                  = QGraphicsItem.ItemPositionChange

NODRAG                      = QGraphicsView.NoDrag
NOFRAME                     = QGraphicsView.NoFrame
ANCHOR_NO                   = QGraphicsView.NoAnchor

ANCHOR_UNDERMICE            = QGraphicsView.AnchorUnderMouse
ANCHOR_CENTER               = QGraphicsView.AnchorViewCenter

CACHE_BG                    = QGraphicsView.CacheBackground

UPDATE_VIEWRECT             = QGraphicsView.BoundingRectViewportUpdate
UPDATE_FULLVIEW             = QGraphicsView.FullViewportUpdate
UPDATE_SMARTVIEW            = QGraphicsView.SmartViewportUpdate
UPDATE_BOUNDINGVIEW         = QGraphicsView.BoundingRectViewportUpdate
UPDATE_MINIMALVIEW          = QGraphicsView.MinimalViewportUpdate

STAY_ON_TOP                 = Qt.WindowStaysOnTopHint
STRONG_FOCUS                = Qt.StrongFocus
FRAMELESS                   = Qt.FramelessWindowHint
CUSTOMIZE                   = Qt.CustomizeWindowHint
CLOSEBTN                    = Qt.WindowCloseButtonHint
MINIMIZEBTN                 = Qt.WindowMinimizeButtonHint
AUTO_COLOR                  = Qt.AutoColor

# -------------------------------------------------------------------------------------------------------------
""" Drawing """

ANTIALIAS                   = QPainter.Antialiasing                                     # Painter
ANTIALIAS_TEXT              = QPainter.TextAntialiasing
ANTIALIAS_HIGH_QUALITY      = QPainter.HighQualityAntialiasing
SMOOTH_PIXMAP_TRANSFORM     = QPainter.SmoothPixmapTransform
NON_COSMETIC_PEN            = QPainter.NonCosmeticDefaultPen

BRUSH_NONE                  = Qt.NoBrush                                                # Brush

PEN_NONE                    = Qt.NoPen                                                  # Pen
ROUND_CAP                   = Qt.RoundCap
ROUND_JOIN                  = Qt.RoundJoin

PATTERN_SOLID               = Qt.SolidPattern                                           # Pattern

LINE_SOLID                  = Qt.SolidLine                                              # Line
LINE_DASH                   = Qt.DashLine
LINE_DOT                    = Qt.DotLine
LINE_DASH_DOT               = Qt.DashDotDotLine

# -------------------------------------------------------------------------------------------------------------
""" Week Day  """

sunday                      = Qt.Sunday
monday                      = Qt.Monday
tuesady                     = Qt.Tuesday
wednesday                   = Qt.Wednesday
thursday                    = Qt.Thursday
friday                      = Qt.Friday
saturday                    = Qt.Saturday

# -------------------------------------------------------------------------------------------------------------
""" Keyboard and cursor """

KEY_ALT                     = Qt.Key_Alt
KEY_DEL                     = Qt.Key_Delete
KEY_TAB                     = Qt.Key_Tab
KEY_SHIFT                   = Qt.Key_Shift
KEY_CTRL                    = Qt.Key_Control
KEY_BACKSPACE               = Qt.Key_Backspace
KEY_ENTER                   = Qt.Key_Enter
KEY_RETURN                  = Qt.Key_Return
KEY_F                       = Qt.Key_F
KEY_S                       = Qt.Key_S
ALT_MODIFIER                = Qt.AltModifier
CTRL_MODIFIER               = Qt.ControlModifier
SHIFT_MODIFIER              = Qt.ShiftModifier
NO_MODIFIER                 = Qt.NoModifier
CLOSE_HAND_CUSOR            = Qt.ClosedHandCursor
SIZEF_CURSOR                = Qt.SizeFDiagCursor

windows                     = os.name = 'nt'
DMK                         = Qt.AltModifier if windows else CTRL_MODIFIER

MOUSE_LEFT                  = Qt.LeftButton
MOUSE_RIGHT                 = Qt.RightButton
MOUSE_MIDDLE                = Qt.MiddleButton
NO_BUTTON                   = Qt.NoButton

ARROW_NONE                  = Qt.NoArrow                                                # Cursor
CURSOR_ARROW                = Qt.ArrowCursor
CURSOR_SIZEALL              = Qt.SizeAllCursor

ACTION_MOVE                 = Qt.MoveAction                                             # Action

# -------------------------------------------------------------------------------------------------------------
""" Set number """

RELATIVE_SIZE               = Qt.RelativeSize                                           # Size

POSX                        = 0
POSY                        = 0


NODE_ROUND                  = 10
NODE_BORDER                 = 2
NODE_REC                    = 30
NODE_STAMP                  = 25

NODE_HEADER_HEIGHT          = 25
NODE_FOOTER_HEIGHT          = 25

ATTR_HEIGHT                 = 30
ATTR_ROUND                  = NODE_ROUND/2
ATTR_REC                    = NODE_REC/2

RADIUS                      = 10
COL                         = 10
ROW                         = 10
GRID_SIZE                   = 50

FLTR                        = 'flow_left_to_right'
FRTL                        = 'flow_right_to_left'

MARGIN                      = 20
ROUNDNESS                   = 0
THICKNESS                   = 1
CURRENT_ZOOM                = 1

UNIT                        = 60                                                                # Base Unit
MARG                        = 5                                                                 # Content margin
BUFF                        = 10                                                                # Buffer size
SCAL                        = 1                                                                 # Scale value
STEP                        = 1                                                                 # Step value changing
VAL                         = 1                                                                 # Default value
MIN                         = 0                                                                 # Minimum value
MAX                         = 1000                                                              # Maximum value
WMIN                        = 50                                                                # Minimum width
HMIN                        = 20                                                                # Minimum height
HFIX                        = 80
ICONSIZE                    = 32
ICONBUFFER                  = -1
BTNTAGSIZE                  = QSize(87, 20)
TAGBTNSIZE                  = QSize(87-1, 20-1)
BTNICONSIZE                 = QSize(ICONSIZE, ICONSIZE)
ICONBTNSIZE                 = QSize(ICONSIZE+ICONBUFFER, ICONSIZE+ICONBUFFER)

ignoreARM                   = Qt.IgnoreAspectRatio

scrollAsNeed                = Qt.ScrollBarAsNeeded
scrollOff                   = Qt.ScrollBarAlwaysOff
scrollOn                    = Qt.ScrollBarAlwaysOn

SiPoMin                     = QSizePolicy.Minimum                                               # Size policy
SiPoMax                     = QSizePolicy.Maximum
SiPoExp                     = QSizePolicy.Expanding
SiPoPre                     = QSizePolicy.Preferred
SiPoIgn                     = QSizePolicy.Ignored

frameStyle                  = QFrame.Sunken | QFrame.Panel

center                      = Qt.AlignCenter                                                    # Alignment
right                       = Qt.AlignRight
left                        = Qt.AlignLeft
top                         = Qt.AlignTop
bottom                      = Qt.AlignBottom
hori                        = Qt.Horizontal
vert                        = Qt.Vertical
black                       = Qt.black
blue                        = Qt.blue
darkBlue                    = Qt.darkBlue
cyan                        = Qt.cyan

dockL                       = Qt.LeftDockWidgetArea                                             # Docking area
dockR                       = Qt.RightDockWidgetArea
dockT                       = Qt.TopDockWidgetArea
dockB                       = Qt.BottomDockWidgetArea
dockAll                     = Qt.AllDockWidgetAreas

# === PIPE ===

PIPE_WIDTH = 1.2
PIPE_STYLE_DEFAULT = 'line'
PIPE_STYLE_DASHED = 'dashed'
PIPE_STYLE_DOTTED = 'dotted'
PIPE_DEFAULT_COLOR = (175, 95, 30, 255)
PIPE_DISABLED_COLOR = (190, 20, 20, 255)
PIPE_ACTIVE_COLOR = (70, 255, 220, 255)
PIPE_HIGHLIGHT_COLOR = (232, 184, 13, 255)
PIPE_SLICER_COLOR = (255, 50, 75)
#: Style to draw the connection pipes as straight lines.
PIPE_LAYOUT_STRAIGHT = 0
#: Style to draw the connection pipes as curved lines.
PIPE_LAYOUT_CURVED = 1
#: Style to draw the connection pipes as angled lines.
PIPE_LAYOUT_ANGLE = 2

# === PORT ===

#: Connection type for input ports.
IN_PORT = 'in'
#: Connection type for output ports.
OUT_PORT = 'out'

PORT_DEFAULT_SIZE = 22.0
PORT_DEFAULT_COLOR = (49, 115, 100, 255)
PORT_DEFAULT_BORDER_COLOR = (29, 202, 151, 255)
PORT_ACTIVE_COLOR = (14, 45, 59, 255)
PORT_ACTIVE_BORDER_COLOR = (107, 166, 193, 255)
PORT_HOVER_COLOR = (17, 43, 82, 255)
PORT_HOVER_BORDER_COLOR = (136, 255, 35, 255)
PORT_FALLOFF = 15.0

# === NODE ===

NODE_WIDTH = 170
NODE_HEIGHT = 80
NODE_ICON_SIZE = 24
NODE_SEL_COLOR = (255, 255, 255, 30)
NODE_SEL_BORDER_COLOR = (254, 207, 42, 255)

# === NODE PROPERTY ===

#: Property type will hidden in the properties bin (default).
NODE_PROP = 0
#: Property type represented with a QLabel widget in the properties bin.
NODE_PROP_QLABEL = 2
#: Property type represented with a QLineEdit widget in the properties bin.
NODE_PROP_QLINEEDIT = 3
#: Property type represented with a QTextEdit widget in the properties bin.
NODE_PROP_QTEXTEDIT = 4
#: Property type represented with a QComboBox widget in the properties bin.
NODE_PROP_QCOMBO = 5
#: Property type represented with a QCheckBox widget in the properties bin.
NODE_PROP_QCHECKBOX = 6
#: Property type represented with a QSpinBox widget in the properties bin.
NODE_PROP_QSPINBOX = 7
#: Property type represented with a ColorPicker widget in the properties bin.
NODE_PROP_COLORPICKER = 8
#: Property type represented with a Slider widget in the properties bin.
NODE_PROP_SLIDER = 9

# === NODE VIEWER ===

VIEWER_BG_COLOR = (35, 35, 35)
VIEWER_GRID_COLOR = (45, 45, 45)
VIEWER_GRID_OVERLAY = True
VIEWER_GRID_SIZE = 20

SCENE_AREA = 8000.0

DRAG_DROP_ID = 'n0deGraphQT'

# === PATHS ===

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(BASE_PATH, 'widgets', 'icons')
ICON_DOWN_ARROW = os.path.join(ICON_PATH, 'down_arrow.png')
ICON_NODE_BASE = os.path.join(ICON_PATH, 'node_base.png')

# === DRAW STACK ORDER ===

Z_VAL_PIPE = -1
Z_VAL_NODE = 1
Z_VAL_PORT = 2
Z_VAL_NODE_WIDGET = 3


# -------------------------------------------------------------------------------------------------------------
""" setting """

PRS = dict( password    = QLineEdit.Password,       center = center ,   left  = left   ,    right  = right,
            spmax       = SiPoMax           ,       sppre  = SiPoPre,   spexp = SiPoExp,    spign  = SiPoIgn,
            expanding   = QSizePolicy.Expanding,    spmin  = SiPoMin,)

""" PLM project base """

PRJ_INFO = dict( APPS               = ["maya", "zbrush", "mari", "nuke", "photoshop", "houdini", "after effects"],
                 MASTER             = ["assets", "sequences", "deliverables", "docs", "editorial", "sound", "rcs", "RnD"],
                 TASKS              = ["art", "plt_model", "rigging", "surfacing"],
                 SEQTASKS           = ["anim", "comp", "fx", "layout", "lighting"],
                 ASSETS             = {"heroObj": ["washer", "dryer"], "environment": [], "props": []},
                 STEPS              = ["publish", "review", "work"],
                 MODELING           = ["scenes", "fromZ", "toZ", "objImport", "objExport", "movie"],
                 RIGGING            = ["scenes", "reference"],
                 SURFACING          = ["scenes", "sourceimages", "images", "movie"],
                 LAYOUT             = ["scenes", "sourceimages", "images", "movie", "alembic"],
                 LIGHTING           = ["scenes", "sourceimages", "images", "cache", "reference"],
                 FX                 = ["scenes", "sourceimages", "images", "cache", "reference", "alembic"],
                 ANIM               = ["scenes", "sourceimages", "images", "movie", "alembic"],)

FIX_KEYS = dict( TextEditor         = 'TextEditor', NoteReminder = 'NoteReminder',  Calculator  = 'Calculator',  Calendar  = 'Calendar',
                 EnglishDictionary  = 'EnglishDictionary',    FindFiles    = 'FindFiles',      ImageViewer = 'ImageViewer', NodeGraph = 'NodeGraph',
                 Screenshot         = 'Screenshot', )


class DarkPalette(object):
    """Theme variables."""

    # Color
    COLOR_BACKGROUND_LIGHT = '#505F69'
    COLOR_BACKGROUND_NORMAL = '#32414B'
    COLOR_BACKGROUND_DARK = '#19232D'

    COLOR_FOREGROUND_LIGHT = '#F0F0F0'
    COLOR_FOREGROUND_NORMAL = '#AAAAAA'
    COLOR_FOREGROUND_DARK = '#787878'

    COLOR_SELECTION_LIGHT = '#148CD2'
    COLOR_SELECTION_NORMAL = '#1464A0'
    COLOR_SELECTION_DARK = '#14506E'

    OPACITY_TOOLTIP = 230

    # Size
    SIZE_BORDER_RADIUS = '4px'

    # Borders
    BORDER_LIGHT = '1px solid $COLOR_BACKGROUND_LIGHT'
    BORDER_NORMAL = '1px solid $COLOR_BACKGROUND_NORMAL'
    BORDER_DARK = '1px solid $COLOR_BACKGROUND_DARK'

    BORDER_SELECTION_LIGHT = '1px solid $COLOR_SELECTION_LIGHT'
    BORDER_SELECTION_NORMAL = '1px solid $COLOR_SELECTION_NORMAL'
    BORDER_SELECTION_DARK = '1px solid $COLOR_SELECTION_DARK'

    # Example of additional widget specific variables
    W_STATUS_BAR_BACKGROUND_COLOR = COLOR_SELECTION_DARK

    # Paths
    PATH_RESOURCES = "':/qss_icons'"

    @classmethod
    def to_dict(cls, colors_only=False):
        """Convert variables to dictionary."""
        order = [
            'COLOR_BACKGROUND_LIGHT',
            'COLOR_BACKGROUND_NORMAL',
            'COLOR_BACKGROUND_DARK',
            'COLOR_FOREGROUND_LIGHT',
            'COLOR_FOREGROUND_NORMAL',
            'COLOR_FOREGROUND_DARK',
            'COLOR_SELECTION_LIGHT',
            'COLOR_SELECTION_NORMAL',
            'COLOR_SELECTION_DARK',
            'OPACITY_TOOLTIP',
            'SIZE_BORDER_RADIUS',
            'BORDER_LIGHT',
            'BORDER_NORMAL',
            'BORDER_DARK',
            'BORDER_SELECTION_LIGHT',
            'BORDER_SELECTION_NORMAL',
            'BORDER_SELECTION_DARK',
            'W_STATUS_BAR_BACKGROUND_COLOR',
            'PATH_RESOURCES',
        ]
        dic = OrderedDict()
        for var in order:
            value = getattr(cls, var)

            if colors_only:
                if not var.startswith('COLOR'):
                    value = None

            if value:
                dic[var] = value

        return dic

    @classmethod
    def color_palette(cls):
        """Return the ordered colored palette dictionary."""
        return cls.to_dict(colors_only=True)


iconMissing                         = []
toolTips                            = {}
statusTips                          = {}

# -------------------------------------------------------------------------------------------------------------
""" Config qssPths from text file """

def read_file(fileName):

    filePth = os.path.join(DOCS_DIR, fileName)

    if os.path.exists(filePth):
        with open(filePth) as f:
            data = f.read()
        return data


ABOUT               = read_file('ABOUT')
CODEOFCONDUCT       = read_file('CODEOFCONDUCT')
CONTRIBUTING        = read_file('CONTRIBUTING')
COPYRIGHT           = read_file('COPYRIGHT')
CREDIT              = read_file('CREDIT')
LICENCE             = read_file('LICENSE')
LINKS               = read_file('LINKS')
REFERENCES          = read_file('REFERENCES')
QUESTIONS           = read_file('QUESTION')
VERSION             = read_file('VERSION')


class ConfigPython(dict):

    key                             = 'ConfigPython'

    pkgsRequires = {

        'cx_Freeze'             : ['>=', '6.1'],
        'pytest'                : ['==', '5.3.2'],
        'pytest-cov'            : ['==', '2.8.1'],
        'msgpack'               : ['>=', '0.6.2'],
        'pip'                   : ['>=', '19.3.1'],
        'PyQtWebEngine'         : ['>=', '5.14.0'],
        'PyQt5-sip'             : ['>=', '12.7.0'],
        'winshell'              : ['>=', '0.6.0'],
        'helpdev'               : ['>=', '0.6.10'],
        'deprecate'             : ['>=', '1.0.5'],
        'argparse'              : ['>=', '1.4.0'],
        'green'                 : ['>=', '3.1.0'],
        'GPUtil'                : ['>=', '1.4.0'],
        'playsound'             : ['>=', '1.2.2'],
        'python-resize-image'   : ['>=', '1.1.19'],

    }

    winRequires = {

        'WMI'                   : ['>=', '1.4.9']

    }


    macRequires = {}

    utuRequires = {}

    pyqt5Required = {

        'PyQt5'                 : ['>=', '5.14.1'],
        'PyQtWebEngine'         : ['>=', '5.14.0'],
        'PyQt5-sip'             : ['>=', '12.7.0'],

    }


    pyside2Required = {

        'Pyside2'               : ['>=', '5.14.1'],
        'shiboken2'             : ['>=', '5.14.1'],

    }


    def __init__(self):
        super(ConfigPython, self).__init__()

        self['python']              = platform.python_build()
        self['python version']      = platform.python_version()

        pths                        = [p.replace('\\', '/') for p in os.getenv('PATH').split(';')[0:]]
        sys.path                    = [p.replace('\\', '/') for p in sys.path]

        for p in pths:
            if os.path.exists(p):
                if not p in sys.path:
                    sys.path.insert(-1, p)

        for py in pkg_resources.working_set:
            self[py.project_name]   = py.version

        self.check_package_required(self.pkgsRequires)

        if platform.system() == 'Windows':
            # microsoft windows
            self.check_package_required(self.winRequires)
        elif platform.system() == 'Darwin':
            # mac os
            self.check_package_required(self.macRequires)
        else:
            # untubu
            self.check_package_required(self.utuRequires)

        if globalSetting.printCfgInfo:
            if globalSetting.printPythonInfo:
                pprint.pprint(self)

        if globalSetting.saveCfgInfo:
            if globalSetting.savePythonInfo:
                save_data(pythonCfg, self)

    def check_package_required(self, pkgs):

        for pk, ver in pkgs.items():
            if pk not in self.keys():
                self.install_python_package_required(pk, pkgs)
            else:
                conReq = ver[0]
                verReq = ver[1]
                verCur = self[pk]

                major, minor, micro     = self.get_version_info(verCur)
                v1, v2, v3              = self.get_version_info(verReq)

                if conReq == '==':
                    if v1 != major or v2 != minor or v3 != micro:
                        self.install_python_package_required(pk, pkgs)
                elif conReq == '>=':
                    if not v1 >= major or not v2 >= minor or not v3 >= micro:
                        self.install_python_package_required(pk, pkgs)
                elif conReq == '<=':
                    if not v1 <= major or not v2 <= minor or not v3 <= micro:
                        self.install_python_package_required(pk, pkgs)
                elif conReq == '<':
                    if not v1 < major or not v2 < minor or not v3 < micro:
                        self.install_python_package_required(pk, pkgs)
                elif conReq == '>':
                    if not v1 > major or not v2 > minor or not v3 > micro:
                        self.install_python_package_required(pk, pkgs)

    def install_python_package_required(self, pk, reqs):

        if pk in reqs.keys():
            ver                         = reqs[pk]
            conReq                      = ver[0]
            if conReq == '==' or conReq == '<=':
                subprocess.Popen('python -m pip install {0}={1} --user'.format(pk, ver), shell=True).wait()
            elif conReq == '>=':
                subprocess.Popen('python -m pip install {0} --user --upgrade'.format(pk, ver), shell=True).wait()
            else:
                subprocess.Popen('python -m pip install {0}={1} --user'.format(pk, ver), shell=True).wait()

    def get_version_info(self, ver):

        if len(ver.split('.')) == 1:
            major               = int(ver.split('.')[0])
            minor               = 0
            micro               = 0
        elif len(ver.split('.')) == 2:
            major               = int(ver.split('.')[0])
            minor               = int(ver.split('.')[1])
            micro               = 0
        else:
            major               = int(ver.split('.')[0])
            minor               = int(ver.split('.')[1])
            micro               = int(ver.split('.')[2])

        return major, minor, micro


class ConfigApps(dict):

    key                         = 'ConfigApps'

    def __init__(self):
        super(ConfigApps, self).__init__()

        shortcuts               = {}
        programs                = winshell.programs(common=1)

        for paths, dirs, names in os.walk(programs):
            relpath = paths[len(programs) + 1:]
            shortcuts.setdefault(relpath, []).extend([winshell.shortcut(os.path.join(paths, n)) for n in names])

        for relpath, lnks in sorted(shortcuts.items()):
            for lnk in lnks:
                name, _ = os.path.splitext(os.path.basename(lnk.lnk_filepath))
                self[str(name)] = lnk.path

        if globalSetting.printCfgInfo:
            if globalSetting.printAppInfo:
                pprint.pprint(self)

        if globalSetting.saveCfgInfo:
            if globalSetting.saveAppInfo:
                save_data(appsCfg, self)


class ConfigPath(dict):

    key                             = 'ConfigPath'

    def __init__(self):
        super(ConfigPath, self).__init__()

        self.add('evnInfoCfg'       , evnInfoCfg)
        self.add('iconCfg'          , iconCfg)
        self.add('avatarCfg'        , avatarCfg)
        self.add('logoCfg'          , logoCfg)
        self.add('webIconCfg'       , webIconCfg)
        self.add('nodeIconCfg'      , nodeIconCfg)
        self.add('imageCfg'         , imageConfig)
        self.add('tagCfg'           , tagCfg)
        self.add('pythonCfg'        , pythonCfg)
        self.add('plmCfg'           , plmCfg)
        self.add('appsCfg'          , appsCfg)
        self.add('envVarCfg'        , envVarCfg)
        self.add('dirCfg'           , dirCfg)
        self.add('pthCfg'           , pthCfg)
        self.add('deviceCfg', pcCfg)
        self.add('urlCfg'           , urlCfg)
        self.add('userCfg'          , userCfg)
        self.add('PLMconfig'        , PLMconfig)
        self.add('sceneGraphCfg'    , sceneGraphCfg)
        self.add('splashImagePth'   , splashImagePth)

        self.add('APP_SETTING'      , APP_SETTING)
        self.add('USER_SETTING'     , USER_SETTING)
        self.add('FORMAT_SETTING'   , FORMAT_SETTING)
        self.add('UNIX_SETTING'     , UNIX_SETTING)
        self.add('LOCAL_DB'         , LOCAL_DB)
        self.add('LOCAL_LOG'        , LOCAL_LOG)
        self.add('QSS_PATH'         , QSS_PATH)
        self.add('MAIN_SCSS_PTH'    , MAIN_SCSS_PTH)
        self.add('STYLE_SCSS_PTH'   , STYLE_SCSS_PTH)
        self.add('VAR_SCSS_PTH'     , VAR_SCSS_PTH)
        self.add('SETTING_FILEPTH'  , SETTING_FILEPTH)

        if globalSetting.printCfgInfo:
            if globalSetting.printPthInfo:
                pprint.pprint(self)

        if globalSetting.saveCfgInfo:
            if globalSetting.savePthInfo:
                save_data(pthCfg, self)

    def add(self, key, value):
        self[key]                   = value


class ConfigDirectory(dict):

    key                                 = 'ConfigDirectory'

    def __init__(self):
        super(ConfigDirectory, self).__init__()

        self.add('ROOT', ROOT)
        self.add('ROOT_APP', ROOT_APP)

        self.add('APPDATA_DAMG', APPDATA_DAMG)
        self.add('APPDATA_PLM', APPDATA_PLM)
        self.add('CFG_DIR', CFG_DIR)
        self.add('TMP_DIR', TMP_DIR)
        self.add('CACHE_DIR', CACHE_DIR)
        self.add('PREF_DIR', PREF_DIR)
        self.add('SETTING_DIR', SETTING_DIR)
        self.add('TASK_DIR', TASK_DIR)
        self.add('TEAM_DIR', TEAM_DIR)
        self.add('PRJ_DIR', PRJ_DIR)
        self.add('ORG_DIR', ORG_DIR)
        self.add('USER_LOCAL_DATA', USER_LOCAL_DATA)
        self.add('DB_DIR', DB_DIR)

        self.add('DOCS_DIR', DOCS_DIR)
        self.add('TEMPLATE_DIR', TEMPLATE_DIR)
        self.add('TEMPLATE_LICENSE', TEMPLATE_LICENSE)

        self.add('INTERGRATIONS_DIR', INTERGRATIONS_DIR)

        self.add('COMMONS_DIR', COMMONS_DIR)
        self.add('CORE_DIR', CORE_DIR)
        self.add('DAMG_DIR', DAMG_DIR)
        self.add('GUI_DIR', GUI_DIR)
        self.add('WIDGET_DIR', WIDGET_DIR)

        self.add('CORES_DIR', CORES_DIR)
        self.add('BASE_DIR', BASE_DIR)
        self.add('LOGGER_DIR', LOGGER_DIR)
        self.add('MODELS_DIR', MODELS_DIR)

        self.add('RESOURCES_DIR', RESOURCES_DIR)
        self.add('AVATAR_DIR', AVATAR_DIR)
        self.add('DESIGN_DIR', DESIGN_DIR)
        self.add('FONT_DIR', FONT_DIR)

        self.add('ICON_DIR', ICON_DIR)
        self.add('TAG_ICON_DIR', TAG_ICON_DIR)
        self.add('NODE_ICON_DIR', NODE_ICON_DIR)
        self.add('WEB_ICON_DIR', WEB_ICON_DIR)
        self.add('WEB_ICON_16', WEB_ICON_16)
        self.add('WEB_ICON_24', WEB_ICON_24)
        self.add('WEB_ICON_32', WEB_ICON_32)
        self.add('WEB_ICON_48', WEB_ICON_48)
        self.add('WEB_ICON_64', WEB_ICON_64)
        self.add('WEB_ICON_128', WEB_ICON_128)
        self.add('ICON_DIR_12', ICON_DIR_12)
        self.add('ICON_DIR_16', ICON_DIR_16)
        self.add('ICON_DIR_24', ICON_DIR_24)
        self.add('ICON_DIR_32', ICON_DIR_32)
        self.add('ICON_DIR_48', ICON_DIR_48)
        self.add('ICON_DIR_64', ICON_DIR_64)

        self.add('IMAGE_DIR', IMAGE_DIR)
        self.add('JSON_DIR', JSON_DIR)
        self.add('LOGO_DIR', LOGO_DIR)
        self.add('DAMG_LOGO_DIR', DAMG_LOGO_DIR)
        self.add('PLM_LOGO_DIR', PLM_LOGO_DIR)
        self.add('SOUND_DIR', SOUND_DIR)

        self.add('SCRIPTS_DIR', SCRIPTS_DIR)
        self.add('CSS_DIR', CSS_DIR)
        self.add('HTML_DIR', HTML_DIR)
        self.add('JS_DIR', JS_DIR)
        self.add('QSS_DIR', QSS_DIR)

        self.add('UI_DIR', UI_DIR)
        self.add('UI_BASE_DIR', UI_BASE_DIR)
        self.add('UI_COMPONENTS_DIR', UI_COMPONENTS_DIR)
        self.add('UI_LAYOUTS_DIR', UI_LAYOUTS_DIR)
        self.add('UI_MODELS_DIR', UI_MODELS_DIR)
        self.add('UI_RCS_DIR', UI_RCS_DIR)
        self.add('UI_TOOLS_DIR', UI_TOOLS_DIR)

        self.add('UTILS_DIR', UTILS_DIR)

        self.add('PLUGIN_DIR', PLUGIN_DIR)

        self.add('TEST_DIR', TEST_DIR)

        self.add('ConfigFolder', CFG_DIR)
        self.add('IconFolder', ICON_DIR)
        self.add('SettingFolder', SETTING_DIR)
        self.add('AppDataFolder', LOCALAPPDATA)
        self.add('PreferenceFolder', PREF_DIR)

        mode = 0o770
        for path in self.values():
            if not os.path.exists(path):
                head, tail              = os.path.split(path)
                try:
                    original_umask = os.umask(0)
                    os.makedirs(path, mode)
                finally:
                    os.umask(original_umask)
                os.chmod(path, mode)

        if globalSetting.printCfgInfo:
            if globalSetting.printDirInfo:
                pprint.pprint(self)

        if globalSetting.saveCfgInfo:
            if globalSetting.saveDirInfo:
                save_data(dirCfg, self)

    def add(self, key, value):
        self[key]                       = value


class ConfigAvatar(dict):

    key                                 = 'ConfigAvatar'

    def __init__(self):
        super(ConfigAvatar, self).__init__()

        for root, dirs, names in os.walk(AVATAR_DIR, topdown=False):
            for name in names:
                self[name.split('.avatar')[0]] = os.path.join(root, name).replace('\\', '/')

        if globalSetting.printCfgInfo:
            if globalSetting.printAvatarInfo:
                pprint.pprint(self)

        if globalSetting.saveCfgInfo:
            if globalSetting.saveAvatarInfo:
                save_data(avatarCfg, self)


class ConfigLogo(dict):

    key                                 = 'ConfigLogo'

    def __init__(self):
        super(ConfigLogo, self).__init__()

        damgLogos                       = dict()
        plmLogos                        = dict()

        for root, dirs, names in os.walk(DAMG_LOGO_DIR, topdown=False):
            for name in names:
                damgLogos[name.split('.png')[0]] = os.path.join(root, name).replace('\\', '/')

        for root, dirs, names in os.walk(PLM_LOGO_DIR, topdown=False):
            for name in names:
                plmLogos[name.split('.png')[0]] = os.path.join(root, name).replace('\\', '/')

        self['DAMGTEAM']                = damgLogos
        self['PLM']                     = plmLogos

        if globalSetting.printCfgInfo:
            if globalSetting.printAvatarInfo:
                pprint.pprint(self)

        if globalSetting.saveCfgInfo:
            if globalSetting.saveAvatarInfo:
                save_data(logoCfg, self)


class ConfigImage(dict):

    key                                 = 'ConfigImage'

    def __init__(self):
        super(ConfigImage, self).__init__()

        for root, dirs, names, in os.walk(IMAGE_DIR, topdown=False):
            for name in names:
                self[name.split('.node')[0]] = os.path.join(root, name).replace('\\', '/')

        if globalSetting.printCfgInfo:
            if globalSetting.printImgInfo:
                pprint.pprint(self)

        if globalSetting.saveCfgInfo:
            if globalSetting.saveImgInfo:
                save_data(imageConfig, self)


class ConfigIcon(dict):

    key                                 = 'ConfigIcon'

    def __init__(self):
        super(ConfigIcon, self).__init__()

        self['icon12']                  = self.get_icons(ICON_DIR_12)
        self['icon16']                  = self.get_icons(ICON_DIR_16)
        self['icon24']                  = self.get_icons(ICON_DIR_24)
        self['icon32']                  = self.get_icons(ICON_DIR_32)
        self['icon48']                  = self.get_icons(ICON_DIR_48)
        self['icon64']                  = self.get_icons(ICON_DIR_64)

        self['node']                    = self.get_icons(NODE_ICON_DIR)
        self['tag']                     = self.get_icons(TAG_ICON_DIR)
        self['web16']                   = self.get_icons(WEB_ICON_16)
        self['web24']                   = self.get_icons(WEB_ICON_24)
        self['web32']                   = self.get_icons(WEB_ICON_32)
        self['web48']                   = self.get_icons(WEB_ICON_48)
        self['web64']                   = self.get_icons(WEB_ICON_64)
        self['web128']                  = self.get_icons(WEB_ICON_128)


        if globalSetting.printCfgInfo:
            if globalSetting.printIconInfo:
                pprint.pprint(self)

        if globalSetting.saveCfgInfo:
            if globalSetting.saveIconInfo:
                save_data(iconCfg, self)

    def get_icons(self, dir):
        icons = dict()
        for root, dirs, names in os.walk(dir, topdown=False):
            for name in names:
                icons[name.split('.icon')[0]] = os.path.join(root, name).replace('\\', '/')
        return icons


class ConfigServer(dict):

    key                             = 'ConfigServer'

    def __init__(self):
        super(ConfigServer, self).__init__()

        self.add('vanila'           , VANILA_LOCAL)
        self.add('AWS'              , AWS_GLOBAL)

        if globalSetting.printCfgInfo:
            if globalSetting.printServerInfo:
                pprint.pprint(self)

        if globalSetting.saveCfgInfo:
            if globalSetting.saveServerInfo:
                save_data(serverCfg, self)

    def add(self, key, value):
        self[key]                   = value


class ConfigEnvVar(dict):

    key                                 = 'ConfigEnvVar'

    def __init__(self):
        super(ConfigEnvVar, self).__init__()
        for k, v in os.environ.items():
            self[k]                     = v.replace('\\', '/')

        if globalSetting.printCfgInfo:
            if globalSetting.printEnvInfo:
                pprint.pprint(self)

        if globalSetting.saveCfgInfo:
            if globalSetting.saveEnvInfo:
                save_data(envVarCfg, self)

    def update(self):
        for k, v in os.environ.items():
            self[k]                     = v.replace('\\', '/')

        if globalSetting.defaults.save_configInfo:
            if globalSetting.defaults.save_envInfo:
                save_data(envVarCfg, self)


class ConfigUrl(dict):

    key                             = 'ConfigUrl'

    def __init__(self):
        super(ConfigUrl, self).__init__()

        self.add('homepage'         , __homepage__)
        self.add('pythonTag'        , PYTHON_TAG)
        self.add('licenceTag'       , LICENCE_TAG)
        self.add('versionTag'       , VERSION_TAG)
        self.add('PLM wiki'         , __plmWiki__)
        self.add('goole'            , __google__)
        self.add('google vn'        , __googleVN__)
        self.add('google nz'        , __googleNZ__)

        if globalSetting.printCfgInfo:
            if globalSetting.printUrlInfo:
                pprint.pprint(self)

        if globalSetting.saveCfgInfo:
            if globalSetting.saveUrlInfo:
                save_data(urlCfg, self)

    def add(self, key, value):
        self[key]                   = value


class ConfigTypes(dict):

    key                     = 'ConfigTypes'

    def __init__(self):
        super(ConfigTypes, self).__init__()

        self['actionTypes'] = actionTypes
        self['layoutTypes'] = layoutTypes
        self['DB_ATTRIBUTE_TYPE'] = DB_ATTRIBUTE_TYPE
        self['CMD_VALUE_TYPE'] = CMD_VALUE_TYPE
        self['RAMTYPE'] = RAMTYPE
        self['FORMFACTOR'] = FORMFACTOR
        self['CPUTYPE'] = CPUTYPE
        self['DRIVETYPE'] = DRIVETYPE

        if globalSetting.printCfgInfo:
            if globalSetting.printTypeInfo:
                pprint.pprint(self)

        if globalSetting.saveCfgInfo:
            if globalSetting.saveTypeInfo:
                save_data(typeCfg, self)


class ConfigFormats(dict):

    key                     = 'ConfigFormats'

    def __init__(self):
        super(ConfigFormats, self).__init__()

        self.add('INI'      , INI)
        self.add('NATIVE', NATIVE)
        self.add('INVALID', INVALID)
        self.add('LOG_FORMAT', LOG_FORMAT)
        self.add('DT_FORMAT' , DT_FORMAT)
        self.add('ST_FORMAT'  , ST_FORMAT)
        self.add('dt datetTimeStamp' , datetTimeStamp)
        self.add('IMGEXT ext', IMGEXT)

        if globalSetting.printCfgInfo:
            if globalSetting.printFmtInfo:
                pprint.pprint(self)

        if globalSetting.saveCfgInfo:
            if globalSetting.saveFmtInfo:
                save_data(fmtCfg, self)

    def add(self, key, value):
        self[key]           = value


class CommandData(dict):

    key                             = 'CommandData'

    def __init__(self, key=None, icon=None, tooltip=None, statustip=None,
                       value=None, valueType=None, arg=None, code=None):
        super(CommandData, self).__init__()

        self.key                    = key
        self.icon                   = icon
        self.toolTip                = tooltip
        self.statusTip              = statustip
        self.value                  = value
        self.valueType              = valueType
        self.arg                    = arg
        self.code                   = code

        ks = ['key', 'icon', 'tooltip', 'statustip', 'value', 'valueType', 'arg', 'code']
        vs = [key, icon, tooltip, statustip, value, valueType, arg, code]

        for i in range(len(ks)):
            self[ks[i]]             = vs[i]


class ConfigPipeline(dict):

    key                         = 'ConfigPipeline'

    def __init__(self, iconInfo, appInfo, urlInfo, dirInfo, pthInfo):
        super(ConfigPipeline, self).__init__()

        self.iconInfo           = iconInfo
        self.appInfo            = appInfo
        self.urlInfo            = urlInfo
        self.dirInfo            = dirInfo
        self.pthInfo            = pthInfo

        removeKeys              = []
        launchAppKeys           = []

        functionKeys            = APP_FUNCS_KEYS
        layoutKeys              = APP_UI_KEYS

        for key in self.appInfo:
            if 'NukeX' in key:
                self.appInfo[key] = '"' + self.appInfo[key] + '"' + " --nukex"
            elif 'Hiero' in key:
                self.appInfo[key] = '"' + self.appInfo[key] + '"' + " --hiero"
            elif 'UVLayout' in key:
                self.appInfo[key] = '"' + self.appInfo[key] + '"' + " -launch"

        for key in KEYDETECT:
            for k in self.appInfo:
                if key in k:
                    removeKeys.append(k)

        for k in removeKeys:
            self.del_key(k)

        self.appInfo.update()

        for k in KEYPACKAGE:
            for key in self.appInfo.keys():
                if k in key:
                    launchAppKeys.append(key)

        qtDesigner = os.path.join(os.getenv('PROGRAMDATA'), 'Anaconda3', 'Library', 'bin', 'designer.exe')
        davinciPth = os.path.join(os.getenv('PROGRAMFILES'), 'Blackmagic Design', 'DaVinci Resolve', 'resolve.exe')

        eVal       = [qtDesigner, davinciPth]
        eKeys      = ['QtDesigner', 'Davinci Resolve']

        for i in range(len(eVal)):
            if os.path.exists(eVal[i]):
                self.appInfo[eKeys[i]] = eVal[i]
                launchAppKeys.append(eKeys[i])

        for key in launchAppKeys:
            try:
                icon = self.iconInfo['icon32'][key]
            except KeyError:
                icon = key
                iconMissing.append(key)
            finally:
                toolTips[key] = 'Launch {0}'.format(key)
                statusTips[key] = 'Launch {0}: {1}'.format(key, self.appInfo[key])
                value = self.appInfo[key]
                valueType = CMD_VALUE_TYPE['pth']
                arg = value
                if 'NukeX' in key:
                    code = 'os.system'
                elif 'Hiero' in key:
                    code = 'os.system'
                elif 'UVLayout' in key:
                    code = 'os.system'
                else:
                    code = 'os.startfile'

            tooltip = toolTips[key]
            statustip = statusTips[key]
            self.add(key, CommandData(key, icon, tooltip, statustip, value, valueType, arg, code))

        for key in functionKeys:

            try:
                icon = self.iconInfo['tag'][key]
            except KeyError:
                try:
                    icon = self.iconInfo['icon32'][key]
                except KeyError:
                    icon = key
                    iconMissing.append(key)
            finally:
                if key in OPEN_URL_KEYS:
                    toolTips[key] = 'Go to {0} website'.format(key)
                    statusTips[key] = 'Open URL: {0}'.format(self.urlInfo[key])
                    value = self.urlInfo[key]
                    valueType = CMD_VALUE_TYPE['url']
                    arg = value
                    code = 'openURL'
                elif key in SYS_CMD_KEYS:
                    toolTips[key] = 'Open command prompt'
                    statusTips[key] = 'Open command prompt'
                    value = 'start /wait cmd'
                    valueType = CMD_VALUE_TYPE['cmd']
                    arg = value
                    code = 'os.system'
                elif key in OPEN_DIR_KEYS:
                    toolTips[key] = 'Open {0} folder'.format(key.replace('Folder', ''))
                    statusTips[key] = 'Open {0} folder'.format(key.replace('Folder', ''))
                    value = self.dirInfo[key]
                    valueType = CMD_VALUE_TYPE['dir']
                    arg = value
                    code = 'os.startfile'
                elif key in APP_EVENT_KEYS:
                    toolTips[key] = 'Release PLM Event: {0}'.format(key)
                    statusTips[key] = 'Activate Event: {0}'.format(key)
                    value = key
                    valueType = CMD_VALUE_TYPE['event']
                    arg = key
                    code = 'appEvent'
                elif key in STYLESHEET_KEYS:
                    toolTips[key] = 'Load stylesheet: {0}'.format(key)
                    statusTips[key] = 'Load stylesheet: {0}'.format(key)
                    value = key
                    valueType = CMD_VALUE_TYPE['stylesheet']
                    arg = value
                    code = 'stylesheet'
                elif key in SHORTCUT_KEYS:
                    toolTips[key] = key
                    statusTips[key] = key
                    value = key
                    valueType = CMD_VALUE_TYPE['shortcut']
                    arg = value
                    code = 'shortcut'
                else:
                    toolTips[key] = 'Execute function: {0}'.format(key)
                    statusTips[key] = 'Execute function: {0}'.format(key)
                    value = key
                    valueType = CMD_VALUE_TYPE['func']
                    arg = value
                    code = 'function'

            tooltip = toolTips[key]
            statustip = statusTips[key]
            self.add(key, CommandData(key, icon, tooltip, statustip, value, valueType, arg, code))

        for key in layoutKeys:
            if not key in launchAppKeys:
                # print(key)
                try:
                    icon = self.iconInfo['icon32'][key]
                except KeyError:
                    icon = key
                    iconMissing.append(key)
                finally:
                    toolTips[key] = 'Show: {0}'.format(key)
                    statusTips[key] = 'Show: {0}'.format(key)
                    value = key
                    valueType = CMD_VALUE_TYPE['uiKey']
                    arg = value
                    code = 'showUI'

                tooltip = toolTips[key]
                statustip = statusTips[key]
                self.add(key, CommandData(key, icon, tooltip, statustip, value, valueType, arg, code))

        if globalSetting.printCfgInfo:
            if globalSetting.printPlmInfo:
                pprint.pprint(self)

        if globalSetting.saveCfgInfo:
            if globalSetting.savePlmInfo:
                save_data(plmCfg, self)

    def del_key(self, key):
        try:
            del self.appInfo[key]
        except KeyError:
            self.appInfo.pop(key, None)

    def add(self, key, value):
        self[key]                           = value


if platform.system() == 'Windows':

    runs                        = subprocess.Popen
    sysKey                      = 'SYSTEMINFO'
    optKey1                     = 'OS Configuration'
    igCase                      = re.IGNORECASE
    scr                         = runs(sysKey, stdin=PIPE, stdout=PIPE).communicate()[0].decode('utf-8')
    optInfo1                    = re.findall("{0}:\w*(.*?)\n".format(optKey1), scr, igCase)
    com                         = wmi.WMI()
    operatingSys                = com.Win32_OperatingSystem()
    computerSys                 = com.Win32_ComputerSystem()
    biosSys                     = com.Win32_BIOS()
    baseBoardSys                = com.Win32_BaseBoard()
    processorSys                = com.Win32_Processor()
    displaySys                  = com.Win32_DisplayControllerConfiguration()
    memorySys                   = com.Win32_PhysicalMemory()
    logicalDiskSys              = com.Win32_LogicalDisk()
    cdromSys                    = com.Win32_CDROMDrive()
    diskDriveSys                = com.Win32_DiskDrive()
    pciSys                      = com.Win32_IDEController()
    networkSys                  = com.Win32_NetworkAdapter()
    keyboardSys                 = com.Win32_Keyboard()
    miceSys                     = com.Win32_PointingDevice()
    totalRam                    = computerSys[0].TotalPhysicalMemory

    class ConfigMachine(dict):

        key = 'ConfigMachine'

        usbCount = dvdCount = hddCount = pttCount = gpuCount = pciCount = keyboardCount = netCount = ramCount = 1
        miceCount = cpuCount = biosCount = osCount = screenCount = 1

        def __init__(self):
            super(ConfigMachine, self).__init__()

            self['os'] = self.osInfo()
            self['bios'] = self.biosInfo()
            self['cpu'] = self.cpuInfo()
            self['gpu'] = self.gpuInfo()
            self['monitors'] = self.screenInfo()
            self['ram'] = self.ramInfo()
            self['drivers'] = self.driverInfo()
            self['PCIs'] = self.pciInfo()
            self['network'] = self.networkInfo()
            self['keyboard'] = self.keyboardInfo()
            self['mice'] = self.miceInfo()

            if globalSetting.printCfgInfo:
                if globalSetting.printPcInfo:
                    pprint.pprint(self)

            if globalSetting.saveCfgInfo:
                if globalSetting.savePcInfo:
                    save_data(pcCfg, self)

        def osInfo(self, **info):

            for o in operatingSys:
                ops = {}
                key = 'os {0}'.format(self.osCount)
                ops['brand'] = o.Manufacturer
                ops['os name'] = o.Caption
                ops['device name'] = computerSys[0].DNSHostName
                ops['device type'] = [item.strip() for item in optInfo1][0]
                ops['registered email'] = o.RegisteredUser
                ops['organisation'] = o.Organization
                ops['version'] = o.Version
                ops['os architecture'] = o.OSArchitecture
                ops['serial number'] = o.SerialNumber
                ops['mac adress'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
                info[key] = ops
                self.osCount += 1
            return info

        def biosInfo(self, **info):
            for b in biosSys:
                bios = {}
                key = 'bios {0}'.format(self.biosCount)
                bios['brand'] = computerSys[0].Manufacturer
                bios['name'] = b.Manufacturer
                bios['model'] = baseBoardSys[0].Product
                bios['type'] = computerSys[0].SystemType
                bios['version'] = b.BIOSVersion
                bios['sockets'] = computerSys[0].NumberOfProcessors
                info[key] = bios
                self.biosCount += 1
            return info

        def cpuInfo(self, **info):
            for c in processorSys:
                cpu = {}
                key = 'cpu {0}'.format(self.cpuCount)
                cpu['name'] = c.Name
                cpu['cores'] = c.NumberOfCores
                cpu['threads'] = c.NumberOfLogicalProcessors
                cpu['family'] = c.Caption
                cpu['max speed'] = '{0} GHz'.format(int(c.MaxClockSpeed) / 1000)
                cpu['type'] = CPUTYPE[c.ProcessorType]
                cpu['l2 size'] = '{0} MB'.format(c.L2CacheSize)
                cpu['l3 size'] = '{0} MB'.format(c.L3CacheSize)
                info[key] = cpu
                self.cpuCount += 1
            return info

        def gpuInfo(self, **info):
            for g in displaySys:
                gpu = {}
                key = 'gpu {0}'.format(self.gpuCount)
                gpu['name'] = g.Name
                gpu['refresh rate'] = g.RefreshRate
                gpu['bit rate'] = g.BitsPerPixel
                info[key] = gpu
                self.gpuCount += 1
            return info

        def screenInfo(self, **info):

            allScreens = QApplication.screens()

            for index, screen_no in enumerate(allScreens):
                screenInfo = {}
                key = 'screen {0}'.format(self.screenCount)
                screen = allScreens[index]
                screenInfo['resolution'] = '{0}x{1}'.format(screen.size().width(), screen.size().height())
                screenInfo['depth'] = screen.depth()
                screenInfo['serial'] = screen.serialNumber()
                screenInfo['brand'] = screen.manufacturer()
                screenInfo['model'] = screen.model()
                screenInfo['name'] = screen.name()
                screenInfo['dpi'] = screen.physicalDotsPerInch()
                info[key] = screenInfo
                self.screenCount += 1
            return info

        def ramInfo(self, **info):
            rams = []
            for r in memorySys:
                ram = {}
                key = 'ram {0}'.format(self.ramCount)
                ram['capacity'] = '{0} GB'.format(round(int(r.Capacity) / (1024.0 ** 3)))
                ram['bus'] = r.ConfiguredClockSpeed
                ram['location'] = r.DeviceLocator
                ram['form'] = FORMFACTOR[r.FormFactor]
                ram['type'] = RAMTYPE[r.MemoryType]
                ram['part number'] = r.PartNumber
                rams.append(ram['capacity'])
                info[key] = ram
                self.ramCount += 1

            info['total'] = '{0} GB'.format(round(int(totalRam) / (1024.0 ** 3)))
            info['details'] = rams
            info['rams'] = len(memorySys)
            return info

        def driverInfo(self, **info):
            for physical_disk in diskDriveSys:
                if physical_disk.associators("Win32_DiskDriveToDiskPartition") == []:
                    disk = {}
                    key = 'USB drive {0}'.format(self.usbCount)
                    disk['brand'] = (physical_disk.PNPDeviceID).replace('SCSI\\DISK&VEN_', '').split('&PROD')[0]
                    disk['index'] = physical_disk.Index
                    disk['name'] = physical_disk.Name.replace('\\\\.\\', '')
                    disk['model'] = physical_disk.Model
                    disk['partition'] = physical_disk.Partitions
                    disk['size'] = '0 GB'
                    disk['type'] = DRIVETYPE[2]
                    for d in logicalDiskSys:
                        if d.DriveType == 2:
                            disk['path'] = '{0}/'.format(d.Caption)

                    disk['firmware'] = physical_disk.FirmwareRevision
                    info[key] = disk
                    self.usbCount += 1
                else:
                    for partition in physical_disk.associators("Win32_DiskDriveToDiskPartition"):
                        if partition.associators("Win32_LogicalDiskToPartition") == []:
                            disk = {}
                            key = 'partition {0}'.format(self.pttCount)
                            disk['brand'] = (physical_disk.PNPDeviceID).replace('SCSI\\DISK&VEN_', '').split('&PROD')[0]
                            disk['firmware'] = physical_disk.FirmwareRevision
                            disk['index'] = '{0} - {1}'.format(partition.DiskIndex, partition.Index)
                            disk['name'] = partition.Name
                            disk['model'] = physical_disk.Model
                            disk['partition'] = partition.Caption
                            disk['size'] = '{0} GB'.format(round(int(partition.size) / (1024.0 ** 3)))
                            disk['block'] = '{0} MB'.format(round(int(partition.NumberOfBlocks) / (1024.0 ** 2)))
                            disk['offset'] = '{0} GB'.format(round(int(partition.StartingOffset) / (1024.0 ** 3)))
                            disk['type'] = partition.Type
                            info[key] = disk
                            self.pttCount += 1
                        else:
                            for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                                disk = {}
                                key = 'harddrive {0}'.format(self.hddCount)
                                disk['brand'] = \
                                (physical_disk.PNPDeviceID).replace('SCSI\\DISK&VEN_', '').split('&PROD')[0]
                                disk['path'] = '{0}/'.format(logical_disk.Caption)
                                disk['index'] = physical_disk.Index
                                disk['name'] = '{0} ({1})'.format(logical_disk.VolumeName, logical_disk.Caption)
                                disk['model'] = physical_disk.Model
                                disk['partition'] = partition.Caption
                                disk['size'] = '{0} GB'.format(round(int(logical_disk.size) / (1024.0 ** 3)))
                                disk['free size'] = '{0} GB'.format(round(int(logical_disk.FreeSpace) / (1024.0 ** 3)))
                                disk['type'] = DRIVETYPE[logical_disk.DriveType]
                                disk['firmware'] = physical_disk.FirmwareRevision
                                disk['setup type'] = logical_disk.FileSystem
                                info[key] = disk
                                self.hddCount += 1

            if not cdromSys is []:
                disk = {}
                key = 'CD drive {0}'.format(self.dvdCount)
                disk['brand'] = (cdromSys[0].DeviceID).replace('SCSI\\DISK&VEN_', '').split('&PROD')[0]
                disk['path'] = '{0}/'.format(cdromSys[0].Drive)
                disk['index'] = cdromSys[0].Id
                disk['name'] = cdromSys[0].Name
                disk['model'] = cdromSys[0].Caption
                disk['type'] = cdromSys[0].MediaType
                info[key] = disk
                self.dvdCount += 1

            return info

        def pciInfo(self, **info):
            for p in pciSys:
                pci = {}
                key = 'PCI rack {0}'.format(self.pciCount)
                pci['name'] = p.Name
                pci['id'] = p.DeviceID
                pci['status'] = p.Status
                info[key] = pci
                self.pciCount += 1
            return info

        def networkInfo(self, **info):
            info['LAN ip'] = socket.gethostbyname(socket.gethostname())
            for n in networkSys:
                if n.AdapterType:
                    network = {}
                    key = 'network device {0}'.format(self.netCount)
                    network['name'] = n.Name
                    network['brand'] = n.Manufacturer
                    network['id'] = n.DeviceID
                    network['uid'] = n.GUID
                    network['index'] = n.Index
                    network['MacAdress'] = n.MACAddress
                    network['connect id'] = n.NetConnectionID
                    network['service name'] = n.ServiceName
                    network['speed'] = n.Speed
                    network['type'] = n.AdapterType
                    network['type id'] = n.AdapterTypeID
                    info[key] = network
                    self.netCount += 1
            return info

        def keyboardInfo(self, **info):
            for k in keyboardSys:
                keyboard = {}
                key = 'keyboard {0}'.format(self.keyboardCount)
                keyboard['name'] = k.Name
                keyboard['id'] = k.DeviceID
                keyboard['status'] = k.Status
                info[key] = keyboard
                self.keyboardCount += 1
            return info

        def miceInfo(self, **info):
            for m in miceSys:
                mice = {}
                key = 'mice {0}'.format(self.miceCount)
                mice['brand'] = m.Manufacturer
                mice['name'] = m.Name
                mice['id'] = m.DeviceID
                mice['status'] = m.Status
                info[key] = mice
                self.miceCount += 1

            return info


dirInfo                            = ConfigDirectory()
pthInfo                            = ConfigPath()
iconInfo                           = ConfigIcon()
appInfo                            = ConfigApps()
urlInfo                            = ConfigUrl()
plmInfo                            = ConfigPipeline(iconInfo, appInfo, urlInfo, dirInfo, pthInfo)

if not os.path.exists(LOCAL_DB):
    from .PresetDB import PresetDB
    localDB = PresetDB(filename=LOCAL_DB)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 10:45 PM
# Pipeline manager - DAMGteam
