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

# Plt
import appData as app
from appData._layoutSetting import *
from appData._exception import KnobConnectionError, UnknownFlowError
from pUtils import *

from pEdge import pEdge

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logger = app.logger

# -------------------------------------------------------------------------------------------------------------
""" pKnob """

class pKnob(QGraphicsItem):

    def __init__(self, **kwargs):
        super(pKnob, self).__init__(**kwargs)

        self.x = 0
        self.y = 0
        self.w = 10
        self.h = 10
        self.margin = 5
        self.flow = FLTR
        self.maxConnections = -1
        self.name = "value"
        self.displayName = self.name

        self.labelColor = QColor(10, 10, 10)
        self.fillColor = QColor(130, 130, 130)
        self.highlightColor = QColor(255, 255, 0)

        self.newEdge = None
        self.edges = []
        self.setAcceptHoverEvents(True)

    def node(self):
        return self.parentItem()

    def boundingRect(self):
        return QRectF(self.x, self.y, self.w, self.h)

    def connectTo(self, knob):
        if knob is self:
            return

        self.checkMaxConnections(knob)

        edge = pEdge()
        edge.source = self
        edge.target = knob
        edge.updatePath()

    def addEdge(self, edge):
        self.edges.append(edge)
        scene = self.scene()
        if edge not in scene.items():
            scene.addItem(edge)

    def removeEdge(self, edge):
        self.edges.remove(edge)
        scene = self.scene()
        if edge in scene.items():
            scene.removeItem(edge)

    def highlight(self, toggle):
        if toggle:
            self._oldFilColor = self.fillColor
            self.fillColor = self.highlightColor
        else:
            self.fillColor = self._oldFilColor

    def checkMaxConnections(self, knob):

        noLimits = self.maxConnections < 0 and knob.maxConnections < 0
        if noLimits:
            return

        numSourceConnections = len(self.edges)  # Edge already added.
        numTargetConnections = len(knob.edges) + 1

        print(numSourceConnections, numTargetConnections)

        sourceMaxReached = numSourceConnections > self.maxConnections
        targetMaxReached = numTargetConnections > knob.maxConnections

        if sourceMaxReached or targetMaxReached:
            raise KnobConnectionError(
                "Maximum number of connections reached.")

    def finalizeEdge(self, edge):
        pass

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

def ensureEdgeDirection(edge):

    print("ensure edge direction")
    if isinstance(edge.target, OutputKnob):
        assert isinstance(edge.source, InputKnob)
        actualTarget = edge.source
        edge.source = edge.target
        edge.target = actualTarget
    else:
        assert isinstance(edge.source, OutputKnob)
        assert isinstance(edge.target, InputKnob)

    print("src:", edge.source.__class__.__name__,
          "trg:", edge.target.__class__.__name__)


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


def main():
    app = QApplication(sys.argv)
    layout = pKnob()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 17/06/2018 - 3:14 PM
# © 2017 - 2018 DAMGteam. All rights reserved