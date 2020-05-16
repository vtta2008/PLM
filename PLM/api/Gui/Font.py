# -*- coding: utf-8 -*-
"""

Script Name: Font.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PLM
from PLM                                import __copyright__
from .io_gui                            import QFont


class Font(QFont):

    Type                                = 'DAMGFONT'
    key                                 = 'Font'
    _name                               = 'DAMG Font'
    _copyright                          = __copyright__()

    def __init__(self, *__args):
        super(Font, self).__init__(*__args)

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
# Created by panda on 3/12/2019 - 3:25 AM
# © 2017 - 2018 DAMGteam. All rights reserved