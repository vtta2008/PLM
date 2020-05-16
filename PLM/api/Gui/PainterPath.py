# -*- coding: utf-8 -*-
"""

Script Name: PainterPath.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PLM
from PLM import __copyright__
from .io_gui                            import QPainterPath


class PainterPath(QPainterPath):

    Type                        = 'DAMGPAINTERPATH'
    key                         = 'PainterPath'
    _name                       = 'DAMG Painter Path'
    _copyright                  = __copyright__()

    def __init__(self, *args, **kwargs):
        QPainterPath.__init__(*args, **kwargs)

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name = newName


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/12/2019 - 2:11 AM
# © 2017 - 2018 DAMGteam. All rights reserved