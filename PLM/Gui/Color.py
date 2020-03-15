# -*- coding: utf-8 -*-
"""

Script Name: Color.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from PLM.__main__ import __copyright__
""" Import """

from PyQt5.QtGui import QColor

class Color(QColor):

    Type                                = 'DAMGCOLOR'
    key                                 = 'Color'
    _name                               = 'DAMG Color'
    _copyright                          = __copyright__()

    def __init__(self, *__args):
        QColor.__init__(self)

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
# Created by panda on 03/01/2020 - 01:27
# © 2017 - 2019 DAMGteam. All rights reserved