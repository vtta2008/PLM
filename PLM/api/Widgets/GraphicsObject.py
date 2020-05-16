# -*- coding: utf-8 -*-
"""

Script Name: GraphicObject.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__
from PLM.api.Widgets.io_widgets             import QGraphicsObject


class GraphicsObject(QGraphicsObject):

    Type                                    = 'DAMGGRAPHICVIEW'
    key                                     = 'GraphicView'
    _name                                   = 'DAMG Graphic View'
    _copyright                              = __copyright__()

    def __init__(self, parent=None):
        QGraphicsObject.__init__(self)

        self.parent                         = parent

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
# Created by panda on 3/12/2019 - 9:18 PM
# © 2017 - 2018 DAMGteam. All rights reserved