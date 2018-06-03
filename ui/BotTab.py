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
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget

# Plt
import appData as app
from ui import uirc as rc
from ui import GeneralSetting

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logger = app.set_log()

# -------------------------------------------------------------------------------------------------------------
""" Bot Tab """
class BotTab(QWidget):

    tbTD = pyqtSignal(bool)
    tbComp = pyqtSignal(bool)
    tbArt = pyqtSignal(bool)
    tbMaster = pyqtSignal(bool)
    subMenu = pyqtSignal(bool)
    statusBar = pyqtSignal(bool)
    serStatus = pyqtSignal(bool)
    notifi = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(BotTab, self).__init__(parent)

        self.settings = app.APPSETTING

        self.layout = QVBoxLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        self.tabs = QTabWidget()

        self.generalSetting = GeneralSetting.GeneralSetting()

        self.generalSetting.tbTD.connect(self.tbTD.emit)
        self.generalSetting.tbComp.connect(self.tbComp.emit)
        self.generalSetting.tbArt.connect(self.tbArt.emit)
        self.generalSetting.tbMaster.connect(self.tbMaster.emit)
        self.generalSetting.subMenu.connect(self.subMenu.emit)
        self.generalSetting.statusBar.connect(self.statusBar.emit)
        self.generalSetting.serStatus.connect(self.serStatus.emit)
        self.generalSetting.notifi.connect(self.notifi.emit)

        self.tabs.addTab(rc.TabContent(self.generalSetting), "General")
        self.tabs.addTab(rc.TabContent(), "Unit")
        self.tabs.addTab(rc.TabContent(), "Quick")

        self.layout.addWidget(self.tabs)

        self.applySetting()

    def applySetting(self):
        self.setSizePolicy(app.SiPoMin, app.SiPoMin)
        self.tabs.setSizePolicy(app.SiPoMin, app.SiPoMin)

        self.tabs.setTabIcon(0, rc.IconPth('General Setting'))
        self.tabs.setTabIcon(1, rc.IconPth('Unit Setting'))
        self.tabs.setTabIcon(2, rc.IconPth('Quick Setting'))

        self.tabs.setTabPosition(QTabWidget.South)
        self.tabs.setMovable(True)


def main():
    app = QApplication(sys.argv)
    layout = BotTab()
    layout.show()
    app.exec_()

if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018