# -*- coding: utf-8 -*-
"""

Script Name: Rect.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from PLM.__main__ import __copyright__
""" Import """

# PyQt5
from PyQt5.QtCore               import QRect, QRectF

# PLM

class Rect(QRect):

    Type                        = 'DAMGRECT'
    key                         = 'Rect'
    _name                       = 'DAMG Rect'
    _copyright                  = __copyright__()

    def __init__(self, *__args):
        QRect.__init__(self)

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name              = val


class RectF(QRectF):

    Type                        = 'DAMGRECTF'
    key                         = 'RectF'
    _name                       = 'DAMG RectF'
    _copyright                  = __copyright__()

    def __init__(self, *__args):
        QRectF.__init__(self)

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/12/2019 - 1:58 AM
# © 2017 - 2018 DAMGteam. All rights reserved