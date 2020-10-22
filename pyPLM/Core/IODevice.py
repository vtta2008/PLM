# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from PySide2.QtCore                 import QIODevice


class IODevice(QIODevice):

    Type                            = 'DAMGIODEVICE'
    key                             = 'IODevice'
    _name                           = 'DAMG IO Device'

    def __init__(self, obj=None):
        super(IODevice, self).__init__(obj)


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name                  = val

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved