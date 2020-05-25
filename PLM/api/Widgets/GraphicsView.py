# -*- coding: utf-8 -*-
"""

Script Name: GraphicView.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from .io_widgets import QGraphicsView


class GraphicsView(QGraphicsView):

    Type                                    = 'DAMGGRAPHICSVIEW'
    key                                     = 'GraphicsView'
    _name                                   = 'DAMG Graphics View'

    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)

        self.parent                         = parent

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/12/2019 - 1:11 AM
# © 2017 - 2018 DAMGteam. All rights reserved