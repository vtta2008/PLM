# -*- coding: utf-8 -*-
"""

Script Name: GraphicView.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__
""" Import """

# PyQt5
from PyQt5.QtWidgets                        import QGraphicsView

# PLM
from PLM.plugins.SignalManager              import SignalManager
from PLM.data.SettingManager import SettingManager


class GraphicsView(QGraphicsView):

    Type                                    = 'DAMGGRAPHICSVIEW'
    key                                     = 'GraphicsView'
    _name                                   = 'DAMG Graphics View'
    _copyright                              = __copyright__()

    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)

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
# Created by panda on 3/12/2019 - 1:11 AM
# © 2017 - 2018 DAMGteam. All rights reserved