# -*- coding: utf-8 -*-
"""

Script Name: Size.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------

from .io_core import QSize


class Size(QSize):

    Type                                    = 'DAMGSIZE'
    key                                     = 'Size'
    _name                                   = 'DAMG Size'

    def __init__(self, *__args):
        super(Size, self).__init__(*__args)


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                          = newName


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 05/01/2020 - 01:48
# © 2017 - 2019 DAMGteam. All rights reserved