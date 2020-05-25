# -*- coding: utf-8 -*-
"""

Script Name: Pen.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from .io_gui                            import QPen


class Pen(QPen):

    Type                                = 'DAMGPEN'
    key                                 = 'Pen'
    _name                               = 'DAMG Pen'

    def __init__(self, *__args):
        super(Pen, self).__init__(*__args)


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/12/2019 - 3:17 AM
# © 2017 - 2018 DAMGteam. All rights reserved