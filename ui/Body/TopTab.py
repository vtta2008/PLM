#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Name: TopTabWidget.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys
from bin.dependencies.damg.damg import DAMGLIST

# PLM
from ui.uikits.Icon             import AppIcon
from ui.uikits.BoxLayout        import VBoxLayout
from ui.uikits.TabWidget        import TabWidget
from ui.Body.Tabs               import TopTab1, TopTap3, TopTab2

# -------------------------------------------------------------------------------------------------------------
""" Tab Layout """

class TopTab(TabWidget):

    key                         = 'TopTab'

    def __init__(self, buttonManager, parent=None):
        super(TopTab, self).__init__(parent)

        self.parent             = parent
        self.layout             = VBoxLayout()
        self.buttonManager      = buttonManager
        self.mode               = self.parent.mode
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.tab1               = TopTab1.TopTab1(self.buttonManager, self.parent)
        self.tab2               = TopTab2.TopTab2(self.buttonManager, self.parent)
        self.tab3               = TopTap3.TopTap3(self.buttonManager, self.parent)

        self.tabs               = DAMGLIST(listData=[self.tab1, self.tab2, self.tab3])
        self.tabNames           = DAMGLIST(listData=['Common', 'User', 'Cmd'])

        for tab in self.tabs:
            # tab.signals.connect('executing', self.signals.executing)
            # tab.signals.connect('regisLayout', self.signals.regisLayout)
            # tab.signals.connect('openBrowser', self.signals.openBrowser)
            # tab.signals.connect('setSetting', self.signals.setSetting)
            # tab.signals.connect('showLayout', self.signals.showLayout)
            # tab.settings._settingEnable = True
            if self.mode == 'Offline':
                if tab.key == 'TopTab2':
                    pass
                else:
                    self.addTab(tab, self.tabNames[self.tabs.index(tab)])
                    self.setTabIcon(self.tabs.index(tab), AppIcon(32, self.tabNames[self.tabs.index(tab)]))
            else:
                self.addTab(tab, self.tabNames[self.tabs.index(tab)])
                self.setTabIcon(self.tabs.index(tab), AppIcon(32, self.tabNames[self.tabs.index(tab)]))

        self.signals.updateAvatar.connect(self.tab2.update_avatar)

    # def resizeEvent(self, event):
    #     w = self.width()
    #     h = self.height()
    #     for tab in self.tabs:
    #         tab.resize(w-4, h-4)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018