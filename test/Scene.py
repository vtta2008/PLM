# -*- coding: utf-8 -*-
"""

Script Name: Scene.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtCore               import QLineF
from test.NodeBase import ConnectionItem
from utils                      import _loadConfig, _convert_to_QColor
from toolkits.Widgets           import GraphicScene
from toolkits.Gui               import Brush, Pen
from appData                    import (sceneGraphCfg, ACTION_MOVE, PATTERN_SOLID)

class Scene(GraphicScene):

    key                         = 'Scene'

    def __init__(self, parent):
        super(Scene, self).__init__(parent)
        self.gridSize               = parent.config['grid_size']

    def dragEnterEvent(self, event):
        event.setDropAction(ACTION_MOVE)
        event.accept()

    def dragMoveEvent(self, event):
        event.setDropAction(ACTION_MOVE)
        event.accept()

    def dropEvent(self, event):
        self.signal_Dropped.emit(event.scenePos())
        event.accept()

    def drawBackground(self, painter, rect):

        config = _loadConfig(sceneGraphCfg)
        self._brush = Brush()
        self._brush.setStyle(PATTERN_SOLID)
        self._brush.setColor(_convert_to_QColor(config['bg_color']))
        painter.fillRect(rect, self._brush)
        if self.views()[0].gridVisToggle:
            leftLine = rect.left() - rect.left() % self.gridSize
            topLine = rect.top() - rect.top() % self.gridSize
            lines = list()
            i = int(leftLine)
            while i < int(rect.right()):
                lines.append(QLineF(i, rect.top(), i, rect.bottom()))
                i += self.gridSize
            u = int(topLine)
            while u < int(rect.bottom()):
                lines.append(QLineF(rect.left(), u, rect.right(), u))
                u += self.gridSize
            self.pen = Pen()
            self.pen.setColor(_convert_to_QColor(config['grid_color']))
            self.pen.setWidth(0)
            painter.setPen(self.pen)
            painter.drawLines(lines)

    def updateScene(self):
        for connection in [i for i in self.items() if isinstance(i, ConnectionItem)]:
            connection.target_point = connection.target.center()
            connection.source_point = connection.source.center()
            connection.updatePath()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/12/2019 - 7:35 PM
# © 2017 - 2018 DAMGteam. All rights reserved