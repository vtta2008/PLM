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
from PyQt5.QtWidgets        import QApplication, QVBoxLayout, QTabWidget

# PLM
from appData                import SiPoMin
from cores.Loggers          import Loggers
from ui.Debugger            import Debugger
from ui.GeneralSetting      import GeneralSetting
from ui.uikits.TabWidget    import TabContent
from ui.uikits.Widget       import Widget
from ui.uikits.UiPreset     import IconPth, VBoxLayout

# -------------------------------------------------------------------------------------------------------------
""" Bot Tab """
class BotTab(Widget):

    key = 'botTab'

    def __init__(self, parent=None):
        super(BotTab, self).__init__(parent)
        self.logger         = Loggers(__file__)


        self.buildUI()

        self.applySetting()

    def buildUI(self):
        layout = VBoxLayout()
        self.tabs           = QTabWidget()

        self.generalSetting = GeneralSetting()
        self.debugger       = Debugger()

        self.tabs.addTab(TabContent(self.generalSetting), "General")
        # self.tabs.addTab(TabContent(), "Unit")
        self.tabs.addTab(TabContent(self.debugger), "Debug")
        # self.tabs.addTab(TabContent(), "Quick")

        self.tabs.setTabIcon(0, IconPth(32, 'General Setting'))
        # self.tabs.setTabIcon(1, IconPth(32, 'Unit Setting'))
        self.tabs.setTabIcon(2, IconPth(32, 'Debug'))
        # self.tabs.setTabIcon(3, IconPth(32, 'Quick Setting'))

        self.tabs.setSizePolicy(SiPoMin, SiPoMin)
        self.tabs.setTabPosition(QTabWidget.South)
        self.tabs.setMovable(True)

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def applySetting(self):
        self.setSizePolicy(SiPoMin, SiPoMin)




def main():
    bottab = QApplication(sys.argv)
    layout = BotTab()
    layout.show()
    bottab.exec_()

if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018