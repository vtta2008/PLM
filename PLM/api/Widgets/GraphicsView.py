# -*- coding: utf-8 -*-
"""

Script Name: GraphicView.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__
from PLM.api.Widgets.io_widgets             import QGraphicsView


class GraphicsView(QGraphicsView):

    Type                                    = 'DAMGGRAPHICSVIEW'
    key                                     = 'GraphicsView'
    _name                                   = 'DAMG Graphics View'
    _copyright                              = __copyright__()

    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)

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
# Created by panda on 3/12/2019 - 1:11 AM
# © 2017 - 2018 DAMGteam. All rights reserved