# -*- coding: utf-8 -*-
"""

Script Name: KeySequence.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from PySide2.QtGui                          import QKeySequence


class KeySequence(QKeySequence):

    Type                        = 'DAMGPAINTERPATH'
    key                         = 'PainterPath'
    _name                       = 'DAMG Painter Path'

    def __init__(self, *__args):
        super(KeySequence, self).__init__(*__args)


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name = newName

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 4/12/2019 - 1:09 AM
# © 2017 - 2018 DAMGteam. All rights reserved