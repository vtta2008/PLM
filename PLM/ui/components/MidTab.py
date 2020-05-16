#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Name: TopTabWidget.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import requests

# PLM
from PLM.configs                import __localServer__
from PLM.commons                import DAMGLIST
from PLM.api.Widgets import TabWidget, VBoxLayout
from PLM.api.Gui import AppIcon
from .MidTab1                   import MidTab1
from .MidTab2                   import MidTab2
from .MidTab3                   import MidTab3

# -------------------------------------------------------------------------------------------------------------
""" Tab Layout """

class MidTab(TabWidget):

    key                         = 'TopTab'

    def __init__(self, buttonManager, parent=None):
        super(MidTab, self).__init__(parent)

        self.parent             = parent
        self.layout             = VBoxLayout()
        self.buttonManager      = buttonManager

        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.tab1               = MidTab1(self.buttonManager, self)
        self.tab2               = MidTab2(self.buttonManager, self)
        self.tab3               = MidTab3(self.buttonManager, self)


        self.tabs               = DAMGLIST(listData=[self.tab1, self.tab2, self.tab3])
        self.tabNames           = DAMGLIST(listData=['Common', 'User', 'Cmd'])

        for tab in self.tabs:
            if tab.key == 'TopTab2':
                if self.test_connectServer():
                    self.addTab(tab, self.tabNames[self.tabs.index(tab)])
                    self.setTabIcon(self.tabs.index(tab), AppIcon(32, self.tabNames[self.tabs.index(tab)]))
            else:
                self.addTab(tab, self.tabNames[self.tabs.index(tab)])
                self.setTabIcon(self.tabs.index(tab), AppIcon(32, self.tabNames[self.tabs.index(tab)]))

    def test_connectServer(self):

        try:
            requests.get(__localServer__)
        except requests.exceptions.ConnectionError:
            self.logger.info('Cannot connect to server')
            return False
        else:
            return True

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018