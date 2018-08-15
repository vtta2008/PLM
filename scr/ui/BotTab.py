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
from scr.core.paths import SiPoMin
from scr.core.Loggers import SetLogger
from scr.ui.uikits.UiPreset import IconPth
from scr.ui.GeneralSetting import GeneralSetting
from scr.ui.Debugger import pDebugger
from scr.ui.uikits.TabWidget import TabContent


# -------------------------------------------------------------------------------------------------------------
""" Bot Tab """
class BotTab(QWidget):

    key = 'botTab'

    def __init__(self, parent=None):
        super(BotTab, self).__init__(parent)
        self.logger = SetLogger(self)
        self.layout = QVBoxLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        self.tabs = QTabWidget()

        self.generalSetting = GeneralSetting()
        self.debugger = pDebugger()

        self.tabs.addTab(TabContent(self.generalSetting), "General")
        self.tabs.addTab(TabContent(), "Unit")
        self.tabs.addTab(TabContent(self.debugger), "Debug")
        # self.tabs.addTab(TabContent(), "Quick")

        self.layout.addWidget(self.tabs)
        self.applySetting()

    def applySetting(self):
        self.setSizePolicy(SiPoMin, SiPoMin)
        self.tabs.setSizePolicy(SiPoMin, SiPoMin)

        self.tabs.setTabIcon(0, IconPth(32, 'General Setting'))
        self.tabs.setTabIcon(1, IconPth(32, 'Unit Setting'))
        self.tabs.setTabIcon(2, IconPth(32, 'Debug'))
        # self.tabs.setTabIcon(3, IconPth(32, 'Quick Setting'))

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