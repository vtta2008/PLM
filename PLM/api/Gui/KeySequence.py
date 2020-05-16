# -*- coding: utf-8 -*-
"""

Script Name: KeySequence.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PLM
from PLM import __copyright__
from .io_gui                            import QKeySequence


class KeySequence(QKeySequence):

    Type                        = 'DAMGPAINTERPATH'
    key                         = 'PainterPath'
    _name                       = 'DAMG Painter Path'
    _copyright                  = __copyright__()

    def __init__(self, *args, **kwargs):
        QKeySequence.__init__(*args, **kwargs)

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
# Created by panda on 4/12/2019 - 1:09 AM
# © 2017 - 2018 DAMGteam. All rights reserved