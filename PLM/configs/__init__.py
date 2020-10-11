# -*- coding: utf-8 -*-
"""

Script Name: path.py
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, winshell
from termcolor                          import cprint
from pyjavaproperties                   import Properties

# PLM
from bin                                import BIN_ROOT
from .baseConfigs                       import Cmds, Cfg, TrackKeys
from .baseScan                          import BaseScan
from PLM                                import create_path, parent_dir, ROOT, ROOT_APP, __organization__, __appName__


iconMissing                             = []
toolTips                                = {}
statusTips                              = {}



notKeys                                  = ['__name__', '__doc__', '__package__', '__loader__', '__spec__', '__file__',
                                            '__cached__', '__builtins__', 'os', '__envKey__', 'cfgdir', 'CFG_DIR',
                                            'SETTING_DIR', 'DB_DIR', 'LOG_DIR', 'QSS_DIR', 'RCS_DIR', 'SCSS_DIR',
                                            '__appname__', 'subprocess', 'unicode_literals', 'absolute_import',
                                            '__organization__']

RAM_TYPE                                = { 0: 'Unknown', 1: 'Other', 2: 'DRAM', 3: 'Synchronous DRAM', 4: 'Cache DRAM',
                                            5: 'EDO', 6: 'EDRAM', 7: 'VRAM', 8: 'SRAM', 9: 'RAM', 10: 'ROM', 11: 'Flash',
                                            12: 'EEPROM', 13: 'FEPROM', 14: 'EPROM', 15: 'CDRAM', 16: '3DRAM', 17: 'SDRAM',
                                            18: 'SGRAM', 19: 'RDRAM', 20: 'DDR', 21: 'DDR2', 22: 'DDR2 FB-DIMM', 24: 'DDR3',
                                            25: 'FBD2', }

FORM_FACTOR                             = { 0: 'Unknown', 1: 'Other', 2: 'SIP', 3: 'DIP', 4: 'ZIP', 5: 'SOJ', 6: 'Proprietary',
                                            7: 'SIMM', 8: 'DIMM', 9: 'TSOP', 10: 'PGA', 11: 'RIMM', 12: 'SODIMM', 13: 'SRIMM',
                                            14: 'SMD', 15: 'SSMP', 16: 'QFP', 17: 'TQFP', 18: 'SOIC', 19: 'LCC', 20: 'PLCC',
                                            21: 'BGA', 22: 'FPBGA', 23: 'LGA', 24: 'FB-DIMM', }

CPU_TYPE                                = { 1: 'Other', 2: 'Unknown', 3: 'Central Processor', 4: 'Math Processor', 5: 'DSP Processor',
                                            6: 'Video Processor', }

DRIVE_TYPE                              = { 0 : "Unknown", 1 : "No Root Directory", 2 : "Removable Disk", 3 : "Local Disk",
                                            4 : "Network Drive", 5 : "Compact Disc", 6 : "RAM Disk", }

DB_ATTRIBUTE_TYPE                       = { 'int_auto_increment'    : 'INTERGER PRIMARY KEY AUTOINCREMENT, ',
                                            'int_primary_key'       : 'INT PRIMARY KEY, ',
                                            'text_not_null'         : 'TEXT NOT NULL, ',
                                            'text'                  : 'TEXT, ',
                                            'bool'                  : 'BOOL, ',
                                            'varchar'               : 'VARCHAR, ',
                                            'varchar_20'            : 'VACHAR(20,)  ', }

CMD_VALUE_TYPE                          = { 'dir'                   : 'directory',
                                            'pth'                   : 'path',
                                            'url'                   : 'link',
                                            'func'                  : 'function',
                                            'cmd'                   : 'commandPrompt',
                                            'event'                 : 'PLM Event',
                                            'stylesheet'            : 'PLMstylesheet',
                                            'shortcut'              : 'shortcut',
                                            'uiKey'                 : 'PLM Layout Key', }

actionTypes                             = ['DAMGACTION', 'DAMGShowLayoutAction', 'DAMGStartFileAction',
                                           'DAMGExecutingAction', 'DAMGOpenBrowserAction', 'DAMGWIDGETACTION']
buttonTypes                             = ['DAMGBUTTON', 'DAMGTOOLBUTTON']
urlTypes                                = ['DAMGURL', 'Url', 'url']
layoutTypes                             = ['DAMGUI', 'DAMGWIDGET', ] + actionTypes

LOCALAPPDATA                            = os.getenv('LOCALAPPDATA')

APPDATA_DAMG                            = create_path(LOCALAPPDATA, __organization__)
APPDATA_PLM                             = create_path(APPDATA_DAMG, __appName__)
CFG_DIR                                 = create_path(APPDATA_PLM, '.configs')
TMP_DIR                                 = create_path(APPDATA_PLM, '.tmp')
CACHE_DIR                               = create_path(APPDATA_PLM, '.cache')
PREF_DIR                                = create_path(APPDATA_PLM, 'preferences')
SETTING_DIR                             = create_path(CFG_DIR, 'settings')
DB_DIR                                  = APPDATA_PLM
LOG_DIR                                 = CFG_DIR
TASK_DIR                                = create_path(CFG_DIR, 'task')
TEAM_DIR                                = create_path(CFG_DIR, 'team')
PRJ_DIR                                 = create_path(CFG_DIR, 'project')
ORG_DIR                                 = create_path(CFG_DIR, 'organisation')
USER_LOCAL_DATA                         = create_path(CFG_DIR, 'userLocal')

APPDATA_DAMG                            = create_path(LOCALAPPDATA, __organization__)
APPDATA_PLM                             = create_path(APPDATA_DAMG, __appName__)

USER_DIR                                = parent_dir(os.getenv('HOME'))
LIBRARY_DIR                             = create_path(APPDATA_DAMG, 'libraries')

APP_SETTING                             = create_path(SETTING_DIR, 'PLM.ini')
USER_SETTING                            = create_path(SETTING_DIR, 'user.ini')
FORMAT_SETTING                          = create_path(SETTING_DIR, 'format.ini')
UNIX_SETTING                            = create_path(SETTING_DIR, 'unix.ini')
LOCAL_LOG                               = create_path(LOG_DIR, 'PLM.logs')

BIN_DIR                                 = BIN_ROOT
BIN_BASE_DIR                            = create_path(BIN_DIR, 'base')
BIN_CORE_DIR                            = create_path(BIN_DIR, 'Core')
BIN_DAMG_DIR                            = create_path(BIN_DIR, 'damg')
BIN_GUI_DIR                             = create_path(BIN_DIR, 'Gui')
BIN_WIDGET_DIR                          = create_path(BIN_DIR, 'Widgets')
BIN_NETWORK_DIR                         = create_path(BIN_DIR, 'Network')

BIN_MODEL_DIR                           = create_path(BIN_DIR, 'models')
BIN_SETTING_DIR                         = create_path(BIN_DIR, 'settings')
BIN_VERSION_DIR                         = create_path(BIN_DIR, 'version')

BIN_DATA_DIR                            = create_path(BIN_DIR, 'data')
DESIGN_DIR                              = create_path(BIN_DATA_DIR, 'design')
FONT_DIR                                = create_path(BIN_DATA_DIR, 'fonts')
JSON_DIR                                = create_path(BIN_DATA_DIR, 'json')
LANGUAGE_DIR                            = create_path(BIN_DATA_DIR, 'language')
PROFILE_DIR                             = create_path(BIN_DATA_DIR, 'profile')

RESOURCES_DIR                           = create_path(BIN_DATA_DIR, 'resources')

AVATAR_DIR                              = create_path(RESOURCES_DIR, 'avatar')
ICON_DIR                                = create_path(RESOURCES_DIR, 'icons')

NODE_ICON_DIR                           = create_path(ICON_DIR, 'nodes')
TAG_ICON_DIR                            = create_path(ICON_DIR, 'tags')
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

SCRIPTS_DIR                             = create_path(BIN_DATA_DIR, 'scripts')

CSS_DIR                                 = create_path(SCRIPTS_DIR, 'css')
HTML_DIR                                = create_path(SCRIPTS_DIR, 'html')
JS_DIR                                  = create_path(SCRIPTS_DIR, 'js')
QSS_DIR                                 = create_path(SCRIPTS_DIR, 'qss')

SOUND_DIR                               = create_path(BIN_DATA_DIR, 'sound')

DOCS_DIR                                = create_path(ROOT_APP, 'docs')
RAWS_DIR                                = create_path(DOCS_DIR, 'raws')
DOCS_READING_DIR                        = create_path(DOCS_DIR, 'reading')
TEMPLATE_DIR                            = create_path(DOCS_DIR, 'template')
TEMPLATE_LICENSE                        = create_path(TEMPLATE_DIR, 'LICENSE')

API_DIR                                 = create_path(ROOT, 'api')
PLM_CFG_DIR                             = create_path(ROOT, 'configs')

CORES_DIR                               = create_path(ROOT, 'cores')
CORES_BASE_DIR                          = create_path(CORES_DIR, 'base')
CORES_DATA_DIR                          = create_path(CORES_DIR, 'data')
CORES_HANDLERS_DIR                      = create_path(CORES_DIR, 'handlers')
CORES_MODELS_DIR                        = create_path(CORES_DIR, 'models')

LOGGER_DIR                              = create_path(ROOT, 'loggers')
PLUGINS_DIR                             = create_path(ROOT, 'plugins')

UI_DIR                                  = create_path(ROOT, 'ui')
UI_BASE_DIR                             = create_path(UI_DIR, 'base')
UI_COMPONENTS_DIR                       = create_path(UI_DIR, 'components')
UI_LAYOUTS_DIR                          = create_path(UI_DIR, 'layouts')
UI_MODELS_DIR                           = create_path(UI_DIR, 'models')
UI_RCS_DIR                              = create_path(UI_DIR, 'rcs')
UI_TOOLS_DIR                            = create_path(UI_DIR, 'tools')

UTILS_DIR                               = create_path(ROOT, 'utils')
TESTS_DIR                               = create_path(ROOT_APP, 'tests')

HUB_DIR                                 = create_path(ROOT_APP, 'ToolHub')
BLENDER_DIR                             = create_path(HUB_DIR, 'Blender')
HOUDINI_DIR                             = create_path(HUB_DIR, 'Houdini')
MARI_DIR                                = create_path(HUB_DIR, 'Mari')
MAYA_DIR                                = create_path(HUB_DIR, 'Maya')
MUDBOX_DIR                              = create_path(HUB_DIR, 'Mudbox')
NUKE_DIR                                = create_path(HUB_DIR, 'Nuke')
SUBSTANCES_DIR                          = create_path(HUB_DIR, 'Substances')
ZBRUSH_DIR                              = create_path(HUB_DIR, 'ZBrush')

iconCfg                                 = create_path(CFG_DIR, 'icons.cfg')
avatarCfg                               = create_path(CFG_DIR, 'avatars.cfg')
webIconCfg                              = create_path(CFG_DIR, 'webIcon.cfg')
nodeIconCfg                             = create_path(CFG_DIR, 'nodeIcons.cfg')
imageCfg                                = create_path(CFG_DIR, 'images.cfg')
tagCfg                                  = create_path(CFG_DIR, 'tags.cfg')
userCfg                                 = create_path(CFG_DIR, 'user.cfg')
plmCfg                                  = create_path(CFG_DIR, 'PLM.cfg')
sceneGraphCfg                           = create_path(CFG_DIR, 'sceneGraph.cfg')
splashImagePth                          = create_path(IMAGE_DIR, 'splash.png')
serverCfg                               = create_path(CFG_DIR, 'server.cfg')
cfgFilePths                             = create_path(CFG_DIR, 'cfgFile.cfg')

LOCAL_DB                                = create_path(DB_DIR, 'local.db')

ks                                      = ['icon12', 'icon16', 'icon24', 'icon32', 'icon48', 'icon64', 'node', 'tag',
                                           'web16', 'web24', 'web32', 'web48', 'web64', 'web128']

ds                                      = [ICON_DIR_12, ICON_DIR_16, ICON_DIR_24, ICON_DIR_32, ICON_DIR_48, ICON_DIR_64,
                                           NODE_ICON_DIR, TAG_ICON_DIR, WEB_ICON_16, WEB_ICON_24, WEB_ICON_32,
                                           WEB_ICON_48, WEB_ICON_64, WEB_ICON_128]

IMAGE_ext                               = "All Files (*);;Img Files (*.jpg);;Img Files (*.png)"

factors                                 = ['Organisation', 'Project', 'Department', 'Team', 'Task', ]
factorActs                              = ['New', 'Config', 'Edit', 'Remove']

FACTOR_KEYS                             = []

for f in factors:
    FACTOR_KEYS.append(f)
    for act in factorActs:
        FACTOR_KEYS.append('{0} {1}'.format(act, f))


# -------------------------------------------------------------------------------------------------------------
""" Config qssPths from text file """


def read_file(fileName):

    filePth = create_path(RAWS_DIR, fileName)

    if os.path.exists(filePth):
        with open(filePth) as f:
            data = f.read()
        return data
    else:
        cprint("PathNotExistsed: {0}".format(filePth), 'red', attrs=['blink'])

ABOUT                               = read_file('ABOUT')
CODEOFCONDUCT                       = read_file('CODEOFCONDUCT')
CONTRIBUTING                        = read_file('CONTRIBUTING')
COPYRIGHT                           = read_file('COPYRIGHT')
CREDIT                              = read_file('CREDIT')
LICENCE                             = read_file('LICENSE')
LINKS                               = read_file('LINKS')
QUESTIONS                           = read_file('QUESTION')
VERSION                             = read_file('VERSION')
REFERENCES                          = read_file('REFERENCES')

propText                            = Properties()
propText.load(open(create_path(BIN_DIR, 'text.properties')))

a = [APP_SETTING, USER_SETTING, FORMAT_SETTING, UNIX_SETTING, LOCAL_LOG]

appDataSpot = [APPDATA_DAMG, APPDATA_PLM, CFG_DIR, TMP_DIR, CACHE_DIR, PREF_DIR, SETTING_DIR, DB_DIR,
               LOG_DIR, TASK_DIR, TEAM_DIR, PRJ_DIR, ORG_DIR, USER_LOCAL_DATA, LIBRARY_DIR]

binSpot = [BIN_DIR, BIN_BASE_DIR, BIN_CORE_DIR, BIN_DAMG_DIR, BIN_GUI_DIR, BIN_WIDGET_DIR,
           BIN_NETWORK_DIR, BIN_MODEL_DIR, BIN_SETTING_DIR, BIN_VERSION_DIR, BIN_DATA_DIR, DESIGN_DIR,
           FONT_DIR, JSON_DIR, LANGUAGE_DIR, PROFILE_DIR, RESOURCES_DIR, ]

iconSpot = [AVATAR_DIR, ICON_DIR, NODE_ICON_DIR, TAG_ICON_DIR, WEB_ICON_DIR, WEB_ICON_16, WEB_ICON_24,
            WEB_ICON_32, WEB_ICON_48, WEB_ICON_64, WEB_ICON_128, ICON_DIR_12, ICON_DIR_16, ICON_DIR_24,
            ICON_DIR_32, ICON_DIR_48, ICON_DIR_64, IMAGE_DIR, LOGO_DIR, ORG_LOGO_DIR, APP_LOGO_DIR, ]

docSpot = [SCRIPTS_DIR, CSS_DIR, HTML_DIR, JS_DIR, QSS_DIR, SOUND_DIR, DOCS_DIR, RAWS_DIR,
           DOCS_READING_DIR, TEMPLATE_DIR, TEMPLATE_LICENSE, ]

plmSpot = [API_DIR, PLM_CFG_DIR, CORES_DIR, CORES_BASE_DIR, CORES_DATA_DIR, CORES_HANDLERS_DIR,
           CORES_MODELS_DIR, LOGGER_DIR, PLUGINS_DIR, UI_DIR, UI_BASE_DIR, UI_COMPONENTS_DIR,
           UI_LAYOUTS_DIR, UI_MODELS_DIR, UI_RCS_DIR, UI_TOOLS_DIR, UTILS_DIR, TESTS_DIR, ]

hookSpot = [HUB_DIR, BLENDER_DIR, HOUDINI_DIR, MARI_DIR, MAYA_DIR, MUDBOX_DIR, NUKE_DIR, SUBSTANCES_DIR,
            ZBRUSH_DIR]


class DirScanner(BaseScan):

    key = 'DirScanner'

    alldirs = appDataSpot + iconSpot + docSpot + plmSpot + hookSpot


    def __init__(self, parent=None):
        super(DirScanner, self).__init__(parent)

    def timelog(self, info, **kwargs):
        pass


class PthScanner(BaseScan):

    key = 'PthScanner'

    def __init__(self, parent=None):
        super(PthScanner, self).__init__(parent)


    def timelog(self, info, **kwargs):
        pass


class CfgUrls(Cfg):

    key                             = 'ConfigUrl'

    def __init__(self):
        Cfg.__init__(self)

        self.add('homepage'         , "https://pipeline.damgteam.com")
        self.add('python'           , 'https://docs.anaconda.com/anaconda/reference/release-notes/')
        self.add('licence'          , 'https://github.com/vtta2008/damgteam/blob/master/LICENCE')
        self.add('version'          , 'https://github.com/vtta2008/damgteam/blob/master/bin/docs/rst/version.rst')
        self.add('PLM wiki'         , "https://github.com/vtta2008/PipelineTool/wiki")


class CfgApps(Cfg):

    key                         = 'CfgApps'

    def __init__(self):
        super(CfgApps, self).__init__()

        shortcuts = {}
        programs = winshell.programs(common=1)

        for paths, dirs, names in os.walk(programs):
            relpath = paths[len(programs) + 1:]
            shortcuts.setdefault(relpath, []).extend([winshell.shortcut(create_path(paths, n)) for n in names])

        for relpath, lnks in sorted(shortcuts.items()):
            for lnk in lnks:
                name, _ = os.path.splitext(os.path.basename(lnk.lnk_filepath))
                self[str(name)] = lnk.path


class CfgIcons(Cfg):

    key                                 = 'CfgIcons'

    def __init__(self):
        super(CfgIcons, self).__init__()

        for i in range(len(ks)):
            k = ks[i]
            d = ds[i]
            self.add(k, self.get_icons(d))

    def get_icons(self, dir):
        icons = dict()

        for root, dirs, names in os.walk(dir, topdown=False):
            for name in names:
                if '.icon.png' in name:
                    icons[name.split('.icon')[0]] = os.path.join(root, name).replace('\\', '/')
                elif '.tag.png' in name:
                    icons[name.split('.tag')[0]] = os.path.join(root, name).replace('\\', '/')
                else:
                    icons[name.split('.png')[0]] = os.path.join(root, name).replace('\\', '/')

        return icons


class ConfigUiKeys(Cfg):

    key                 = 'ConfigUiKeys'

    APP_EVENT_KEYS      = [ 'ShowAll', 'HideAll', 'CloseAll', 'SwitchAccount', 'LogIn', 'LogOut', 'Quit', 'Exit',
                            'ChangePassword', 'UpdateAvatar', ]

    STYLESHEET_KEYS     = ['bright', 'dark', 'charcoal', 'nuker', ]
    STYLE_KEYS          = []
    OPEN_DIR_KEYS       = ['ConfigFolder', 'IconFolder', 'SettingFolder', 'AppDataFolder', 'PreferenceFolder', ]
    OPEN_URL_KEYS       = ['python', 'licence', 'version', 'PLM wiki']
    SYS_CMD_KEYS        = ['Command Prompt', 'cmd', ]
    SHORTCUT_KEYS       = ['Copy', 'Cut', 'Paste', 'Delete', 'Find', 'Rename']

    APP_FUNCS_KEYS      = ['ReConfig', 'CleanPyc', 'Debug', 'Maximize', 'Minimize', 'Restore', ] + FACTOR_KEYS + \
                          APP_EVENT_KEYS + STYLESHEET_KEYS + STYLE_KEYS + OPEN_DIR_KEYS + OPEN_URL_KEYS + SYS_CMD_KEYS + \
                          SHORTCUT_KEYS

    UI_ELEMENT_KEYS     = ['BotTab', 'ConnectStatus', 'GridLayout', 'MainMenuSection', 'MainToolBar', 'MainToolBarSection',
                           'Notification', 'StatusBar', 'TopTab', 'TopTab1', 'TopTab2', 'TopTab3', 'UserSetting', ]
    MAIN_UI_KEYS        = ['SysTray', 'PipelineManager', 'ForgotPassword', 'SignIn', 'SignUp', 'SignOut', 'CommandUI', ]
    INFO_UI_KEYS        = ['About', 'CodeOfConduct', 'Contributing', 'Credit', 'Version', 'AppLicence', 'PythonLicence',
                           'OrgInfo', 'References', ]
    PROJ_UI_KEYS        = ['ProjectManager', 'PreProductionProj', 'ProductionProj', 'PostProductionPrj', 'VFXProj',
                           'ResearchProject', ]

    ORG_UI_KEYS         = ['OrganisationManager', ]
    TASK_UI_KEYS        = ['TaskManager', ]
    TEAM_UI_KEYS        = ['TeamManager', ]

    SETTING_UI_KEYS     = ['Configurations', 'Preferences', 'SettingUI', 'glbSettings', 'UserSetting', 'BrowserSetting',
                           'ProjSetting', 'OrgSetting', 'TaskSetting', 'TeamSetting']
    LIBRARY_UI_KEYS     = ['UserLibrary', 'HDRILibrary', 'TextureLibrary', 'AlphaLibrary', ]
    TOOL_UI_KEYS        = ['Calculator', 'Calendar', 'EnglishDictionary', 'FindFiles', 'ImageViewer', 'NoteReminder',
                           'ScreenShot', 'TextEditor', ]
    PLUGIN_UI_KEY       = ['PluginManager', 'NodeGraph', 'Browser', 'Messenger', 'QtDesigner']
    FORM_KEY            = ['ContactUs', 'InviteFriend', 'ReportBug', ]
    KEYDETECT           = ["Non-commercial", "Uninstall", "Verbose", "License", "Skype", ".url", "Changelog", "Settings"]

    APP_UI_KEYS         = MAIN_UI_KEYS + INFO_UI_KEYS + PROJ_UI_KEYS + ORG_UI_KEYS + TASK_UI_KEYS + TEAM_UI_KEYS + \
                          SETTING_UI_KEYS + LIBRARY_UI_KEYS + TOOL_UI_KEYS + PLUGIN_UI_KEY + FORM_KEY

    tracker             = TrackKeys()

    def __init__(self):
        super(ConfigUiKeys, self).__init__()

        self.KEYPACKAGE = self.tracker.generate_key_packages()

        # Toolbar _data
        self.CONFIG_TDS     = self.tracker.generate_config('TDS')                               # TD & animators
        self.CONFIG_VFX     = self.tracker.generate_config('VFX')                               # VFX
        self.CONFIG_ART     = self.tracker.generate_config('ART')                               # 2D
        self.CONFIG_PRE     = self.tracker.generate_config('PRE')                               # Preproduction
        self.CONFIG_TEX     = self.tracker.generate_config('TEXTURE')                           # ShadingTD
        self.CONFIG_POST    = self.tracker.generate_config('POST')                              # Post production

        # Tab 1 sections _data
        self.CONFIG_OFFICE  = self.tracker.generate_config('Office')                            # Office
        self.CONFIG_DEV     = self.tracker.generate_config('Dev') + ['Command Prompt']          # Rnd
        self.CONFIG_TOOLS   = self.tracker.generate_config('Tools') + self.TOOL_UI_KEYS         # useful/custom tools
        self.CONFIG_EXTRA   = self.tracker.generate_config('Extra')                             # Extra tools
        self.CONFIG_SYSTRAY = self.tracker.generate_config('sysTray') + ['Exit', 'SignIn']      # System tray tools

        self.__dict__.update()


class CfgFiles(Cfg):

    key = 'CfgFiles'

    def __init__(self):
        super(CfgFiles, self).__init__()

        ks = ['avatar', 'webIcon', 'nodeIcon', 'image', 'tag', 'user', 'PLM', 'sceneGraph', 'splash', 'server', 'icon',
              'file', 'localDB']
        vs = [iconCfg, avatarCfg, webIconCfg, nodeIconCfg, imageCfg, tagCfg, userCfg, plmCfg, sceneGraphCfg,
              splashImagePth, serverCfg, cfgFilePths, LOCAL_DB]

        for i in range(len(ks)):
            self.add(ks[i], vs[i])


class ConfigPipeline(Cfg):

    key                         = 'ConfigPipeline'

    appInfo                     = CfgApps()
    uiKeyInfo                   = ConfigUiKeys()
    iconInfo                    = CfgIcons()
    urlInfo                     = CfgUrls()
    dirInfo                     = {'ConfigFolder': CFG_DIR, 'IconFolder': ICON_DIR, 'SettingFolder': SETTING_DIR,
                                    'AppDataFolder': APPDATA_PLM, 'PreferenceFolder': PREF_DIR, }

    scanDir                     = DirScanner()
    scanPth                     = PthScanner()

    def __init__(self):
        super(ConfigPipeline, self).__init__()

        self.scanDir.scanAndFix()

        removeKeys              = []
        launchAppKeys           = []

        KEYDETECT               = self.uiKeyInfo.KEYDETECT
        KEYPACKAGE              = self.uiKeyInfo.KEYPACKAGE
        OPEN_URL_KEYS           = self.uiKeyInfo.OPEN_URL_KEYS
        SYS_CMD_KEYS            = self.uiKeyInfo.SYS_CMD_KEYS
        OPEN_DIR_KEYS           = self.uiKeyInfo.OPEN_DIR_KEYS
        APP_EVENT_KEYS          = self.uiKeyInfo.APP_EVENT_KEYS
        STYLESHEET_KEYS         = self.uiKeyInfo.STYLESHEET_KEYS
        SHORTCUT_KEYS           = self.uiKeyInfo.SHORTCUT_KEYS

        functionKeys            = self.uiKeyInfo.APP_FUNCS_KEYS
        layoutKeys              = self.uiKeyInfo.APP_UI_KEYS


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
            self.appInfo.removeKey(k)

        self.appInfo.update()

        for k in KEYPACKAGE:
            for key in self.appInfo.keys():
                if k in key:
                    launchAppKeys.append(key)

        qtDesigner = create_path(os.getenv('PROGRAMDATA'), 'Anaconda3', 'Library', 'bin', 'designer.exe')
        davinciPth = create_path(os.getenv('PROGRAMFILES'), 'Blackmagic Design', 'DaVinci Resolve', 'resolve.exe')

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
            self.add(key, Cmds(key, icon, tooltip, statustip, value, valueType, arg, code))

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
            self.add(key, Cmds(key, icon, tooltip, statustip, value, valueType, arg, code))

        for key in layoutKeys:
            if not key in launchAppKeys:
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
                self.add(key, Cmds(key, icon, tooltip, statustip, value, valueType, arg, code))




# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 10:45 PM
# Pipeline manager - DAMGteam
