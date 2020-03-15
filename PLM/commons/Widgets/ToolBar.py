# -*- coding: utf-8 -*-
"""

Script Name: ToolBar.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__
""" Import """

# PyQt5
from PyQt5.QtWidgets                        import QToolBar

from PLM.cores import SettingManager
from PLM.cores import SignalManager

# -------------------------------------------------------------------------------------------------------------
""" Tool bar class """

class ToolBar(QToolBar):

    Type                                    = 'DAMGUI'
    key                                     = 'ToolBar'
    _name                                   = 'DAMG Tool Bar'
    _copyright                              = __copyright__()
    actions                                 = []

    def __init__(self, parent=None):
        QToolBar.__init__(self)

        self.parent                         = parent
        self.settings                       = SettingManager(self)
        self.signals                        = SignalManager(self)
        self.setWindowTitle(self._name)

    def add_action(self, action):
        self.actions.append(action)
        return self.addAction(action)

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key, decode=None):
        if decode is None:
            return self.settings.initValue(key, self.key)
        else:
            return self.settings.initValue(key, self.key, decode)

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 31/07/2018 - 12:50 AM
# © 2017 - 2018 DAMGteam. All rights reserved