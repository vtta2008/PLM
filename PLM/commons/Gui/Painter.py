# -*- coding: utf-8 -*-
"""

Script Name: Painter.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__
""" Import """

# PyQt5
from PyQt5.QtGui                import QPainter


class Painter(QPainter):

    Type                        = 'DAMGPAINTER'
    key                         = 'Painter'
    _name                       = 'DAMG Painter'
    _copyright                  = __copyright__()

    def __init__(self, parent=None):
        Painter.__init__(self)

        self.parent             = parent

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name = newName

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/20/2020 - 5:31 AM
# © 2017 - 2019 DAMGteam. All rights reserved