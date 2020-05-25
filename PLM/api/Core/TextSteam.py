# -*- coding: utf-8 -*-
"""

Script Name: TextSteam.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from .io_core import QTextStream

class TextStream(QTextStream):

    Type                                    = 'DAMGTEXTSTREAM'
    key                                     = 'TextStream'
    _name                                   = 'DAMG Text Stream'


    def __init__(self, fileName):
        QTextStream.__init__(self)
        self.setDevice(fileName)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                          = newName

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 15/11/2019 - 5:43 PM
# © 2017 - 2018 DAMGteam. All rights reserved