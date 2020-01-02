# -*- coding: utf-8 -*-
"""

Script Name: _data.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from __buildtins__ import ROOT, globalSetting
from functools import partial

""" Import """

# Python
import os, sys, platform, subprocess, json, shutil, pkg_resources, requests, uuid, socket, pprint, wmi, winshell
from platform import system

PIPE = subprocess.PIPE
STDOUT = subprocess.STDOUT

from .dirs                          import (APPDATA_DAMG, APPDATA_PLM, CFG_DIR, TMP_DIR, SETTING_DIR, LOG_DIR, PREF_DIR,
                                            TASK_DIR, TEAM_DIR, ORG_DIR, APP_DATA_DIR, DB_DIR, ASSETS_DIR, AVATAR_DIR,
                                            FONT_DIR, IMAGE_DIR, LOGO_DIR, DAMG_LOGO_DIR, PLM_LOGO_DIR, PIC_DIR, STYLE_DIR,
                                            STYLE_IMAGE_DIR, STYLE_RC_DIR, STYLE_SVG_DIR, BIN_DIR, DATA_DIR, JSON_DIR,
                                            DEPENDANCIES_DIR, DOCS_DIR, RST_DIR, TXT_DIR, RAWS_DATA_DIR, TEMPLATE_DIR,
                                            TEMPLATE_LICENCE, RCS_DIR, CSS_DIR, HTML_DIR, JS_DIR, QSS_DIR,
                                            BUILD_DIR, CORES_DIR, CORES_ASSETS_DIR, CORES_BASE_DIR, DEVKIT_DIR,
                                            DEVKIT_CORE, DEVKIT_GUI, DEVKIT_WIDGET, HOOK_DIR, MAYA_DIR, MARI_DIR,
                                            NUKE_DIR, ZBRUSH_DIR, HOUDINI_DIR, ICON_DIR, TAG_ICON_DIR, MAYA_ICON_DIR,
                                            NODE_ICON_DIR, WEB_ICON_DIR, WEB_ICON_16, WEB_ICON_24, WEB_ICON_32,
                                            WEB_ICON_48, WEB_ICON_64, WEB_ICON_128, ICON_DIR_12, ICON_DIR_16,
                                            ICON_DIR_24, ICON_DIR_32, ICON_DIR_48, ICON_DIR_64, LIB_DIR, SOUND_DIR,
                                            MODULE_DIR, PLUGIN_DIR, NODEGRAPH_DIR, SCRIPT_DIR, TEST_DIR, UI_DIR,
                                            UI_BASE_DIR, UI_ASSET_DIR, BODY_DIR, TABS_DIR, FOOTER_DIR, HEADER_DIR,
                                            SUBUI_DIR, FUNCS_DIR, PRJ_DIR, SETTINGS_DIR, TOOLS_DIR, UTILS_DIR)

from .pths                          import (evnInfoCfg, iconCfg, avatarCfg, logoCfg, mayaCfg, webIconCfg, nodeIconCfg,
                                            picCfg, tagCfg, pythonCfg, plmCfg, appsCfg, envVarCfg, dirCfg, pthCfg,
                                            deviceCfg, userCfg, PLMconfig, sceneGraphCfg, APP_SETTING, USER_SETTING,
                                            FORMAT_SETTING, UNIX_SETTING, LOCAL_DB, LOCAL_LOG, QSS_PATH, MAIN_SCSS_PTH,
                                            STYLE_SCSS_PTH, VAR_SCSS_PTH, SETTING_FILEPTH)

from .types                         import (RAMTYPE, CPUTYPE, FORMFACTOR, DRIVETYPE, DB_ATTRIBUTE_TYPE, CMD_VALUE_TYPE, actionTypes,
                                            layoutTypes)

from .text                          import (TRADE_MARK, PLM_ABOUT, WAIT_FOR_UPDATE, WAIT_TO_COMPLETE, WAIT_LAYOUT_COMPLETE,
                                            PASSWORD_FORGOTTON, SIGNUP, DISALLOW, TIT_BLANK, PW_BLANK, PW_WRONG,
                                            PW_UNMATCH, PW_CHANGED, FN_BLANK, LN_BLANK, SEC_BLANK, USER_CHECK_REQUIRED,
                                            USER_NOT_CHECK, USER_BLANK, USER_CHECK_FAIL, USER_NOT_EXSIST, USER_CONDITION,
                                            SYSTRAY_UNAVAI, PTH_NOT_EXSIST, ERROR_OPENFILE, ERROR_QIMAGE, tooltips_present,
                                            tooltips_missing, N_MESSAGES_TEXT, SERVER_CONNECT_FAIL, TEMPLATE_QRC_HEADER,
                                            TEMPLATE_QRC_FILE, TEMPLATE_QRC_FOOTER, HEADER_SCSS, HEADER_QSS)

from .keys                          import (TRACK_TDS, TRACK_VFX, TRACK_ART, TRACK_PRE, TRACK_TEX, TRACK_POST,
                                            TRACK_OFFICE, TRACK_DEV, TRACK_TOOLS, TRACK_EXTRA, TRACK_SYSTRAY,
                                            KEYDETECT, FIX_KEY, APP_UI_KEYS, KEYPACKAGE, CONFIG_TDS, CONFIG_VFX,
                                            CONFIG_ART, CONFIG_PRE, CONFIG_TEX, CONFIG_POST, CONFIG_OFFICE, CONFIG_DEV,
                                            CONFIG_TOOLS, CONFIG_EXTRA, CONFIG_SYSTRAY, ACTIONS_DATA, SHOWLAYOUT_KEY,
                                            RESTORE_KEY, SHOWMAX_KEY, SHOWMIN_KEY,
                                            START_FILE, SHORTCUT_KEYS, START_FILE_KEY, EXECUTING_KEY, IGNORE_ICON_NAME,
                                            QT_BINDINGS, QT_ABSTRACTIONS, QT5_IMPORT_API, QT_API_VALUES, QT_LIB_VALUES,
                                            QT_BINDING, QT_ABSTRACTION, IMAGE_BLACKLIST, PY2, SYS_OPTS, APP_FUNCS_KEYS,
                                            APP_EVENT_KEYS, STYLESHEET_KEYS, OPEN_URL_KEYS, OPEN_DIR_KEYS, SYS_CMD_KEYS,
                                            notKeys, autodeskVer, )

from .formats                       import (INI, Native, Invalid, LOG_FORMAT, DT_FORMAT, ST_FORMAT, datetTimeStamp,
                                            IMGEXT, )
from .options                       import *

from .device                        import ConfigMachine

from bin                            import DAMGDICT

from .metadatas                     import (__plmWiki__, __localServer__, __pkgsReq__, __homepage__, __appname__,
                                            __organization__, __organizationID__, __organizationName__, __globalServer__,
                                            __google__, __plmSlogan__, __localServerAutho__, __version__, __website__,
                                            VERSION, )

iconMissing                         = []
toolTips                            = {}
statusTips                          = {}


class CommandData(DAMGDICT):
    key = 'CommandData'

    def __init__(self, key=None, icon=None, tooltip=None, statustip=None,
                       value=None, valueType=None, arg=None, code=None):
        super(CommandData, self).__init__()

        self.key = key
        self.icon = icon
        self.tooltip = tooltip
        self.statusTip = statustip
        self.value = value
        self.valueType = valueType
        self.arg = arg
        self.code = code

        ks = ['key', 'icon', 'tooltip', 'statustip', 'value', 'valueType', 'arg', 'code']
        vs = [key, icon, tooltip, statustip, value, valueType, arg, code]

        for i in range(len(ks)):
            self[ks[i]] = vs[i]


# -------------------------------------------------------------------------------------------------------------
""" Configs """

class ConfigPython(DAMGDICT):

    key                 = 'ConfigPython'

    def __init__(self):
        super(ConfigPython, self).__init__()

        self['python'] = platform.python_build()
        self['python version'] = platform.python_version()

        pths = [p.replace('\\', '/') for p in os.getenv('PATH').split(';')[0:]]
        sys.path = [p.replace('\\', '/') for p in sys.path]

        for p in pths:
            if os.path.exists(p):
                if not p in sys.path:
                    sys.path.insert(-1, p)

        for py in pkg_resources.working_set:
            self[py.project_name] = py.version

        # pprint.pprint(self)


class ConfigDirectory(DAMGDICT):

    key                                 = 'ConfigDirectory'

    def __init__(self):
        super(ConfigDirectory, self).__init__()
        from . import dirs
        keys                            = [k for k in vars(dirs).keys() if not k in notKeys]
        for k in keys:
            self[k]                     = vars(dirs)[k]

        mode = 0o770
        for path in self.values():
            if not os.path.exists(path):
                (head, tail) = os.path.split(path)
                try:
                    original_umask = os.umask(0)
                    os.makedirs(path, mode)
                finally:
                    os.umask(original_umask)
                os.chmod(path, mode)

        self.add('ConfigDir', CFG_DIR)
        self.add('IconDir', ICON_DIR)
        self.add('SettingDir', SETTING_DIR)
        self.add('AppdataDir', APP_DATA_DIR)
        self.add('PreferenceDir', PREF_DIR)


class ConfigPath(DAMGDICT):

    key                                = 'ConfigPath'

    def __init__(self):
        super(ConfigPath, self).__init__()
        from . import pths
        keys                            = [k for k in vars(pths).keys() if not k in notKeys]
        for k in keys:
            self[k]                     = vars(pths)[k]

        # pprint.pprint(self)


class ConfigEnvVar(DAMGDICT):

    key                                 = 'ConfigEnvVar'

    def __init__(self):
        super(ConfigEnvVar, self).__init__()
        for k, v in os.environ.items():
            self[k]                     = v.replace('\\', '/')
        # pprint.pprint(self)

    def update(self):
        for k, v in os.environ.items():
            self[k]                     = v.replace('\\', '/')


class ConfigAvatar(DAMGDICT):

    key                                 = 'ConfigAvatar'

    def __init__(self):
        super(ConfigAvatar, self).__init__()

        for root, dirs, names in os.walk(AVATAR_DIR, topdown=False):
            for name in names:
                self[name.split('.avatar')[0]] = os.path.join(root, name).replace('\\', '/')

        # pprint.pprint(self)


class ConfigLogo(DAMGDICT):

    key                                 = 'ConfigLogo'

    def __init__(self):
        super(ConfigLogo, self).__init__()

        damgLogos                       = DAMGDICT()
        plmLogos                        = DAMGDICT()

        for root, dirs, names in os.walk(DAMG_LOGO_DIR, topdown=False):
            for name in names:
                damgLogos[name.split('.png')[0]] = os.path.join(root, name).replace('\\', '/')

        for root, dirs, names in os.walk(PLM_LOGO_DIR, topdown=False):
            for name in names:
                plmLogos[name.split('.png')[0]] = os.path.join(root, name).replace('\\', '/')

        self['DAMGTEAM']                = damgLogos
        self['PLM']                     = plmLogos

        # pprint.pprint(self)


class ConfigPics(DAMGDICT):

    key                                 = 'ConfigPics'

    def __init__(self):
        super(ConfigPics, self).__init__()

        for root, dirs, names, in os.walk(PIC_DIR, topdown=False):
            for name in names:
                self[name.split('.node')[0]] = os.path.join(root, name).replace('\\', '/')

        # pprint.pprint(self)


class ConfigIcon(DAMGDICT):

    key                                 = 'ConfigIcon'

    def __init__(self):
        super(ConfigIcon, self).__init__()

        self['icon12'] = self.get_icons(ICON_DIR_12)
        self['icon16'] = self.get_icons(ICON_DIR_16)
        self['icon24'] = self.get_icons(ICON_DIR_24)
        self['icon32'] = self.get_icons(ICON_DIR_32)
        self['icon48'] = self.get_icons(ICON_DIR_48)
        self['icon64'] = self.get_icons(ICON_DIR_64)

        self['maya']   = self.get_icons(MAYA_ICON_DIR)

        self['node']   = self.get_icons(NODE_ICON_DIR)

        self['tag']    = self.get_icons(TAG_ICON_DIR)

        self['web32']  = self.get_icons(WEB_ICON_32)
        self['web128'] = self.get_icons(WEB_ICON_128)

        self['avatar'] = ConfigAvatar()
        self['logo']   = ConfigLogo()
        self['pic']    = ConfigPics()

        missingKey = ['ForgotPassword', 'PLMBrowser', 'Messenger', 'InviteFriend', 'SignOut', 'SwitchAccount']

        for k in missingKey:
            self['icon32'].add(k, '{0}.icon.png'.format(k))

        # pprint.pprint(self)

    def get_icons(self, dir):
        icons = DAMGDICT()
        for root, dirs, names in os.walk(dir, topdown=False):
            for name in names:
                icons[name.split('.icon')[0]] = os.path.join(root, name).replace('\\', '/')
        return icons


class ConfigMaya(DAMGDICT):

    key                                 = 'ConfigMaya'

    def __init__(self):
        super(ConfigMaya, self).__init__()
        modules = ['anim', 'lib', 'modeling', 'rendering', 'simulating', 'surfacing']
        modulePth = os.path.join(MAYA_DIR, 'modules')
        paths = [os.path.join(modulePth, m) for m in modules]
        sys.path.insert(-1, ';'.join(paths))

        usScr = os.path.join(MAYA_DIR, 'userSetup.py')

        if os.path.exists(usScr):
            mayaVers = [os.path.join(MAYA_DIR, v) for v in autodeskVer if os.path.exists(os.path.join(MAYA_DIR, v))] or []
            if not len(mayaVers) == 0 or not mayaVers == []:
                for usDes in mayaVers:
                    shutil.copy(usScr, usDes)


class ConfigApps(DAMGDICT):

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


class ConfigUrl(DAMGDICT):

    key = 'ConfigUrl'

    def __init__(self):
        super(ConfigUrl, self).__init__()

        self.add('pythonTag', 'https://docs.anaconda.com/anaconda/reference/release-notes/')
        self.add('licenceTag', 'https://github.com/vtta2008/damgteam/blob/master/LICENCE')
        self.add('versionTag', 'https://github.com/vtta2008/damgteam/blob/master/appData/documentations/version.rst')
        self.add('PLM wiki', __plmWiki__)


class ConfigPipeline(DAMGDICT):

    key                         = 'ConfigPipeline'

    def __init__(self, iconInfo, appInfo, urlInfo, dirInfo):
        super(ConfigPipeline, self).__init__()

        self.iconInfo           = iconInfo
        self.appInfo            = appInfo
        self.urlInfo            = urlInfo
        self.dirInfo            = dirInfo

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

        for key in eKeys:
            if os.path.exists(eVal[eKeys.index(key)]):
                for k in self.appInfo.keys():
                    if key in k:
                        self.appInfo[k] = eVal[eKeys.index(key)]
                        launchAppKeys.append(k)

        self.appInfo.update()

        for key in launchAppKeys:
            try:
                icon = self.iconInfo['icon32'][key]
            except KeyError:
                icon = 'Icon Missing: {0}'.format(key)
                print('Icon Missing: {0}'.format(key))
                iconMissing.append(key)
            finally:
                toolTips[key] = 'Lauch {0}'.format(key)
                statusTips[key] = 'Lauch {0}: {1}'.format(key, self.appInfo[key])
                value = self.appInfo[key]
                valueType = CMD_VALUE_TYPE['pth']
                arg = value
                code = partial(os.startfile, arg)

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
                    icon = 'Icon Missing: {0}'.format(key)
                    print('Icon Missing: {0}'.format(key))
                    iconMissing.append(key)
            finally:
                if key in OPEN_URL_KEYS:
                    toolTips[key] = 'Go to {0} website'.format(key)
                    statusTips[key] = 'Open URL: {0}'.format(self.urlInfo[key])
                    value = self.urlInfo[key]
                    valueType = CMD_VALUE_TYPE['url']
                    arg = value
                    code = 'OpenUrl'
                elif key in SYS_CMD_KEYS:
                    toolTips[key] = 'Open command prompt'
                    statusTips[key] = 'Open command prompt'
                    value = 'start /wait cmd'
                    valueType = CMD_VALUE_TYPE['cmd']
                    arg = value
                    code = partial(os.system, 'start /wait cmd')
                elif key in OPEN_DIR_KEYS:
                    toolTips[key] = 'Open {0} folder'.format(key.replace('Dir', ''))
                    statusTips[key] = 'Open {0} folder'.format(key.replace('Dir', ''))
                    value = self.dirInfo[key]
                    valueType = CMD_VALUE_TYPE['dir']
                    arg = value
                    code = partial(os.startfile, value)
                elif key in APP_EVENT_KEYS:
                    toolTips[key] = 'Release PLM Event: {0}'.format(key)
                    statusTips[key] = 'Activate Event: {0}'.format(key)
                    value = key
                    valueType = CMD_VALUE_TYPE['event']
                    arg = key
                    code = key
                elif key in STYLESHEET_KEYS:
                    toolTips[key] = 'Load stylesheet: {0}'.format(key)
                    statusTips[key] = 'Load stylesheet: {0}'.format(key)
                    value = key
                    valueType = CMD_VALUE_TYPE['stylesheet']
                    arg = value
                    code = value
                elif key in SHORTCUT_KEYS:
                    toolTips[key] = key
                    statusTips[key] = key
                    value = key
                    valueType = CMD_VALUE_TYPE['shortcut']
                    arg = value
                    code = value
                else:
                    toolTips[key] = 'Execute function: {0}'.format(key)
                    statusTips[key] = 'Execute function: {0}'.format(key)
                    value = key
                    valueType = CMD_VALUE_TYPE['func']
                    arg = value
                    code = value

            tooltip = toolTips[key]
            statustip = statusTips[key]
            self.add(key, CommandData(key, icon, tooltip, statustip, value, valueType, arg, code))

        for key in layoutKeys:
            try:
                icon = self.iconInfo['icon32'][key]
            except KeyError:
                icon = 'Icon Missing: {0}'.format(key)
                print('Icon Missing: {0}'.format(key))
                iconMissing.append(key)
            finally:
                toolTips[key] = 'Show: {0}'.format(key)
                statusTips[key] = 'Show: {0}'.format(key)
                value = key
                valueType = CMD_VALUE_TYPE['uiKey']
                arg = value
                code = value

            tooltip = toolTips[key]
            statustip = statusTips[key]
            self.add(key, CommandData(key, icon, tooltip, statustip, value, valueType, arg, code))

    def del_key(self, key):
        try:
            del self.appInfo[key]
        except KeyError:
            self.appInfo.pop(key, None)


pythonInfo                          = ConfigPython()
dirInfo                             = ConfigDirectory()
pthInfo                             = ConfigPath()
envInfo                             = ConfigEnvVar()
iconInfo                            = ConfigIcon()
mayaInfo                            = ConfigMaya()
appInfo                             = ConfigApps()
urlInfo                             = ConfigUrl()
plmInfo                             = ConfigPipeline(iconInfo, appInfo, urlInfo, dirInfo)
deviceInfo                          = ConfigMachine()


# -------------------------------------------------------------------------------------------------------------
""" Config qssPths from text file """

def read_file(fileName):

    filePth = os.path.join(RAWS_DATA_DIR, fileName)

    if not os.path.exists(filePth):
        filePth = os.path.join(RST_DIR, "{}.rst".format(fileName))

    if os.path.exists(filePth):
        with open(filePth, 'r') as f:
            data = f.read()
        return data

QUESTIONS           = read_file('QUESTION')
ABOUT               = read_file('ABOUT')
CREDIT              = read_file('CREDIT')
CODECONDUCT         = read_file('CODECONDUCT')
CONTRIBUTING        = read_file('CONTRIBUTING')
REFERENCE           = read_file('REFERENCE')
LICENCE             = read_file('LICENCE_MIT')

CONFIG_OFFICE = [k for k in plmInfo.keys() if k in CONFIG_OFFICE]

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 10:56 PM
# Pipeline manager - DAMGteam
