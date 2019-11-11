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

    key = 'Settings'
    setFormat = pyqtSignal(str)
    setScope = pyqtSignal(str)
    _settingEnable = False

    def __init__(self, filename, fm=QSettings.IniFormat, parent=None):
        super(Settings, self).__init__(filename, fm, parent)

        self._parent = parent
        self._filename = filename
        self.grpLst = self.childGroups()

    @property
    def groups(self):
        return self.grpLst

    def checkGrp(self, grp):
        if grp is None:
            return 'General'
        else:
            if not grp in self.grpLst:
                self.addGrp(grp)
            return grp

    def initSetValue(self, key=None, value=None, grp=None):
        if self._settingEnable:
            grpChecked = self.checkGrp(grp)
            self.beginGroup(grpChecked)

            if key is None or key == "":
                KeyError(key)
            else:
                oldValue = self.value(key)
                if not value == oldValue:
                    # print('set setting: {0} {1} {2}'.format(grp, key, value))
                    self.setValue(key, value)
            while self.group():
                self.endGroup()
            # self.logger.info("setting configKey: {0}, value: {1}, group: {2}".format(configKey, value, grp))

    def initValue(self, key=None, grp=None):
        if self._settingEnable:
            grpChecked = self.checkGrp(grp)

            # self.logger.info("Loading setting: {0}".format(configKey))

            self.beginGroup(grpChecked)
            if key is None or key == "":
                KeyError(key)
            else:
                return self.value(key)
            while self.group():
                self.endGroup()

    def addGrp(self, grpName):
        self.grpLst.append(grpName)
        return True

    def delete_file(self):
        return os.remove(self.fileName())

    @pyqtSlot(str)
    def removeGrp(self, grpName):
        if grpName in self.grpLst:
            self.grpLst.remove(grpName)
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

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 12/07/2018 - 10:45 AM
# © 2017 - 2018 DAMGteam. All rights reserved