# -*- coding: utf-8 -*-
"""

Script Name: Polygon.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PLM
from PLM import __copyright__
from .io_gui                            import QPolygon


class Polygon(QPolygon):

    Type                                = 'DAMGPOLYGON'
    key                                 = 'Polygon'
    _name                               = 'DAMG Polygon'
    _copyright                          = __copyright__()

    def __init__(self, *__args):
        super(Polygon, self).__init__(*__args)

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
# Created by panda on 5/4/2020 - 6:34 PM
# © 2017 - 2019 DAMGteam. All rights reserved