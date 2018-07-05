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
from PyQt5.QtWidgets import QGridLayout, QCheckBox, QApplication

# Plt
from core.Settings import Settings
from utilities import utils as func
from appData.Loggers import SetLogger
logger = SetLogger()

# -------------------------------------------------------------------------------------------------------------
""" Quick Setting """
class GeneralSetting(QGridLayout):

    tbTD = pyqtSignal(bool)
    tbComp = pyqtSignal(bool)
    tbArt = pyqtSignal(bool)
    tbMaster = pyqtSignal(bool)
    subMenu = pyqtSignal(bool)
    statusBar = pyqtSignal(bool)
    serStatus = pyqtSignal(bool)
    notifi = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(GeneralSetting, self).__init__(parent)

        self.setSpacing(2)
        # from core.Settings import Settings
        self.settings = Settings(self)

        self.tbTDCB = QCheckBox("TD toolbar")
        self.tbCompCB = QCheckBox("Comp toolbar")
        self.tbArtCB = QCheckBox("Art toolbar")
        self.tbMasterCB = QCheckBox("Toolbar")
        self.statusBarCB = QCheckBox("Status Bar")
        self.subMenuCB = QCheckBox("Sub Menu")
        self.serStatusCB = QCheckBox("Server Status")
        self.notifiCB = QCheckBox("Notification")

        self.buildUI()

    def buildUI(self):

        self.tbTDCB.stateChanged.connect(self.emit_tbTD)
        self.tbCompCB.stateChanged.connect(self.emit_tbComp)
        self.tbArtCB.stateChanged.connect(self.emit_tbArt)
        self.tbMasterCB.stateChanged.connect(self.emit_tbMaster)
        self.statusBarCB.stateChanged.connect(self.emit_statusBar)
        self.subMenuCB.stateChanged.connect(self.emit_subMenu)
        self.serStatusCB.stateChanged.connect(self.emit_serStatus)
        self.notifiCB.stateChanged.connect(self.emit_notifi)

        self.addWidget(self.tbTDCB, 0, 0, 1, 2)
        self.addWidget(self.tbCompCB, 1, 0, 1, 2)
        self.addWidget(self.tbArtCB, 2, 0, 1, 2)

        self.addWidget(self.tbMasterCB, 0, 2, 1, 2)
        self.addWidget(self.statusBarCB, 1, 2, 1, 2)
        self.addWidget(self.subMenuCB, 2, 2, 1, 2)

        self.addWidget(self.serStatusCB, 0, 4, 1, 2)
        self.addWidget(self.notifiCB, 1, 4, 1, 2)

        self.applySetting()

    def applySetting(self):
        keys = ["tbTD", "tbComp", "tbArt", "subMenu", "tbMaster", "statusBar", "serStatus", "notifi"]
        cbs = [self.tbTDCB, self.tbCompCB, self.tbArtCB, self.subMenuCB, self.tbMasterCB, self.statusBarCB, self.serStatusCB, self.notifiCB]
        sigs = [self.tbTD, self.tbComp, self.tbArt, self.subMenu, self.tbMaster, self.statusBar, self.serStatus, self.notifi]
        for key in keys:
            value = func.str2bool(self.settings.value(key, True))
            cbs[keys.index(key)].setChecked(value)
            sigs[keys.index(key)].emit(value)

    def emit_tbTD(self):
        self.tbTD.emit(func.str2bool(self.tbTDCB.checkState()))

    def emit_tbComp(self):
        self.tbComp.emit(func.str2bool(self.tbCompCB.checkState()))

    def emit_tbArt(self):
        self.tbArt.emit(func.str2bool(self.tbArtCB.checkState()))

    def emit_tbMaster(self):
        self.tbMaster.emit(func.str2bool(self.tbMasterCB.checkState()))

    def emit_statusBar(self):
        self.statusBar.emit(func.str2bool(self.statusBarCB.checkState()))

    def emit_subMenu(self):
        self.subMenu.emit(func.str2bool(self.subMenuCB.checkState()))

    def emit_serStatus(self):
        self.serStatus.emit(func.str2bool(self.serStatusCB.checkState()))

    def emit_notifi(self):
        self.notifi.emit(func.str2bool(self.notifiCB.checkState()))


def main():

    app = QApplication(sys.argv)
    quickSetting = GeneralSetting()
    quickSetting.show()
    app.exec_()

if __name__ == '__main__':
    main()