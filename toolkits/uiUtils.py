# -*- coding: utf-8 -*-
"""

Script Name: okButton.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from toolkits                       import ELIDE_RIGHT
from toolkits.Widgets               import (GroupBoxBase, VBoxLayout, HBoxLayout,
                                            Widget, GridLayout, Label, TabWidget, TabBar)

class GroupGrid(GroupBoxBase):

    key = 'GroupGrid'

    def __init__(self, title="", parent=None):
        super(GroupGrid, self).__init__(parent)

        self._title = title
        self.setTitle(self._title)
        self.layout = GridLayout(self)
        self.setLayout(self.layout)

class GroupVBox(GroupBoxBase):

    key = 'GroupVBox'

    def __init__(self, parent=None):
        super(GroupVBox, self).__init__(parent)

        self.layout = VBoxLayout(self)
        self.setLayout(self.layout)

class GroupHBox(GroupBoxBase):

    key = 'GroupHBox'

    def __init__(self, parent=None):
        super(GroupHBox, self).__init__(parent)

        self.layout = HBoxLayout(self)
        self.setLayout(self.layout)

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
        self.tabs = TabWidget()
        tabBar = TabBar()
        self.tabs.setTabBar(tabBar)
        self.tabs.setMovable(True)
        self.tabs.setDocumentMode(True)
        self.tabs.setElideMode(ELIDE_RIGHT)
        self.tabs.setUsesScrollButtons(True)

        content = TabContent()
        tabBar.addAction(content)

        self.layout.addWidget(self.tabs)


def check_preset(data):
    if data == {}:
        pass
    else:
        return True

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 6:05 AM
# © 2017 - 2018 DAMGteam. All rights reserved