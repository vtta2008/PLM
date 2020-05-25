# -*- coding: utf-8 -*-
"""

Script Name: GraphicsItem.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PyQt5

from PLM.api.Widgets.io_widgets             import QGraphicsItem
from PLM.cores.SignalManager                import SignalManager
from PLM.settings                           import AppSettings


class GraphicsItem(QGraphicsItem):

    Type                                    = 'DAMGGRAPHICVIEW'
    key                                     = 'GraphicView'
    _name                                   = 'DAMG Graphic View'

    def __init__(self, parent=None):
        QGraphicsItem.__init__(self)

        self.parent                         = parent
        self.settings                       = AppSettings(self)
        self.signals                        = SignalManager()

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key, decode=None):
        if decode is None:
            return self.settings.initValue(key, self.key)
        else:
            return self.settings.initValue(key, self.key, decode)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/12/2019 - 2:39 AM
# © 2017 - 2018 DAMGteam. All rights reserved