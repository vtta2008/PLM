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
from PyQt5.QtWidgets import QToolBar

# PLM
from appData                    import (__envKey__, CONFIG_TDS, CONFIG_VFX, CONFIG_ART, CONFIG_TEX, CONFIG_TOOLS,
                                        CONFIG_POST, SETTING_FILEPTH, ST_FORMAT, __copyright__)
from cores.base                 import DAMGLIST, DAMGDICT
from ui.uikits.Action           import Action
from ui.SignalManager               import SignalManager
from cores.Loggers              import Loggers
from cores.Settings             import Settings

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

    Type                                    = 'DAMGUI'
    key                                     = 'ToolBar'
    _name                                   = 'DAMG Tool Bar'
    _copyright                              = __copyright__
    _data                                   = dict()

    def __init__(self, configKey=None, parent=None):
        QToolBar.__init__(self)

        self.parent             = parent
        self.signals            = SignalManager(self)
        self.logger             = Loggers(self.__class__.__name__)
        self.settings           = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.configKey = configKey

        self.buildUI()

        self.applySetting()

    def add_multiple_actions(self, actions=[]):
        for action in actions:
            self.addAction(action)

    def add_actions_by_key(self, key):

        apps = self.tbData[self.configKey]
        for app in apps:
            if app in self.appInfo:
                action = Action({'icon': app, 'stt': self.appInfo[app][0], 'txt': app, 'trg': (partial(self.executing.emit, self.appInfo[app][2]))}, self)
                self.acts.append(action)
                self.addAction(action)

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.configKey)

    def getValue(self, key):
        return self.settings.initValue(key, self.configKey)

    def showEvent(self, event):
        sizeX = self.getValue('width')
        sizeY = self.getValue('height')

        if not sizeX is None and not sizeY is None:
            self.resize(int(sizeX), int(sizeY))

        posX = self.getValue('posX')
        posY = self.getValue('posY')

        if not posX is None and not posX is None:
            self.move(posX, posY)

    def moveEvent(self, event):
        self.setValue('posX', self.x())
        self.setValue('posY', self.y())

    def resizeEvent(self, event):
        self.setValue('width', self.frameGeometry().width())
        self.setValue('height', self.frameGeometry().height())

    def sizeHint(self):
        size = super(ToolBar, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

    def closeEvent(self, event):
        if __name__=='__main__':
            self.close()
        else:
            self.signals.showLayout.emit(self.configKey, 'hide')
            event.ignore()

    def hideEvent(self, event):
        if __name__=='__main__':
            self.hide()
        else:
            self.signals.showLayout.emit(self.configKey, 'hide')
            event.ignore()

    @property
    def copyright(self):
        return self._copyright

    @property
    def data(self):
        return self._data

    @property
    def name(self):
        return self._name

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, newVal):
        self._count                     = newVal

    @data.setter
    def data(self, newData):
        self._data                      = newData

    @name.setter
    def name(self, newName):
        self._name                      = newName

class ToolBarPreset(ToolBar):

    key = "ToolBarPreset"
    toolbarPreset = DAMGDICT()
    toolbarPreset.input(TOOLBAR_DATA)

    def __init__(self, configKey, parent=None):
        super(ToolBarPreset, self).__init__(parent)

        with open(os.path.join(os.getenv(__envKey__), 'appData/.config', 'main.cfg'), 'r') as f:
            self.appInfo = json.load(f)

        self._parent = parent
        self.key = configKey
        self.signals = SignalManager(self)

        self.acts = DAMGLIST()

        self.applySetting()

    def buildUI(self):
        self.add_actions()

    def applySetting(self):
        self.setAccessibleName(self.key)
        self.setMinimumWidth((len(self.acts) + 1)*32)

    def add_actions(self):
        apps = self.tbData[self.key]
        for app in apps:
            if app in self.appInfo:
                action = Action({'icon': app, 'stt': self.appInfo[app][0], 'txt': app, 'trg': (partial(self.executing.emit, self.appInfo[app][2]))}, self)
                self.acts.append(action)
                self.addAction(action)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 31/07/2018 - 12:50 AM
# © 2017 - 2018 DAMGteam. All rights reserved