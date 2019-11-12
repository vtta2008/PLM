# -*- coding: utf-8 -*-
"""

Script Name: Settings.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

import os

from PyQt5.QtCore                   import pyqtSignal, pyqtSlot, QSettings

class Settings(QSettings):

    key                     = 'Settings'
    setFormat               = pyqtSignal(str)
    setScope                = pyqtSignal(str)
    _settingEnable          = False
    _data                   = dict()

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

        self._filename = filename
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
                    # print('{0}: set {1} - {2} - {3}.'.format(self.key, key, value, grp))
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
                # print('{0}: get value from key: {1}, value: {2}, at group: {3}.'.format(self.key, key, value, grp))
                value = self.value(key)
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
            if len(lst) >= 2:
                self.remove(key)

    def delete_file(self):
        return os.remove(self.fileName())

    @pyqtSlot(str)
    def removeGrp(self, grpName):
        if grpName in self._groups:
            self._groups.remove(grpName)
            return True
        else:
            return False

    @pyqtSlot(str)
    def set_format(self, fm):
        if fm == 'ini':
            _format = QSettings.IniFormat
        elif fm == 'native':
            _format = QSettings.NativeFormat
        else:
            _format = QSettings.InvalidFormat
        self.setDefaultFormat(_format)
        return _format

    @pyqtSlot(str)
    def set_scope(self, scope):
        if scope == 'system':
            return QSettings.SystemScope
        else:
            return QSettings.UserScope

    @property
    def settingEnable(self):
        return self._settingEnable

    @settingEnable.setter
    def settingEnable(self, val):
        self._settingEnable = val

    @property
    def groups(self):
        return self._groups

    @groups.setter
    def groups(self, lst):
        self._groups = lst

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 12/07/2018 - 10:45 AM
# © 2017 - 2018 DAMGteam. All rights reserved