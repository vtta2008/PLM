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
from PLM.commons                import DAMGLIST
from PLM.commons.Widgets        import TabWidget, VBoxLayout
from PLM.commons.Gui            import AppIcon
from PLM.ui.components          import TopTab1, TopTab2, TopTap3

# -------------------------------------------------------------------------------------------------------------
""" Tab Layout """

class TopTab(TabWidget):

    key                         = 'TopTab'

    def __init__(self, buttonManager, parent=None):
        super(TopTab, self).__init__(parent)

        self.parent             = parent
        self.layout             = VBoxLayout()
        self.buttonManager      = buttonManager

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
            if tab.key == 'TopTab2':
                if not self.parent.connectServer:
                    pass
                else:
                    self.addTab(tab, self.tabNames[self.tabs.index(tab)])
                    self.setTabIcon(self.tabs.index(tab), AppIcon(32, self.tabNames[self.tabs.index(tab)]))
            else:
                self.addTab(tab, self.tabNames[self.tabs.index(tab)])
                self.setTabIcon(self.tabs.index(tab), AppIcon(32, self.tabNames[self.tabs.index(tab)]))



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018