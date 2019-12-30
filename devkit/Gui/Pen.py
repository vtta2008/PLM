# -*- coding: utf-8 -*-
"""

Script Name: Pen.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import __copyright__
""" Import """

# PyQt5
from PyQt5.QtGui                       import QPen

# PLM
from cores.Settings                    import Settings
from cores.SignalManager               import SignalManager

class Pen(QPen):

    Type                                = 'DAMGPEN'
    key                                 = 'Pen'
    _name                               = 'DAMG Pen'
    _copyright                          = __copyright__()

    def __init__(self, *args, **kwargs):
        QPen.__init__(*args, **kwargs)

        self.signals                    = SignalManager(self)
        self.settings                   = Settings(self)


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