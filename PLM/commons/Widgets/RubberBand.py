# -*- coding: utf-8 -*-
"""

Script Name: RubberBand.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__
""" Import """

# PyQt5
from PyQt5.QtWidgets                        import QRubberBand

# PLM
from PLM.cores import SettingManager
from PLM.cores import SignalManager


class RubberBand(QRubberBand):

    Type                                    = 'DAMGGRAPHICVIEW'
    key                                     = 'GraphicView'
    _name                                   = 'DAMG Graphic View'
    _copyright                              = __copyright__()

    def __init__(self, shape, parent=None):
        QRubberBand.__init__(self, shape, parent)

        self.parent                         = parent
        self.settings                       = SettingManager(self)
        self.signals                        = SignalManager()

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key, decode=None):
        if decode is None:
            return self.settings.initValue(key, self.key)
        else:
            return self.settings.initValue(key, self.key, decode)

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
# Created by panda on 3/12/2019 - 2:43 AM
# © 2017 - 2018 DAMGteam. All rights reserved