# -*- coding: utf-8 -*-
"""

Script Name: Node.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
import sys, uuid

# PyQt5
from PyQt5.QtCore import pyqtSignal, QPointF, QRectF, QLineF, pyqtProperty
from PyQt5.QtWidgets import QGraphicsItem, QApplication, QGraphicsScene, QGraphicsView, QGraphicsObject, QStyle, QAbstractButton
from PyQt5.QtGui import QColor, QPen, QBrush, QRadialGradient

# Plt
from appData import center
from appData._pNN import *
from utilities.pUtils import *
from ui.NodeGraph.pKnob import InputKnob, OutputKnob

# -------------------------------------------------------------------------------------------------------------
""" Variables """

class pNodeParts(QGraphicsObject):

    def __init__(self, parent=None):
        super(pNodeParts, self).__init__(parent)

        self.color = QColor(LIGHTGRAY)
        self.dragOver = False
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        pass

    def dragLeaveEvent(self, event):
        pass

    def dropEvent(self, event):
        pass

class HeaderText(pNodeParts):

    def __init__(self, txt, parent=None):
        super(HeaderText, self).__init__(parent)

        self.text = txt

    def boundingRect(self):
        return QRectF(0, 0, 120, 25)

    def paint(self, painter, option, widget=None):
        rect = self.boundingRect()
        painter.setPen(QColor(168, 34, 3))
        painter.setFont(QFont('Decorative', 10))
        painter.drawText(rect, center, self.text)

class FooterText(pNodeParts):

    def __init__(self, txt, parent=None):
        super(FooterText, self).__init__(parent)

        self.text = txt

    def boundingRect(self):
        return QRectF(0, 0, 120, 25)

    def paint(self, painter, option, widget=None):
        rect = self.boundingRect()
        painter.setPen(QColor(168, 34, 3))
        painter.setFont(QFont('Decorative', 10))
        painter.drawText(rect, center, self.text)

class BodyText(pNodeParts):

    def __init__(self, txt, parent=None):
        super(BodyText, self).__init__(parent)

        self.text = txt

    def boundingRect(self):
        return QRectF(0, 0, 120, 40)

    def paint(self, painter, option, widget=None):
        rect = self.boundingRect()
        painter.setPen(QColor(168, 34, 3))
        painter.setFont(QFont('Decorative', 10))
        painter.drawText(rect, center, self.text)

class HeaderShape(pNodeParts):

    def boundingRect(self):
        return QRectF(0, 0, 120, 25)

    def paint(self, painter, option, widget=None):

        # Draw header
        rect = QRectF(0, 0, 120, 25)
        painter.setBrush(GRAY)
        painter.setPen(QPen(BLACK, 0))
        painter.drawRoundedRect(rect, 10, 200, RELATIVESIZE)

class BodyShape(pNodeParts):

    def boundingRect(self):
        return QRectF(0, 0, 120, 80)

    def paint(self, painter, option, widget=None):

        # Draw header
        rect = QRectF(0, 0, 120, 80)
        painter.setBrush(YELLOW)
        painter.setPen(QPen(BLACK, 0))
        painter.drawRoundedRect(rect, 10, 200, RELATIVESIZE)

class FooterShape(pNodeParts):

    def boundingRect(self):
        return QRectF(0, 0, 120, 25)

    def paint(self, painter, option, widget=None):

        # Draw header
        rect = QRectF(0, 0, 120, 25)
        painter.setBrush(GRAY)
        painter.setPen(QPen(BLACK, 0))
        painter.drawRoundedRect(rect, 10, 200, RELATIVESIZE)

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
        painter.drawEllipse(-10, -10, 20, 20)

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

class pNode(pNodeParts):

    def __init__(self, text):
        super(pNode, self).__init__()

        self.uuid = str(uuid.uuid4())

        self.x, self.y = DEFAULT_POS
        self.w, self.h = DEFAULT_WH

        self.fillColor = QColor(220, 220, 220)

        self.txt = text

        self.margin = MARGIN
        self.roundness = ROUNDNESS

        self.setFlag(SELECTABLE)
        self.setFlag(MOVEABLE)
        self.setCursor(SIZEALLCURSOR)

        self.setAcceptTouchEvents(True)
        self.setAcceptHoverEvents(True)
        self.setAcceptDrops(True)

        self.setZValue(1)

        self.pKnobLst = []
        self.setToolTip(self.txt)

        self.headerShape = HeaderShape(self)
        self.headerTitle = HeaderText(self.txt, self.headerShape)

        self.bodyShape1 = BodyShape(self)
        self.bodyShape1.setPos(0, 26)

        self.body_pKnob1 = Knob(self)
        self.body_pKnob1.setPos(0,46)

        self.body_pKnob2 = Knob(self)
        self.body_pKnob2.setPos(0, 86)

        self.body_pKnob3 = Knob(self)
        self.body_pKnob3.setPos(120, 46)

        self.body_pKnob4 = Knob(self)
        self.body_pKnob4.setPos(120, 86)

        self.footerShape = FooterShape(self)
        self.footerShape.setPos(0, 106)
        self.footerTitle = FooterText("Wait to update", self.footerShape)

    def addpKnob(self, pKnob):
        self.pKnobLst.append(pKnob)

    def pKnobs(self):
        return self.pKnobLst

    def boundingRect(self):
        return QRectF(0, 0, 120, 181)

    def paint(self, painter, option, widget=None):
       pass

    def itemChange(self, change, value):
        if change == POSHASCHANGE:
            for edge in self.pKnobLst:
                edge.adjust()
            self.itemMoved()

        return super(pNode, self).itemChange(change, value)

    def mousePressEvent(self, event):
        self.update()
        super(pNode, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.update()
        super(pNode, self).mouseReleaseEvent(event)


if __name__ == '__main__':
    nodeTest = QApplication(sys.argv)
    scene = QGraphicsScene(0, 0, 400, 400)

    node = pNode("Test node with a name")
    node.setPos(0, 0)
    scene.addItem(node)

    view = QGraphicsView(scene)
    view.setRenderHint(ANTIALIAS)
    view.setViewportUpdateMode(BOUNDINGVIEWPORTUPDATE)
    view.setBackgroundBrush(QColor(230, 200, 167))
    view.setWindowTitle("pNode test")
    view.show()

    nodeTest.exec_()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 17/06/2018 - 2:58 PM
# © 2017 - 2018 DAMGteam. All rights reserved