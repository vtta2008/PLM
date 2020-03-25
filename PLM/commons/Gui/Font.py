# -*- coding: utf-8 -*-
"""

Script Name: Font.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__
""" Import """

# PyQt5
from PyQt5.QtGui                       import QFont

# PLM
from PLM.commons                        import SignalManager, SettingManager


class Font(QFont):

    Type                                = 'DAMGFONT'
    key                                 = 'Font'
    _name                               = 'DAMG Font'
    _copyright                          = __copyright__()

    def __init__(self, *__args):
        QFont.__init__(self)

        self.settings                   = SettingManager(self)
        self.signals                    = SignalManager(self)

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