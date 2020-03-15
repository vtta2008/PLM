# -*- coding: utf-8 -*-
"""

Script Name: Brush.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__
""" Import """

# PyQt5
from PyQt5.QtGui                       import QBrush

# PLM
from PLM.cores import SettingManager
from PLM.cores import SignalManager

class Brush(QBrush):

    Type                                = 'DAMGBRUSH'
    key                                 = 'Brush'
    _name                               = 'DAMG Brush'
    _copyright                          = __copyright__()

    def __init__(self, *args, **kwargs):
        QBrush.__init__(*args, **kwargs)

        self.signals                    = SignalManager(self)
        self.settings                   = SettingManager(self)

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/12/2019 - 3:11 AM
# © 2017 - 2018 DAMGteam. All rights reserved