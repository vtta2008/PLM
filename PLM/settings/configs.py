# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
import os, json, yaml, pprint
from PLM import glbSettings, create_path, CFG_DIR, APP_SETTING, USER_SETTING, FORMAT_SETTING, UNIX_SETTING
from PLM.api.Core                       import Settings


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



class Sts(Cfg):

    key                                 = 'Sts'
    _filePath                           = create_path(CFG_DIR, 'settings.cfg')

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


class ConfigSettings(Sts):

    key                                 = 'ConfigSettings'

    def __iter__(self):
        super(ConfigSettings, self).__iter__()

        if glbSettings.printCfgInfo:
            if glbSettings.printSettingInfo:
                self.pprint()

        if glbSettings.saveCfgInfo:
            if glbSettings.saveSettingInfo:
                self.save_data()

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved