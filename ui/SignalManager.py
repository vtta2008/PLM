# -*- coding: utf-8 -*-
"""

Script Name: UiSignals.py
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
from cores.Loggers                  import Loggers
from appData                        import TMP_DIR
from bin.data.damg                  import DAMG, DAMGLIST, DAMGDICT

# -------------------------------------------------------------------------------------------------------------
""" Signal class: setup all the signal which will be using. """

class Signal(DAMG):

    key                             = 'Signal'

    _emittable                      = False

    # PLM class
    showLayout                      = pyqtSignal(str, str, name="showLayout")
    executing                       = pyqtSignal(str, name="executing")
    regisLayout                     = pyqtSignal(DAMG, name="regisLaout")
    openBrowser                     = pyqtSignal(str, name="openBrowser")
    setSetting                      = pyqtSignal(str, str, str, name="setSetting")
    sysNotify                       = pyqtSignal(str, str, str, int, name="sysNotify")
    loginChanged                    = pyqtSignal(bool, name='loginChanged')

    #
    updateAvatar                    = pyqtSignal(bool, name="updateAvatar")

    # Settings class
    removeGrp                       = pyqtSignal(str, name='removeGroup')
    setFormat                       = pyqtSignal(str, name='setFormat')
    setScope                        = pyqtSignal(str, name='setScope')

    print_emittable                 = False
    print_emit                      = False
    print_block                     = False
    print_checkRepeat               = False
    print_getSignal                 = False
    print_checkState                = False
    auto_changeEmmittable           = True

    _signals                        = DAMGDICT()
    _settings                       = DAMGDICT()

    states                          = DAMGDICT()

    def __init__(self, parent):
        super(Signal, self).__init__(parent)

        self.parent                 = parent
        self.logger                 = Loggers(self.parent.key)
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
        keys = ['showLayout', 'executing', 'regisLayout', 'openBrowser', 'setSetting', 'sysNotify', 'updateAvatar',
                'loginChanged']
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
""" Signal class: setup all the signal which will be using. """

class SignalManager(Signal):

    key                             = "SignalManager"

    showLayoutOld                   = DAMGLIST()
    executingOld                    = DAMGLIST()
    regisLayoutOld                  = DAMGLIST()
    openBrowserOld                  = DAMGLIST()
    setSettingOld                   = DAMGLIST()
    sysNotifyOld                    = DAMGLIST()
    updateAvatarOld                 = DAMGLIST()
    loginChangedOld                 = DAMGLIST()

    def __init__(self, parent=None):
        super(SignalManager, self).__init__(parent)

        self.parent                 = parent

        try:
            self.parent.children()
        except AttributeError:
            pass
        else:
            self.setParent(self.parent)
        finally:
            self.key = '{0}_{1}'.format(self.parent.key, self.key)

    def emit(self, signal, op1=None, op2=None, op3=None, op4=None):

        if self._emittable:
            sig = self.getSignal(signal)
            self.loadState()
            if signal == 'showLayout':
                self.showLayoutOld, repeat      = self.checkSignalRepeat(self.showLayoutOld, [op1, op2])
                old = self.showLayoutOld
                if repeat:
                    if self.print_checkState:
                        print(self.key, self.states)
                    if not self.states[op1] == op2:
                        self.states.add(op1, op2)
                        self.updateState()
                        sig.emit(op1, op2)
                else:
                    if self.print_checkState:
                        print(self.key, self.states)
                    self.states.add(op1, op2)
                    self.updateState()
                    sig.emit(op1, op2)
            elif signal == 'executing':
                self.executingOld, repeat       = self.checkSignalRepeat(self.executingOld, [op1])
                old = self.executingOld
                if not repeat:
                    sig.emit(op1)
            elif signal == 'regisLayout':
                self.regisLayoutOld, repeat     = self.checkSignalRepeat(self.regisLayoutOld, [op1])
                old = self.regisLayoutOld
                if not repeat:
                    sig.emit(op1)
            elif signal == 'openBrowser':
                self.openBrowserOld, repeat     = self.checkSignalRepeat(self.openBrowserOld, [op1])
                old = self.openBrowserOld
                if not repeat:
                    sig.emit(op1)
            elif signal == 'setSetting':
                self.setSettingOld, repeat      = self.checkSignalRepeat(self.setSettingOld, [op1, op2, op3])
                old = self.setSettingOld
                if not repeat:
                    sig.emit(op1, op2, op3)
            elif signal == 'sysNotify':
                self.sysNotifyOld, repeat       = self.checkSignalRepeat(self.sysNotifyOld, [op1, op2, op3, op4])
                old = self.sysNotifyOld
                if not repeat:
                    sig.emit(op1, op2, op3, op4)
            elif signal == 'updateAvatar':
                self.updateAvatarOld, repeat    = self.checkSignalRepeat(self.updateAvatarOld, [op1])
                old = self.updateAvatarOld
                if not repeat:
                    sig.emit(op1)
            elif signal == 'loginChanged':
                self.loginChangedOld, repeat    = self.checkSignalRepeat(self.loginChangedOld, [op1])
                old = self.loginChangedOld
                if not repeat:
                    sig.emit(op1)
            else:
                repeat                          = False
                old                             = []

            if repeat:
                if self.print_block:
                    print('{2}: block signal {0}: {1}'.format(signal, old, self.key))
                return
            else:
                if self.print_emit:
                    print('{0} signal {1} emmited'.format(self.parent.key, signal))
                return
        else:
            if self.print_emittable:
                print('UnEmittableError: {0} is not allowed to emit'.format(self.key))
            return

    def getSignal(self, signal):
        if self.print_getSignal:
            print('{0} get signal: {1}'.format(self.parent.key, signal))
        return self.signals[signal][0]

    def connect(self, signal, target):
        sig = self.getSignal(signal)
        if self.auto_changeEmmittable:
            self._emittable = True
            return sig.connect(target)
        else:
            print('EmittableAllowError: Signal is not allowed to emit: {0}'.format(signal))

    def checkSignalRepeat(self, old, data):
        new = [i for i in data]

        if self.print_checkRepeat:
            print(new, old)

        if len(new) == 0:
            repeat = False
        elif len(new) == len(old):
            repeat = True
            for i in range(len(new)):
                if not new[i] == old[i]:
                    repeat = False
                    break
        else:
            repeat = False

        old = DAMGLIST()
        old.appendList(new)
        return old, repeat

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/10/2019 - 6:59 AM
# © 2017 - 2018 DAMGteam. All rights reserved