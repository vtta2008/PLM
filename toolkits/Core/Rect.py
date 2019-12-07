# -*- coding: utf-8 -*-
"""

Script Name: Rect.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import __copyright__
""" Import """

# PyQt5
from PyQt5.QtCore               import QRect, QRectF

# PLM
from cores.Settings                         import Settings
from cores.SignalManager                    import SignalManager


class Rect(QRect):

    Type                        = 'DAMGRECT'
    key                         = 'Rect'
    _name                       = 'DAMG Rect'
    _copyright                  = __copyright__()

    def __init__(self, *args, **kwargs):
        QRect.__init__(*args, **kwargs)

        self.settings           = Settings(self)
        self.signals            = SignalManager(self)

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val


class RectF(QRectF):
    Type = 'DAMGRECT'
    key = 'Rect'
    _name = 'DAMG Rect'
    _copyright = __copyright__()

    def __init__(self, *args):
        QRectF.__init__(*args)

        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.signals = SignalManager(self)

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/12/2019 - 1:58 AM
# © 2017 - 2018 DAMGteam. All rights reserved