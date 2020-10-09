#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: ToolBar.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PLM
from PLM.options import SiPoMin
from bin.Widgets import MainWindow, ToolBar, GroupHBox
from bin.Core import Size
from PLM.utils import str2bool, bool2str
from PLM.cores.Errors import ToolbarNameError

# -------------------------------------------------------------------------------------------------------------
""" ToolBar """

class MainToolBar(GroupHBox):

    key                                 = 'MainToolBar'
    toolBars                            = dict()
    _count                              = 0

    def __init__(self, actionManager, parent=None):
        super(MainToolBar, self).__init__(parent=parent)

        self.parent                     = parent
        self.actionManager              = actionManager
        self.mainLayout                 = MainWindow(self.parent)
        self.layout.addWidget(self.mainLayout)

        self.tdToolBar                  = self.build_toolBar("TD")
        self.compToolBar                = self.build_toolBar("VFX")
        self.artToolBar                 = self.build_toolBar("ART")
        self.textureToolBar             = self.build_toolBar('TEX')
        self.preToolBar                 = self.build_toolBar('PRE')
        self.postToolBar                = self.build_toolBar('POST')
        self.officeToolBar              = self.build_toolBar('MCO')
        self.devToolBar                 = self.build_toolBar('DEV')
        self.toolToolBar                = self.build_toolBar('TOOL')
        self.extraToolBar               = self.build_toolBar('EXTRA')
        self.systrayToolBar             = self.build_toolBar('SYSTRAY')

        self.tbs                        = [tb for tb in self.toolBars.values()]

        for tb in self.tbs:
            tb.settings._settingEnable = True
            state = tb.getValue('visible')
            if state is None:
                tb.setVisible(True)
            else:
                tb.setVisible(str2bool(state))

        for tb in [self.artToolBar, self.officeToolBar, self.devToolBar, self.toolToolBar, self.extraToolBar,
                   self.systrayToolBar, self.compToolBar, self.preToolBar]:
            tb.setVisible(False)

        self.updateWidth()

    def build_toolBar(self, name=''):

        toolBar = ToolBar(self)
        toolBar.setIconSize(Size(24, 24))
        toolBar.key = '{0}_{1}'.format(self.key, name)
        toolBar._name = toolBar.key
        toolBar.setWindowTitle(name)

        actions = self.getActions(name)

        for action in actions:
            toolBar.add_action(action)

        toolBar.setSizePolicy(SiPoMin, SiPoMin)
        toolBar.visibilityChanged.connect(self.updateWidth)
        self.toolBars[name] = toolBar
        self.addToolBar(toolBar)
        return toolBar

    def getActions(self, title):
        if title == 'TD':
            actions = self.actionManager.tdToolBarActions(self.parent)
        elif title == 'PRE':
            actions = self.actionManager.preToolbarActions(self.parent)
        elif title == 'VFX':
            actions = self.actionManager.vfxToolBarActions(self.parent)
        elif title == 'ART':
            actions = self.actionManager.artToolBarActions(self.parent)
        elif title == 'TEX':
            actions = self.actionManager.texToolBarActions(self.parent)
        elif title == 'POST':
            actions = self.actionManager.postToolBarActions(self.parent)
        elif title == 'MCO':
            actions = self.actionManager.officeMenuActions(self.parent)
        elif title == 'DEV':
            actions = self.actionManager.devToolbarActions(self.parent)
        elif title == 'TOOL':
            actions = self.actionManager.toolsMenuActions(self.parent)
        elif title == 'EXTRA':
            actions = self.actionManager.extraToolbarActions(self.parent)
        elif title == 'SYSTRAY':
            actions = self.actionManager.sysTrayMenuActions(self.parent)
        else:
            print(ToolbarNameError('There is no toolBar name: {0}'.format(title)))

        return actions

    def show_toolBar(self, toolbar, mode):
        if toolbar in self.toolBars.keys():
            tb = self.toolBars[toolbar]
            tb.setVisible(str2bool(mode))
            self.settings.initSetValue('visible', bool2str(mode), tb.key)
        else:
            for tb in self.toolBars.values():
                tb.setVisible(str2bool(mode))
                self.settings.iniSetValue('visible', bool2str(mode), tb.key)

    def add_actions_to_menu(self, menu, actions):
        for action in actions:
            menu.addAction(action)

    def updateWidth(self):
        i = 0
        for tb in self.tbs:
            if tb.isVisible():
                i += 1
        w = i*32
        self.setMinimumWidth(w)

    def addToolBar(self, toolbar):
        self.mainLayout.addToolBar(toolbar)

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, val):
        self._count = val




