# -*- coding: utf-8 -*-
"""

Script Name: GraphicsItem.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from PySide2.QtWidgets                      import QGraphicsItem
from bin.models                             import DamgSignals
from bin.settings                           import AppSettings


class GraphicsItem(QGraphicsItem):

    Type                                    = 'DAMGGRAPHICVIEW'
    key                                     = 'GraphicView'
    _name                                   = 'DAMG Graphic View'

    def __init__(self, parent=None):
        QGraphicsItem.__init__(self)

        self.parent                         = parent
        self.settings                       = AppSettings(self)
        self.signals                        = DamgSignals()

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