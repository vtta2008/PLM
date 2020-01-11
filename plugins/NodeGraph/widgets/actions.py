# -*- coding: utf-8 -*-
"""

Script Name: actions.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from devkit.Widgets import Menu, Action
from PyQt5.QtCore import pyqtSignal
from .stylesheet import STYLE_QMENU

class BaseMenu(Menu):

    def __init__(self, *args, **kwargs):
        super(BaseMenu, self).__init__(*args, **kwargs)
        self.setStyleSheet(STYLE_QMENU)

    def hideEvent(self, event):
        super(BaseMenu, self).hideEvent(event)
        for a in self.actions():
            if hasattr(a, 'node_id'):
                a.node_id = None

    def get_menu(self, name):
        for action in self.actions():
            if action.menu() and action.menu().title() == name:
                return action.menu()


class GraphAction(Action):

    executed = pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(GraphAction, self).__init__(*args, **kwargs)
        self.graph = None
        self.triggered.connect(self._on_triggered)

    def _on_triggered(self):
        self.executed.emit(self.graph)

    def get_action(self, name):
        for action in self.qmenu.actions():
            if not action.menu() and action.text() == name:
                return action


class NodeAction(GraphAction):

    executed = pyqtSignal(object, object)

    def __init__(self, *args, **kwargs):
        super(NodeAction, self).__init__(*args, **kwargs)
        self.node_id = None

    def _on_triggered(self):
        node = self.graph.get_node_by_id(self.node_id)
        self.executed.emit(self.graph, node)

    def get_action(self, name):
        for action in self.qmenu.actions():
            if not action.menu() and action.text() == name:
                return action

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 05/01/2020 - 14:49
# © 2017 - 2019 DAMGteam. All rights reserved