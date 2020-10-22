# -*- coding: utf-8 -*-
"""

Script Name: Rect.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from PySide2.QtCore                 import QRect, QRectF

# PLM

class Rect(QRect):

    Type                            = 'DAMGRECT'
    key                             = 'Rect'
    _name                           = 'DAMG Rect'

    def __init__(self, *__args):
        super(Rect, self).__init__(*__args)


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name                  = val


class RectF(QRectF):

    Type                            = 'DAMGRECTF'
    key                             = 'RectF'
    _name                           = 'DAMG RectF'


    def __init__(self, *__args):
        super(RectF, self).__init__(*__args)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name                  = val

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/12/2019 - 1:58 AM
# © 2017 - 2018 DAMGteam. All rights reserved