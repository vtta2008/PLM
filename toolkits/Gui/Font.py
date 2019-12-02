# -*- coding: utf-8 -*-
"""

Script Name: Font.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import __copyright__
""" Import """

# PyQt5
from PyQt5.QtGui                       import QFont

# PLM
from appData                           import SETTING_FILEPTH, ST_FORMAT
from toolkits.Core                     import Settings, SignalManager

class Font(QFont):

    Type                                = 'DAMGFONT'
    key                                 = 'Font'
    _name                               = 'DAMG Font'
    _copyright                          = __copyright__()

    def __init__(self, font, fontsize, fontAttr, parent=None):
        QFont.__init__(font, fontsize, fontAttr)

        self.parent                     = parent
        self.signals                    = SignalManager(self)
        self.settings                   = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)

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