# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from .io_gui                            import QPaintDevice


class PaintDevice(QPaintDevice):

    Type                            = 'DAMGPAINTDEVICE'
    key                             = 'PaintDevice'
    _name                           = 'DAMG Paint Device'

    def __init__(self):
        super(PaintDevice, self).__init__()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name = newName

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved