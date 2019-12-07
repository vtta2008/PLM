# -*- coding: utf-8 -*-
"""

Script Name: Signal.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
""" Import """

# Python
import os, json

# PyQt5
from PyQt5.QtCore                   import pyqtSignal

# PLM
from bin                            import DAMG, DAMGDICT, DAMGLIST
from appData                        import TMP_DIR
from cores.Loggers                  import Loggers

# -------------------------------------------------------------------------------------------------------------
""" Signal class: setup all the signal which will be using. """

class SignalBase(DAMG):

    key                             = 'Signal'

    _emittable                      = False
    print_emittable                 = False
    print_emit                      = False
    print_block                     = False
    print_checkRepeat               = False
    print_getSignal                 = False
    print_checkState                = False
    auto_changeEmmittable           = True

    # PLM class
    showLayout                      = pyqtSignal(str, str, name="showLayout")
    executing                       = pyqtSignal(str, name="executing")
    regisLayout                     = pyqtSignal(DAMG, name="regisLaout")
    openBrowser                     = pyqtSignal(str, name="openBrowser")
    setSetting                      = pyqtSignal(str, str, str, name="setSetting")
    sysNotify                       = pyqtSignal(str, str, str, int, name="sysNotify")
    loginChanged                    = pyqtSignal(bool, name='loginChanged')

    # Avatar
    updateAvatar                    = pyqtSignal(bool, name="updateAvatar")

    # Settings class
    removeGrp                       = pyqtSignal(str, name='removeGroup')
    setFormat                       = pyqtSignal(str, name='setFormat')
    setScope                        = pyqtSignal(str, name='setScope')

    _signals                        = DAMGDICT()
    _settings                       = DAMGDICT()
    states                          = DAMGDICT()

    showLayoutOld                   = DAMGLIST()
    executingOld                    = DAMGLIST()
    regisLayoutOld                  = DAMGLIST()
    openBrowserOld                  = DAMGLIST()
    setSettingOld                   = DAMGLIST()
    sysNotifyOld                    = DAMGLIST()
    updateAvatarOld                 = DAMGLIST()
    loginChangedOld                 = DAMGLIST()

    def __init__(self, parent):
        super(SignalBase, self).__init__(parent)

        self.parent                 = parent
        self.logger                 = Loggers(self.__class__.__name__)
        self.update()

    def update(self):
        return self.updateSignals(), self.updateSettings()

    def updateState(self):
        filePth = os.path.join(TMP_DIR, '.states')
        with open(filePth, 'w') as f:
            json.dump(self.states, f, indent=4)

    def loadState(self):
        filePth = os.path.join(TMP_DIR, '.states')
        if not os.path.exists(filePth):
            self.updateState()

        with open(filePth, 'r') as f:
            data = json.load(f)
        self.states.appendDict(data)

    def updateSignals(self):
        keys = ['showLayout', 'executing', 'regisLayout', 'openBrowser', 'setSetting', 'sysNotify', 'updateAvatar', 'loginChanged']

        signals = [self.showLayout, self.executing, self.regisLayout, self.openBrowser, self.setSetting, self.sysNotify,
                   self.updateAvatar, self.loginChanged]
        olds = [self.showLayoutOld, self.executingOld, self.regisLayoutOld, self.openBrowserOld, self.setSettingOld,
                self.sysNotifyOld, self.updateAvatarOld, self.loginChangedOld]
        for i in range(len(keys)):
            key, signal, old = [keys[i], signals[i], olds[i]]
            self._signals.add(key, [signal, old])
        return self._signals

    def updateSettings(self):
        keys = ['emittable', 'emit', 'block', 'checkRepeat', 'getSignal', 'checkState']
        values = [self.print_emittable, self.print_emit, self.print_block, self.print_checkRepeat, self.print_getSignal,
                  self.print_checkState]
        for i in range(len(keys)):
            self._settings.add(keys[i], values[i])
        return self._settings

    def changeSignalsSetting(self, key, value):
        self._settings[key] = value
        self._settings.update()
        return self._settings

    @property
    def signals(self):
        return self._signals

    @property
    def printCheckState(self):
        return self.print_checkState

    @property
    def autoChangeEmittable(self):
        return self.auto_changeEmmittable

    @property
    def printGetSignal(self):
        return self.print_getSignal

    @property
    def emitable(self):
        return self._emittable

    @property
    def printEmitable(self):
        return self.print_emittable

    @property
    def printEmit(self):
        return self.print_emit

    @property
    def printBlock(self):
        return self.print_block

    @property
    def printCheckRepeat(self):
        return self.print_checkRepeat

    @signals.setter
    def signals(self, val):
        self._signals               = val

    @printCheckState.setter
    def printCheckState(self, val):
        self.print_checkState       = val

    @autoChangeEmittable.setter
    def autoChangeEmittable(self, val):
        self.auto_changeEmmittable  = val

    @printGetSignal.setter
    def printGetSignal(self, val):
        self.print_getSignal        = val

    @printEmitable.setter
    def printEmitable(self, val):
        self.print_emittable        = val

    @printEmit.setter
    def printEmit(self, val):
        self.print_emit             = val

    @printBlock.setter
    def printBlock(self, val):
        self.print_block            = val

    @printCheckRepeat.setter
    def printCheckRepeat(self, val):
        self.print_checkRepeat      = val

    @emitable.setter
    def emitable(self, val):
        self._emittable             = val

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 28/11/2019 - 12:52 AM
# © 2017 - 2018 DAMGteam. All rights reserved