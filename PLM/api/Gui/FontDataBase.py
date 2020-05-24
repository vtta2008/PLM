# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from PLM import __copyright__
from .io_gui import QFontDatabase


class FontDataBase(QFontDatabase):

    Type                                = 'DAMGFONTDATABASE'
    key                                 = 'FontDataBase'
    _name                               = 'DAMG Font Database'
    _copyright                          = __copyright__()

    def __init__(self, app=None):
        super(FontDataBase, self).__init__(self)

        # writingSystemSample(QFontDatabase.WritingSystem) -> str

        self.app                        = app

    @property
    def name(self):
        return self._name

    @property
    def copyright(self):
        return self._copyright

    @name.setter
    def name(self, val):
        self._name                      = val

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved