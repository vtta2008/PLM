# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os
from PLM                        import glbSettings
from PLM.types                  import CMD_VALUE_TYPE
from .baseConfigs               import Pls, Cmds
from .modelConfigs              import ConfigDirs, ConfigPths, ConfigIcons, ConfigApps, ConfigUrls, ConfigUiKeys
from .utils                     import create_path



iconMissing                     = []
toolTips                        = {}
statusTips                      = {}


class ConfigPipeline(Pls):

    key                         = 'ConfigPipeline'

    dirInfo                     = ConfigDirs()
    pthInfo                     = ConfigPths()
    iconInfo                    = ConfigIcons()
    appInfo                     = ConfigApps()
    urlInfo                     = ConfigUrls()
    uiKeyInfo                   = ConfigUiKeys()


    def __init__(self):
        super(ConfigPipeline, self).__init__()

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
            self.del_key(k)

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
                self.add(key, Cmds(key, icon, tooltip, statustip, value, valueType, arg, code))

        if glbSettings.printCfgInfo:
            if glbSettings.printPlmInfo:
                self.pprint()

        if glbSettings.saveCfgInfo:
            if glbSettings.savePlmInfo:
                self.save_data()

    def del_key(self, key):
        try:
            del self.appInfo[key]
        except KeyError:
            self.appInfo.pop(key, None)


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved