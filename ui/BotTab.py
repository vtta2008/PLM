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
from appData import SiPoMin
from core.Loggers import SetLogger
from ui.uikits.UiPreset import IconPth
from ui.GeneralSetting import GeneralSetting
from ui.uikits.TabWidget import TabContent


# -------------------------------------------------------------------------------------------------------------
""" Bot Tab """
class BotTab(QWidget):

    key = 'botTab'
    loadSetting = pyqtSignal(str, str)
    returnValue = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(BotTab, self).__init__(parent)
        self.logger = SetLogger(self)
        self.layout = QVBoxLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        self.tabs = QTabWidget()

        self.generalSetting = GeneralSetting()

        self.tabs.addTab(TabContent(self.generalSetting), "General")
        self.tabs.addTab(TabContent(), "Debug")
        # self.tabs.addTab(TabContent(), "Unit")
        # self.tabs.addTab(TabContent(), "Quick")

        self.layout.addWidget(self.tabs)
        self.generalSetting.loadSetting.connect(self.loadSetting)
        self.returnValue.connect(self.generalSetting.return_setting)
        self.applySetting()

    def applySetting(self):
        self.setSizePolicy(SiPoMin, SiPoMin)
        self.tabs.setSizePolicy(SiPoMin, SiPoMin)

        self.tabs.setTabIcon(0, IconPth(32, 'General Setting'))
        self.tabs.setTabIcon(1, IconPth(32, 'Debug'))
        self.tabs.setTabIcon(2, IconPth(32, 'Unit Setting'))
        self.tabs.setTabIcon(3, IconPth(32, 'Quick Setting'))

        self.tabs.setTabPosition(QTabWidget.South)
        self.tabs.setMovable(True)


def main():
    bottab = QApplication(sys.argv)
    layout = BotTab()
    layout.show()
    bottab.exec_()

if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018