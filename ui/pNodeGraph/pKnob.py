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
from appData.scr._pNN import *
from utilities.pUtils import *
from ui.pNodeGraph.pEdge import pEdge

# -------------------------------------------------------------------------------------------------------------
""" pKnob """


class pKnob(QGraphicsItem):
    Type = 'pKnob'

    def __init__(self, **kwargs):
        super(pKnob, self).__init__(**kwargs)

        self.name = "knob"

        self.x = 0
        self.y = 0
        self.w = 10
        self.h = 10

        self.margin = 5
        self.flow = FLTR
        self.maxConnections = -1
        self.displayName = self.name

        self.labelColor = QColor(10, 10, 10)
        self.fillColor = QColor(130, 130, 130)
        self.highlightColor = QColor(255, 255, 0)

        self.newEdge = None
        self.edges = []
        self.setAcceptHoverEvents(True)

    def pNode(self):
        return self.parentItem()

    def connectTo(self, pKnob):
        if pKnob is self:
            return

        self.checkMaxConnections(pKnob)

        edge = pEdge()
        edge.source = self
        edge.target = pKnob
        edge.updatePath()

    def addEdge(self, pEdge):
        self.edges.append(pEdge)
        scene = self.scene()
        if pEdge not in scene.items():
            scene.addItem(pEdge)

    def removeEdge(self, pEdge):
        self.edges.remove(pEdge)
        scene = self.scene()
        if pEdge in scene.items():
            scene.removeItem(pEdge)

    def highlight(self, toggle):
        if toggle:
            self._oldFilColor = self.fillColor
            self.fillColor = self.highlightColor
        else:
            self.fillColor = self._oldFilColor
        self.update()
        super(pKnob, self).highlight()

    def checkMaxConnections(self, knob):

        noLimits = self.maxConnections < 0 and knob.maxConnections < 0
        if noLimits:
            return

        numSourceConnections = len(self.edges)  # Edge already added.
        numTargetConnections = len(knob.pKnobs) + 1

        print(numSourceConnections, numTargetConnections)

        sourceMaxReached = numSourceConnections > self.maxConnections
        targetMaxReached = numTargetConnections > knob.maxConnections

        if sourceMaxReached or targetMaxReached:
            raise KnobConnectionError(
                "Maximum number of connections reached.")

    def destroy(self):

        print("destroy knob:", self)
        edgesToDelete = self.edges[::]  # Avoid shrinking during deletion.
        for edge in edgesToDelete:
            edge.destroy()
        node = self.parentItem()
        if node:
            node.removeKnob(self)

        self.scene().removeItem(self)
        del self

    def finalizeEdge(self, edge):
        pass

    def type(self):
        return self.Type

    def boundingRect(self):
        return QRectF(self.x, self.y, self.w, self.h)

    def paint(self, painter, option, widget):
        bbox = self.boundingRect()

        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(QBrush(self.fillColor))
        painter.drawRect(bbox)
        painter.setRenderHint(QPainter.Antialiasing)

        textSize = getTextSize(self.displayName, painter=painter)

        if self.flow == FRTL:
            x = bbox.right() + self.margin
        elif self.flow == FLTR:
            x = bbox.left() - self.margin - textSize.width()
        else:
            raise UnknownFlowError("Flow not recognized: {0}".format(self.flow))

        y = bbox.bottom()

        painter.setPen(QPen(self.labelColor))
        painter.drawText(x, y, self.displayName)

    def hoverEnterEvent(self, event):
        self.highlight(True)
        super(pKnob, self).hoverEnterEvent(event)

    def mousePressEvent(self, event):
        self.highlight(False)
        super(pKnob, self).mousePressEvent(event)

    def hoverLeaveEvent(self, event):
        self.highlight(False)
        super(pKnob, self).hoverLeaveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.leftButton:

            node = self.parentItem()
            scene = node.scene()
            target = scene.iteamAt(event.scenePos())

            try:
                if self.newEdge and target:
                    raise KnobConnectionError("Can't connect a knob to itself")
                if isinstance(target, pKnob):

                    if type(self) == type(target):
                        raise KnobConnectionError(
                            "Can't connect Knobs of same type.")

                    newConn = [self, target]
                    for edge in self.edges:
                        existingConn = [edge.source, edge.target]
                        diff = existingConn.difference(newConn)
                        if not diff:
                            raise KnobConnectionError("Connection already exists.")
                            return

                    self.checkMaxConnections(target)

                    print("finish edge")
                    target.addEdge(self.newEdge)
                    self.newEdge.target = target
                    self.newEdge.updatePath()
                    self.finalizeEdge(self.newEdge)
                    self.newEdge = None
                    return

                raise KnobConnectionError(
                    "Edge creation cancelled by user.")

            except KnobConnectionError as err:
                print(err)
            # Abort Edge creation and do some cleanup.
            self.removeEdge(self.newEdge)
            self.newEdge = None


def ensureEdgeDirection(pEdge):
    print("ensure edge direction")
    if isinstance(pEdge.target, OutputKnob):
        assert isinstance(pEdge.source, InputKnob)
        actualTarget = pEdge.source
        pEdge.source = pEdge.target
        pEdge.target = actualTarget
    else:
        assert isinstance(pEdge.source, OutputKnob)
        assert isinstance(pEdge.target, InputKnob)

    print("src:", pEdge.source.__class__.__name__,
          "trg:", pEdge.target.__class__.__name__)


class InputKnob(pKnob):
    """A Knob that represents an input value for its Node."""

    def __init__(self, *args, **kwargs):
        super(InputKnob, self).__init__(*args, **kwargs)

        self.name = kwargs.get("name", "input")
        self.displayName = kwargs.get("displayName", self.name)
        self.fillColor = kwargs.get("fillColor", QColor(130, 230, 130))

    def finalizeEdge(self, edge):
        ensureEdgeDirection(edge)


class OutputKnob(pKnob):
    """A Knob that represents an output value for its Node."""

    def __init__(self, *args, **kwargs):
        super(OutputKnob, self).__init__(*args, **kwargs)

        self.name = kwargs.get("name", "output")
        self.displayName = kwargs.get("displayName", self.name)
        self.fillColor = kwargs.get("fillColor", QColor(230, 130, 130))
        self.flow = kwargs.get("flow", FLTR)

    def finalizeEdge(self, edge):
        ensureEdgeDirection(edge)
# -------------------------------------------------------------------------------------------------------------
# Created by panda on 5/07/2018 - 7:09 AM
# © 2017 - 2018 DAMGteam. All rights reserved