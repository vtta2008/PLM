# -*- coding: utf-8 -*-
"""

Script Name: KeySequence.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import __copyright__

# PyQt5
from PyQt5.QtGui import QKeySequence

# PLM
from appData                    import SETTING_FILEPTH, ST_FORMAT
# from toolkits.Core              import Settings, SignalManager

class KeySequence(QKeySequence):

    Type                        = 'DAMGPAINTERPATH'
    key                         = 'PainterPath'
    _name                       = 'DAMG Painter Path'
    _copyright                  = __copyright__()

    def __init__(self, parent=None):
        QKeySequence.__init__(self)

        self.parent = parent
        # self.signals = SignalManager(self)
        # self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)

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