# -*- coding: utf-8 -*-
"""

Script Name: Pen.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__
""" Import """

# PyQt5
from PyQt5.QtGui                       import QPen

# PLM
from PLM.cores import SettingManager
from PLM.cores import SignalManager

class Pen(QPen):

    Type                                = 'DAMGPEN'
    key                                 = 'Pen'
    _name                               = 'DAMG Pen'
    _copyright                          = __copyright__()

    def __init__(self, *__args):
        QPen.__init__(self)

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
# Created by panda on 3/12/2019 - 3:17 AM
# © 2017 - 2018 DAMGteam. All rights reserved