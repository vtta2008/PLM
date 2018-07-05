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
from PyQt5.QtCore import Q_CLASSINFO, pyqtSlot, QSettings, QSize
from PyQt5.QtWidgets import QDockWidget


# Plm
from utilities.utils import get_unix
from core.Signals import Signals
from core.Errors import PathSettingError, KeySettingError

from appData.config import FORMAT_SETTING, USER_SETTING, APP_SETTING, UNIX_SETTING, PREFERENCES
from appData.Loggers import SetLogger
logger = SetLogger()

class Settings(QSettings):

    staticMetaObject = {

        Q_CLASSINFO("id" , "SETTING MANAGER"),
        Q_CLASSINFO("type", "Core Object"),
        Q_CLASSINFO("unixID", "{0}".format(get_unix())),
        Q_CLASSINFO("ClassID", "HUB"),
        Q_CLASSINFO("Flag", "Contributing Setting" )
    }

    def __init__(self, filename, fm=QSettings.IniFormat, parent=None, section='app', max_files=10):
        super(Settings, self).__init__(filename, fm, parent)

        self.setObjectName("Settings Manager")
        self.section = section
        self._max_files = max_files
        self._parent = parent
        self.grpLst = ['MainWindow', 'RecentFiles', 'Preferences']

    def initSetting(self):
        for grp in self.grpLst:
            if grp not in self.childGroups():
                if self._parent is not None:
                    if grp == 'MainWindow':
                        self.setValue('MainWindow/geometry/default', self._parent.saveGeometry())
                        self.setValue('MainWindow/windowState/default', self._parent.saveState())
                    elif grp == 'RecentFiles':
                        self.beginWriteArray('RecentFiles', 0)
                        self.endArray()

        while self.group():
            self.endGroup()

        if 'Preferences' not in self.childGroups():
            self.beginGroup('Preferences')
            for opt in PREFERENCES:
                if 'default' in PREFERENCES.get(opt):
                    defValue = PREFERENCES.get(opt).get('default')
                    if type(defValue) is bool:
                        defValue = int(defValue)
                    self.setValue("default/{0}".format(opt), defValue)

        while self.group():
            self.endGroup()

    @property
    def groups(self):
        return self.grpLst

    @property
    def recent_files(self):
        files = self.getRecentFiles()
        tmp = []
        for f in reversed(files):
            tmp.append(f)

        return tuple(tmp[:self._max_files])

    def addGrp(self, grpName):
        if grpName not in self.grpLst:
            self.grpLst.append(grpName)
            return True
        else:
            return False

    def removeGrp(self, grpName):
        if grpName in self.grpLst:
            self.grpLst.remove(grpName)
            return True
        else:
            return False

    def windowKeys(self):
        if self._parent is None:
            return []
        keys = ['MainWindow']
        for dock in self._parent.findChildren(QDockWidget):
            dockName = dock.objectName()
            keys.append(str(dockName))
        return keys

    def get_layout(self):
        layoutNames = []
        layoutKeys = ["{0}/geometry".format(k) for k in self.windowKeys()]
        for k in self.allKeys():
            if 'geometry' in k:
                attrs = k.split('/geometry')
                if len(attrs) > 1:
                    layoutNames.append(str(attrs[-1]))

        return sorted(list(set(layoutNames)))

    def saveLayout(self, layoutName):
        self.setValue("MainWindow/geometry/{0}".format(layoutName), self._parent.saveGeometry())
        self.setValue("MainWindow/windowState/{0}".format(layoutName), self._parent.saveState())

        for dock in self._parent.findChildren(QDockWidget):
            dockName = dock.objectName()
            self.setValue("{0}/geometry/{1}".format(dockName, layoutName, dock.saveGeometry()))

    def restoreLayout(self, layoutName):
        windowKeys = self.windowKeys()

        for widgetName in windowKeys:
            keyName = "{0}/geometry/{1}".format(widgetName, layoutName)
            if widgetName != 'MainWindow':
                dock = self._parent.findChildren(QDockWidget, widgetName)
                if dock:
                    dock[0].restoreGeometry(value)
            else:
                if keyName in self.allKeys():
                    value = self.value(keyName)
                    self._parent.restoreGeometry(value)

                windowState = "{0}/windowState/{1}".format(widgetName, layoutName)
                if windowState in self.allKeys():
                    self._parent.restoreState(self.value(windowState))

    def delete_layout(self, layoutName):
        windowKeys = self.windowKeys()
        for widgetName in windowKeys:
            keyName = "{0}/geometry/{1}".format(widgetName, layoutName)
            if keyName in self.allKeys():
                self.remove(keyName)

            if widgetName == 'MainWindow':
                windowState = "{0}/windowState/{1}".format(widgetName, layoutName)
                if windowState in self.allKeys():
                    self.remove(windowState)

    def get_default_value(self, key, grpLst):

        if self.group():
            try:
                self.endGroup()
            except:
                pass

        result = None
        grpNamne = grpLst[0]
        for grp in grpLst[1:]:
            grpNamne += "/{0}".format(grp)

        grpNamne += "/{0}".format("default")
        grpNamne += "/{0}".format(key)

        if grpNamne in self.allKeys():
            result = self.value(grpNamne)
        return result

    def save(self, key='default'):
        self.beginGroup("MainwWindow/{0}".format(key))
        self.setValue("size", QSize(self._parent.width(), self._parent.height()))
        self.setValue("pos", self._parent.pos())
        self.setValue("windowState", self._parent.saveState())
        self.endGroup()

    def delete_file(self):
        return os.remove(self.fileName())

    def get_recent_files(self):
        recentFiles = []
        cnt = self.beginReadArray('recentFiles')
        for i in range(cnt):
            self.setArrayIndex(i)
            fn = self.value('file')
            recentFiles.append(fn)

        self.endArray()
        return tuple(recentFiles)

    def add_recent_files(self, filename):
        recentFiles = self.get_recent_files()
        if filename in recentFiles:
            recentFiles = tuple(x for x in recentFiles if x != filename)

        recentFiles = recentFiles + (filename)
        self.beginWriteArray('recentFiles')

        for i in range(len(recentFiles)):
            self.setArrayIndex(i)
            self.setValue('file', recentFiles[i])

        self.endArray()

    def clear_recent_files(self):
        self.remove('RecentFiles')

    def writeSetting(self, key, value):
            logger.debug("Saving setting: {0} = {1}".format(key, value))
            if key is None or key == "":
                KeySettingError(key)
            else:
                self.setValue(key, value)

    def readSetting(self, key):
        logger.debug("Loading setting: {0}".format(key))
        if key is None or key == "":
            KeySettingError()
        else:
            return self.value(key)

    def _path(self):
        if self.section == 'format':
            pth = FORMAT_SETTING
        elif self.section == 'unix':
            pth = UNIX_SETTING
        elif self.section == 'user':
            pth = USER_SETTING
        elif self.section == 'app':
            pth = APP_SETTING
        else:
            pth = APP_SETTING

        return pth

    def _format(self, fm='ini'):
        if fm == 'ini':
            _format = QSettings.IniFormat
        elif fm == 'native':
            _format = QSettings.NativeFormat
        else:
            _format = QSettings.InvalidFormat
        self.setDefaultFormat(_format)
        return _format

    def _scope(self, scope='system'):
        if scope == 'system':
            return QSettings.SystemScope
        else:
            return QSettings.UserScope

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 11:52 AM
# © 2017 - 2018 DAMGteam. All rights reserved