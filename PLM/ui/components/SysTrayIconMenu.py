# -*- coding: utf-8 -*-
"""

Script Name: SysTrayIconMenu.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from PLM.ui.framework.Widgets import Menu

# -------------------------------------------------------------------------------------------------------------

class SysTrayIconMenu(Menu):

    key                             = 'SysTrayIconMenu'
    _login                          = False

    def __init__(self, actionManager, parent=None):
        super(SysTrayIconMenu, self).__init__()

        self.parent                 = parent
        self.actionManager          = actionManager
        self.actions                = self.actionManager.sysTrayMenuActions(self.parent)
        self.loginChanged(self._login)

    def loginChanged(self, val):
        self._login = val
        if not self._login:
            for action in self.actions:
                self.removeAction(action)
            self.addAction(self.actions[-1])
            self.addAction(self.actions[-2])
        else:
            for action in self.actions:
                self.removeAction(action)

            self.addActions(self.actions[3:5])
            self.sep1 = self.addSeparator()
            self.addActions(self.actions[0:3])
            self.addSeparator()
            self.addAction(self.actions[-2])

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