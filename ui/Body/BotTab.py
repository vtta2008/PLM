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
from bin                                import DAMGLIST

# PLM
from ui.Body.Tabs.BotTab2               import BotTab2
from ui.Body.Tabs.BotTab1               import BotTab1
from toolkits.Widgets                   import TabWidget, AppIcon, VBoxLayout

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
        self.tabNames                   = DAMGLIST(listData=['Tracking', 'Debug'])

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
    #         tab.resize(w - 4, h - 4)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018