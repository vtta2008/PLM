# -*- coding: utf-8 -*-
"""

Script Name: Settings.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

import os

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSettings

from core.Errors import KeySettingError
from core.Loggers import SetLogger
from docker.Storage import PObj


class Settings(QSettings):

    key = 'settings'
    setFormat = pyqtSignal(str)
    setScope = pyqtSignal(str)

    def __init__(self, filename, fm=QSettings.IniFormat, parent=None):
        super(Settings, self).__init__(filename, fm, parent)
        self.logger = SetLogger(self)
        self.setObjectName("Settings")

        self._parent = parent
        self._filename = filename
        self.grpLst = self.childGroups()
        self.reg = PObj(self)

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
        grpChecked = self.checkGrp(grp)
        self.beginGroup(grpChecked)

        if key is None or key == "":
            KeySettingError(key)
        else:
            self.setValue(key, value)
        while self.group():
            self.endGroup()

    def initValue(self, key=None, grp=None):
        grpChecked = self.checkGrp(grp)
        # self.logger.debug("Loading setting: {0}".format(key))
        self.beginGroup(grpChecked)
        if key is None or key == "":
            KeySettingError(key)
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

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 12/07/2018 - 10:45 AM
# © 2017 - 2018 DAMGteam. All rights reserved