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
from bin.data.damg                  import DAMG, DAMGLIST, DAMGDICT

# PyQt5
from PyQt5.QtCore                   import pyqtSignal
from PyQt5.QtCore                   import Qt

# PLM
from cores.Loggers                  import Loggers
from appData                        import SiPoMin, SiPoMax, SiPoExp, SiPoIgn, SiPoPre, STAY_ON_TOP


class SignalManager(DAMG):

    key                             = "SignalManager"
    _emittable                      = False

    showLayout                      = pyqtSignal(str, str, name="showLayout")
    executing                       = pyqtSignal(str, name="executing")
    regisLayout                     = pyqtSignal(DAMG, name="regisLaout")
    openBrowser                     = pyqtSignal(str, name="openBrowser")
    setSetting                      = pyqtSignal(str, str, str, name="setSetting")
    sysNotify                       = pyqtSignal(str, str, str, int, name="sysNotify")
    updateAvatar                    = pyqtSignal(bool, name="updateAvatar")
    loginChanged                    = pyqtSignal(bool, name='loginChanged')

    showLayoutOld                   = DAMGLIST()
    executingOld                    = DAMGLIST()
    regisLayoutOld                  = DAMGLIST()
    openBrowserOld                  = DAMGLIST()
    setSettingOld                   = DAMGLIST()
    sysNotifyOld                    = DAMGLIST()
    updateAvatarOld                 = DAMGLIST()
    loginChangedOld                 = DAMGLIST()

    signals                         = DAMGDICT()
    states                          = DAMGDICT()

    print_emittable                 = False
    print_emit                      = False
    print_block                     = False
    print_checkRepeat               = False

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

        self.logger                 = Loggers(self.parent.key)


        keys    = ['showLayout'      , 'executing'      , 'regisLayout'     , 'openBrowser'       , 'setSetting'      , 'sysNotify'      , 'updateAvatar'      , 'loginChanged'         ]
        signals = [self.showLayout   , self.executing   , self.regisLayout  , self.openBrowser    , self.setSetting   , self.sysNotify   , self.updateAvatar   , self.loginChanged      ]
        olds    = [self.showLayoutOld, self.executingOld, self.regisLayoutOld, self.openBrowserOld, self.setSettingOld, self.sysNotifyOld, self.updateAvatarOld, self.loginChangedOld   ]

        for i in range(len(keys)):
            key, signal, old = [keys[i], signals[i], olds[i]]
            self.signals.add(key, [signal, old])

        self.objects        = ['PLMCORE', 'PLM', 'IconPth', 'ActionManager']

        self.notContenMargin = ['Configurations', 'ServerConfig', 'ComboBox', 'Button', 'HBoxLayout',
                                'VBoxLayout', 'ServerConfigPage1', 'ServerConfigPage2', 'ServerConfig', 'Label',
                                'Widget', 'SettingUI', 'SettingInput', 'GridLayout', 'signin', 'GroupBox', 'LineEdit',
                                'forgotPW', 'signup', 'CheckBox', 'mainUI', 'MainMenuBar', 'Action', 'SubMenuBar',
                                'mainToolBar', 'TopTab', 'topTab1', 'topTab2', 'topTab3', 'topTab4', 'topTab5', 'TabBar',
                                'TabWidget', 'tabs', 'botTab', 'GeneralSetting', 'Footer', 'statusBar']

        self.notSizePolicy = []

        self.notSpacing = []

        self.globalSetting()

    def globalSetting(self):
        # if self.parent.key not in self.objects:
        # if self.parent.key not in self.notContenMargin:
        try:
            self.parent.setContentMargin(1,1,1,1)
        except AttributeError:
            pass
        # elif self.parent.key not in self.notSizePolicy:
        try:
            self.parent.setSizePolicy(SiPoExp, SiPoExp)
        except AttributeError:
            pass
        # elif self.parent.key not in self.notSpacing:
        try:
            self.parent.setSpacing(2)
        except AttributeError:
            pass

        if self.parent.key == 'PipelineManager':
            self.parent.setFixedWidth(500)
            # self.parent.setWindowFlags(STAY_ON_TOP)

        if self.parent.key == 'TobTab' and self.parent.key == 'BotTab':
            self.parent.setMovable(True)
            self.parent.setElideMode(Qt.ElideRight)
            self.parent.setUsesScrollButtons(True)

    def emit(self, signal, op1=None, op2=None, op3=None, op4=None):

        # data = [op1, op2, op3, op4]

        if self._emittable:
            sig = self.getSignal(signal)

            if signal == 'showLayout':
                self.showLayoutOld, repeat      = self.checkSignalRepeat(self.showLayoutOld, [op1, op2])
                if repeat:
                    # print(self.key, self.states)
                    if self.states[op1] == op2:
                        if self.print_block:
                            print('{2}: block signal {0}: {1}'.format(signal, self.showLayoutOld, self.key))
                        return
                    else:
                        self.states.add(op1, op2)
                        sig.emit(op1, op2)
                else:
                    # print(self.key, self.states)
                    self.states.add(op1, op2)
                    sig.emit(op1, op2)
            elif signal == 'executing':
                self.executingOld, repeat       = self.checkSignalRepeat(self.executingOld, [op1])
                if repeat:
                    if self.print_block:
                        print('{2}: block signal {0}: {1}'.format(signal, self.executingOld, self.key))
                    return
                else:
                    sig.emit(op1)
            elif signal == 'regisLayout':
                self.regisLayoutOld, repeat     = self.checkSignalRepeat(self.regisLayoutOld, [op1])
                if repeat:
                    if self.print_block:
                        print('{2}: block signal {0}: {1}'.format(signal, self.regisLayoutOld, self.key))
                    return
                else:
                    sig.emit(op1)
            elif signal == 'openBrowser':
                self.openBrowserOld, repeat     = self.checkSignalRepeat(self.openBrowserOld, [op1])
                if repeat:
                    if self.print_block:
                        print('{2}: block signal {0}: {1}'.format(signal, self.openBrowserOld, self.key))
                    return
                else:
                    sig.emit(op1)
            elif signal == 'setSetting':
                self.setSettingOld, repeat      = self.checkSignalRepeat(self.setSettingOld, [op1, op2, op3])
                if repeat:
                    if self.print_block:
                        print('{2}: block signal {0}: {1}'.format(signal, self.setSettingOld, self.key))
                    return
                else:
                    sig.emit(op1, op2, op3)
            elif signal == 'sysNotify':
                self.sysNotifyOld, repeat       = self.checkSignalRepeat(self.sysNotifyOld, [op1, op2, op3, op4])
                if repeat:
                    if self.print_block:
                        print('{2}: block signal {0}: {1}'.format(signal, self.sysNotifyOld, self.key))
                    return
                else:
                    sig.emit(op1, op2, op3, op4)
            elif signal == 'updateAvatar':
                self.updateAvatarOld, repeat    = self.checkSignalRepeat(self.updateAvatarOld, [op1])
                if repeat:
                    if self.print_block:
                        print('{2}: block signal {0}: {1}'.format(signal, self.updateAvatarOld, self.key))
                    return
                else:
                    sig.emit(op1)
            elif signal == 'loginChanged':
                self.loginChangedOld, repeat    = self.checkSignalRepeat(self.loginChangedOld, [op1])
                if repeat:
                    if self.print_block:
                        print('{2}: block signal {0}: {1}'.format(signal, self.loginChangedOld, self.key))
                    return
                else:
                    sig.emit(op1)
            if self.print_emit:
                print('{0} signal {1} emmited'.format(self.parent.key, signal))
            return
        else:
            if self.print_emittable:
                print('UnEmittableError: {0} is connected to nowhere.'.format(self.key))
            return

    def getSignal(self, signal):
        # print('{0} : {1}'.format(self.parent.key, signal))
        return self.signals[signal][0]

    def connect(self, signal, target):
        sig = self.getSignal(signal)
        self._emittable = True
        return sig.connect(target)

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

    @property
    def emitable(self):
        return self._emittable

    @emitable.setter
    def emitable(self, newVal):
        self._emittable = newVal

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/10/2019 - 6:59 AM
# © 2017 - 2018 DAMGteam. All rights reserved