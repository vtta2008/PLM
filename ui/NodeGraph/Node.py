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
from PyQt5.QtWidgets import QGraphicsObject, QApplication, QGraphicsPathItem, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPen, QBrush, QPainterPath
from PyQt5.QtCore import Qt, QPointF

# Plt
from appData import center, left
from appData.scr._nodeGraph import (POSX, POSY, NODE_WIDTH, NODE_ROUND, NODE_STAMP, NODE_REC, SELECTABLE, MOVEABLE,
                                    NODE_FOOTER_HEIGHT, NODE_HEADER_HEIGHT, ATTR_HEIGHT, POS_CHANGE, RELATIVE_SIZE,
                                    UPDATE_BOUNDINGVIEW, DARKGRAY, MARGIN)
from utilities.pUtils import *
from core.Loggers import SetLogger
from ui.NodeGraph.NodeAttr import NodeAttr

# -------------------------------------------------------------------------------------------------------------
""" Node """

attrData1 = {'key': 'int', 'value': 5, 'tooltip': 'attr int'}
attrData2 = {'key': 'float', 'value': 5.0, 'tooltip': 'attr float'}
attrData3 = {'key': 'string', 'value': 'abcd', 'tooltip': 'attr string'}
attrData4 = {'key': 'func', 'value': 'plus', 'tooltip': 'attr func'}

class NodeBase(QGraphicsObject):

    def set_stamp(self, value=NODE_STAMP):
        self.nodeStamp = value

    def set_nodeWidth(self, width=NODE_WIDTH):
        self.nodeW = width

    def set_round(self, round=NODE_ROUND):
        self.nodeRound = round

    def set_rec(self, rec=NODE_REC):
        self.nodeRec = rec


class Node(NodeBase):

    Type = 'Color Node'

    def __init__(self, nodeData, parent=None):
        super(Node, self).__init__(parent)

        self.logger = SetLogger(self)
        self.name = nodeData['name']
        self.setObjectName(self.name)

        self.margin = MARGIN
        self.nodeW = NODE_WIDTH + self.margin
        self.nodeRound = NODE_ROUND
        self.nodeRec = NODE_REC
        self.xpos = POSX
        self.ypos = POSY
        self.headerH = NODE_HEADER_HEIGHT
        self.footerH = NODE_FOOTER_HEIGHT

        self.headerRect = QRect(self.xpos, self.ypos, self.nodeW, self.headerH)

        self.attrH = ATTR_HEIGHT
        self.attrLst = []
        self.dragOver = False
        self.tooltip = 'Dev Node'
        self.font = 'Arial'
        self.fontH = 10
        self.align = center
        self.nodeH = self.height()

        self.setFlag(SELECTABLE)
        self.setFlag(MOVEABLE)
        self.setAcceptTouchEvents(True)
        self.setAcceptHoverEvents(True)
        self.setAcceptDrops(True)
        self.setToolTip(self.tooltip)
        self.setZValue(1)

        self.nodeH = self.height()
        self._rect = self.boundingRect()

        attr1 = self.add_attr(attrData1)
        attr2 = self.add_attr(attrData2)
        attr3 = self.add_attr(attrData3)
        attr4 = self.add_attr(attrData4)

        self.highlight()

    def attrs(self):
        return self.attrLst

    def add_attr(self, attrData):
        attr = NodeAttr(attrData, self)
        attr.setPos(self.xpos + self.margin/2, len(self.attrLst)*self.attrH + self.headerH)
        self.attrLst.append(attr)
        return attr

    def highlight(self):
        self.stage = self.isSelected()
        return self.stage

    def set_tag(self, tag):
        self.tag = tag

    def set_flag(self, flag):
        return self.setFlag(flag)

    def height(self):
        return self.headerH + len(self.attrLst)*self.attrH + self.footerH

    def type(self):
        return self.Type

    def paint(self, painter, option, widget=None):

        self._rect = self.boundingRect()

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
        painter.drawRoundedRect(self._rect, self.nodeRound, self.nodeRec, RELATIVE_SIZE)
        painter.setFont(font)
        painter.drawText(self.headerRect, self.align, self.name)

    def boundingRect(self):
        self.nodeH = self.height()
        return QRectF(self.xpos, self.ypos, self.nodeW, self.nodeH)

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

    nodeData = {'name': 'PLM'}
    node = Node(nodeData)
    node.setPos(0, 0)
    scene.addItem(node)

    view = QGraphicsView(scene)
    # view.setRenderHint(ANTIALIAS)
    view.setViewportUpdateMode(UPDATE_BOUNDINGVIEW)
    view.setBackgroundBrush(DARKGRAY)
    view.setWindowTitle("pNode test")
    view.show()

    nodeTest.exec_()
# -------------------------------------------------------------------------------------------------------------
# Created by panda on 5/07/2018 - 7:04 AM
# © 2017 - 2018 DAMGteam. All rights reserved