# -*- coding: utf-8 -*-
"""

Script Name: GraphicPathItem.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PyQt5
from PLM                                    import __copyright__
from PLM.api.Widgets.io_widgets             import QGraphicsPathItem
from PLM.plugins.SignalManager              import SignalManager
from PLM.cores.Settings.app_settings import AppSettings


class GraphicPathItem(QGraphicsPathItem):

    Type                                    = 'DAMGGRAPHICVIEW'
    key                                     = 'GraphicView'
    _name                                   = 'DAMG Graphic View'
    _copyright                              = __copyright__()

    def __init__(self, *__args):
        QGraphicsPathItem.__init__(self)

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
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/12/2019 - 4:12 AM
# © 2017 - 2018 DAMGteam. All rights reserved