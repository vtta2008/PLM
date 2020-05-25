#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: BotTab.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from PLM.api.damg import DAMGLIST
from PLM.api.Gui import AppIcon
from PLM.api.Widgets import TabWidget, VBoxLayout
from PLM.ui.components import BotTab1, BotTab2

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
            self.addTab(layout, AppIcon(32, self.tabNames[self.tabs.index(layout)]), self.tabNames[self.tabs.index(layout)])
            self.setTabIcon(self.tabs.index(layout), AppIcon(32, self.tabNames[self.tabs.index(layout)]))


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018