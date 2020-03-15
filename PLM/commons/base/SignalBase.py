# -*- coding: utf-8 -*-
"""

Script Name: Signal.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from PLM.__main__ import globalSetting
""" Import """

# PyQt5
from PyQt5.QtCore                            import pyqtSignal, pyqtSlot

# PLM
from bin                                     import DAMG, DAMGDICT
from PLM.cores import Loggers

# -------------------------------------------------------------------------------------------------------------
""" Signal class: setup all the signal which will be using. """

class SignalBase(DAMG):

    key                                      = 'Signal'

    _emitable                                = False

    commandSig                               = pyqtSignal(str, name='command')
    # startfileSig                             = pyqtSignal(str, name='os.startfile')
    # ossystemSig                              = pyqtSignal(str, name='os.system')
    # appEventSig                              = pyqtSignal(str, name='appEvent')
    # openURLSig                               = pyqtSignal(str, name='openURL')
    # stylesheetSig                            = pyqtSignal(str, name='stylesheet')
    # shortcutSig                              = pyqtSignal(str, name='shortcut')
    # functionSig                              = pyqtSignal(str, name='function')
    # showUISig                                = pyqtSignal(str, name='showUI')
    # executingSig                             = pyqtSignal(str, name='executing')
    # regisLaoutSig                            = pyqtSignal(str, name='regisLaout')
    # setSettingSig                            = pyqtSignal(str, name='setSetting')
    # sysNotifySig                             = pyqtSignal(str, name='sysNotify')
    # removeGroupSig                           = pyqtSignal(str, name='removeGroup')
    # setFormatSig                             = pyqtSignal(str, name='setFormat')
    # setScopeSig                              = pyqtSignal(str, name='setScope')
    loginChangedSig                          = pyqtSignal(bool, name='loginChanged')
    updateAvatarSig                          = pyqtSignal(str, name='updateAvatar')

    commandSlot                              = pyqtSlot(str, name='command')
    # startfileSlot                            = pyqtSlot(str, name='os.startfile')
    # ossystemSlot                             = pyqtSlot(str, name='os.system')
    # appEventSlot                             = pyqtSlot(str, name='appEvent')
    # openURLSlot                              = pyqtSlot(str, name='openURL')
    # stylesheetSlot                           = pyqtSlot(str, name='stylesheet')
    # shortcutSlot                             = pyqtSlot(str, name='shortcut')
    # functionSlot                             = pyqtSlot(str, name='function')
    # showUISlot                               = pyqtSlot(str, name='showUI')
    # executingSlot                            = pyqtSlot(str, name='executing')
    # regisLaoutSlot                           = pyqtSlot(str, name='regisLaout')
    # setSettingSlot                           = pyqtSlot(str, name='setSetting')
    # sysNotifySlot                            = pyqtSlot(str, name='sysNotify')
    # removeGroupSlot                          = pyqtSlot(str, name='removeGroup')
    # setFormatSlot                            = pyqtSlot(str, name='setFormat')
    # setScopeSlot                             = pyqtSlot(str, name='setScope')
    loginChangedSlot                         = pyqtSlot(bool, name='loginChanged')
    updateAvatarSlot                         = pyqtSlot(str, name='updateAvatar')

    _signals                                 = DAMGDICT()
    _slots                                   = DAMGDICT()

    def __init__(self, parent):
        super(SignalBase, self).__init__(parent)

        self.parent                          = parent
        self.logger                          = Loggers(self.__class__.__name__)

        self._signals.add('command'          , self.commandSig)
        # self._signals.add('os.startfile'     , self.startfileSig)
        # self._signals.add('os.system'        , self.ossystemSig)
        # self._signals.add('appEvent'         , self.appEventSig)
        # self._signals.add('openURL'          , self.openURLSig)
        # self._signals.add('stylesheet'       , self.stylesheetSig)
        # self._signals.add('shortcut'         , self.shortcutSig)
        # self._signals.add('function'         , self.functionSig)
        # self._signals.add('showUI'           , self.showUISig)
        # self._signals.add('executing'        , self.executingSig)
        # self._signals.add('regisLaout'       , self.regisLaoutSig)
        # self._signals.add('setSetting'       , self.setSettingSig)
        # self._signals.add('sysNotify'        , self.sysNotifySig)
        # self._signals.add('removeGroup'      , self.removeGroupSig)
        # self._signals.add('setFormat'        , self.setFormatSig)
        # self._signals.add('setScope'         , self.setScopeSig)
        self._signals.add('loginChanged'     , self.loginChangedSig)
        self._signals.add('updateAvatar'     , self.updateAvatarSig)

        self._slots.add('command'            , self.commandSlot)
        # self._slots.add('os.startfile'       , self.startfileSlot)
        # self._slots.add('os.system'          , self.ossystemSlot)
        # self._slots.add('appEvent'           , self.appEventSlot)
        # self._slots.add('openURL'            , self.openURLSlot)
        # self._slots.add('stylesheet'         , self.stylesheetSlot)
        # self._slots.add('shortcut'           , self.shortcutSlot)
        # self._slots.add('function'           , self.functionSlot)
        # self._slots.add('showUI'             , self.showUISlot)
        # self._slots.add('executing'          , self.executingSlot)
        # self._slots.add('regisLaout'         , self.regisLaoutSlot)
        # self._slots.add('setSetting'         , self.setSettingSlot)
        # self._slots.add('sysNotify'          , self.sysNotifySlot)
        # self._slots.add('removeGroup'        , self.removeGroupSlot)
        # self._slots.add('setFormat'          , self.setFormatSlot)
        # self._slots.add('setScope'           , self.setScopeSlot)
        self._slots.add('loginChanged'       , self.loginChangedSlot)
        self._slots.add('updateAvatar'       , self.updateAvatarSlot)

        self.update()

    def changeParent(self, parent):
        self.parent                          = parent
        self.key                             = '{0}_{1}'.format(self.parent.key, self.key)
        self._name                           = self.key.replace('_', ' ')
        self._data['key']                    = self.key

    def update(self):
        self._signals.update()
        self._slots.update()

    def getSignal(self, key):
        if globalSetting.tracks.getSignal:
            self.logger.info('{0} get signal: {1}'.format(self.parent.key, key))
        return self.signals.get(key)

    def getSlot(self, key):
        if globalSetting.tracks.getSlot:
            self.logger.info('{0} get slot: {1}'.format(self.parent.key, key))
        return self.slots.get(key)

    def emit(self, key, arg):
        if self.emitable:
            signal                           = self.getSignal(key)
            signal.emit(arg)
        else:
            if globalSetting.tracks.emittable:
                self.logger.info('EmittableError: {0} is not allowed to emit'.format(self.key))
            return

    def connect(self, key, target):
        if globalSetting.defaults.auto_changeEmitable:
            self._emitable                   = True
        else:
            self.logger.info('SignalConnectArror: {0} is not allowed to connect'.format(self.key))
            return
        signal                               = self.getSignal(key)
        signal.connect(target)

    @property
    def signals(self):
        return self._signals

    @property
    def slots(self):
        return self._slots

    @property
    def emitable(self):
        return self._emitable

    @signals.setter
    def signals(self, val):
        self._signals                        = val

    @slots.setter
    def slots(self, val):
        self._slots                          = val

    @emitable.setter
    def emitable(self, val):
        self._emitable                       = val

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 28/11/2019 - 12:52 AM
# © 2017 - 2018 DAMGteam. All rights reserved