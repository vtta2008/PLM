# -*- coding: utf-8 -*-
"""

Script Name: Color.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from .io_gui                            import QColor


class Color(QColor):

    Type                                = 'DAMGCOLOR'
    key                                 = 'Color'
    _name                               = 'DAMG Color'

    def __init__(self, *__args):
        super(Color, self).__init__(*__args)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 03/01/2020 - 01:27
# © 2017 - 2019 DAMGteam. All rights reserved