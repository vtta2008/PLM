# -*- coding: utf-8 -*-
"""

Script Name: Templates.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
# PyQt5
from PyQt5.QtWidgets import QGraphicsObject, QApplication
from PyQt5.QtGui import QPen, QBrush, QPainterPath

# Plt
from appData import center
from appData.scr._nodeGraph import *
from utilities.pUtils import *
from core.Specs import Specs
from core.Loggers import SetLogger

class Node(QGraphicsObject):
    Type = 'Color Node'

    def __init__(self, name, parent=None):
        super(Node, self).__init__(parent)

        self.logger = SetLogger(self)
        self.text = 'Color Profile'
        self.name = name
        self.setObjectName(name)
        self.tooltip = 'Library of color'
        self.applySetting()
        self._rect = QRectF(0, 0, 125, 180)
        self.dragOver = False

        self.AttrLst = []
        self.KnobLst = []
        self.step = 25
        self.nodeWidth = 125
        self._round = 1
        self.rec = 400
        self.xpos = 0
        self.ypos = 0

        self.headerRect = QRectF(self.xpos, self.ypos, self.nodeWidth, 2 * self.step)
        self.colorStamp = QRectF(self.xpos, self.ypos, self.step, self.step)
        self.footerRect = QRectF(0, 0, self.nodeWidth, 2 * self.step)

        self.margin = MARGIN
        self.roundness = ROUNDNESS

    def set_flag(self, flag):
        self.setFlag(flag)

    def set_text(self, txt):
        return self.text

    def nodeType(self):
        return "PLM color data node"

    def applySetting(self):
        self.setFlag(SELECTABLE)
        self.setFlag(MOVEABLE)

        self.setAcceptTouchEvents(True)
        self.setAcceptHoverEvents(True)
        self.setAcceptDrops(True)
        self.setToolTip(self.tooltip)
        self.setZValue(1)

    def addKnob(self, Knob):
        self.pKnobLst.append(Knob)

    def Knobs(self):
        return self.KnobLst

    def Attrs(self):
        return self.AttrLst

    def highlight(self, ):
        self.stage = self.isSelected()
        return self.stage

    def type(self):
        return self.Type

    def paint(self, painter, option, widget=None):
        # Draw header
        rect = QRectF(-10, 10, 145, 260)
        pen = QPen()
        pen.setWidth(2)
        pen.setWidthF(1)
        painter.setBrush(QColor(25,25,25))
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)
        painter.setFont(QFont('Myriad', 10))
        painter.drawText(rect, center, self.text)

        # -------------------------------------------------------------------------------------------------------------
        rect = QRectF(0, 40, 25, 25)
        painter.setBrush(COLOR_CODE['blush'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(25, 40, 25, 25)
        painter.setBrush(COLOR_CODE['petal'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(50, 40, 25, 25)
        painter.setBrush(COLOR_CODE['petunia'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(75, 40, 25, 25)
        painter.setBrush(COLOR_CODE['deep_pink'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(100, 40, 25, 25)
        painter.setBrush(COLOR_CODE['melon'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)
        # -------------------------------------------------------------------------------------------------------------
        rect = QRectF(0, 65, 25, 25)
        painter.setBrush(COLOR_CODE['pomegranate'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(25, 65, 25, 25)
        painter.setBrush(COLOR_CODE['poppy_red'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(50, 65, 25, 25)
        painter.setBrush(COLOR_CODE['orange_red'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(75, 65, 25, 25)
        painter.setBrush(COLOR_CODE['olive'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(100, 65, 25, 25)
        painter.setBrush(COLOR_CODE['spring'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)
        # -------------------------------------------------------------------------------------------------------------
        rect = QRectF(0, 90, 25, 25)
        painter.setBrush(COLOR_CODE['mango'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(25, 90, 25, 25)
        painter.setBrush(COLOR_CODE['cantaloupe'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(50, 90, 25, 25)
        painter.setBrush(COLOR_CODE['tangelo'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(75, 90, 25, 25)
        painter.setBrush(COLOR_CODE['burnt_orange'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(100, 90, 25, 25)
        painter.setBrush(COLOR_CODE['bright_orange'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        # -------------------------------------------------------------------------------------------------------------
        rect = QRectF(0, 115, 25, 25)
        painter.setBrush(COLOR_CODE['moss'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(25, 115, 25, 25)
        painter.setBrush(COLOR_CODE['sage'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(50, 115, 25, 25)
        painter.setBrush(COLOR_CODE['apple'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(75, 115, 25, 25)
        painter.setBrush(COLOR_CODE['grass'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(100, 115, 25, 25)
        painter.setBrush(COLOR_CODE['forest'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        # -------------------------------------------------------------------------------------------------------------
        rect = QRectF(0, 140, 25, 25)
        painter.setBrush(COLOR_CODE['peacock'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(25, 140, 25, 25)
        painter.setBrush(COLOR_CODE['teal'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(50, 140, 25, 25)
        painter.setBrush(COLOR_CODE['aqua'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(75, 140, 25, 25)
        painter.setBrush(COLOR_CODE['violet'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(100, 140, 25, 25)
        painter.setBrush(COLOR_CODE['deep_blue'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        # -------------------------------------------------------------------------------------------------------------
        rect = QRectF(0, 165, 25, 25)
        painter.setBrush(COLOR_CODE['hydrangea'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(25, 165, 25, 25)
        painter.setBrush(COLOR_CODE['sky'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(50, 165, 25, 25)
        painter.setBrush(COLOR_CODE['dusk'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(75, 165, 25, 25)
        painter.setBrush(COLOR_CODE['midnight'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(100, 165, 25, 25)
        painter.setBrush(COLOR_CODE['seaside'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        # -------------------------------------------------------------------------------------------------------------
        rect = QRectF(0, 190, 25, 25)
        painter.setBrush(COLOR_CODE['poolside'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(25, 190, 25, 25)
        painter.setBrush(COLOR_CODE['eggplant'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(50, 190, 25, 25)
        painter.setBrush(COLOR_CODE['lilac'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(75, 190, 25, 25)
        painter.setBrush(COLOR_CODE['chocolate'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(100, 190, 25, 25)
        painter.setBrush(COLOR_CODE['blackout'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        # -------------------------------------------------------------------------------------------------------------

        rect = QRectF(0, 215, 25, 25)
        painter.setBrush(COLOR_CODE['stone'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(25, 215, 25, 25)
        painter.setBrush(COLOR_CODE['gravel'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(50, 215, 25, 25)
        painter.setBrush(COLOR_CODE['pebble'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(75, 215, 25, 25)
        painter.setBrush(COLOR_CODE['sand'])
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

        rect = QRectF(100, 215, 25, 25)
        painter.setBrush(DARKBLUE)
        painter.setPen(QPen(BLACK, 1))
        painter.drawRoundedRect(rect, self._round, self.rec, RELATIVE_SIZE)

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
# Created by panda on 10/07/2018 - 6:38 AM
# © 2017 - 2018 DAMGteam. All rights reserved