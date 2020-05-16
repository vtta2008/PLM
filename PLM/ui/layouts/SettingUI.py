# -*- coding: utf-8 -*-
"""

Script Name: SettingUI.py.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os
import sys

# PyQt5

from PyQt5.QtWidgets        import QAction, QFileDialog, QInputDialog, QLineEdit
from PyQt5.QtCore           import QSettings

# PLM
from PLM.cores              import AppSettings
from PLM.api.Widgets        import Widget, GridLayout, MenuBar
from PLM.ui.components      import SettingOutput, SettingInput
from PLM.configs            import SETTING_FILEPTH, __appname__, __organization__


# -------------------------------------------------------------------------------------------------------------
""" Setting Manager """

class SettingUI(Widget):

    key                     = 'AppSetting'

    def __init__(self, parent=None):
        super(SettingUI, self).__init__(parent)


        self.setWindowTitle("Application Settings")

        self.parent         = parent
        self.menubar        = MenuBar(self)
        self.regValue       = SettingOutput(self.settings)
        self.regInfo        = SettingInput(self.settings)
        self.settings       = AppSettings(self)
        self.createMenus()

        self.layout         = GridLayout()
        self.layout.addWidget(self.menubar, 0, 0, 1, 1)
        self.layout.addWidget(self.regInfo, 1, 0, 1, 1)
        self.layout.addWidget(self.regValue, 2, 0, 1, 1)

        self.setLayout(self.layout)

        self.autoRefreshAct.setChecked(True)
        self.fallbacksAct.setChecked(True)

        self.setSettingsObject(self.settings)

        self.fallbacksAct.setEnabled(True)

    def openIniFile(self):
        if not os.path.exists(self.settings.settingFile):
            fileName, _ = QFileDialog.getOpenFileName(self, "Open INI File", '', "INI Files (*.ini *.conf)")

            if fileName:
                self.settings._settingFile = fileName
        else:
            self.settings._settingFile = SETTING_FILEPTH['app']
            self.setSettingsObject(self.settings)
            self.fallbacksAct.setEnabled(False)

    def openPropertyList(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Property List", '', "Property List Files (*.plist)")

        if fileName:
            self.settings.set_format(QSettings.NativeFormat)
            self.setSettingsObject(self.settings)
            self.fallbacksAct.setEnabled(False)

    def openRegistryPath(self):
        path, ok = QInputDialog.getText(self, "Open Registry Path",
                                        "Enter the path in the Windows registry:", QLineEdit.Normal,
                                        'HKEY_CURRENT_USER\\Software\\{0}\\{1}'.format(__organization__, __appname__))

        if ok and path != '':
            settings = QSettings(path, QSettings.NativeFormat)
            self.setSettingsObject(settings)
            self.fallbacksAct.setEnabled(False)

    def createActions(self):

        self.openSettingsAct        = QAction("&Open Application Settings...", self, shortcut="Ctrl+O", triggered=self.openSettings)
        self.openIniFileAct         = QAction("&Open INI File...", self, shortcut="Ctrl+N", triggered=self.openIniFile)
        self.openPropertyListAct    = QAction("&Open Mac Property List...", self, shortcut="Ctrl+P", triggered=self.openPropertyList)
        self.openRegistryPathAct    = QAction("&Open Windows &Registry Path...", self, shortcut="Ctrl+G", triggered=self.openRegistryPath)
        self.refreshAct             = QAction("&Refresh", self, shortcut="Ctrl+R", enabled=False, triggered=self.regValue.refresh)
        self.exitAct                = QAction("&Exit", self, shortcut="Ctrl+Q", triggered=self.close)
        self.autoRefreshAct         = QAction("&Auto-Refresh", self, shortcut="Ctrl+A", checkable=True, enabled=False)
        self.fallbacksAct           = QAction("&Fallbacks", self, shortcut="Ctrl+F", checkable=True, enabled=False,  triggered=self.regValue.setFallbacksEnabled)

        if sys.platform != 'darwin':
            self.openPropertyListAct.setEnabled(False)

        if sys.platform != 'win32':
            self.openRegistryPathAct.setEnabled(False)

        self.autoRefreshAct.triggered.connect(self.regValue.setAutoRefresh)
        self.autoRefreshAct.triggered.connect(self.refreshAct.setDisabled)

    def createMenus(self):
        self.createActions()
        self.fileMenu               = self.menubar.addMenu("&File")

        self.fileMenu.addAction(self.openSettingsAct)
        self.fileMenu.addAction(self.openIniFileAct)
        self.fileMenu.addAction(self.openPropertyListAct)
        self.fileMenu.addAction(self.openRegistryPathAct)
        self.fileMenu.addSeparator()

        self.fileMenu.addAction(self.refreshAct)
        self.fileMenu.addSeparator()

        self.fileMenu.addAction(self.exitAct)

        self.optionsMenu            = self.menubar.addMenu("&Options")
        self.optionsMenu.addAction(self.autoRefreshAct)
        self.optionsMenu.addAction(self.fallbacksAct)

    def setSettingsObject(self, settings):
        settings.setFallbacksEnabled(self.fallbacksAct.isChecked())
        self.regValue.setSettingsObject(settings)

        self.refreshAct.setEnabled(True)
        self.autoRefreshAct.setEnabled(True)

        niceName = settings.fileName()
        niceName.replace('\\', '/')
        niceName = niceName.split('/')[-1]

        if not settings.isWritable():
            niceName += " (read only)"

        self.setWindowTitle("%s - Settings Editor" % niceName)

    def setting_mode(self, filename, fm, parent):
        pass



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 11/07/2018 - 1:59 AM
# © 2017 - 2018 DAMGteam. All rights reserved