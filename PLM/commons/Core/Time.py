# -*- coding: utf-8 -*-
"""

Script Name: Time.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__
""" Import """

# PyQt5
from PyQt5.QtCore                           import QTime


class Time(QTime):

    Type                                    = 'DAMGTIME'
    key                                     = 'Time'
    _name                                   = 'DAMG Time'
    _copyright                              = __copyright__


    def __init__(self, *__args):
        QTime.__init__(self)

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name              = val



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/17/2020 - 1:47 AM
# © 2017 - 2019 DAMGteam. All rights reserved