# -*- coding: utf-8 -*-
"""

Script Name: keys.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys

# --------------------------------------------------------------------------------------------------------------
""" Autodesk _data """

autodeskVer         = ["2017", "2018", "2019", "2020", "2021"]
autodeskApp         = ["Maya", "MudBox", "3ds Max", "AutoCAD"]
# userMayaDir         = os.path.expanduser(r"~/Documents/maya")

# --------------------------------------------------------------------------------------------------------------
""" Adobe _data """

adobeVer            = ["CC 2017", "CC 2018", "CC 2019", "CC 2020", "CC 2021"]
adobeApp            = ["Adobe Photoshop", "Adobe Illustrator", "Adobe Audition", "Adobe After Effects",
                       "Adobe Premiere Pro", "Adobe Media Encoder", ]

# --------------------------------------------------------------------------------------------------------------
""" Foundry _data """

foundryVer          = ["11.1v1", "11.2v1", "4.0v1", "4.1v1", "2.6v3", "4.6v1", "12.0v1"]
foundryApp          = ['Hiero', 'Mari', 'NukeStudio', 'NukeX', 'Katana',]

# --------------------------------------------------------------------------------------------------------------
""" Pixologic _data """

pixologiVer         = [ "4R6", "4R7", "4R8", "4R9", '2018', '2019', '2020']
pixologiApp         = [ 'ZBrush' ]

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

anacondaApp         = ['Spyder', 'QtDesigner', 'Git Bash']
windowApps          = ['Sublime Text 2', 'Sublime Text 3', 'Wordpad', 'Headus UVLayout', 'Snipping Tool', ]

# --------------------------------------------------------------------------------------------------------------
""" Combine data package """

pVERSION = dict(adobe=adobeVer, autodesk=autodeskVer, allegorithmic = allegorithmicVer, foundry=foundryVer,
                pixologic=pixologiVer, sizefx=sizefxVer, office=officeVer, jetbrains=jetbrainsVer, wonderUnit=wonderUnitVer, )

pPACKAGE = dict(adobe=adobeApp, autodesk=autodeskApp, allegorithmic = allegorithmicApp, foundry=foundryApp,
                pixologic=pixologiApp, sizefx=sizefxApp, office=officeApp, jetbrains=jetbrainsApp, wonderUnit=wonderUniApp,)

# --------------------------------------------------------------------------------------------------------------
""" Tracking configKey """

TRACK_TDS           = ['Maya', 'ZBrush', 'Houdini', '3Ds Max', 'Mudbox', 'BLender', ]
TRACK_VFX           = ['NukeX', 'After Effects', ]
TRACK_ART           = ['Photoshop', ]
TRACK_PRE           = ['Storyboarder', 'Illustrator', 'Krita (x64)', 'Krita (x32)']
TRACK_TEX           = ['Mari', 'Painter', ]
TRACK_POST          = ['Davinci Resolve', 'Hiero', 'HieroPlayer', 'Premiere Pro']
TRACK_OFFICE        = ['Word', 'Excel', 'PowerPoint', 'Wordpad']
TRACK_DEV           = ['PyCharm', 'Sublime Text', 'QtDesigner', 'Git Bash', 'Spyder', 'Command Prompt']
TRACK_TOOLS         = ['Calculator', 'Calendar', 'EnglishDictionary', 'FindFiles', 'ImageViewer', 'ScreenShot', 'NodeGraph']
TRACK_EXTRA         = ['ReConfig', 'CleanPyc', 'Debug', 'Snipping Tool']
TRACK_SYSTRAY       = ['Snipping Tool', 'ScreenShot', 'Maximize', 'Minimize', 'Restore', 'Exit', ]
KEYDETECT           = ["Non-commercial", "Uninstall", "Verbose", "License", "Skype", ".url", "Changelog", "Settings"]

FIX_KEY             = {'ScreenShot': 'ScreenShot', 'Snipping Tool': 'SnippingTool'}

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

SETTING_UI_KEYS     = ['Configuratons', 'Preferences', 'AppSetting', 'GlobalSetting', 'UserSetting', 'BrowserSetting',
                       'ProjSetting', 'OrgSetting', 'TaskSetting', 'TeamSetting']

LIBRARY_UI_KEYS     = ['UserLibrary', 'HDRILibrary', 'TextureLibrary', 'AlphaLibrary', ]

TOOL_UI_KEYS        = ['Calculator', 'Calendar', 'ContactUs', 'EnglishDictionary', 'FeedBack', 'ReportBug', 'FindFiles',
                       'ImageViewer', 'InviteFriend', 'Messenger', 'NoteReminder', 'ScreenShot', 'TextEditor', ]

PLUGIN_UI_KEYS      = ['PluginManager', 'NodeGraph', 'Browser', ]

APP_UI_KEYS        = MAIN_UI_KEYS + INFO_UI_KEYS + PROJ_UI_KEYS + ORG_UI_KEYS + TASK_UI_KEYS + TEAM_UI_KEYS + \
                     SETTING_UI_KEYS + LIBRARY_UI_KEYS + TOOL_UI_KEYS + PLUGIN_UI_KEYS

# --------------------------------------------------------------------------------------------------------------
""" PLM Function key """

factors             = ['Organisation', 'Project', 'Department', 'Team', 'Task', ]
factorActs          = ['New', 'Config', 'Edit', 'Remove']

factorKeys     = []
for f in factors:
    for act in factorActs:
        factorKeys.append('{0} {1}'.format(act, f))

APP_EVENT_KEYS      = ['ShowAll', 'SwitchAccount', 'LogIn', 'LogOut', 'Quit', 'Exit', 'ChangePassword', 'UpdateAvatar',]

STYLESHEET_KEYS     = ['bright', 'dark', 'charcoal', 'nuker', ]

STYLE_KEYS          = []

OPEN_DIR_KEYS       = ['ConfigDir', 'IconDir', 'SettingDir', 'AppdataDir', 'PreferenceDir', ]

OPEN_URL_KEYS       = ['pythonTag', 'licenceTag', 'versionTag', 'PLM wiki']

SYS_CMD_KEYS        = ['Command Promt', 'cmd', ]

SHORTCUT_KEYS       = ['Copy', 'Cut', 'Paste', 'Delete', 'Find', 'ReName']

APP_FUNCS_KEYS      = ['ReConfig', 'CleanPyc', 'Debug', 'Restore', 'Maximize', 'Minimize', ] + factorKeys + \
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

    return keyPackage + windowApps + anacondaApp + ['Word', 'Excel', 'PowerPoint']

def generate_config(key, *args):
    keyPackages = generate_key_packages()
    keys = []
    for k in keyPackages:
        for t in pTRACK[key]:
            if t in k:
                keys.append(k)
    return list(sorted(set(keys)))

KEYPACKAGE      = generate_key_packages()

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
CONFIG_TOOLS    = generate_config('Tools')                          # useful/custom tool supporting for the whole pipeline
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

SHOWLAYOUT_KEY          = ['About', 'Alpha', 'BotTab', 'Browser', 'Calculator', 'Calendar', 'CodeOfConduct', 'Configuration',
                           'ConfigOrganisation', 'ConfigProject', 'ConfigTask', 'ConfigTeam', 'Configurations',
                           'ConnectStatus', 'ContactUs', 'Contributing', 'Credit', 'EditOrganisation', 'EditProject',
                           'EditTask', 'EditTeam', 'EnglishDictionary', 'Feedback', 'FindFiles', 'Footer',
                           'ForgotPassword', 'GridLayout', 'HDRI', 'ImageViewer', 'Licence', 'MainMenuSection',
                           'MainToolBar', 'MainToolBarSection', 'NodeGraph', 'NoteReminder', 'Notification',
                           'Organisation', 'PipelineManager', 'Preferences', 'Project', 'Reference', 'ScreenShot',
                           'SettingUI', 'SignIn', 'SignOut', 'SignUp', 'StatusBar', 'SwitchAccount', 'SysTray',
                           'Task', 'Team', 'TextEditor', 'Texture', 'TopTab', 'TopTab1', 'TopTab2', 'TopTab3',
                           'UserSetting', 'Version']

RESTORE_KEY             = ['Restore']
SHOWMAX_KEY             = ['Maximize']
SHOWMIN_KEY             = ['Minimize']

START_FILE              = CONFIG_DEV + CONFIG_OFFICE + CONFIG_TDS + CONFIG_VFX + CONFIG_ART + CONFIG_TEX + CONFIG_POST + \
                          ['ConfigFolder', 'IconFolder', 'SettingFolder', 'AppFolder', 'Snipping Tool']

START_FILE_KEY          = sorted([i for i in START_FILE if not i == 'Command Prompt'])

EXECUTING_KEY           = ['Exit', 'CleanPyc', 'ReConfig', 'Debug', 'Command Prompt', 'Showall'] + SHORTCUT_KEYS + STYLESHEET_KEYS

IGNORE_ICON_NAME        = ['Widget', 'TopTab1', 'TopTab2', 'TopTab3', 'ItemWidget']

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
           'QSS_DIR', 'RCS_DIR', 'SCSS_DIR', '__appname__', 'subprocess', 'unicode_literals', 'absolute_import', ]

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/08/2018 - 2:30 AM
# © 2017 - 2018 DAMGteam. All rights reserved