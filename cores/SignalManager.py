# -*- coding: utf-8 -*-
"""

Script Name: UiSignals.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
""" Import """

# PLM
from bin                                import DAMGLIST
from .base                              import SignalBase

# -------------------------------------------------------------------------------------------------------------
""" Signal class: setup all the signal which will be using. """

class SignalManager(SignalBase):

    key                             = "SignalManager"

    def __init__(self, parent=None):
        super(SignalManager, self).__init__(parent)

        self.parent                 = parent
        self.key                    = '{0}_{1}'.format(self.parent.key, self.key)
        self._data['key']           = self.key

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

    def changeParent(self, parent):
        self.parent             = parent
        self.key                = '{0}_{1}'.format(self.parent.key, self.key)
        self._name              = self.key.replace('_', ' ')

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/10/2019 - 6:59 AM
# © 2017 - 2018 DAMGteam. All rights reserved