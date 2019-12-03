#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Name: TopTabWidget.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PLM
from toolkits.Widgets           import TabWidget, VBoxLayout, AppIcon
from .Tabs                      import TopTab1, TopTab2, TopTap3, SceneGraph
from bin                        import DAMGLIST

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

        self.tab1               = TopTab1(self.buttonManager, self.parent)
        # self.tab1               = SceneGraph(self.buttonManager, self.parent)
        self.tab2               = TopTab2(self.buttonManager, self.parent)
        self.tab3               = TopTap3(self.buttonManager, self.parent)
        # self.tab4               = SceneGraph(self.parent)

        self.tabs               = DAMGLIST(listData=[self.tab1, self.tab2, self.tab3])
        self.tabNames           = DAMGLIST(listData=['Common', 'User', 'Cmd'])

        for tab in self.tabs:
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

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018