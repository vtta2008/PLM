# -*- coding: utf-8 -*-
"""

Script Name: Setting.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__                     import absolute_import, unicode_literals
from __buildtins__                  import __copyright__
""" Import """

# Python
import os

# PyQt5
from PyQt5.QtCore                   import pyqtSlot, QSettings


class Setting(QSettings):

    Type                            = 'DAMGSETTING'
    key                             = 'Setting'
    _name                           = 'DAMG Setting'
    _copyright                      = __copyright__()

    _settingEnable                  = False
    _checkSettingAble               = False
    _trackSetting                   = False
    _trackFixKey                    = False
    _trackDeleteKey                 = False

    _groups                         = None
    _settingFile                    = None
    _data                           = dict()

    keyFixedOld                     = '  '

    def __init__(self, parent=None):
        QSettings.__init__(self)

        self.parent                 = parent

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
                        print('{0}: set {1} - {2} - {3}.'.format(self.key, key, value, grpChecked))
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
                    print('{0}: get value from key: {1}, value: {2}, at group: {3}.'.format(self.key, key, value,
                                                                                            grpChecked))
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

    def print(self):
        from pprint import pprint
        pprint(self._data)

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

    @name.setter
    def name(self, newName):
        self._name = newName

    @checkSettingAble.setter
    def checkSettingAble(self, val):
        self._checkSettingAble = val

    @trackSetting.setter
    def trackSetting(self, val):
        self._trackSetting = val

    @trackFixKey.setter
    def trackFixKey(self, val):
        self._trackFixKey = val

    @trackDeleteKey.setter
    def trackDeleteKey(self, val):
        self._trackDeleteKey = val

    @settingEnable.setter
    def settingEnable(self, val):
        self._settingEnable = val

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 28/11/2019 - 12:42 AM
# © 2017 - 2018 DAMGteam. All rights reserved