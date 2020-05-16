# -*- coding: utf-8 -*-
"""

Script Name: ToolBar.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PLM                                    import __copyright__
from PLM.api.Widgets.io_widgets             import QToolBar


class ToolBar(QToolBar):

    Type                                    = 'DAMGUI'
    key                                     = 'ToolBar'
    _name                                   = 'DAMG Tool Bar'
    _copyright                              = __copyright__()
    actions                                 = []

    def __init__(self, parent=None):
        super(ToolBar, self).__init__(parent)

        self.parent                         = parent

    def add_action(self, action):
        self.actions.append(action)
        return self.addAction(action)

    def add_actions(self, actions):
        for action in actions:
            self.add_action(action)

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