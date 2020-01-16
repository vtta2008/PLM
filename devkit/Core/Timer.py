# -*- coding: utf-8 -*-
"""

Script Name: Timer.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import __copyright__
""" Import """

# PyQt5
from PyQt5.QtCore import QTimer



class Timer(QTimer):

    Type                                = 'DAMGTIMER'
    key                                 = 'Timer'
    _name                               = 'DAMG Timer'
    _copyright                          = __copyright__

    def __init__(self, parent=None):
        QTimer.__init__(self)

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