#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: BotTab.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from pyPLM.damg import DAMGLIST
from pyPLM.Gui import AppIcon
from pyPLM.Widgets import TabWidget, VBoxLayout
from .BotTab1 import BotTab1
from .BotTab2 import BotTab2

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

        self.tabs                       = DAMGLIST(listData=[self.botTab1, ])
        self.tabNames                   = DAMGLIST(listData=['Console', ])

        for layout in self.tabs:
            self.addTab(layout, AppIcon(32, self.tabNames[self.tabs.index(layout)]), self.tabNames[self.tabs.index(layout)])
            self.setTabIcon(self.tabs.index(layout), AppIcon(32, self.tabNames[self.tabs.index(layout)]))


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018