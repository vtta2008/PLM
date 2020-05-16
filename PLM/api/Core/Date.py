# -*- coding: utf-8 -*-
"""

Script Name: Date.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__
from .io_core import QDate


class Date(QDate):

    Type                                    = 'DAMGDATE'
    key                                     = 'Date'
    _name                                   = 'DAMG Date'
    _copyright                              = __copyright__()


    def __init__(self, *__args):
        super(Date, self).__init__(*__args)

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
# Created by panda on 1/17/2020 - 12:48 AM
# © 2017 - 2019 DAMGteam. All rights reserved