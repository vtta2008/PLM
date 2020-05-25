# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys, platform, json, yaml, pprint, winshell, pkg_resources

# PLM
from PLM                                import ROOT, ROOT_APP, glbSettings, create_path, CFG_DIR, TMP_DIR, CACHE_DIR, PREF_DIR, USER_DIR
from PLM.api.Gui                        import FontDataBase, Color
from PLM.api.Core.io_core               import Qt
from PLM.cores.data                     import PresetDB


dirCfg                                  = create_path(CFG_DIR, 'dirs.cfg')
pthCfg                                  = create_path(CFG_DIR, 'paths.cfg')
iconCfg                                 = create_path(CFG_DIR, 'icons.cfg')
appsCfg                                 = create_path(CFG_DIR, 'installations.cfg')
pythonCfg                               = create_path(CFG_DIR, 'pythons.cfg')
urlCfg                                  = create_path(CFG_DIR, 'urls.cfg')
plmCfg                                  = create_path(CFG_DIR, 'pipeline.cfg')
deviceCfg                               = create_path(CFG_DIR, 'pc.cfg')
logoCfg                                 = create_path(CFG_DIR, 'logo.cfg')
fontCfg                                 = create_path(CFG_DIR, 'fonts.cfg')
settingCfg                              = create_path(CFG_DIR, 'settings.cfg')
formatCfg                               = create_path(CFG_DIR, 'formats.cfg')
uiKeyCfg                                = create_path(CFG_DIR, 'uiKey.cfg')
colorCfg                                = create_path(CFG_DIR, 'colors.cfg')


factors                                 = ['Organisation', 'Project', 'Department', 'Team', 'Task', ]

factorActs                              = ['New', 'Config', 'Edit', 'Remove']

FACTOR_KEYS                             = []

for f in factors:
    FACTOR_KEYS.append(f)
    for act in factorActs:
        FACTOR_KEYS.append('{0} {1}'.format(act, f))



class Cfg(dict):

    key                                 = 'ConfigBase'
    _filePath                           = None

    def __init__(self):
        dict.__init__(self)

        self.update()

    def save_data(self):
        if not self.filePath:
            return

        if os.path.exists(self.filePath):
            try:
                os.remove(self.filePath)
            except FileNotFoundError:
                pass

        with open(self.filePath, 'w+') as f:
            if glbSettings.formatSaving == 'json':
                json.dump(self, f, indent=4)
            elif glbSettings.formatSaving == 'yaml':
                yaml.dump(self, f, default_flow_style=False)
            else:
                # will update more data type library later if need
                pass
        return True

    def pprint(self):
        return pprint.pprint(self.__dict__)

    def add(self, key, value):
        self[key]                   = value

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, val):
        self._filePath              = val


class Cmds(dict):

    key                             = 'Cmds'

    def __init__(self, key=None, icon=None, tooltip=None, statustip=None,
                       value=None, valueType=None, arg=None, code=None):
        super(Cmds, self).__init__()

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


class TrackKeys(Cfg):

    key                                 = 'TrackKeys'
    _filePath                           = None

    pVERSION = dict(adobe=["CC 2017", "CC 2018", "CC 2019", "CC 2020", "CC 2021"],
                    autodesk=["2017", "2018", "2019", "2020", "2021"],
                    allegorithmic=[],
                    foundry=["11.1v1", "11.2v1", "4.0v1", "4.1v1", "2.6v3", "4.6v1", "12.0v1",
                             '3.5v2', '3.2v4', '2.6v3'],
                    pixologic=["4R6", "4R7", "4R8", '2018', '2019', '2020', '2021'],
                    sizefx=['16.5.439', '16.5.496', '17.5.425', '18.0.327'],
                    office=['2017', "2018", "2019", "2020"],
                    jetbrains=['2017.3.3', '2018.1', ],
                    wonderUnit=[],
                    anaconda=[], )

    pPACKAGE = dict(
        adobe=["Adobe Photoshop", "Adobe Illustrator", "Adobe Audition", "Adobe After Effects",
               "Adobe Premiere Pro", "Adobe Media Encoder", ],
        autodesk=["Autodesk Maya", "Autodesk Mudbox", "Maya", "Mudbox", "3ds Max", "AutoCAD"],
        allegorithmic=['Substance Painter', 'Substance Designer'],
        foundry=['Hiero', 'Mari', 'NukeStudio', 'NukeX', 'Katana', ],
        pixologic=['ZBrush'],
        sizefx=['Houdini FX', ],
        office=['Word', 'Excel', 'PowerPoint', 'Wordpad'],
        jetbrains=['JetBrains PyCharm', ],
        wonderUnit=['Storyboarder', 'Krita (x64)', 'Krita (x32)'],
        anaconda=['Spyder', 'QtDesigner', 'Git Bash']
    )

    windowApps = ['Sublime Text 2', 'Sublime Text 3', 'Wordpad', 'Headus UVLayout',
                  'Snipping Tool', ] + pPACKAGE['anaconda'] + pPACKAGE['office']

    TOOL_UI_KEYS = ['Calculator', 'Calendar', 'EnglishDictionary', 'FindFiles', 'ImageViewer',
                    'NoteReminder', 'ScreenShot', 'TextEditor', ]

    def __init__(self):
        super(TrackKeys, self).__init__()

        self.__dict__.update()

    def generate_key_packages(self, *info):
        keyPackage = []
        for k in self.pPACKAGE:
            for name in self.pPACKAGE[k]:
                if len(self.pVERSION[k]) == 0:
                    key = name
                    keyPackage.append(key)
                else:
                    for ver in self.pVERSION[k]:
                        if name == 'Hiero' or name == 'HieroPlayer' or name == 'NukeX':
                            key = name + " " + ver
                        else:
                            if not ver or ver == []:
                                key = name
                            else:
                                key = name + " " + ver
                        keyPackage.append(key)

        info = keyPackage + self.windowApps

        return info

    def generate_config(self, key):

        info = []

        for k in self.KEYPACKAGE:
            for t in self.pTRACK[key]:
                if t in k:
                    info.append(k)

        return list(sorted(set(info)))



















class Uis(Cfg):

    key                                 = 'Uis'
    _filePath                           = uiKeyCfg

    APP_EVENT_KEYS = ['ShowAll', 'HideAll', 'CloseAll', 'SwitchAccount', 'LogIn', 'LogOut', 'Quit',
                      'Exit', 'ChangePassword', 'UpdateAvatar', ]

    STYLESHEET_KEYS = ['bright', 'dark', 'charcoal', 'nuker', ]

    STYLE_KEYS = []

    OPEN_DIR_KEYS = ['ConfigFolder', 'IconFolder', 'SettingFolder', 'AppDataFolder',
                     'PreferenceFolder', ]

    OPEN_URL_KEYS = ['pythonTag', 'licenceTag', 'versionTag', 'PLM wiki']

    SYS_CMD_KEYS = ['Command Prompt', 'cmd', ]

    SHORTCUT_KEYS = ['Copy', 'Cut', 'Paste', 'Delete', 'Find', 'Rename']

    APP_FUNCS_KEYS = ['ReConfig', 'CleanPyc', 'Debug', 'Maximize', 'Minimize', 'Restore', ] + \
                     FACTOR_KEYS + APP_EVENT_KEYS + STYLESHEET_KEYS + STYLE_KEYS + OPEN_DIR_KEYS + \
                     OPEN_URL_KEYS + SYS_CMD_KEYS + SHORTCUT_KEYS


    UI_ELEMENT_KEYS = ['BotTab', 'ConnectStatus', 'GridLayout', 'MainMenuSection', 'MainToolBar',
                       'MainToolBarSection', 'Notification', 'StatusBar', 'TopTab', 'TopTab1',
                       'TopTab2', 'TopTab3', 'UserSetting', ]

    MAIN_UI_KEYS = ['SysTray', 'PipelineManager', 'ForgotPassword', 'SignIn', 'SignUp', 'SignOut',
                    'CommandUI', ]

    INFO_UI_KEYS = ['About', 'CodeOfConduct', 'Contributing', 'Credit', 'Version', 'AppLicence',
                    'PythonLicence', 'OrgInfo', 'References', ]

    PROJ_UI_KEYS = ['ProjectManager', 'PreProductionProj', 'ProductionProj', 'PostProductionPrj',
                    'VFXProj', 'ResearchProject', ]

    ORG_UI_KEYS = ['OrganisationManager', ]

    TASK_UI_KEYS = ['TaskManager', ]

    TEAM_UI_KEYS = ['TeamManager', ]

    DEPA_UI_KEYS = ['DepartmentManager']

    SETTING_UI_KEYS = ['Configurations', 'Preferences', 'SettingUI', 'glbSettings', 'UserSetting',
                       'BrowserSetting', 'ProjSetting', 'OrgSetting', 'TaskSetting', 'TeamSetting']

    LIBRARY_UI_KEYS = ['UserLibrary', 'HDRILibrary', 'TextureLibrary', 'AlphaLibrary', ]

    TOOL_UI_KEYS = ['Calculator', 'Calendar', 'EnglishDictionary', 'FindFiles', 'ImageViewer',
                    'NoteReminder', 'ScreenShot', 'TextEditor', ]

    PLUGIN_UI_KEY = ['PluginManager', 'NodeGraph', 'Browser', 'Messenger', 'QtDesigner']

    FORM_KEY = ['ContactUs', 'InviteFriend', 'ReportBug', ]

    APP_UI_KEYS = MAIN_UI_KEYS + INFO_UI_KEYS + PROJ_UI_KEYS + ORG_UI_KEYS + TASK_UI_KEYS + \
                  TEAM_UI_KEYS + SETTING_UI_KEYS + LIBRARY_UI_KEYS + TOOL_UI_KEYS + \
                  PLUGIN_UI_KEY + FORM_KEY

    KEYDETECT = ["Non-commercial", "Uninstall", "Verbose", "License", "Skype", ".url",
                 "Changelog", "Settings"]

    tracker = TrackKeys()

    def __init__(self):
        super(Uis, self).__init__()

        self.KEYPACKAGE         = self.tracker.generate_key_packages()

        # Toolbar _data
        self.CONFIG_TD                 = self.tracker.generate_config('TDS'),  # TD artist
        self.CONFIG_VFX                = self.tracker.generate_config('VFX'),  # VFX artist
        self.CONFIG_ART                = self.tracker.generate_config('ART'),  # 2D artist
        self.CONFIG_PRE                = self.tracker.generate_config('PRE'),  # Preproduction
        self.CONFIG_TEXTURE            = self.tracker.generate_config('TEXTURE'),  # ShadingTD artist
        self.CONFIG_POST               = self.tracker.generate_config('POST'),  # Post production

        # Tab 1 sections _data
        self.CONFIG_OFFICE             = self.tracker.generate_config('Office'),  # Paper work department
        self.CONFIG_DEV                = self.tracker.generate_config('Dev') + ['Command Prompt'],  # Rnd - Research and development
        self.CONFIG_TOOLS              = self.tracker.generate_config('Tools') + self.TOOL_UI_KEYS,  # useful/custom tools
        self.CONFIG_EXTRA              = self.tracker.generate_config('Extra'),  # Extra tools
        self.CONFIG_SYSTRAY            = self.tracker.generate_config('sysTray') + ['Exit', 'SignIn'],  # System tray tools

        self.__dict__.update()


class Clrs(Cfg):

    key                             = 'CLrs'
    _filePath                       = colorCfg




    def __init__(self):
        super(Clrs, self).__init__()

        self.__dict__.update()



# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved