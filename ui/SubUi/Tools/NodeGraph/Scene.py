# -*- coding: utf-8 -*-
"""

Script Name: Scene.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python

# PyQt5
from PyQt5.QtCore                           import pyqtSignal, QLineF
from PyQt5.QtGui                            import QColor, QPen
from PyQt5.QtWidgets                        import QGraphicsScene

# PLM
from appData.config                         import GRID_SIZE, ACTION_MOVE
from ui.SubUi.Tools.NodeGraph.NodeGraph     import Edge

# -------------------------------------------------------------------------------------------------------------
""" Scene """

class Scene(QGraphicsScene):

    nodeMoved = pyqtSignal(str, object)
    dropped = pyqtSignal()

    def __init__(self, parent=None):
        super(Scene, self).__init__(parent)
        self.gridSize = GRID_SIZE
        self.Nodes = dict()

    def setGridSize(self, gridSize):
        self.gridSize = gridSize
        return self.gridSize

    def dragEnterEvent(self, event):
        event.setDropAction(ACTION_MOVE)
        event.accept()

    def dragMoveEvent(self, event):
        event.setDropAction(ACTION_MOVE)
        event.accept()

    def dropEvent(self, event):
        self.dropped.emit(event.scenePos())
        event.accept()

    def drawBackground(self, painter, rect):
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

            self.pen = QPen()
            self.pen.setColor(QColor(230, 230, 230))
            self.pen.setWidth(1)
            painter.setPen(self.pen)
            painter.drawLines(lines)

    def updateScene(self):
        for edge in [i for i in self.items() if isinstance(i, Edge)]:
            edge.target_point = edge.target.center()
            edge.source_point = edge.source.center()
            edge.updatePath()


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/07/2018 - 8:33 PM
# © 2017 - 2018 DAMGteam. All rights reserved