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
from bin.data.damg                               import DAMGLIST

# PyQt5
from PyQt5.QtWidgets                    import QApplication

# PLM
from ui.Body.Tabs.BotTab2 import BotTab2
from ui.Body.Tabs.BotTab1 import BotTab1
from ui.uikits.TabWidget                import TabWidget
from ui.uikits.BoxLayout                import VBoxLayout
from ui.uikits.Icon                     import AppIcon

# -------------------------------------------------------------------------------------------------------------
""" Bot Tab """
class BotTab(TabWidget):

    key = 'BotTab'

    def __init__(self, parent=None):
        super(BotTab, self).__init__(parent)

        self.parent = parent
        self.layout = VBoxLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.botTab1        = BotTab1(self)
        self.botTab2        = BotTab2(self)

        self.tabLst         = DAMGLIST(listData=[self.botTab1, self.botTab2])
        self.tabNames       = DAMGLIST(listData=['General', 'Debug'])

        for layout in self.tabLst:
            # layout.signals.showLayout.connect(self.signals.showLayout)
            # layout.signals.executing.connect(self.signals.executing)
            # layout.signals.regisLayout.connect(self.signals.regisLayout)
            # layout.signals.setSetting.connect(self.signals.setSetting)
            # layout.signals.openBrowser.connect(self.signals.openBrowser)

            self.addTab(layout, AppIcon(32, self.tabNames[self.tabLst.index(layout)]), self.tabNames[self.tabLst.index(layout)])
            self.setTabIcon(self.tabLst.index(layout), AppIcon(32, self.tabNames[self.tabLst.index(layout)]))

    # def hideEvent(self, event):
    #     self.setValue('currentTab', self.currentWidget())
    #
    # def closeEvent(self, event):
    #     self.setValue('currentTab', self.currentWidget().key)

def main():
    bottab = QApplication(sys.argv)
    layout = BotTab()
    layout.show()
    bottab.exec_()

if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018