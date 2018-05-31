#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: QuickSetting.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

    This script is the layout part of quick setting for main layout.

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys

# PtQt5
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGridLayout, QCheckBox, QApplication, QWidget

# Plt
import appData as app
from utilities import utils as func

# -------------------------------------------------------------------------------------------------------------
""" Quick Setting """
class QuickSetting(QGridLayout):

    checkboxTDSig = pyqtSignal(bool)
    checkboxCompSig = pyqtSignal(bool)
    checkboxArtSig = pyqtSignal(bool)
    checkboxMasterSig = pyqtSignal(bool)
    checkboxMenuBarSig = pyqtSignal(bool)
    showStatusSig = pyqtSignal(bool)
    showServerStatusSig = pyqtSignal(bool)
    showNotificationSig = pyqtSignal(bool)
    quickSettingSig = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(QuickSetting, self).__init__(parent)

        self.setSpacing(2)
        self.settings = app.APPSETTING

        self.toolBarTDCB = QCheckBox("TD toolbar")
        self.toolBarCompCB = QCheckBox("Comp toolbar")
        self.toolBarArtCB = QCheckBox("Art toolbar")
        self.toolBarCB = QCheckBox("Toolbar")
        self.statusBarCB = QCheckBox("Status Bar")
        self.subMenuBarCB = QCheckBox("Sub Menu")
        self.serverStatusCB = QCheckBox("Server Status")
        self.notificationCB = QCheckBox("Notification")
        self.quickSettingCB = QCheckBox("Quick Setting")

        self.buildUI()

    def buildUI(self):
        quickSettingInfo = dict(
            showTDToolbar = [self.toolBarTDCB, self.checkboxTDSig],
            showCompToolbar =  [self.toolBarCompCB, self.checkboxCompSig],
            showArtToolBar = [self.toolBarArtCB, self.checkboxArtSig],
            showToolBar = [self.toolBarCB, self.checkboxMasterSig],
            showStatusBar = [self.statusBarCB, self.checkboxMenuBarSig],
            showSubMenuBar = [self.subMenuBarCB, self.showStatusSig],
            showServerStatus = [self.serverStatusCB, self.showServerStatusSig],
            showNotificatuon = [self.notificationCB, self.showNotificationSig],
            showQuickSetting = [self.quickSettingCB, self.quickSettingSig]
        )

        for key in quickSettingInfo:
            value = func.str2bool(self.settings.value(key, True))
            quickSettingInfo[key][0].setChecked(value)
            quickSettingInfo[key][1].emit(value)

        self.toolBarTDCB.stateChanged.connect(self.toolBarTDStateChanged)
        self.toolBarCompCB.stateChanged.connect(self.toolBarCompStateChanged)
        self.toolBarArtCB.stateChanged.connect(self.toolBarArtStateChanged)
        self.toolBarCB.stateChanged.connect(self.toolBarStateChanged)
        self.statusBarCB.stateChanged.connect(self.statusBarStateChanged)
        self.subMenuBarCB.stateChanged.connect(self.menuBarStateChanged)
        self.serverStatusCB.stateChanged.connect(self.serverStatusStateChanged)
        self.notificationCB.stateChanged.connect(self.notificationStateChanged)
        self.quickSettingCB.stateChanged.connect(self.quickSettingStateChanged)

        self.addWidget(self.toolBarTDCB, 0, 0, 1, 2)
        self.addWidget(self.toolBarCompCB, 1, 0, 1, 2)
        self.addWidget(self.toolBarArtCB, 2, 0, 1, 2)

        self.addWidget(self.toolBarCB, 0, 2, 1, 2)
        self.addWidget(self.statusBarCB, 1, 2, 1, 2)
        self.addWidget(self.subMenuBarCB, 2, 2, 1, 2)

        self.addWidget(self.serverStatusCB, 0, 4, 1, 2)
        self.addWidget(self.notificationCB, 1, 4, 1, 2)
        self.addWidget(self.quickSettingCB, 2, 4, 1, 2)

    def toolBarTDStateChanged(self):
        self.checkboxTDSig.emit(self.toolBarTDCB.isChecked())

    def toolBarCompStateChanged(self):
        self.checkboxCompSig.emit(self.toolBarCompCB.isChecked())

    def toolBarArtStateChanged(self):
        self.checkboxArtSig.emit(self.toolBarArtCB.isChecked())

    def toolBarStateChanged(self):
        self.settings.setValue("showToolBar", self.toolBarCB.checkState())
        self.checkboxMasterSig.emit(self.toolBarCB.isChecked())

    def menuBarStateChanged(self):
        self.checkboxMenuBarSig.emit(self.subMenuBarCB.isChecked())

    def statusBarStateChanged(self):
        self.showStatusSig.emit(self.statusBarCB.isChecked())

    def serverStatusStateChanged(self):
        self.showServerStatusSig.emit(self.serverStatusCB.isChecked())

    def notificationStateChanged(self):
        self.showNotificationSig.emit(self.notificationCB.isChecked())

    def quickSettingStateChanged(self):
        self.quickSettingSig.emit(self.quickSettingCB.isChecked())


def main():

    app = QApplication(sys.argv)
    quickSetting = QuickSetting()
    quickSetting.show()
    app.exec_()

if __name__ == '__main__':
    main()