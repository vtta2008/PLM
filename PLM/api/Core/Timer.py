# -*- coding: utf-8 -*-
"""

Script Name: Timer.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__
from .io_core import QTimer



class Timer(QTimer):

    Type                                = 'DAMGTIMER'
    key                                 = 'Timer'
    _name                               = 'DAMG Timer'
    _copyright                          = __copyright__

    def __init__(self, parent=None):
        super(Timer, self).__init__(parent)

        self.parent                     = parent

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name                      = val


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/17/2020 - 12:50 AM
# © 2017 - 2019 DAMGteam. All rights reserved