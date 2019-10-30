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
from PyQt5.QtWidgets        import QApplication

# PLM
from ui.Debugger            import Debugger
from ui.GeneralSetting      import GeneralSetting
from ui.uikits.Widget                 import Widget
from ui.uikits.TabWidget import TabWidget, TabContent
from ui.uikits.BoxLayout import VBoxLayout
from ui.uikits.Icon import AppIcon

# -------------------------------------------------------------------------------------------------------------
""" Bot Tab """
class BotTab(Widget):

    key = 'BotTab'

    def __init__(self, parent=None):
        super(BotTab, self).__init__(parent)

        self.layout = VBoxLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        self.tabs           = TabWidget()

        self.generalSetting = GeneralSetting()
        self.debugger       = Debugger()

        self.tabs.addTab(TabContent(self.generalSetting), "General")
        self.tabs.addTab(TabContent(self.debugger), "Debug")
        self.tabs.setTabIcon(0, AppIcon(32, 'General Setting'))
        self.tabs.setTabIcon(2, AppIcon(32, 'Debug'))


        self.tabs.setTabPosition(TabWidget.South)
        self.tabs.setMovable(True)

        self.layout.addWidget(self.tabs)

def main():
    bottab = QApplication(sys.argv)
    layout = BotTab()
    layout.show()
    bottab.exec_()

if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018