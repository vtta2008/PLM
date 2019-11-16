# -*- coding: utf-8 -*-
"""

Script Name: Settings.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

import os

from PyQt5.QtCore                   import pyqtSlot, QSettings

from __buildtins__                  import copyright

class Setting(QSettings):

    Type                            = 'DAMG SETTING'
    key                             = 'Setting'
    _name                           = 'DAMG Setting'
    _copyright                      = copyright()

    _settingEnable                  = False
    _checkSettingAble               = False
    _trackSetting                   = False
    _trackFixKey                    = False
    _trackDeleteKey                 = False

    _group                          = None
    _settingFile                    = None
    _data                           = dict()

    keyFixedOld                     = '  '

    def print(self):
        from pprint import pprint
        pprint(self._data)

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

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
    def checkSettingAble(self):
        return self._checkSettingAble

    @property
    def trackSetting(self):
        return self._trackSetting

    @property
    def trackFixKey(self):
        return self._trackFixKey

    @property
    def trackDeleteKey(self):
        return self._trackDeleteKey

    @settingEnable.setter
    def settingEnable(self, val):
        self._settingEnable         = val

    @groups.setter
    def groups(self, lst):
        self._groups                = lst

    @settingFile.setter
    def settingFile(self, val):
        self._settingFile           = val

    @name.setter
    def name(self, newName):
        self._name                   = newName

    @checkSettingAble.setter
    def checkSettingAble(self, val):
        self._checkSettingAble      = val

    @trackSetting.setter
    def trackSetting(self, val):
        self._trackSetting          = val

    @trackFixKey.setter
    def trackFixKey(self, val):
        self._trackFixKey           = val

    @trackDeleteKey.setter
    def trackDeleteKey(self, val):
        self._trackDeleteKey        = val

    @settingEnable.setter
    def settingEnable(self, val):
        self._settingEnable         = val

class Settings(Setting):

    key                     = 'Settings'

    def __init__(self, filename, fm=QSettings.IniFormat, parent=None):
        super(Settings, self).__init__(filename, fm, parent)

        self.parent = parent

        try:
            self.parent.children()
        except AttributeError:
            pass
        else:
            self.setParent(self.parent)
        finally:
            self.key = '{0}_{1}'.format(self.parent.key, self.key)
            self._name = self.key

        self._settingFile = filename
        self._groups = self.childGroups()
        self.clean_long_keys()

    def initSetValue(self, key=None, value=None, grp=None):
        if self._settingEnable:

            grpChecked = self.checkGrp(grp)
            self.beginGroup(grpChecked)

            if key is None or key == "":
                KeyError(key)
            else:
                oldValue = self.value(key)
                if not value == oldValue:
                    if self._trackSetting:
                        print('{0}: set {1} - {2} - {3}.'.format(self.key, key, value, grp))
                    self.setValue(key, value)
                    self.clean_long_keys()
            while self.group():
                self.endGroup()

    def initValue(self, key=None, grp=None):
        if self._settingEnable:

            grpChecked = self.checkGrp(grp)
            self.beginGroup(grpChecked)

            if key is None or key == "":
                KeyError(key)
            else:
                value = self.value(key)
                if self._trackSetting:
                    print('{0}: get value from key: {1}, value: {2}, at group: {3}.'.format(self.key, key, value, grp))
                self.clean_long_keys()
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

    def clean_long_keys(self):
        for key in self.allKeys():
            lst = key.split('/')
            # if len(lst) == 2:
            #     if self.checkGrp(lst[-2]):
            #         repeat = True
            #         for i in range(len(key)):
            #             if not key[i] == self.keyFixedOld[i]:
            #                 repeat = False
            #                 break
            #
            #         if not repeat:
            #             if self._trackFixKey:
            #                 print('{0}: key fixed: {1}'.format(self.key, key))
            #             value = self.value(key)
            #             self.initSetValue(lst[-1], value, lst[-2])
            #         else:
            #             if self._trackDeleteKey:
            #                 print('{0}: key: {1} has been removed.'.format(self.key, key))
            #             self.remove(key)
            #     else:
            #         if self._trackDeleteKey:
            #             print('{0}: key: {1} has been removed.'.format(self.key, key))
            #         self.remove(key)
            if len(lst) >= 2:
                if self._trackDeleteKey:
                    print('{0}: key: {1} has been removed.'.format(self.key, key))
                self.remove(key)

        self.update()

    def update(self):

        self._data['key'] = self.key

        for g in self.childGroups():
            print(g)
            grp = {}
            self.beginGroup(g)
            for k in self.childKeys():
                v = self.value(k)
                print(g, k, v)
                if not v is None:
                    grp[k] = v
            grp.update()
            # print(grp)
            self._data[g] = grp
            self._data.update()
            while self.group():
                self.endGroup()

        return self._data

    def delete_file(self):
        return os.remove(self._settingFile)

    @pyqtSlot(str, name='removeGroup')
    def removeGrp(self, grpName):
        if grpName in self._groups:
            self._groups.remove(grpName)
            return True
        else:
            return False

    @pyqtSlot(str, name='setFormat')
    def set_format(self, fm):
        if fm == 'ini':
            _format = QSettings.IniFormat
        elif fm == 'native':
            _format = QSettings.NativeFormat
        else:
            _format = QSettings.InvalidFormat
        self.setDefaultFormat(_format)
        return _format

    @pyqtSlot(str, name='setScope')
    def set_scope(self, scope):
        if scope == 'system':
            return QSettings.SystemScope
        else:
            return QSettings.UserScope



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 12/07/2018 - 10:45 AM
# © 2017 - 2018 DAMGteam. All rights reserved