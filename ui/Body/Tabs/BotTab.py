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
from bin.data.damg                      import DAMGLIST

# PyQt5
from PyQt5.QtWidgets                    import QApplication
from PyQt5.QtGui                        import QResizeEvent

# PLM
from ui.Body.Tabs.BotTab2               import BotTab2
from ui.Body.Tabs.BotTab1               import BotTab1
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

        self.botTab1                    = BotTab1(self.parent)
        self.botTab2                    = BotTab2(self.parent)

        self.tabs                       = DAMGLIST(listData=[self.botTab1, self.botTab2])
        self.tabNames                   = DAMGLIST(listData=['General', 'Debug'])

        for layout in self.tabs:
            # layout.signals.connect('executing', self.signals.executing)
            # layout.signals.connect('regisLayout', self.signals.regisLayout)
            # layout.signals.connect('openBrowser', self.signals.openBrowser)
            # layout.signals.connect('setSetting', self.signals.setSetting)
            # layout.signals.connect('showLayout', self.signals.showLayout)
            # layout.settings._settingEnable = True

            self.addTab(layout, AppIcon(32, self.tabNames[self.tabs.index(layout)]), self.tabNames[self.tabs.index(layout)])
            self.setTabIcon(self.tabs.index(layout), AppIcon(32, self.tabNames[self.tabs.index(layout)]))

    # def resizeEvent(self, event):
    #     w = self.width()
    #     h = self.height()
    #     for tab in self.tabs:
    #         tab.resize(w-2, h-2)

def main():
    bottab = QApplication(sys.argv)
    layout = BotTab()
    layout.show()
    bottab.exec_()

if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018