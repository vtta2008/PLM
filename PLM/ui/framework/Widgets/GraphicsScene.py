# -*- coding: utf-8 -*-
"""

Script Name: GraphicScene.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__
""" Import """

# PyQt5
from PyQt5.QtWidgets                        import QGraphicsScene

# PLM
from PLM.plugins.SignalManager              import SignalManager
from PLM.data.SettingManager import SettingManager


class GraphicsScene(QGraphicsScene):

    Type                                    = 'DAMGGRAPHICSScene'
    key                                     = 'GraphicsScene'
    _name                                   = 'DAMG Graphic Scene'
    _copyright                              = __copyright__()

    def __init__(self, parent=None):
        QGraphicsScene.__init__(self)

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
# Created by panda on 3/12/2019 - 2:30 AM
# © 2017 - 2018 DAMGteam. All rights reserved