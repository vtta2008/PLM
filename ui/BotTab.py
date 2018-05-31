#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: BotTab.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys

# PyQt5
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QSizePolicy

# Plt
import appData as app

from ui import uirc as rc
from ui import QuickSetting
from utilities import utils as func

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logger = app.set_log()

# -------------------------------------------------------------------------------------------------------------
# Get apps info config
APPINFO = func.preset_load_appInfo()

# -------------------------------------------------------------------------------------------------------------
""" Tab Widget """

class TabWidget(QWidget):

    def __init__(self, layout, parent=None):
        super(TabWidget, self).__init__(parent)

        self.settings = app.APPSETTING
        self.layout = layout
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.applySetting()

    def applySetting(self):

        pass


# -------------------------------------------------------------------------------------------------------------
""" Bot Tab """
class BotTab(QWidget):

    tdToolBarSig = pyqtSignal(bool)
    compToolBarSig = pyqtSignal(bool)
    artToolBarSig = pyqtSignal(bool)
    toolBarSig = pyqtSignal(bool)
    subMenuSig = pyqtSignal(bool)
    statusBarSig = pyqtSignal(bool)
    serverStatSig = pyqtSignal(bool)
    notifiSig = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(BotTab, self).__init__(parent)

        self.settings = app.APPSETTING

        self.layout = QVBoxLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        self.tabs = QTabWidget()

        self.quickSetting = QuickSetting.QuickSetting()

        self.quickSetting.checkboxTDSig.connect(self.tdToolBarSig.emit)
        self.quickSetting.checkboxCompSig.connect(self.compToolBarSig.emit)
        self.quickSetting.checkboxArtSig.connect(self.artToolBarSig.emit)
        self.quickSetting.checkboxMasterSig.connect(self.toolBarSig.emit)
        self.quickSetting.checkboxMenuBarSig.connect(self.subMenuSig.emit)
        self.quickSetting.showStatusSig.connect(self.statusBarSig.emit)
        self.quickSetting.showServerStatusSig.connect(self.serverStatSig.emit)
        self.quickSetting.showNotificationSig.connect(self.notifiSig.emit)
        self.quickSetting.showNotificationSig.connect(self.show_hide_quickSetting)

        self.tabs.addTab(QWidget(), "General")
        self.tabs.addTab(QWidget(), "Unit")
        self.tabs.addTab(rc.TabContent(self.quickSetting), "Quick")

        self.layout.addWidget(self.tabs)

        self.applySetting()

    def show_hide_quickSetting(self, param):
        self.show_hide_statusBar(param)
        self.show_hide_toolBar(param)
        self.show_hide_sub_menu(param)
        self.show_hide_serverStatus(param)
        self.show_hide_notification(param)
        self.settings.setValue("showMasterQuickSetting", param)
        self.quickSetting.setVisible(param)

    def applySetting(self):
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.tabs.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)


def main():
    app = QApplication(sys.argv)
    layout = BotTab()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018