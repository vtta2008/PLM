# -*- coding: utf-8 -*-
"""

Script Name: pEdge.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys, math

# PyQt5
from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QApplication, QGraphicsPathItem
from PyQt5.QtGui import QPainterPath, QPen

# Plt

from appData.scr._pNN import *
from appData.Loggers import SetLogger
logger = SetLogger()

# -------------------------------------------------------------------------------------------------------------
""" pEdge """

class pEdge(QGraphicsPathItem):

    Type = 'pEdge'

    def __init__(self, **kwargs):
        super(pEdge, self).__init__(**kwargs)

        self.lineColor = QColor(10, 10, 10)
        self.removalColor = Qt.red
        self.thickness = 1

        self.srcKnob = None
        self.tarKnob = None

        self.srcPos = QPointF(0, 0)
        self.tarPos = QPointF(0, 0)

        self.curve1 = 0.6
        self.curve3 = 0.4

        self.curve2 = 0.2
        self.curve4 = 0.8

        self.setAcceptHoverEvents(True)

    def updatePath(self):
        if self.srcKnob:
            self.srcPos = self.srcKnob.mapToScene(self.srcKnob.boundingRect().center)

        if self.tarKnob:
            self.tarPos = self.tarKnob.mapToScene(self.tarKnob.boundingRect().center)

        path = QPainterPath()
        path.moveTo(self.srcKnob)

        dx = self.tarPos.x() - self.srcPos.x()
        dy = self.tarPos.y() - self.srcPos.y()

        ctrl1 = QPointF(self.srcPos.x() + dx*self.curve1, self.srcPos.y() + dy*self.curve2)
        ctrl2 = QPointF(self.srcPos.x() + dx*self.curve3, self.srcPos.y() + dy*self.curve4)

        path.cubicTo(ctrl1, ctrl2, self.tarPos)
        self.setPath(path)

    def destroy(self):
        logger.info("Destroy pEdge: {0}".format(self))
        self.srcKnob.removeEdge(self)
        self.tarKnob.removeEdge(self)

    def paint(self, painter, option, widget):

        mod = QApplication.keyboardModifiers() == DMK
        if mod:
            self.setPen(QPen(self.removalColor, self.thickness))
        else:
            self.setPen(QPen(self.lineColor, self.thickness))

        self.setBrush(Qt.NoBrush)
        self.setZValue(-1)
        super(pEdge, self).paint(painter, option, widget)

    def type(self):
        return pEdge.Type

    def mousePressEvent(self, event):
        leftMouse = event.button() == MOUSE_LEFT
        mod = event.modifiers() == DMK
        if leftMouse and mod:
            self.destroy()
# -------------------------------------------------------------------------------------------------------------
# Created by panda on 5/07/2018 - 7:10 AM
# © 2017 - 2018 DAMGteam. All rights reserved