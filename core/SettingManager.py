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
from PyQt5.QtCore import QObject, Q_CLASSINFO, pyqtSignal, pyqtSlot, QFile, QTextStream

# Plm
from appData.config import unixSetting, formatSetting, appSetting, userSetting
from appData import QSSDIR
from utilities.utils import get_unix
from core.SignalManager import Signals
from core.ErrorManager import SettingError
from appData.Loggers import SetLogger
logger = SetLogger()

class SettingManager(QObject):

    setvalueSig = pyqtSignal(str, str)

    def __init__(self, section, parent=None):
        super(SettingManager, self).__init__(parent)

        self.section = section
        self.settings = self.config_setting(section)

    def config_setting(self, section):

        if section == 'format':
            settings = formatSetting
        elif section == 'unix':
            settings = unixSetting
        elif section == 'user':
            settings = userSetting
        elif section == 'app':
            settings = appSetting
        else:
            settings = None

        if settings is None:
            SettingError()
        else:
            logger.debug(settings.fileName())

    def setValue(self, key, value):
        if key == 'stylesheet':
            self.setvalueSig.emit(key, value)
            # self.settings.setValue(key, value)

    def value(self, key):
        value = self.settings.value(key=key)
        return value

class Settings(SettingManager):

    staticMetaObject = {

        Q_CLASSINFO("id" , "SETTING MANAGER"),
        Q_CLASSINFO("type", "Core Object"),
        Q_CLASSINFO("unixID", "{0}".format(get_unix())),
        Q_CLASSINFO("ClassID", "HUB"),
        Q_CLASSINFO("Flag", "Contributing Setting" )
    }

    stylesheetSig = pyqtSignal(str)
    setvalueSig = pyqtSignal(str, str)

    def __init__(self, key=None, value=None, section=None, parent=None):
        super(Settings, self).__init__(parent)
        self.settings = SettingManager(section=section)
        self._key = key
        self._value = value

        if not self._key == None:
            data = self.setValue(self._key, self._value)
            if not data == None:
                self._return(key, data)

    def value(self, key):
        self.settings.value(key)

    def setValue(self, key, value):
        self.settings.setValue(key, value)




# setting = Settings('app')
# setting.setValue('stylesheet', 'darkstyle')
# setting.value('stylesheet', str)
# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 11:52 AM
# © 2017 - 2018 DAMGteam. All rights reserved