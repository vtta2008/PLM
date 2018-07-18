# -*- coding: utf-8 -*-
"""

Script Name: NodeAttr.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import sys, uuid

# PyQt5
from PyQt5.QtWidgets import QApplication, QGraphicsItem, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPen, QBrush, QPainterPath
from PyQt5.QtCore import Qt, QPointF

# Plt
from appData import center
from appData.scr._nodeGraph import (POSX, POSY, NODE_WIDTH, ATTR_HEIGHT, RELATIVE_SIZE, ANTIALIAS, UPDATE_BOUNDINGVIEW,
                                    DARKGRAY, ATTR_ROUND, ATTR_REC)
from utilities.pUtils import *
from core.Loggers import SetLogger
from ui.NodeGraph.Knob import Knob

# -------------------------------------------------------------------------------------------------------------
""" Node's Attribute """

class NodeAttr(QGraphicsItem):

    Type = "Node Attribute"

    def __init__(self, attrData, parent=None):
        super(NodeAttr, self).__init__(parent)

        self.logger = SetLogger(self)

        self.xpos = POSX
        self.ypos = POSY
        self.attrW = NODE_WIDTH
        self.attrH = ATTR_HEIGHT
        self.attrRound = ATTR_ROUND
        self.attrRec = ATTR_REC

        self._rect = QRectF(self.xpos, self.ypos, self.attrW, self.attrH)

        self.key = attrData['key']
        self.value = attrData['value']
        self.tooltip = attrData['tooltip']
        self.content = "{0}: {1}".format(self.key, self.value)
        self.font = 'Arial'
        self.fontH = 10
        self.align = center
        self.stage = None

        self.KnobLst = []

        self.setAcceptTouchEvents(True)
        self.setAcceptHoverEvents(True)
        self.setToolTip(self.tooltip)
        self.setZValue(1)

        posx1 = self.xpos
        posy1 = self.attrH/2

        posx2 = self.xpos + self.attrW
        posy2 = posy1

        self.knob1 = self.add_knob(posx1, posy1)
        self.knob2 = self.add_knob(posx2, posy2)

    def Knobs(self):
        return self.KnobLst

    def add_knob(self, x, y):
        knob = Knob(self)
        self.KnobLst.append(knob)
        knob.setPos(x, y)
        return knob

    def highlight(self, toggle):
        self.stage = toggle
        return self.stage

    def boundingRect(self):
        return self._rect

    def paint(self, painter, option, widget=None):

        if self.stage:
            pen = QPen(QColor(240, 101, 53, 255))
            brush = QBrush(QColor(50, 50, 50))
        else:
            pen = QPen(QColor(236, 137, 36, 255))
            brush = QBrush(QColor(40, 40, 40))

        pen.setStyle(Qt.SolidLine)
        pen.setWidthF(1)
        pen.setWidth(2)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)

        font = QFont(self.font, self.fontH)

        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawRoundedRect(self._rect, self.attrRound, self.attrRec, RELATIVE_SIZE)
        painter.setFont(font)
        painter.drawText(self._rect, self.align, self.content)

    def type(self):
        return self.Type

    def hoverEnterEvent(self, event):
        self.highlight(True)
        super(NodeAttr, self).hoverEnterEvent(event)

    def mousePressEvent(self, event):
        self.highlight(True)
        super(NodeAttr, self).mousePressEvent(event)

    def hoverLeaveEvent(self, event):
        self.highlight(False)
        super(NodeAttr, self).hoverLeaveEvent(event)

if __name__ == '__main__':
    nodeTest = QApplication(sys.argv)
    scene = QGraphicsScene(0, 0, 400, 400)
    attrData = {'key': 'Number', 'value': 5, 'tooltip': 'attr tooltip'}
    node = NodeAttr(attrData)
    node.setPos(0, 0)
    scene.addItem(node)

    view = QGraphicsView(scene)
    view.setRenderHint(ANTIALIAS)
    view.setViewportUpdateMode(UPDATE_BOUNDINGVIEW)
    view.setBackgroundBrush(DARKGRAY)
    view.setWindowTitle("Node test")
    view.show()

    nodeTest.exec_()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 18/07/2018 - 1:06 PM
# © 2017 - 2018 DAMGteam. All rights reserved