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

from appData import APPINFO, CONFIG_TDS, CONFIG_VFX, CONFIG_ART, CONFIG_TEXTURE, CONFIG_TOOLS, CONFIG_POST, SiPoExp
from ui.uikits.Action import Action

TOOLBAR_DATA = dict(TD = CONFIG_TDS,
                    VFX = CONFIG_VFX,
                    ART = CONFIG_ART,
                    TEXTURE = CONFIG_TEXTURE,
                    TOOLS = CONFIG_TOOLS,
                    POST = CONFIG_POST)

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

    def applySetting(self):
        self.setMinimumWidth((len(self.acts) + 1)*32 + 32)

    def add_actions(self):
        apps = self.tbData[self.key]
        for app in apps:
            if app in self.appInfo:
                action = Action({'icon': app,
                                 'stt': self.appInfo[app][0],
                                 'txt': app,
                                 'trg': (partial(self.executing.emit, self.appInfo[app][2]))}, self)
                self.acts.append(action)
                self.addAction(action)

    def sizeHint(self):
        size = super(ToolBar, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

class ToolBarDock(QDockWidget):

    showLayout = pyqtSignal(str, str)
    executing = pyqtSignal(str)
    addLayout = pyqtSignal(object)
    setSetting = pyqtSignal(str, str, str)
    key = 'Toolbar'

    def __init__(self, name="TEXTURE", parent=None):
        super(ToolBarDock, self).__init__(parent)
        # print(self.__class__.isWindowType())
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

    def showEvent(self, event):
        pass

    def closeEvent(self, event):
        self.showLayout.emit(self.key, 'hide')
        event.ignore()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 21/07/2018 - 6:43 AM
# © 2017 - 2018 DAMGteam. All rights reserved