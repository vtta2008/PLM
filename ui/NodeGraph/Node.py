# -*- coding: utf-8 -*-
"""

Script Name: pNode.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
import sys, uuid

# PyQt5
from PyQt5.QtWidgets import QGraphicsObject, QApplication
from PyQt5.QtGui import QPen, QBrush, QPainterPath
from PyQt5.QtCore import Qt

# Plt
from appData import center, left
from appData.scr._pNN import *
from utilities.pUtils import *
from core.Loggers import SetLogger

# -------------------------------------------------------------------------------------------------------------
""" Variables """
class Knob(QGraphicsItem):

    Type = "Input"

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
            painter.setBrush(self.on_color_1)
        else:
            painter.setBrush(self.off_color_1)
        painter.setPen(QPen(BLACK, 0))
        painter.drawEllipse(-5, -5, 10, 10)

        if self.stage:
            painter.setBrush(self.on_color_2)
        else:
            painter.setBrush(self.off_color_2)
        painter.setPen(QPen(DARKGRAY, 0))
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

class NodeBase(QGraphicsObject):

    def set_text(self, txt = "PLM node"):
        self.text = txt

    def nodeType(self):
        return "PLM color data"

    def set_stamp(self, value=25):
        self.stamp = value

    def set_nodeWidth(self, width=125):
        self.nodeW = width

    def set_round(self, round=5):
        self._round = round

    def set_rec(self, rec=400):
        self._rec = rec


class Node(QGraphicsObject):

    Type = 'Color Node'

    def __init__(self, name, parent=None):
        super(Node, self).__init__(parent)

        self.logger = SetLogger(self)
        self.text = 'title'
        self.name = name
        self.setObjectName(name)

        self.applySetting()
        self._rect = QRectF(0,0,125, 180)
        self._round = 2.5
        self.rec = 500
        self.AttrLst = []
        self.KnobLst = []
        self.headerRect = QRectF(self.xpos, self.ypos, self.nodeW, self.headerH)
        self.stampRect = QRectF(self.xpos, self.ypos, self.stamp, self.stamp)
        knob1 = self.add_knob(0, 65)
        knob2 = self.add_knob(0, 95)
        knob3 = self.add_knob(0, 125)
        knob4 = self.add_knob(0, 155)
        knob5 = self.add_knob(125, 65)
        knob6 = self.add_knob(125, 95)
        knob7 = self.add_knob(125, 125)
        knob8 = self.add_knob(125, 155)

        self.highlight()

    def Knobs(self):
        return self.KnobLst

    def remove_item(self, item):
        pass

    def regItem(self, attr):
        pass

    def add_knob(self, x, y):
        knob = Knob(self)
        self.KnobLst.append(knob)
        knob.setPos(x, y)
        return knob

    def highlight(self,):
        self.stage = self.isSelected()
        return self.stage

    def set_tag(self, tag):
        pass

    def set_flag(self, flag):
        self.setFlag(flag)

    def type(self):
        return self.Type

    def paint(self, painter, option, widget=None):
        # Draw header
        pen = QPen()
        pen.setStyle(Qt.DashLine)
        pen.setWidthF(1)
        pen.setWidth(2)
        pen.setCapStyle(Qt.RoundCap);
        pen.setJoinStyle(Qt.RoundJoin)

        if self.stage:
            painter.setPen(QPen(QColor(240, 101, 53, 255)))
            painter.setBrush(QColor(50, 50, 50))
        else:
            painter.setPen(QColor(236, 137, 36, 255))
            painter.setBrush(QColor(20, 20, 20))

        self.headerRect = QRectF(0, 3, 125, 190)
        painter.drawRoundedRect(self.headerRect, 10, 500, RELATIVE_SIZE)

        rect = QRect(0, 20, 125, 30)
        painter.drawRoundedRect(rect, 1, 500, RELATIVE_SIZE)
        painter.setFont(QFont('Menlo', 8))
        painter.drawText(rect, center, "Node Name")

        rect = QRect(0, 50, 125, 30)
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)
        painter.setFont(QFont('Menlo', 8))
        painter.drawText(rect, center, "Attr1")

        rect = QRect(0, 80, 125, 30)
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)
        painter.setFont(QFont('Menlo', 8))
        painter.drawText(rect, center, "Attr2")

        rect = QRect(0, 110, 125, 30)
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)
        painter.setFont(QFont('Menlo', 8))
        painter.drawText(rect, center, "Attr3")

        rect = QRect(0, 140, 125, 30)
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)
        painter.setFont(QFont('Menlo', 8))
        rect = QRect(0, 145, 125, 30)
        painter.drawText(rect, center, "Attr4")

    def updateRect(self, rect):
        self.nodeH = self.nodeH + rect.height()

    def applySetting(self):
        self.dragOver = False
        self.tooltip = 'Dev Node'
        self.margin = MARGIN
        self.roundness = ROUNDNESS
        self.stamp = 25
        self.nodeW = 125
        self._round = 2.5
        self._rec = 400
        self.xpos = 0
        self.ypos = 0
        self.headerH = 25
        self.footerH = 25
        self.nodeH = 30
        self.attrH = 30
        self.setFlag(SELECTABLE)
        self.setFlag(MOVEABLE)

        self.setAcceptTouchEvents(True)
        self.setAcceptHoverEvents(True)
        self.setAcceptDrops(True)
        self.setToolTip(self.tooltip)
        self.setZValue(1)

    def boundingRect(self):
        return self._rect

    def itemChange(self, change, value):
        if change == POS_CHANGE:
            for edge in self.pKnobLst:
                edge.adjust()
            self.itemMoved()
        return super(Node, self).itemChange(change, value)

    def mousePressEvent(self, event):
        self.update()
        super(Node, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.update()
        super(Node, self).mouseReleaseEvent(event)





if __name__ == '__main__':
    nodeTest = QApplication(sys.argv)
    scene = QGraphicsScene(0, 0, 400, 400)

    node = Node("PLM")
    node.setPos(0, 0)
    scene.addItem(node)

    view = QGraphicsView(scene)
    view.setRenderHint(ANTIALIAS)
    view.setViewportUpdateMode(UPDATE_BOUNDINGVIEW)
    view.setBackgroundBrush(DARKGRAY)
    view.setWindowTitle("pNode test")
    view.show()

    nodeTest.exec_()
# -------------------------------------------------------------------------------------------------------------
# Created by panda on 5/07/2018 - 7:04 AM
# © 2017 - 2018 DAMGteam. All rights reserved