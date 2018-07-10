# -*- coding: utf-8 -*-
"""

Script Name: pView.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys

# PyQt5
from PyQt5.QtCore import pyqtSignal, QPoint
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtGui import QColor, QBrush, QPen

# Plt

from appData.scr._pNN import (SCROLLBAROFF, RUBBERDRAG, ANCHOR_UNDERMICE, CACHE_BACKGROUND, UPDATE_VIEWRECT,
                              ANTIALIAS, ANCHOR_VIEWCENTER, NODRAG, BLOCK, CURRENT_ZOOM, KEY_ALT, KEY_TAB, MOUSE_MIDDLE,
                              CURSOR_SIZEALL, MOUSE_LEFT, CURSOR_ARROW)


# -------------------------------------------------------------------------------------------------------------
""" Variables """

# -------------------------------------------------------------------------------------------------------------
""" pView """

class pView(QGraphicsView):

    def __init__(self, *args, **kwargs):
        super(pView, self).__init__(*args, **kwargs)

        self.fillColor = QColor(250, 250, 250)
        self.lineColor = QColor(230, 230, 230)

        self.xStep = 20
        self.yStep = 20

        self.panningMult = 2.0 * CURRENT_ZOOM
        self.panning = False
        self.zoomStep = 1.1

        self.setHorizontalScrollBarPolicy(SCROLLBAROFF)
        self.setVerticalScrollBarPolicy(SCROLLBAROFF)

        self.setDragMode(RUBBERDRAG)
        self.setTransformationAnchor(ANCHOR_UNDERMICE)
        self.setCacheMode(CACHE_BACKGROUND)
        self.setViewportUpdateMode(UPDATE_VIEWRECT)
        self.setRenderHint(ANTIALIAS)
        self.setTransformationAnchor(ANCHOR_VIEWCENTER)
        self.setResizeAnchor(ANCHOR_VIEWCENTER)

    def pNodes(self):
        return [i for i in self.scene().items() if isinstance(i, pNodeParts)]

    def pEdges(self):
        return [i for i in self.scene().items() if isinstance(i, pEdge)]

    def reDrawEdge(self):
        for pEdge in self.pEdges():
            pEdge.updatePath()

    def keyPressEvent(self, event):
        if event.key() == KEY_ALT:
            self.reDrawEdge()
        elif event.key() == KEY_TAB:
            print("open qline edit window")

        super(pView, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == KEY_ALT:
            self.reDrawEdge()
        super(pView, self).keyReleaseEvent(event)

    def mousePressEvent(self, event):

        if event.button() == MOUSE_MIDDLE:
            self.setDragMode(NODRAG)
            self.panning = True
            self.prevPos = event.pos()
            self.setCursor(CURSOR_SIZEALL)
        elif event.button() == MOUSE_LEFT:
            self.setDragMode(RUBBERDRAG)
        super(pView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.panning:
            delta = (self.mapToScene(event.pos())*self.panningMult - self.mapToScene(self.prevPos)* self.panningMult)*(-1.0)

            center = QPoint(self.viewport().width()/2 + delta.x(), self.viewport().height()/2 + delta.y())

            newCenter = self.mapToScene(center)
            self.centerOn(newCenter)
            self.prevPos = event.pos()
            return
        super(pView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.panning:
            self.panning = False
            self.setCursor(CURSOR_ARROW)
        super(pView, self).mouseReleaseEvent(event)

    def wheelEvent(self, event):
        value = event.angleDelta().y()
        if value > 0:
            zoom = self.zoomStep
        else:
            zoom = 1/self.zoomStep
        self.scale(zoom, zoom)

        global CURRENT_ZOOM
        CURRENT_ZOOM = self.transform().m11()

    def drawBackground(self, painter, rect):
        gr = rect.toRect()

        painter.setBrush(QBrush(self.fillColor))
        painter.setPen(QPen(self.lineColor))

        startX = gr.left() + BLOCK - (gr.left() % BLOCK)
        startY = gr.top() + BLOCK - (gr.top() % BLOCK)
        painter.save()

        for x in range(startX, gr.right(), BLOCK):
            painter.drawLine(x, gr.top(), x, gr.bottom())

        for y in range(startY, gr.bottom(), BLOCK):
            painter.drawLine(gr.left(), y, gr.right(), y)

        painter.restore()
        super(pView, self).drawBackground(painter, rect)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 5/07/2018 - 7:03 AM
# © 2017 - 2018 DAMGteam. All rights reserved