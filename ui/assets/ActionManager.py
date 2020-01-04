# -*- coding: utf-8 -*-
"""

Script Name: ActionManager.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from ui.base                    import KeyBase

class ActionManager(KeyBase):

    key                         = 'ActionManager'
    _name                       = 'ActionManager'

    def __init__(self, parent=None):
        super(ActionManager, self).__init__(self)
        self.parent             = parent

    def register(self, action):
        if not action.key in self.keys():
            self[action.key] = action
        else:
            self.actionRegisterError(action.key)

    def actions(self):
        return self.values()

    def preToolbarActions(self, parent):
        return self.createActions(self.preActions, parent)

    def officeToolBarActions(self, parent):
        return self.createActions(self.officeActions, parent)

    def editMenuActions(self, parent):
        return self.createActions(self.editActions, parent)

    def viewMenuActions(self, parent):
        return self.createActions(self.viewActions, parent)

    def extraToolActions(self, parent):
        return self.createActions(self.extraActions, parent)

    def tdToolBarActions(self, parent):
        return self.createActions(self.tdActions, parent)

    def artToolBarActions(self, parent):
        return self.createActions(self.artActions, parent)

    def texToolBarActions(self, parent):
        return self.createActions(self.texActions, parent)

    def postToolBarActions(self, parent):
        return self.createActions(self.postActions, parent)

    def vfxToolBarActions(self, parent):
        return self.createActions(self.vfxActions, parent)

    def sysTrayMenuActions(self, parent):
        return self.createActions(self.sysTrayActions, parent)

    def appMenuActions(self, parent):
        return self.createActions(self.appActions, parent)

    def orgMenuActions(self, parent):
        return self.createActions(self.orgActions, parent)

    def teamMenuActions(self, parent):
        return self.createActions(self.teamActions, parent)

    def stylesheetMenuActions(self, parent):
        return self.createActions(self.stylesheetActions, parent)

    def projectMenuActions(self, parent):
        return self.createActions(self.prjActions, parent)

    def taskMenuActions(self, parent):
        return self.createActions(self.taskActions, parent)

    def goMenuActions(self, parent):
        return self.createActions(self.goActions, parent)

    def officeMenuActions(self, parent):
        return self.createActions(self.officeActions, parent)

    def toolsMenuActions(self, parent):
        return self.createActions(self.toolsActions, parent)

    def devMenuActions(self, parent):
        return self.createActions(self.devActions, parent)

    def libMenuActions(self, parent):
        return self.createActions(self.libActions, parent)

    def helpMenuActions(self, parent):
        return self.createActions(self.helpActions, parent)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/11/2019 - 5:26 PM
# © 2017 - 2018 DAMGteam. All rights reserved