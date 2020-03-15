# -*- coding: utf-8 -*-
"""

Script Name: Size.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__
""" Import """

# PyQt5
from PyQt5.QtCore                           import QSize


class Size(QSize):
    Type                                    = 'DAMGSIZE'
    key                                     = 'Size'
    _name                                   = 'DAMG Size'
    _copyright                              = __copyright__()

    def __init__(self, *__args):
        QSize.__init__(self)

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                          = newName


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 05/01/2020 - 01:48
# © 2017 - 2019 DAMGteam. All rights reserved