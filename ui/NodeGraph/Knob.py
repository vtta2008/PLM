# -*- coding: utf-8 -*-
"""

Script Name: pKnob.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys

# PyQt5
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QRectF
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsItem
from PyQt5.QtGui import QColor, QPen, QBrush, QPainter

from core.Errors import KnobConnectionError, UnknownFlowError
from appData.scr._nodeGraph import *
from utilities.pUtils import *
from ui.NodeGraph.Edge import Edge

# -------------------------------------------------------------------------------------------------------------
""" Knob """

class Knob(QGraphicsItem):

    Type = "Knob"

    def __init__(self, parent=None):
        super(Knob, self).__init__(parent)

        self.on_color_1 = QColor(0, 192, 0)
        self.on_color_2 = QColor(0, 255, 0)

        self.off_color_1 = QColor(0, 28, 0)
        self.off_color_2 = QColor(0, 128, 0)

        self.maxConnections = -1
        self.displayName = self.type()

        self.newEdge = None
        self.edges = []
        self.stage = False
        self.setAcceptHoverEvents(True)

    def highlight(self, toggle):
        self.stage = toggle
        return self.stage

    def type(self):
        return self.Type

    def boundingRect(self):
        return QRectF(-10, -10, 20, 20)

    def paint(self, painter, option, widget=None):
        # Draw header
        rect = QRectF(0, 0, 20, 20)

        if self.stage:
            brush = QBrush(self.on_color_1)
        else:
            brush = QBrush(self.on_color_1)

        pen = QPen()
        pen.setStyle(Qt.SolidLine)
        pen.setWidthF(1)
        pen.setWidth(2)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setBrush(brush)
        painter.setPen(pen)
        painter.drawEllipse(-5, -5, 10, 10)

        if self.stage:
            brush = QBrush(self.on_color_2)
        else:
            brush = QBrush(self.off_color_2)
        painter.setBrush(brush)
        painter.setPen(pen)
        painter.drawEllipse(-7, -7, 14, 14)

    def hoverEnterEvent(self, event):
        self.highlight(True)
        super(Knob, self).hoverEnterEvent(event)

    def mousePressEvent(self, event):
        self.highlight(True)
        super(Knob, self).mousePressEvent(event)

    def hoverLeaveEvent(self, event):
        self.highlight(False)
        super(Knob, self).hoverLeaveEvent(event)

if __name__ == '__main__':
    nodeTest = QApplication(sys.argv)
    scene = QGraphicsScene(0, 0, 400, 400)

    node = Knob()
    node.setPos(0, 0)
    scene.addItem(node)

    view = QGraphicsView(scene)
    view.setRenderHint(ANTIALIAS)
    view.setViewportUpdateMode(UPDATE_BOUNDINGVIEW)
    view.setBackgroundBrush(DARKGRAY)
    view.setWindowTitle("Knob test")
    view.show()

    nodeTest.exec_()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 5/07/2018 - 7:09 AM
# © 2017 - 2018 DAMGteam. All rights reserved