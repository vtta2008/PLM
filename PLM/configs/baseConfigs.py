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
from PLM                                import ROOT, ROOT_APP, glbSettings, create_path, parent_dir
from PLM.api.Gui                        import FontDataBase
from PLM.api.Core                       import Settings
from PLM.cores.data                     import PresetDB
from .metadatas                         import (__appname__, __organizationName__, )


LOCALAPPDATA                            = os.getenv('LOCALAPPDATA')
USER_DIR                                = parent_dir(os.getenv('HOME'))

APPDATA_DAMG                            = create_path(LOCALAPPDATA, __organizationName__)
APPDATA_PLM                             = create_path(APPDATA_DAMG, __appname__)

CFG_DIR                                 = create_path(APPDATA_PLM, '.configs')
TMP_DIR                                 = create_path(APPDATA_PLM, '.tmp')
CACHE_DIR                               = create_path(APPDATA_PLM, '.cache')
PREF_DIR                                = create_path(APPDATA_PLM, 'preferences')

SETTING_DIR                             = CFG_DIR
DB_DIR                                  = APPDATA_PLM
LOG_DIR                                 = CFG_DIR

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


ks                                      = ['icon12', 'icon16', 'icon24', 'icon32', 'icon48', 'icon64', 'node', 'tag',
                                           'web16', 'web24', 'web32', 'web48', 'web64', 'web128']

ds                                      = [ICON_DIR_12, ICON_DIR_16, ICON_DIR_24, ICON_DIR_32, ICON_DIR_48, ICON_DIR_64,
                                           NODE_ICON_DIR, TAG_ICON_DIR, WEB_ICON_16, WEB_ICON_24, WEB_ICON_32,
                                           WEB_ICON_48, WEB_ICON_64, WEB_ICON_128]


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

APP_SETTING                             = create_path(SETTING_DIR, 'PLM.ini')
USER_SETTING                            = create_path(SETTING_DIR, 'user.ini')
FORMAT_SETTING                          = create_path(SETTING_DIR, 'format.ini')
UNIX_SETTING                            = create_path(SETTING_DIR, 'unix.ini')


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


class Dirs(Cfg):

    key                             = 'Dirs'
    _filePath                       = dirCfg

    CFG_DIR                         = CFG_DIR
    TMP_DIR                         = TMP_DIR
    CACHE_DIR                       = CACHE_DIR
    PREF_DIR                        = PREF_DIR

    TASK_DIR                        = create_path(CFG_DIR, 'task')
    TEAM_DIR                        = create_path(CFG_DIR, 'team')
    PRJ_DIR                         = create_path(CFG_DIR, 'project')
    ORG_DIR                         = create_path(CFG_DIR, 'organisation')
    USER_LOCAL_DATA                 = create_path(CFG_DIR, 'userLocal')

    LIBRARY_DIR                     = create_path(USER_DIR, 'UserLibraries')

    BIN_DIR                         = create_path(ROOT_APP, 'bin')

    DOCS_DIR                        = create_path(ROOT_APP, 'docs')
    RAWS_DIR                        = create_path(DOCS_DIR, 'raws')
    DOCS_READING_DIR                = create_path(DOCS_DIR, 'reading')
    TEMPLATE_DIR                    = create_path(DOCS_DIR, 'template')
    TEMPLATE_LICENSE                = create_path(TEMPLATE_DIR, 'LICENSE')

    INTERGRATIONS_DIR               = create_path(ROOT_APP, 'intergrations')
    INTERGRATE_BLENDER_DIR          = create_path(INTERGRATIONS_DIR, 'Blender')
    INTERGRATE_HOUDINI_DIR          = create_path(INTERGRATIONS_DIR, 'Houdini')
    INTERGRATE_MARI_DIR             = create_path(INTERGRATIONS_DIR, 'Mari')
    INTERGRATE_MAYA_DIR             = create_path(INTERGRATIONS_DIR, 'Maya')
    INTERGRATE_MUDBOX_DIR           = create_path(INTERGRATIONS_DIR, 'Mudbox')
    INTERGRATE_NUKE_DIR             = create_path(INTERGRATIONS_DIR, 'Nuke')
    INTERGRATE_SUBSTANCES_DIR       = create_path(INTERGRATIONS_DIR, 'Substances')
    INTERGRATE_ZBRUSH_DIR           = create_path(INTERGRATIONS_DIR, 'ZBrush')
    INTERGRATE_Others_DIR           = create_path(INTERGRATIONS_DIR, 'Others')

    API_DIR                         = create_path(ROOT, 'api')
    CORE_DIR                        = create_path(API_DIR, 'Core')
    DAMG_DIR                        = create_path(API_DIR, 'damg')
    GUI_DIR                         = create_path(API_DIR, 'Gui')
    NETWORK_DIR                     = create_path(API_DIR, 'Network')
    WIDGET_DIR                      = create_path(API_DIR, 'Widgets')

    CONFIGS_DIR                     = create_path(ROOT, 'configs')

    CORES_DIR                       = create_path(ROOT, 'cores')
    CORES_BASE_DIR                  = create_path(CORES_DIR, 'base')
    CORES_DATA_DIR                  = create_path(CORES_DIR, 'data')
    CORES_HANDLERS_DIR              = create_path(CORES_DIR, 'handlers')
    CORES_MODELS_DIR                = create_path(CORES_DIR, 'models')
    CORES_SETTINGS_DIR              = create_path(CORES_DIR, 'settings')

    LOGGER_DIR                      = create_path(ROOT, 'loggers')
    PLUGINS_DIR                     = create_path(ROOT, 'plugins')

    RESOURCES_DIR                   = create_path(ROOT, 'resources')

    AVATAR_DIR                      = create_path(RESOURCES_DIR, 'avatar')

    DESIGN_DIR                      = create_path(RESOURCES_DIR, 'design')

    FONT_DIR                        = FONT_DIR

    ICON_DIR                        = ICON_DIR

    TAG_ICON_DIR                    = TAG_ICON_DIR

    NODE_ICON_DIR                   = NODE_ICON_DIR

    WEB_ICON_DIR                    = WEB_ICON_DIR
    WEB_ICON_16                     = WEB_ICON_16
    WEB_ICON_24                     = WEB_ICON_24
    WEB_ICON_32                     = WEB_ICON_32
    WEB_ICON_48                     = WEB_ICON_48
    WEB_ICON_64                     = WEB_ICON_64
    WEB_ICON_128                    = WEB_ICON_128

    ICON_DIR_12                     = ICON_DIR_12
    ICON_DIR_16                     = ICON_DIR_16
    ICON_DIR_24                     = ICON_DIR_24
    ICON_DIR_32                     = ICON_DIR_32
    ICON_DIR_48                     = ICON_DIR_48
    ICON_DIR_64                     = ICON_DIR_64

    IMAGE_DIR                       = IMAGE_DIR

    JSON_DIR                        = create_path(RESOURCES_DIR, 'json')

    LOGO_DIR                        = LOGO_DIR
    ORG_LOGO_DIR                    = ORG_LOGO_DIR
    APP_LOGO_DIR                    = APP_LOGO_DIR

    SOUND_DIR                       = create_path(RESOURCES_DIR, 'sound')

    SCRIPTS_DIR                     = create_path(ROOT, 'scripts')
    CSS_DIR                         = create_path(SCRIPTS_DIR, 'css')
    HTML_DIR                        = create_path(SCRIPTS_DIR, 'html')
    JS_DIR                          = create_path(SCRIPTS_DIR, 'js')
    QSS_DIR                         = create_path(SCRIPTS_DIR, 'qss')

    SETTINGS_DIR                    = create_path(ROOT, 'settings')
    TYPES_DIR                       = create_path(ROOT, 'types')

    UI_DIR                          = create_path(ROOT, 'ui')
    UI_BASE_DIR                     = create_path(UI_DIR, 'base')
    UI_COMPONENTS_DIR               = create_path(UI_DIR, 'components')
    UI_LAYOUTS_DIR                  = create_path(UI_DIR, 'layouts')
    UI_MODELS_DIR                   = create_path(UI_DIR, 'models')
    UI_RCS_DIR                      = create_path(UI_DIR, 'rcs')
    UI_TOOLS_DIR                    = create_path(UI_DIR, 'tools')

    UTILS_DIR                       = create_path(ROOT, 'utils')

    TESTS_DIR                       = create_path(ROOT_APP, 'tests')

    def __init__(self):
        super(Dirs, self).__init__()

        self.__dict__.update()

        mode = 0o770
        for path in self.values():
            if not os.path.exists(path):
                head, tail = os.path.split(path)
                try:
                    original_umask = os.umask(0)
                    os.makedirs(path, mode)
                finally:
                    os.umask(original_umask)
                os.chmod(path, mode)


class Pths(Cfg):
    
    key                                     = 'Dirs'
    _filePath                               = pthCfg

    evnInfoCfg                              = create_path(CFG_DIR, 'envs.cfg')
    iconCfg                                 = iconCfg
    avatarCfg                               = create_path(CFG_DIR, 'avatars.cfg')
    logoCfg                                 = logoCfg
    webIconCfg                              = create_path(CFG_DIR, 'webIcon.cfg')
    nodeIconCfg                             = create_path(CFG_DIR, 'nodeIcons.cfg')
    imageCfg                                = create_path(CFG_DIR, 'images.cfg')
    tagCfg                                  = create_path(CFG_DIR, 'tags.cfg')
    pythonCfg                               = pythonCfg
    plmCfg                                  = plmCfg
    appsCfg                                 = appsCfg
    envVarCfg                               = create_path(CFG_DIR, 'envVar.cfg')
    dirCfg                                  = dirCfg
    pthCfg                                  = pthCfg
    deviceCfg                               = deviceCfg
    urlCfg                                  = urlCfg
    userCfg                                 = create_path(CFG_DIR, 'user.cfg')
    PLMconfig                               = create_path(CFG_DIR, 'PLM.cfg')
    sceneGraphCfg                           = create_path(CFG_DIR, 'sceneGraph.cfg')
    splashImagePth                          = create_path(IMAGE_DIR, 'splash.png')
    fontCfg                                 = fontCfg
    serverCfg                               = create_path(CFG_DIR, 'server.cfg')
    formatCfg                               = formatCfg

    settingCfg                              = settingCfg

    APP_SETTING                             = APP_SETTING
    USER_SETTING                            = USER_SETTING
    FORMAT_SETTING                          = FORMAT_SETTING
    UNIX_SETTING                            = UNIX_SETTING

    LOCAL_DB                                = create_path(DB_DIR, 'local.db')

    LOCAL_LOG                               = create_path(LOG_DIR, 'PLM.logs')

    QSS_PATH                                = create_path(QSS_DIR, 'dark.qss')

    SETTING_FILEPTH                         = dict(app=APP_SETTING, user=USER_SETTING, unix=UNIX_SETTING, format=FORMAT_SETTING, )



    def __init__(self):
        super(Pths, self).__init__()

        self.__dict__.update()

        if not os.path.exists(self.LOCAL_DB):
            PresetDB(filename=self.LOCAL_DB)


class Sts(Cfg):

    key                                 = 'Sts'
    _filePath                           = settingCfg

    APP_SETTING                         = APP_SETTING
    USER_SETTING                        = USER_SETTING
    FORMAT_SETTING                      = FORMAT_SETTING
    UNIX_SETTING                        = UNIX_SETTING

    SYS_SCOPE                           = Settings.SystemScope,
    USER_SCOPE                          = Settings.UserScope,

    INI                                 = Settings.IniFormat,
    NATIVE                              = Settings.NativeFormat,
    INVAILD                             = Settings.InvalidFormat,

    def __iter__(self):
        super(Sts, self).__iter__()

        self.__dict__.update()


class Ics(Cfg):

    key                                     = 'Ics'
    _filePath                               = iconCfg

    def __init__(self):
        super(Ics, self).__init__()

        for i in range(len(ks)):
            k = ks[i]
            d = ds[i]
            self.add(k, self.get_icons(d))

        self.__dict__.update(self)

    def get_icons(self, dir):

        for root, dirs, names in os.walk(dir, topdown=False):
            for name in names:
                self[name.split('.icon')[0]] = create_path(root, name)

        self.update()


class Apps(Cfg):

    key                                 = 'Apps'
    _filePath                           = appsCfg

    def __init__(self):
        super(Apps, self).__init__()

        shortcuts = {}
        programs = winshell.programs(common=1)

        for paths, dirs, names in os.walk(programs):
            relpath = paths[len(programs) + 1:]
            shortcuts.setdefault(relpath, []).extend([winshell.shortcut(create_path(paths, n)) for n in names])

        for relpath, lnks in sorted(shortcuts.items()):
            for lnk in lnks:
                name, _ = os.path.splitext(os.path.basename(lnk.lnk_filepath))
                self[str(name)] = lnk.path


class Pys(Cfg):

    key                             = 'Pys'
    _filePath                       = pythonCfg

    def __init__(self):
        super(Pys, self).__init__()

        self['python']              = platform.python_build()
        self['python version']      = platform.python_version()

        pths                        = [p for p in os.getenv('PATH').split(';')[0:]]
        sys.path                    = [p for p in sys.path]

        for p in pths:
            if os.path.exists(p):
                if not p in sys.path:
                    sys.path.insert(-1, p)

        for py in pkg_resources.working_set:
            self[py.project_name]   = py.version


class Urls(Cfg):

    key                             = 'Urls'
    _filePath                       = urlCfg

    website                         = "https://damgteam.com"
    homepage                        = "https://pipeline.damgteam.com"
    plmWiki                         = "https://github.com/vtta2008/PLM/wiki"

    pythonTag                       = 'https://docs.anaconda.com/anaconda/reference/release-notes/'
    licenceTag                      = 'https://github.com/vtta2008/damgteam/blob/master/LICENCE'
    versionTag                      = 'https://github.com/vtta2008/damgteam/blob/master/bin/docs/rst/version.rst'

    google                          = "https://google.com"
    googleVN                        = "https://google.com.vn"
    googleNZ                        = "https://google.co.nz"

    def __init__(self):
        super(Urls, self).__init__()

        self.__dict__.update()


class Pls(Cfg):

    key                                     = 'Pls'
    _filePath                               = plmCfg

    def __init__(self):
        super(Pls, self).__init__()

        self.__dict__.update()


class Pcs(Cfg):

    key                                     = 'Pcs'
    _filePath                               = deviceCfg

    usbCount = dvdCount = hddCount = pttCount = gpuCount = pciCount = keyboardCount = netCount = ramCount = 1
    miceCount = cpuCount = biosCount = osCount = screenCount = 1


    def __init__(self):
        super(Pcs, self).__init__()

        self.__dict__.update()


class Lgs(Cfg):

    key                         = 'Lgs'
    _filePath                   = logoCfg

    orgLogos                    = dict()
    appLogos                    = dict()

    def __init__(self):
        super(Lgs, self).__init__()

        for root, dirs, names in os.walk(ORG_LOGO_DIR, topdown=False):
            for name in names:
                self.appLogos[name.split('.png')[0]] = create_path(root, name)

        for root, dirs, names in os.walk(APP_LOGO_DIR, topdown=False):
            for name in names:
                self.appLogos[name.split('.png')[0]] = create_path(root, name)

        self.add('DAMGTEAM', self.orgLogos)
        self.add('PLM', self.appLogos)


        self.__dict__.update()


class Fnts(Cfg):

    key                             = 'Fnts'
    _filePath                       = fontCfg

    def __init__(self):
        super(Fnts, self).__init__()

        self.fontData               = FontDataBase()

        installedFont = self.update_installed_fonts()
        filePths                    = []

        for root, dirs, fontPth in os.walk(FONT_DIR, topdown=False):
            for filename in fontPth:
                filePths.append(create_path(root, filename))  # Add to file list.

        for pth in filePths:
            fontName = os.path.basename(pth).split('.')[0]
            if not fontName in installedFont:
                self.fontData.addApplicationFont(pth)

        for family in self.fontData.families():
            fontStyle               = []
            for style in self.fontData.styles(family):
                fontStyle.append(style)

            self[family] = fontStyle

        self.__dict__.update()

    def update_installed_fonts(self):
        fonts                       = []

        for family in self.fontData.families():
            for font in self.fontData.styles(family):
                fonts.append(font)

        return fonts


class Fmts(Cfg):

    key                                 = 'Fmts'
    _filePath                           = formatCfg

    LoggingFullOpt                      = "%(levelname)s: %(asctime)s %(name)s, line %(lineno)s: %(message)s",
    LoggingRelative                     = "(relativeCreated:d) (levelname): (message)",
    LoggingSimpleFmt1                   = "{asctime:[{lvelname}: :{message}",
    LoggingSimpleFmt2                   = '%(asctime)s|%(levelname)s|%(message)s|',
    LoggingDistance1                    = "%(asctime)s  %(name)-22s  %(levelname)-8s %(message)s",
    LoggingDistance2                    = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'


    DATETIME_dmyhms                     = "%d/%m/%Y %H:%M:%S",
    DATETIME_mdhm                       = "'%m-%d %H:%M'",
    DATETIME_fullOpt                    = '(%d/%m/%Y %H:%M:%S)',

    IMAGE_ext                           = "All Files (*);;Img Files (*.jpg);;Img Files (*.png)"


    def __init__(self):
        super(Fmts, self).__init__()

        self.__dict__.update()


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved