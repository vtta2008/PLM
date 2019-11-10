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

    def __init__(self, parent=None):
        super(SignalManager, self).__init__(parent)

        self.parent                 = parent
        self.logger                 = Loggers(self.parent.key)
        self.key                    = '{0}_{1}'.format(self.parent.key, self.key)

        self.signals.add('showLayout'   , [self.showLayout, self.showLayoutOld])
        self.signals.add('executing'    , [self.executing, self.executingOld])
        self.signals.add('regisLayout'  , [self.regisLayout,self.regisLayoutOld])
        self.signals.add('openBrowser'  , [self.openBrowser, self.openBrowserOld])
        self.signals.add('setSetting'   , [self.setSetting, self.setSettingOld])
        self.signals.add('sysNotify'    , [self.sysNotify, self.sysNotifyOld])
        self.signals.add('updateAvatar' , [self.updateAvatar, self.updateAvatarOld])
        self.signals.add('loginChanged' , [self.loginChanged, self.loginChangedOld])

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
        if self.parent.key not in self.notContenMargin:
            try:
                self.parent.setContentMargin(1,1,1,1)
            except AttributeError:
                pass
        elif self.parent.key not in self.notSizePolicy:
            try:
                self.parent.setSizePolicy(SiPoExp, SiPoExp)
            except AttributeError:
                pass
        elif self.parent.key not in self.notSpacing:
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

        if self._emittable:
            sig = self.getSignal(signal)
            # print('Signal {0} emitted: {1}: {2} {3} {4} from {5}'.format(self.parent.key, op1, op2, op3, op4, __name__))

            if signal == 'showLayout':
                return sig.emit(op1, op2)
            elif signal == 'executing':
                return sig.emit(op1)
            elif signal == 'regisLayout':
                return sig.emit(op1)
            elif signal == 'openBrowser':
                return sig.emit(op1)
            elif signal == 'setSetting':
                return sig.emit(op1, op2, op3)
            elif signal == 'sysNotify':
                return sig.emit(op1, op2, op3, op4)
            elif signal == 'updateAvatar':
                return sig.emit(op1)
            elif signal == 'loginChanged':
                return sig.emit(op1)

            print('{0} emmited'.format(self.parent))
        else:
            return # print('UnEmittableError: {0} is connected to nowhere.'.format(self.key))

    def getSignal(self, signal):
        # print('{0} : {1}'.format(self.parent.key, signal))
        return self.signals[signal][0]

    def connect(self, signal, target):
        sig = self.getSignal(signal)
        self._emittable = True
        return sig.connect(target)

    def check_repeat_signal(self, signal, op1, op2, op3, op4):

        new = DAMGLIST()
        old = self.signals[signal][1]

        if signal == 'showLayout':
            new.appendList([op1, op2])
        elif signal == 'executing':
            new.append(op1)
        elif signal == 'regisLayout':
            new.append(op1)
        elif signal == 'openBrowser':
            new.append(op1)
        elif signal == 'setSetting':
            new.appendList([op1, op2, op3])
        elif signal == 'sysNotify':
            new.appendList([op1, op2, op3, op4])
        elif signal == 'updateAvatar':
            new.append(op1)
        elif signal == 'loginChanged':
            new.append(op1)

        repeat = True
        if len(new) == len(old):
            for i in range(len(new)):
                if new[i] == old[i]:
                    continue
                else:
                    repeat = False
                    break
        else:
            repeat = False

        if not repeat:
            self.signals[signal][1] = new
        else:
            return ('signal repeat')

        self.signals.update()
        return repeat

    @property
    def emitable(self):
        return self._emittable

    @emitable.setter
    def emitable(self, newVal):
        self._emittable = newVal

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/10/2019 - 6:59 AM
# © 2017 - 2018 DAMGteam. All rights reserved