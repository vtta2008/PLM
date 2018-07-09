# -*- coding: utf-8 -*-
"""

Script Name: Settings.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" import """

# Python
import os, platform

# PyQt5
from PyQt5.QtCore import QSettings, pyqtSlot, pyqtSignal

# Plm
from core.Errors import KeySettingError
from core.Loggers import SetLogger

class Settings(QSettings):


    setFormat = pyqtSignal(str)
    setScope = pyqtSignal(str)

    def __init__(self, filename, fm=QSettings.IniFormat, parent=None):
        super(Settings, self).__init__(filename, fm, parent)

        if parent is None:
            raise (EnvironmentError("Need to have specific parent to be able to log"))

        self.logger = SetLogger(self)
        self.setObjectName("Settings")

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
        grpChecked = self.checkGrp(grp)
        self.beginGroup(grpChecked)
        # self.logger.debug("Saving setting: {0} = {1}".format(key, value))
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

    @pyqtSlot(str)
    def removeGrp(self, grpName):
        if grpName in self.grpLst:
            self.grpLst.remove(grpName)
            return True
        else:
            return False

    def delete_file(self):
        return os.remove(self.fileName())

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
# Created by panda on 19/06/2018 - 11:52 AM
# © 2017 - 2018 DAMGteam. All rights reserved