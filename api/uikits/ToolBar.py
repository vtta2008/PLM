# -*- coding: utf-8 -*-
"""

Script Name: ToolBar.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import json
import os
from functools import partial

# PyQt5
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QToolBar

# PLM
from core.Metadata import __envKey__
from core.keys import CONFIG_TDS, CONFIG_VFX, CONFIG_ART, CONFIG_TEX, CONFIG_TOOLS, CONFIG_POST
from ui.uikits.Action import Action

# -------------------------------------------------------------------------------------------------------------
""" Tool bar data preset """

TOOLBAR_DATA = dict(TD = CONFIG_TDS,
                    VFX = CONFIG_VFX,
                    ART = CONFIG_ART,
                    TEXTURE = CONFIG_TEX,
                    TOOLS = CONFIG_TOOLS,
                    POST = CONFIG_POST)

# -------------------------------------------------------------------------------------------------------------
""" Tool bar class """

class ToolBar(QToolBar):

    executing = pyqtSignal(str)

    def __init__(self, key, parent=None):
        super(ToolBar, self).__init__(parent)

        with open(os.path.join(os.getenv(__envKey__), 'cfg', 'main.cfg'), 'r') as f:
            self.appInfo = json.load(f)

        self._parent = parent
        self.key = key
        self.setAccessibleName(self.key)
        self.acts = []
        self.tbData = TOOLBAR_DATA
        self.add_actions()
        self.applySetting()

    def applySetting(self):
        self.setMinimumWidth((len(self.acts) + 1)*32)

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
# -------------------------------------------------------------------------------------------------------------
# Created by panda on 31/07/2018 - 12:50 AM
# © 2017 - 2018 DAMGteam. All rights reserved