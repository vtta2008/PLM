# -*- coding: utf-8 -*-
"""

Script Name: Brush.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """


from PySide2.QtGui                 import QBrush


class Brush(QBrush):

    Type                                = 'DAMGBRUSH'
    key                                 = 'Brush'
    _name                               = 'DAMG Brush'

    def __init__(self, *__args):
        super(Brush, self).__init__(*__args)

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
# Created by panda on 3/12/2019 - 3:11 AM
# © 2017 - 2018 DAMGteam. All rights reserved