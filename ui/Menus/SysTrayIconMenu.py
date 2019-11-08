# -*- coding: utf-8 -*-
"""

Script Name: SysTrayIconMenu.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from ui.uikits.Menu import Menu

# -------------------------------------------------------------------------------------------------------------

class SysTrayIconMenu(Menu):

    key = 'SysTrayIconMenu'
    _login = False

    def __init__(self, actionManager, parent=None):
        super(SysTrayIconMenu, self).__init__(parent)

        self.actionManager      = actionManager
        self.actions                 = self.actionManager.sysTrayMenuActions(self.parent)

    def loginChanged(self, val):
        self._login = val
        if not self._login:
            self.removeAction(self.sep1)
            for action in self.actions[0:3]:
                self.removeAction(action)
        else:
            for action in self.actions:
                self.removeAction(action)

            self.addActions(self.actions[3:5])
            self.sep1 = self.addSeparator()
            self.addActions(self.actions[0:3])
            self.addSeparator()
            self.addAction(self.actions[-1])

        return self._login

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, val):
        self._login = val

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 6:28 PM
# © 2017 - 2018 DAMGteam. All rights reserved