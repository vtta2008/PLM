# -*- coding: utf-8 -*-
"""

Script Name: okButton.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from appData                        import ELIDE_RIGHT
from .Widgets                       import Widget, GridLayout, Label, TabWidget, TabBar

class TabContent(Widget):

    key = 'TabContent'

    def __init__(self, layout=None, parent=None):
        super(TabContent, self).__init__(parent)

        if layout is None:
            layout = GridLayout()
            layout.addWidget(Label())

        self.layout = layout
        self.setLayout(self.layout)

class Tabs(Widget):

    key = 'Tabs'

    def __init__(self, parent=None):
        super(Tabs, self).__init__(parent)
        self.layout = GridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        self.tabs               = TabWidget()
        tabBar                  = TabBar()
        self.tabs.setTabBar(tabBar)
        self.tabs.setMovable(True)
        self.tabs.setDocumentMode(True)
        self.tabs.setElideMode(ELIDE_RIGHT)
        self.tabs.setUsesScrollButtons(True)

        content = TabContent()
        tabBar.addAction(content)

        self.layout.addWidget(self.tabs)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 6:05 AM
# © 2017 - 2018 DAMGteam. All rights reserved