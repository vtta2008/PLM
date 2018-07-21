# -*- coding: utf-8 -*-
"""

Script Name: ToolBarDock.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

import sys
from functools import partial

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QToolBar, QDockWidget, QGridLayout

from appData import APPINFO, CONFIG_TDS, CONFIG_VFX, CONFIG_ART, SiPoExp
from ui.Libs.Action import Action

TOOLBAR_DATA = dict(TD = CONFIG_TDS, VFX = CONFIG_VFX, ART = CONFIG_ART)

class ToolBar(QToolBar):

    executing = pyqtSignal(str)

    def __init__(self, key, parent=None):
        super(ToolBar, self).__init__(parent)
        self.appInfo = APPINFO
        self._parent = parent
        self.key = key
        self.acts = []
        self.tbData = TOOLBAR_DATA
        self.add_actions()
        self.applySetting()

    def add_actions(self):
        apps = self.tbData[self.key]
        for app in apps:
            if app in self.appInfo:
                action = Action({'icon': app, 'stt': self.appInfo[app][0], 'txt': app,
                                        'trg': (partial(self.executing.emit, self.appInfo[app][2]))}, self)
                self.acts.append(action)
                self.addAction(action)

    def applySetting(self):
        self.resize(len(self.acts)*32, 32)

class ToolBarDock(QDockWidget):

    showLayout = pyqtSignal(str, str)
    executing = pyqtSignal(str)
    addLayout = pyqtSignal(object)
    setSetting = pyqtSignal(str, str, str)

    def __init__(self, name="TD", parent=None):
        super(ToolBarDock, self).__init__(parent)
        self.name = name
        self.setWindowTitle(self.name)
        self.layout = QGridLayout()
        self.toolbar = ToolBar(self.name, self)
        # self.toolbar.move(0, 30)
        self.layout.addWidget(self.toolbar, 0, 0, 1, 1)
        self.setLayout(self.layout)

        self.applySetting()

    def applySetting(self):
        self.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.setSizePolicy(SiPoExp, SiPoExp)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 21/07/2018 - 6:43 AM
# © 2017 - 2018 DAMGteam. All rights reserved