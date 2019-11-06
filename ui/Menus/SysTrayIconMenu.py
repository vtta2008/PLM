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

    def __init__(self, actionManager, parent=None):
        super(SysTrayIconMenu, self).__init__(parent)

        self.actionManager      = actionManager
        actions                 = self.actionManager.sysTrayMenuActions(self.parent)

        self.addActions(actions[3:5])
        self.addSeparator()
        self.addActions(actions[0:3])
        self.addSeparator()
        self.addAction(actions[-1])

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 6:28 PM
# © 2017 - 2018 DAMGteam. All rights reserved