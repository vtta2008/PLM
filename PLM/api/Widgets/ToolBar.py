# -*- coding: utf-8 -*-
"""

Script Name: ToolBar.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from .io_widgets import QToolBar
from PLM.settings import AppSettings

class ToolBar(QToolBar):

    Type                                    = 'DAMGUI'
    key                                     = 'ToolBar'
    _name                                   = 'DAMG Tool Bar'
    actions                                 = []

    def __init__(self, parent=None):
        super(ToolBar, self).__init__(parent)

        self.parent                         = parent
        self.settings                       = AppSettings(self)

    def add_action(self, action):
        self.actions.append(action)
        return self.addAction(action)

    def add_actions(self, actions):
        for action in actions:
            self.add_action(action)

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key, decode=None):
        if decode is None:
            return self.settings.initValue(key, self.key)
        else:
            return self.settings.initValue(key, self.key, decode)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 31/07/2018 - 12:50 AM
# © 2017 - 2018 DAMGteam. All rights reserved