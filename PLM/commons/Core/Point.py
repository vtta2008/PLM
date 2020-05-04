# -*- coding: utf-8 -*-
"""

Script Name: Point.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__

from PyQt5.QtCore import QPoint

class Point(QPoint):

    Type                                    = 'DAMGPOINT'
    key                                     = 'Point'
    _name                                   = 'DAMG Point'
    __copyright__                           = __copyright__()

    def __init__(self, *__args):
        QPoint.__init__(self)



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
# Created by panda on 5/4/2020 - 6:45 PM
# © 2017 - 2019 DAMGteam. All rights reserved