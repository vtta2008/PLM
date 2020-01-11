# -*- coding: utf-8 -*-
"""

Script Name: _data.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import ROOT, __envKey__, globalSetting

""" Import """

# Python
import os, platform, subprocess, json, shutil, pkg_resources, pprint, winshell

if os.getenv(__envKey__) != ROOT:
    subprocess.Popen('Set {0} {1}'.format(__envKey__, ROOT), shell=True).wait()

PIPE = subprocess.PIPE
STDOUT = subprocess.STDOUT

from bin                            import DAMGDICT
from .dirs                          import ConfigDirectory
from .pths                          import ConfigPath

from .types                         import (RAMTYPE, CPUTYPE, FORMFACTOR, DRIVETYPE, DB_ATTRIBUTE_TYPE, CMD_VALUE_TYPE,
                                            actionTypes, layoutTypes)

from .text                          import (TRADE_MARK, PLM_ABOUT, WAIT_FOR_UPDATE, WAIT_TO_COMPLETE, WAIT_LAYOUT_COMPLETE,
                                            PASSWORD_FORGOTTON, SIGNUP, DISALLOW, TIT_BLANK, PW_BLANK, PW_WRONG,
                                            PW_UNMATCH, PW_CHANGED, FN_BLANK, LN_BLANK, SEC_BLANK, USER_CHECK_REQUIRED,
                                            USER_NOT_CHECK, USER_BLANK, USER_CHECK_FAIL, USER_NOT_EXSIST, USER_CONDITION,
                                            SYSTRAY_UNAVAI, PTH_NOT_EXSIST, ERROR_OPENFILE, ERROR_QIMAGE, tooltips_present,
                                            tooltips_missing, N_MESSAGES_TEXT, SERVER_CONNECT_FAIL, TEMPLATE_QRC_HEADER,
                                            TEMPLATE_QRC_FILE, TEMPLATE_QRC_FOOTER, HEADER_SCSS, HEADER_QSS)

from .keys                          import *

from .formats                       import (INI, Native, Invalid, LOG_FORMAT, DT_FORMAT, ST_FORMAT, datetTimeStamp,
                                            IMGEXT, )
from .options                       import *

from .metadatas                     import (__plmWiki__, __localServer__, __pkgsReq__, __homepage__, __appname__,
                                            __organization__, __organizationID__, __organizationName__, __globalServer__,
                                            __google__, __plmSlogan__, __localServerAutho__, __version__, __website__,
                                            VERSION, )

from .device                        import ConfigMachine


def save_data(filePth, data):
    if os.path.exists(filePth):
        os.remove(filePth)
    with open(filePth, 'w+') as f:
        json.dump(data, f, indent=4)
    return True

iconMissing                         = []
toolTips                            = {}
statusTips                          = {}


# from . import dirs
# keys                            = [k for k in vars(dirs).keys() if not k in notKeys]
# for k in keys:
#     print("self.add('{0}', {0})".format(k))

dirInfo                            = ConfigDirectory()
pthInfo                            = ConfigPath()

from bin import PresetDB
localDB = PresetDB(filename=pthInfo['LOCAL_DB'])

class CommandData(DAMGDICT):
    key = 'CommandData'

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
            self[ks[i]] = vs[i]


# -------------------------------------------------------------------------------------------------------------
""" Configs """

class ConfigPython(DAMGDICT):

    key                             = 'ConfigPython'

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

        # pprint.pprint(self)


class ConfigEnvVar(DAMGDICT):

    key                                 = 'ConfigEnvVar'

    def __init__(self):
        super(ConfigEnvVar, self).__init__()
        for k, v in os.environ.items():
            self[k]                     = v.replace('\\', '/')

    def update(self):
        for k, v in os.environ.items():
            self[k]                     = v.replace('\\', '/')


class ConfigAvatar(DAMGDICT):

    key                                 = 'ConfigAvatar'

    def __init__(self):
        super(ConfigAvatar, self).__init__()

        for root, dirs, names in os.walk(dirInfo['AVATAR_DIR'], topdown=False):
            for name in names:
                self[name.split('.avatar')[0]] = os.path.join(root, name).replace('\\', '/')


class ConfigLogo(DAMGDICT):

    key                                 = 'ConfigLogo'

    def __init__(self):
        super(ConfigLogo, self).__init__()

        damgLogos                       = DAMGDICT()
        plmLogos                        = DAMGDICT()

        for root, dirs, names in os.walk(dirInfo['DAMG_LOGO_DIR'], topdown=False):
            for name in names:
                damgLogos[name.split('.png')[0]] = os.path.join(root, name).replace('\\', '/')

        for root, dirs, names in os.walk(dirInfo['PLM_LOGO_DIR'], topdown=False):
            for name in names:
                plmLogos[name.split('.png')[0]] = os.path.join(root, name).replace('\\', '/')

        self['DAMGTEAM']                = damgLogos
        self['PLM']                     = plmLogos


class ConfigPics(DAMGDICT):

    key                                 = 'ConfigPics'

    def __init__(self):
        super(ConfigPics, self).__init__()

        for root, dirs, names, in os.walk(dirInfo['PIC_DIR'], topdown=False):
            for name in names:
                self[name.split('.node')[0]] = os.path.join(root, name).replace('\\', '/')


class ConfigIcon(DAMGDICT):

    key                                 = 'ConfigIcon'

    def __init__(self):
        super(ConfigIcon, self).__init__()

        self['icon12']                  = self.get_icons(dirInfo['ICON_DIR_12'])
        self['icon16']                  = self.get_icons(dirInfo['ICON_DIR_16'])
        self['icon24']                  = self.get_icons(dirInfo['ICON_DIR_24'])
        self['icon32']                  = self.get_icons(dirInfo['ICON_DIR_32'])
        self['icon48']                  = self.get_icons(dirInfo['ICON_DIR_48'])
        self['icon64']                  = self.get_icons(dirInfo['ICON_DIR_64'])

        self['maya']                    = self.get_icons(dirInfo['MAYA_ICON_DIR'])

        self['node']                    = self.get_icons(dirInfo['NODE_ICON_DIR'])

        self['tag']                     = self.get_icons(dirInfo['TAG_ICON_DIR'])

        self['web32']                   = self.get_icons(dirInfo['WEB_ICON_32'])
        self['web128']                  = self.get_icons(dirInfo['WEB_ICON_128'])

        self['avatar']                  = ConfigAvatar()
        self['logo']                    = ConfigLogo()
        self['pic']                     = ConfigPics()

        if globalSetting.tracks.configInfo:
            if globalSetting.tracks.iconInfo:
                pprint.pprint(self)

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
        modulePth = os.path.join(dirInfo['MAYA_DIR'], 'modules')
        paths = [os.path.join(modulePth, m) for m in modules]
        sys.path.insert(-1, ';'.join(paths))

        usScr = os.path.join(dirInfo['MAYA_DIR'], 'userSetup.py')

        if os.path.exists(usScr):
            mayaVers = [os.path.join(dirInfo['MAYA_DIR'], v) for v in autodeskVer if os.path.exists(os.path.join(dirInfo['MAYA_DIR'], v))] or []
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

        if globalSetting.tracks.configInfo:
            if globalSetting.tracks.appInfo:
                pprint.pprint(self)


class ConfigUrl(DAMGDICT):

    key = 'ConfigUrl'

    def __init__(self):
        super(ConfigUrl, self).__init__()

        self.add('pythonTag', 'https://docs.anaconda.com/anaconda/reference/release-notes/')
        self.add('licenceTag', 'https://github.com/vtta2008/damgteam/blob/master/LICENCE')
        self.add('versionTag', 'https://github.com/vtta2008/damgteam/blob/master/appData/documentations/version.rst')
        self.add('PLM wiki', __plmWiki__)

        if globalSetting.tracks.configInfo:
            if globalSetting.tracks.urlInfo:
                pprint.pprint(self)

        if globalSetting.defaults.save_configInfo:
            if globalSetting.defaults.save_urlInfo:
                save_data(pthInfo['urlCfg', self])


class ConfigPipeline(DAMGDICT):

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

        if globalSetting.tracks.configInfo:
            if globalSetting.tracks.plmInfo:
                pprint.pprint(self)

        if globalSetting.defaults.save_configInfo:
            if globalSetting.defaults.save_plmInfo:
                save_data(pthInfo['plmCfg'], self)

    def del_key(self, key):
        try:
            del self.appInfo[key]
        except KeyError:
            self.appInfo.pop(key, None)

def ignoreIDs(*info):
    path = os.path.join(dirInfo['TMP_DIR'], '.ignoreIDs')
    if os.path.exists(path):
        with open(path, 'r') as f:
            info = json.load(f)
    else:
        info      = ['BotTab'       , 'ConnectStatus'      , 'ConnectStatusSection', 'Footer'                   ,
                     'GridLayout'   , 'MainMenuBar'        , 'MainMenuSection'     , 'MainMenuSectionSection'   ,
                     'MainStatusBar', 'MainToolBar'        , 'MainToolBarSection'  , 'MainToolBarSectionSection',
                     'Notification' , 'NotificationSection', 'TerminalLayout'      , 'TopTab'                   ,
                     'TopTab1'      , 'TopTab2'            , 'TopTab3'             , ]
        # if os.path.exists(path):
        #     os.remove(path)
        # with open(path, 'w') as f:
        #     info = json.dump(info, f, indent=4)
    if globalSetting.checks.ignoreIDs:
        print(info)
    return info

def tobuildUis(*info):
    path = os.path.join(dirInfo['TMP_DIR'], '.toBuildUis')
    if os.path.exists(path):
        with open(path, 'r') as f:
            info = json.load(f)
    else:
        info = [  'Alpha'           , 'ConfigOrganisation', 'ConfigProject'      , 'ConfigTask'         ,
                  'ConfigTeam'      , 'ContactUs'         , 'EditOrganisation'   , 'EditProject'        ,
                  'EditTask'        , 'EditTeam'          , 'Feedback'           , 'HDRI'               ,
                  'NewOrganisation' ,  'NewTask'          , 'NewTeam'            , 'OrganisationManager',
                  'ProjectManager'  , 'TaskManager'       , 'TeamManager'        , 'Texture'            ,]
    if globalSetting.checks.toBuildUis:
        print(info)
    return info

def tobuildCmds(*info):
    path = os.path.join(dirInfo['TMP_DIR'], '.cmds')
    if os.path.exists(path):
        with open(path, 'r') as f:
            try:
                info = json.load(f)
            except json.decoder.JSONDecodeError:
                info = {}
    if globalSetting.checks.toBuildCmds:
        print(info)
    return info


ignoreIDs                           = ignoreIDs()
toBuildUis                          = tobuildUis()
toBuildCmds                         = tobuildCmds()

# pythonInfo                          = ConfigPython()
# envInfo                             = ConfigEnvVar()
# iconInfo                            = ConfigIcon()
# mayaInfo                            = ConfigMaya()
# appInfo                             = ConfigApps()
# urlInfo                             = ConfigUrl()
# plmInfo                             = ConfigPipeline(iconInfo, appInfo, urlInfo, dirInfo, pthInfo)
# deviceInfo                          = ConfigMachine()


# -------------------------------------------------------------------------------------------------------------
""" Config qssPths from text file """

def read_file(fileName):

    filePth = os.path.join(dirInfo['RAWS_DATA_DIR'], fileName)

    if not os.path.exists(filePth):
        filePth = os.path.join(dirInfo['RST_DIR'], "{}.rst".format(fileName))

    if os.path.exists(filePth):
        with open(filePth, 'r') as f:
            data = f.read()
        return data

QUESTIONS           = read_file('QUESTION')
ABOUT               = read_file('ABOUT')
CREDIT              = read_file('CREDIT')
CODECONDUCT         = read_file('CODECONDUCT')
CONTRIBUTING        = read_file('CONTRIBUTING')
REFERENCES          = read_file('REFERENCES')
LICENCE             = read_file('LICENCE_MIT')

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 10:56 PM
# Pipeline manager - DAMGteam
