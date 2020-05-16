#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: BotTab.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from PLM.commons                    import DAMGLIST
from PLM.ui.framework.Gui import AppIcon
from PLM.ui.framework.Widgets import TabWidget, VBoxLayout
from PLM.ui.components.BotTab1      import BotTab1
from PLM.ui.components.BotTab2      import BotTab2

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