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
autodeskApp         = ["Autodesk Maya", "Autodesk Mudbox", "Maya", "Mudbox", "3ds Max", "AutoCAD"]

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

TRACK_TDS           = ['Maya', 'ZBrush', 'Houdini', '3Ds Max', 'Mudbox', 'BLender', 'Katana']
TRACK_VFX           = ['NukeX', 'After Effects', ]
TRACK_ART           = ['Photoshop', 'Krita (x64)', 'Krita (x32)']
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

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/08/2018 - 2:30 AM
# © 2017 - 2018 DAMGteam. All rights reserved