# -*- coding: utf-8 -*-
"""

Script Name: PainterPath.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from PySide2.QtGui                          import QPainterPath


class PainterPath(QPainterPath):

    Type                        = 'DAMGPAINTERPATH'
    key                         = 'PainterPath'
    _name                       = 'DAMG Painter Path'

    def __init__(self, *args, **kwargs):
        QPainterPath.__init__(*args, **kwargs)


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name = newName


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/12/2019 - 2:11 AM
# © 2017 - 2018 DAMGteam. All rights reserved