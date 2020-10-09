# -*- coding: utf-8 -*-
"""

Script Name: UiSignals.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import logging
from PySide2.QtCore                         import Signal, Slot
from bin.damg                               import DAMG, DAMGDICT


logging.basicConfig()


# -------------------------------------------------------------------------------------------------------------
""" Signal class: setup all the signal which will be using. """

class SignalManager(DAMG):


    key                                      = 'SignalManager'

    _emitable                                = True

    commandSig                               = Signal(str, name='command')
    loginChangedSig                          = Signal(bool, name='loginChanged')
    updateAvatarSig                          = Signal(str, name='updateAvatar')

    commandSlot                              = Slot(str, name='command')
    loginChangedSlot                         = Slot(bool, name='loginChanged')
    updateAvatarSlot                         = Slot(str, name='updateAvatar')

    _signals                                 = DAMGDICT()
    _slots                                   = DAMGDICT()

    def __init__(self, parent):
        super(SignalManager, self).__init__(parent)

        self.parent                          = parent
        self.logger                          = logging.getLogger(__file__)
        self.logger.setLevel(logging.DEBUG)

        self._signals.add('command'          , self.commandSig)
        self._signals.add('loginChanged'     , self.loginChangedSig)
        self._signals.add('updateAvatar'     , self.updateAvatarSig)

        self._slots.add('command'            , self.commandSlot)
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
        # if glbSettings.printSignalReceive:
        #     self.logger.info('{0} get signal: {1}'.format(self.parent.key, key))
        return self.signals.get(key)

    def getSlot(self, key):
        # if glbSettings.tracks.getSlot:
        #     self.logger.info('{0} get slot: {1}'.format(self.parent.key, key))
        return self.slots.get(key)

    def emit(self, key, arg):
        if self.emitable:
            signal                           = self.getSignal(key)
            # signal.emit(arg)
        else:
            return self.logger.info('EmittableError: {0} is not allowed to emit'.format(self.key))

    def connect(self, key, target):
        if not self._emitable:
            return self.logger.info('SignalConnectArror: {0} is not allowed to connect'.format(self.key))
        else:
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
# Created by panda on 25/10/2019 - 6:59 AM
# © 2017 - 2018 DAMGteam. All rights reserved