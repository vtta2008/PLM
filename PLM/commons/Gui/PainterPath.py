# -*- coding: utf-8 -*-
"""

Script Name: PainterPath.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__
""" Import """

# PyQt5
from PyQt5.QtGui                import QPainterPath

# PLM
from PLM.commons                        import SignalManager, SettingManager


class PainterPath(QPainterPath):

    Type                        = 'DAMGPAINTERPATH'
    key                         = 'PainterPath'
    _name                       = 'DAMG Painter Path'
    _copyright                  = __copyright__()

    def __init__(self, *args):
        QPainterPath.__init__(*args)

        self.signals            = SignalManager(self)
        self.settings           = SettingManager(self)

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