#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: ToolBar.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PyQt5
from PyQt5.QtCore           import pyqtSlot, Qt
from PyQt5.QtWidgets        import QScrollArea

# PLM
from appData                import SiPoMin
from devkit.Widgets       import MainWindow, ToolBar, GroupVBox
from utils                  import str2bool, bool2str

# -------------------------------------------------------------------------------------------------------------
""" ToolBar """

class MainToolBar(GroupVBox):

    key                     = 'MainToolBar'
    toolBars                = dict()
    _count                  = 0

    def __init__(self, actionManager, parent=None):
        super(MainToolBar, self).__init__(parent=parent)

        self.parent         = parent
        self.actionManager  = actionManager
        self.mainLayout     = MainWindow(self)

        # self.scrollbar      = QScrollArea()
        # self.scrollbar.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.scrollbar.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.scrollbar.setWidgetResizable(True)
        # self.mainLayout.setCentralWidget(self.scrollbar)

        self.tdToolBar      = self.build_toolBar("TD")
        self.compToolBar    = self.build_toolBar("VFX")
        self.artToolBar     = self.build_toolBar("ART")
        self.textureToolBar = self.build_toolBar('TEX')
        self.postToolBar    = self.build_toolBar('POST')
        self.officeToolBar  = self.build_toolBar('MCO')

        self.tbs = [tb for tb in self.toolBars.values()]

        for tb in self.tbs:
            tb.settings._settingEnable = True
            state = tb.getValue('visible')
            if state is None:
                tb.setVisible(True)
            else:
                tb.setVisible(str2bool(state))

        self.updateWidth()
        self.layout.addWidget(self.mainLayout)

    def updateWidth(self):
        i = 0
        for tb in self.tbs:
            i = i + len(tb.actions)

        for tb in self.tbs:
            if not tb.isVisible():
                i = i - len(tb.actions)

        w = i*32 + i*2
        # if w >=490:
        #     self.scrollbar.setVisible(True)
        # else:
        #     self.scrollbar.setVisible(False)

        self.mainLayout.setMinimumWidth(w)
        # self.parent.setFixedWidth(w + 20)

    def build_toolBar(self, name=''):
        toolBar = ToolBar(self)
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
            actions = self.actionManager.tdToolBarActions(self)
        elif title == 'PRE':
            actions = self.actionManager.preToolBarActrions(self)
        elif title == 'VFX':
            actions = self.actionManager.vfxToolBarActions(self)
        elif title == 'ART':
            actions = self.actionManager.artToolBarActions(self)
        elif title == 'TEX':
            actions = self.actionManager.texToolBarActions(self)
        elif title == 'POST':
            actions = self.actionManager.postToolBarActions(self)
        elif title == 'MCO':
            actions = self.actionManager.officeMenuActions(self)
        else:
            print('WindowTitleError: There is no toolBar name: {0}'.format(title))
            actions = self.actionManager.extraToolActions(self)

        return actions

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, val):
        self._count = val

    @pyqtSlot(str, bool)
    def showToolBar(self, toolbar, mode):
        if toolbar in self.toolBars.keys():
            tb = self.toolBars[toolbar]
            tb.setVisible(str2bool(mode))
            self.settings.initSetValue('visible', bool2str(mode), tb.key)
        else:
            for tb in self.toolBars.values():
                tb.setVisible(str2bool(mode))
                self.settings.iniSetValue('visible', bool2str(mode), tb.key)

    def addToolBar(self, toolbar):
        self.mainLayout.addToolBar(toolbar)


