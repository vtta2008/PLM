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

class DamgSignals(DAMG):


    key                                      = 'DamgSignals'

    commandSig                               = Signal(str, name='command')
    loginChangedSig                          = Signal(bool, name='loginChanged')
    updateAvatarSig                          = Signal(str, name='updateAvatar')
    notify                                   = Signal(str, str, str, int, name='notify')

    def __init__(self, parent):
        super(DamgSignals, self).__init__(parent)

        self.parent                          = parent
        self.key                             = '{0}_{1}'.format(self.parent.key, self.key)
        self._name                           = self.key.replace('_', ' ')
        self._data['key']                    = self.key



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/10/2019 - 6:59 AM
# © 2017 - 2018 DAMGteam. All rights reserved