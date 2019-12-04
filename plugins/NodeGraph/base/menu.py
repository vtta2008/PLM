# -*- coding: utf-8 -*-
"""

Script Name: menu.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from plugins.NodeGraph.widgets  import STYLE_QMENU
from distutils.version          import LooseVersion
from PyQt5.QtWidgets            import QAction, QMenu
from PyQt5.QtGui                import QKeySequence
from PyQt5.QtCore               import qVersion

class Menu(object):

    def __init__(self, viewer, qmenu):
        self.__viewer = viewer
        self.__qmenu = qmenu

    def __repr__(self):
        cls_name = self.__class__.__name__
        return '<{}("{}") object at {}>'.format(cls_name, self.name(), hex(id(self)))

    @property
    def qmenu(self):
        return self.__qmenu

    def name(self):
        return self.qmenu.title()

    def get_menu(self, name):
        for action in self.qmenu.actions():
            if action.menu() and action.menu().title() == name:
                return Menu(self.__viewer, action.menu())

    def get_command(self, name):
        for action in self.qmenu.actions():
            if not action.menu() and action.text() == name:
                return MenuCommand(self.__viewer, action)

    def all_commands(self):
        def get_actions(menu):
            actions = []
            for action in menu.actions():
                if not action.menu():
                    if not action.isSeparator():
                        actions.append(action)
                else:
                    actions += get_actions(action.menu())
            return actions
        child_actions = get_actions(self.qmenu)
        return [MenuCommand(self.__viewer, a) for a in child_actions]

    def add_menu(self, name):

        menu = QMenu(name, self.qmenu)
        menu.setStyleSheet(STYLE_QMENU)
        self.qmenu.addMenu(menu)
        return Menu(self.__viewer, menu)

    def add_command(self, name, func=None, shortcut=None):

        action = QAction(name, self.__viewer)
        if LooseVersion(qVersion()) >= LooseVersion('5.10'):
            action.setShortcutVisibleInContextMenu(True)
        if shortcut:
            action.setShortcut(shortcut)
        if func:
            action.triggered.connect(func)
        qaction = self.qmenu.addAction(action)
        return MenuCommand(self.__viewer, qaction)

    def add_separator(self):
        self.qmenu.addSeparator()


class MenuCommand(object):

    def __init__(self, viewer, qaction):
        self.__viewer = viewer
        self.__qaction = qaction

    def __repr__(self):
        cls_name = self.__class__.__name__
        return 'NodeGraphQt.{}(\'{}\')'.format(cls_name, self.name())

    @property
    def qaction(self):
        return self.__qaction

    def name(self):
        return self.qaction.text()

    def set_shortcut(self, shortcut=None):

        shortcut = shortcut or QKeySequence()
        self.qaction.setShortcut(shortcut)

    def run_command(self):

        self.qaction.trigger()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 4/12/2019 - 1:31 AM
# © 2017 - 2018 DAMGteam. All rights reserved