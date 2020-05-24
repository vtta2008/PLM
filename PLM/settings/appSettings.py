# -*- coding: utf-8 -*-
"""

Script Name: Settings.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os

# PLM
from PLM.configs                        import ConfigSettings
from PLM.api.Core                       import Settings

settingInfo                             = ConfigSettings()
APP_SETTING                             = settingInfo.APP_SETTING
INI                                     = settingInfo.INI
NATIVE                                  = settingInfo.NATIVE
INVAILD                                 = settingInfo.INVAILD
SYS_SCOPE                               = settingInfo.SYS_SCOPE
USER_SCOPE                              = settingInfo.USER_SCOPE

class AppSettings(Settings):

    key                                 = 'AppSettings'

    _settingEnable                      = False

    _groups                             = None
    _settingFile                        = None
    _data                               = dict()

    modes                               = APP_SETTING
    _mode                               = 'app'

    def __init__(self, parent=None, filename = APP_SETTING, fm=INI):
        super(AppSettings, self).__init__(filename, fm)

        self.parent                     = parent
        if not self.parent is None:
            self.changeParent(self.parent)

        self._format                    = fm
        self._settingFile               = filename
        self._groups                    = self.childGroups()
        self.cleanKey()

    def cleanKey(self):
        for key in self.allKeys():
            if len(key.split('/')) > 2:
                self.remove(key)

    def update(self):

        self._data['key'] = self.key
        for g in self.childGroups():
            grp = {}
            self.beginGroup(g)
            for k in self.childKeys():
                v = self.value(k)
                if not v is None:
                    grp[k] = v
            grp.update()
            self._data[g] = grp
            self._data.update()
            while self.group():
                self.endGroup()

        return self._data

    def changeParent(self, parent):
        self.parent             = parent
        self.key                = '{0}_{1}'.format(self.parent.key, self.key)
        self._name              = self.key.replace('_', ' ')
        self.update()

    def initSetValue(self, key=None, value=None, grp=None):
        if self._settingEnable:

            grpChecked = self.checkGrp(grp)
            self.beginGroup(grpChecked)

            if key is None or key == "":
                KeyError(key)
            else:
                oldValue = self.value(key)
                if not value == oldValue:
                    if glbSettings.printSettingInfo:
                        print('{0}: set {1} - {2} - {3}.'.format(self.key, key, value, grpChecked))
                    self.setValue(key, value)

            while self.group():
                self.endGroup()

    def initValue(self, key=None, grp=None, decode=None):
        if self._settingEnable:
            grpChecked = self.checkGrp(grp)
            self.beginGroup(grpChecked)

            if key is None or key == "":
                KeyError(key)
            else:
                if decode is None:
                    value = self.value(key)
                else:
                    value = self.value(key, decode)
                if glbSettings.printSettingInfo:
                    print('{0}: get value from key: {1}, value: {2}, at group: {3}.'.format(self.key, key, value, grpChecked))
                return value

            while self.group():
                self.endGroup()

    def addGrp(self, grpName):
        self._groups.append(grpName)
        return True

    def checkGrp(self, grp):
        if grp is None:
            return 'General'
        else:
            if not grp in self._groups:
                self.addGrp(grp)
            return grp

    def print(self):
        from pprint import pprint
        pprint(self._data)

    def delete_file(self):
        return os.remove(self._settingFile)

    def setMode(self, mode):
        self._mode = mode
        self.setPath(self.format(), self.scope(), self.modes[self._mode])

    def removeGrp(self, grpName):
        if grpName in self._groups:
            self._groups.remove(grpName)
            return True
        else:
            return False

    def set_format(self, fm):
        if fm == 'ini':
            _format = INI
        elif fm == 'native':
            _format = NATIVE
        else:
            _format = INVAILD
        self.setDefaultFormat(_format)
        return _format

    def set_scope(self, scope):
        if scope == 'system':
            return SYS_SCOPE
        else:
            return USER_SCOPE

    @property
    def mode(self):
        return self._mode

    @property
    def settingFile(self):
        return self._settingFile

    @property
    def settingEnable(self):
        return self._settingEnable

    @property
    def groups(self):
        return self._groups

    @property
    def grp(self):
        return self._grp

    @grp.setter
    def grp(self, val):
        self._grp = val

    @settingEnable.setter
    def settingEnable(self, val):
        self._settingEnable = val

    @groups.setter
    def groups(self, lst):
        self._groups = lst

    @settingFile.setter
    def settingFile(self, val):
        self._settingFile = val

    @settingEnable.setter
    def settingEnable(self, val):
        self._settingEnable = val

    @mode.setter
    def mode(self, val):
        self._mode = val

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 28/11/2019 - 1:15 AM
# © 2017 - 2018 DAMGteam. All rights reserved