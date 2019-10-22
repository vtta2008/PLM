# -*- coding: utf-8 -*-
"""

Script Name: pNode.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
import sys

from PyQt5.QtCore import QPointF, QRect, QRectF, pyqtSignal
from PyQt5.QtGui import QPen, QBrush, QPainterPath, QFontMetrics, QTransform, QFont, QColor
# PyQt5
from PyQt5.QtWidgets import QGraphicsObject, QApplication, QGraphicsPathItem, QGraphicsItem, QGraphicsScene

from cores.Loggers import Loggers
# Plt
from appData.config import (DMK, BRUSH_NONE, COLOR_LIBS, PATTERN_SOLID, ITEMPOSCHANGE, LINE_SOLID, ROUND_CAP, ROUND_JOIN,
                           MOUSE_LEFT, POSX, POSY, NODE_WIDTH, ATTR_HEIGHT, ATTR_ROUND, ATTR_REC, NODE_BORDER, NODE_ROUND,
                           NODE_STAMP, NODE_REC, MOVEABLE, SELECTABLE, NODE_HEADER_HEIGHT, NODE_FOOTER_HEIGHT, POS_CHANGE,
                           UPDATE_BOUNDINGVIEW, center, MARGIN)

from utilities.utils import get_pointer_bounding_box, convert_to_QColor, getUnix

# -------------------------------------------------------------------------------------------------------------
""" pEdge """

class Edge(QGraphicsPathItem):

    Type = 'Edge'

    def __init__(self, source_point, target_point, source, target, parent=None):
        super(Edge, self).__init__(parent)

        self.logger = Loggers(self)
        self.applySetting()

        self.socketNode = None
        self.socketAttr = None
        self.socketKnob = None

        self.plugNode = None
        self.plugAttr = None
        self.plugKnob = None

        self.source_point = source_point
        self.target_point = target_point
        self.source = source                                    # Source knob
        self.target = target                                    # Target knob

        self.movable_point = None
        self.data = tuple()

    def applySetting(self):
        self.lineColor = QColor(10, 10, 10)
        self.removalColor = COLOR_LIBS['RED']
        self.thickness = 1
        self.srcPos = QPointF(0, 0)
        self.tarPos = QPointF(0, 0)
        self.curve1 = 0.6
        self.curve3 = 0.4
        self.curve2 = 0.2
        self.curve4 = 0.8
        self.setAcceptHoverEvents(True)
        self.setZValue(-1)

        self._pen = QPen(QColor(255, 155, 0, 255))
        self._pen.setWidth(2)

    def _outputData(self):
        return ("{0}.{1}".format(self.plugNode, self.plugAttr), "{0}.{1}".format(self.socketNode, self.socketAttr))

    def updatePath(self):
        if self.source:
            self.srcPos = self.source.mapToScene(self.source.boundingRect().center())

        if self.target:
            self.tarPos = self.target.mapToScene(self.target.boundingRect().center())

        path = QPainterPath()
        path.moveTo(self.source_point)

        dx = self.tarPos.x() - self.srcPos.x()
        dy = self.tarPos.y() - self.srcPos.y()

        ctrl1 = QPointF(self.srcPos.x() + dx*self.curve1, self.srcPos.y() + dy*self.curve2)
        ctrl2 = QPointF(self.srcPos.x() + dx*self.curve3, self.srcPos.y() + dy*self.curve4)

        path.cubicTo(ctrl1, ctrl2, self.tarPos)
        self.setPath(path)

    def _remove(self):
        if self.source is not None:
            self.source.disconnect(self)
        if self.target is not None:
            self.target.disconnect(self)

        scene = self.scene()
        scene.removeItem(self)
        scene.update()

    def sourceKnob(self):
        return self.source

    def setSourceKnob(self, knob):
        self.source = knob
        self.updatePath()

    def targetKnob(self):
        return self.target

    def setTargetKnob(self, knob):
        self.source = knob
        self.updatePath()

    def paint(self, painter, option, widget):

        mod = QApplication.keyboardModifiers() == DMK
        if mod:
            self.setPen(QPen(self.removalColor, self.thickness))
        else:
            self.setPen(QPen(self.lineColor, self.thickness))

        self.setBrush(QBrush(BRUSH_NONE))
        self.setZValue(-1)
        super(Edge, self).paint(painter, option, widget)

    def type(self):
        return Edge.Type

    def mousePressEvent(self, event):
        nodzInst = self.scene().views()[0]
        for item in nodzInst.scene().items():
            if isinstance(item, Edge):
                item.setZValue(0)

        nodzInst.drawingConnection = True

        d_to_target = (event.pos() - self.target_point).manhattanLength()
        d_to_source = (event.pos() - self.source_point).manhattanLength()
        if d_to_target < d_to_source:
            self.target_point = event.pos()
            self.movable_point = 'target_point'
            self.target.disconnect(self)
            self.target = None
            nodzInst.sourceSlot = self.source
        else:
            self.source_point = event.pos()
            self.movable_point = 'source_point'
            self.source.disconnect(self)
            self.source = None
            nodzInst.sourceSlot = self.target

        self.updatePath()

    def mouseMoveEvent(self, event):
        nodzInst = self.scene().views()[0]
        mbb = get_pointer_bounding_box(pointerPos=event.scenePos().toPoint(), bbSize=80)

        targets = self.scene().items(mbb)

        if any(isinstance(target, Node) for target in targets):

            if nodzInst.sourceSlot.parentItem() not in targets:
                for target in targets:
                    if isinstance(target, Node):
                        nodzInst.currentHoveredNode = target
        else:
            nodzInst.currentHoveredNode = None

        if self.movable_point == 'target_point':
            self.target_point = event.pos()
        else:
            self.source_point = event.pos()

        self.updatePath()

    def mouseReleaseEvent(self, event):
        nodzInst = self.scene().views()[0]
        nodzInst.drawingConnection = False

        slot = self.scene().itemAt(event.scenePos().toPoint(), QTransform())

        if not isinstance(slot, QGraphicsItem):
            self._remove()
            self.updatePath()
            super(Edge, self).mouseReleaseEvent(event)
            return

        if self.movable_point == 'target_point':
            if slot.accepts(self.source):
                self.target = slot
                self.target_point = slot.center()
                plug = self.source
                socket = self.target
                socket.connect(plug, self)
                self.updatePath()
            else:
                self._remove()

        else:
            if slot.accepts(self.target):
                self.source = slot
                self.source_point = slot.center()
                socket = self.target
                plug = self.source
                plug.connect(socket, self)
                self.updatePath()
            else:
                self._remove()

# -------------------------------------------------------------------------------------------------------------
""" Knob """

class Knob(QGraphicsItem):

    Type = 'Knob'

    def __init__(self, parent=None):
        super(Knob, self).__init__(parent)

        self.mtd = dict()
        self.applySetting()
        self.nodeAttr = parent
        self.node = self.nodeAttr.node
        self.knobID = '{0}.{1}.{2}'.format(self.node.nodeName, self.nodeAttr.key, self.type())
        self.knobUnix = self.node.nodeUnix
        self.dataType = self.nodeAttr.dataType
        self.Edges = []
        self.connected_slots = []
        self.maxEdges = -1
        self.newEdge = None
        self.slotType = 'slot'

    def setSlotType(self, slotType):
        self.slotType = slotType
        return self.slotType

    def addEdge(self, edge):
        self.Edges.append(edge)
        edge.updatePath()

    def edges(self):
        return self.Edges

    def accepts(self, knob):
        if self.knobUnix == knob.knobUnix:
            return False
        elif self.maxEdges == 0:
            return False
        else:
            return True

    def setMaxConnection(self, value = -5):
        self.maxEdges = value

    def connect(self, knob, edge):

        if self.maxEdges > 0 and len(self.connected_slots) >= self.maxEdges:
            self.Edges[self.maxEdges - 1]._remove()

        if self.slotType == 'slot':
            if not self.isSelected():
                self.slotType = 'plug'
                edge.socketItem = knob
                edge.plugNode = self.node
                edge.plugAttr = self.nodeAttr
                knobSigal = self.node.plugConnected
            else:
                self.slotType = 'socket'
                edge.plugItem = knob
                edge.socketItem = self.node
                edge.socketItem = self.nodeAttr
                knobSigal = self.node.socketConnected
        else:
            if self.slotType == 'plug':
                edge.socketItem = knob
                edge.plugNode = self.node
                edge.plugAttr = self.nodeAttr
                knobSigal = self.node.plugConnected
            else:
                edge.plugItem = knob
                edge.socketItem = self.node
                edge.socketItem = self.nodeAttr
                knobSigal = self.node.socketConnected

        if knob in self.connected_slots:                                                # Add socket to connected slots.
            self.connected_slots.remove(knob)
        else:
            self.connected_slots.append(knob)

        if edge not in self.Edges:                                                      # Add connection.
            self.Edges.append(edge)

        knobSigal.emit(edge.plugNode, edge.plugAttr, edge.socketNode, edge.socketAttr)

    def disconnect(self, edge):
        if self.slotType == 'plug':
            knobSigal = self.node.plugDisconnected
            knob = edge.socketKnob
        else:
            knobSigal = self.node.socketDisconnected
            knob = edge.plugKnob

        knobSigal.emit(edge.plugNode, edge.plugAttr, edge.socketNode, edge.socketAttr)

        if knob in self.connected_slots :
            self.connected_slots.remove(knob)
        self.Edges.remove(edge)

    def center(self):
        rect = self.boundingRect()
        center = QPointF(rect.x() + rect.width()/2, rect.y() + rect.height()/2)
        return self.mapToScene(center)

    def highlight(self, toggle):
        self.stage = toggle
        return self.stage

    def applySetting(self):
        self.on_color_1 = QColor(240, 101, 53, 255)
        self.on_color_2 = QColor(247, 151, 47, 255)
        self.off_color_1 = QColor(242, 124, 53, 255)
        self.off_color_2 = QColor(236, 137, 36, 255)

        self.brush = QBrush()
        self.brush.setStyle(PATTERN_SOLID)
        self.brush.setColor(QColor(255, 155, 0, 255))

        self.stage = False
        self.setAcceptHoverEvents(True)

    def itemChange(self, change, value):
        if change == ITEMPOSCHANGE:
            for edge in self.Edges:
                edge.updatePath()
            self.node.itemMoved()
        return super(Knob, self).itemChange(change, value)

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
            brush = QBrush(self.off_color_1)

        pen = QPen()
        pen.setStyle(LINE_SOLID)
        pen.setWidthF(1)
        pen.setWidth(2)
        pen.setCapStyle(ROUND_CAP)
        pen.setJoinStyle(ROUND_JOIN)
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

    def mousePressEvent(self, event):
        self.highlight(True)
        if event.button() == MOUSE_LEFT:
            self.newEdge = Edge(self.center(), self.mapToScene(event.pos()), self, None)
            self.Edges.append(self.newEdge)
            self.scene().addItem(self.newEdge)

            self.node.drawingConnection = True
            self.nodeAttr.scrSlot = self
        else:
            super(Knob, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.node.drawingConnection:
            mbb = get_pointer_bounding_box(pointerPos=event.scenePos().toPoint(), bbSize=80)
            targets = self.scene().items(mbb)

            if any(isinstance(target, QGraphicsObject) for target in targets):
                if self.parentItem() not in targets:
                    for target in targets:
                        if isinstance(target, QGraphicsObject):
                            self.node.currentHoveredNode = target
            else:
                self.node.currentHoveredNode = None

            self.newEdge.target_point = self.mapToScene(event.pos())
            self.newEdge.updatePath()
        else:
            super(Knob, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == MOUSE_LEFT:
            self.node.drawingConnection = False

            target = self.scene().itemAt(event.scenePos().toPoint(), QTransform())
            if not isinstance(target, Knob):
                self.newEdge._remove()
                super(Knob, self).mouseReleaseEvent(event)
                return

            if target.accepts(self):
                self.newEdge.target = target
                self.newEdge.source = self
                self.newEdge.target_point = target.center()
                self.newEdge.source_point = self.center()

                self.connect(target, self.newEdge)
                target.connect(self, self.newEdge)

                self.newEdge.updatePath()
            else:
                self.newEdge._remove()
        else:
            super(Knob, self).mouseReleaseEvent(event)

        self.node.currentHoveredNode = None

    def hoverEnterEvent(self, event):
        self.highlight(True)
        super(Knob, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.highlight(False)
        super(Knob, self).hoverLeaveEvent(event)

# -------------------------------------------------------------------------------------------------------------
""" Node's Attribute """

class NodeAttr(QGraphicsItem):

    Type = "Node attribute"
    key = Type

    def __init__(self, attrData, parent=None):
        super(NodeAttr, self).__init__(parent)

        self.logger = Loggers(self)
        self.mtd = dict()
        self.node = parent
        self.index = None
        self.AttrsData = dict()
        self.attrData = attrData
        self.dataType = None
        self.key = self.attrData['key']
        self.value = self.attrData['value']
        self.tooltip = self.attrData['tooltip']
        self.alternate = self.attrData['alternate']
        self.applySetting()

        if not self.dataType or self.dataType is None:
            try:
                self.dataType = self.attrData['dataType']
            except KeyError:
                self.dataType = self.setDataType(type(self.value))
        else:
            if self.dataType is None:
                self.dataType = self.setDataType(type(self.value))
            else:
                pass

        self.mtd['dataType'] = self.dataType
        self.mtd['attrData'] = self.attrData

        self.knobL = self.createKnob('left')
        self.knobR = self.createKnob('right')

        self.mtd['attrName'] = self.key
        self.mtd['nodeName'] = self.node.nodeName
        self.mtd['value'] = self.value

    def createKnob(self, side):
        if side == 'left':
            key = 'knobL'
            posx = self.xpos
        else:
            key = 'knobR'
            posx = self.xpos + self.attrW
        posy = self.attrH / 2 + 20
        knob = Knob(self)
        knob.setPos(posx, posy)
        self.mtd[key] = knob
        return knob

    def highlight(self, toggle):
        self.stage = toggle
        return self.stage

    def setIndex(self, index):
        self.index = index
        self.mtd['index'] = self.index
        return self.index

    def setDataType(self, dataType):
        self.dataType = dataType
        return self.dataType

    def applySetting(self):

        self.xpos = POSX
        self.ypos = POSY
        self.attrW = NODE_WIDTH
        self.attrH = ATTR_HEIGHT
        self.attrRound = ATTR_ROUND
        self.attrRec = ATTR_REC
        self.border = NODE_BORDER/2
        self.radius = NODE_ROUND

        self._rect = QRectF(self.xpos, self.ypos, self.attrW, self.attrH)

        self.content = "{0}: {1}".format(self.key, self.value)
        self.font = 'Arial'
        self.fontH = 10
        self.align = center
        self.stage = None
        self.sourceSlot = None

        self.setAcceptTouchEvents(True)
        self.setAcceptHoverEvents(True)
        self.setToolTip(self.tooltip)
        self.setZValue(1)

        self._attrBrush = QBrush()
        self._attrBrush.setStyle(PATTERN_SOLID)

        self._attrBrushAlt = QBrush()
        self._attrBrushAlt.setStyle(PATTERN_SOLID)

        self._attrPen = QPen()
        self._attrPen.setStyle(LINE_SOLID)

        self._attrTextFont = QFont('Arial', 10, QFont.Normal)

    def boundingRect(self):
        return self._rect

    def paint(self, painter, option, widget=None):
        rect = QRect(self.border, self.attrH - self.radius, self.attrW - self.border, self.attrH)

        self.AttrsData[self] = self.attrData
        name = self.key
        self._attrBrush.setColor(QColor(247, 151, 47, 255))
        if self.alternate:
            self._attrBrushAlt.setColor(convert_to_QColor([19, 17, 15, 255], True, 20))

        self._attrPen.setColor(QColor(16, 102, 162, 255))
        painter.setPen(self._attrPen)
        painter.setBrush(self._attrBrush)

        painter.drawRect(rect)
        painter.setPen(QColor(69, 149, 62, 255))
        painter.setFont(self._attrTextFont)

        if self.node.drawingConnection:
            if self.knobL.slotType == 'slot' and self.knobR.slotType == 'slot':
                painter.setPen(QColor(100, 100, 100, 255))

        textRect = QRect(rect.left() + self.radius, rect.top(), rect.width() - 2*self.radius, rect.height())
        painter.drawText(textRect, center, name)

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

# -------------------------------------------------------------------------------------------------------------
""" Node """

attrData1 = {'key': 'int', 'value': 5, 'tooltip': 'attr int', 'alternate': 20}
attrData2 = {'key': 'float', 'value': 5.0, 'tooltip': 'attr float', 'alternate': 20}
attrData3 = {'key': 'string', 'value': 'abcd', 'tooltip': 'attr string', 'alternate': 20}
attrData4 = {'key': 'func', 'value': None, 'tooltip': 'attr func', 'alternate': 20}

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

    Type = 'Custome Node'
    key = 'nodeBase'
    plugConnected = pyqtSignal(object, object, object, object)
    plugDisconnected = pyqtSignal(object, object, object, object)
    socketConnected = pyqtSignal(object, object, object, object)
    socketDisconnected = pyqtSignal(object, object, object, object)

    def __init__(self, nodeData, parent=None):
        super(Node, self).__init__(parent)

        self.logger = Loggers(self)
        self.mtd = dict()
        self.Knobs = dict()
        self.Attrs = list()
        self.AttrsData = dict()

        self.Flags = list()
        self._parent = parent
        self.nodeName = nodeData['name']
        self.nodeID = None
        self.nodeUnix = getUnix()
        self.drawingConnection = False

        self.attrCount = 0
        self.currentDataType = None

        self.height()
        self.applySetting()
        self.index = -1

        self.attr1 = self.createAttribute(attrData1)
        self.attr2 = self.createAttribute(attrData2)
        self.attr3 = self.createAttribute(attrData3)
        self.attr4 = self.createAttribute(attrData4)

        self.height()
        self._rect = self.boundingRect()

        self.mtd['nodeName'] = self.nodeName
        self.mtd['nodeUnix'] = self.nodeUnix
        self.mtd['pos'] = [self._rect.x(), self._rect.y()]
        self.mtd['width'] = self._rect.width()
        self.mtd['height'] = self._rect.height()

        if len(self.Attrs) > 0:
            self.mtd['attrs'] = self.Attrs
            for attr in self.Attrs:
                attrName = attr.mtd['attrName']
                self.mtd[attrName] = attr.mtd

        self.highlight()

    def set_flag(self, flag):
        self.setFlag(flag)

    def flags(self):
        return self.Flags

    def setTag(self, tag):
        if tag is not None:
            self.tag = tag
            self.mtd['tag'] = self.tag

    def removeTag(self):
        self.tag = None
        self.mtd.pop('tag')

    def setType(self, type):
        self.Type = type
        self.mtd.update(type = self.Type)

    def type(self):
        return self.Type

    def createAttribute(self, attrData):
        attr = NodeAttr(attrData, self)
        attr.setIndex(self.getIndex())
        attr.setPos(self.xpos + self.margin/2, len(self.Attrs)*self.attrH + self.headerH)
        self.Attrs.append(attr)
        return attr

    def deleteAttribute(self, attr):
        if attr in self.Attrs:
            attr.destroy()

    def attrs(self):
        return self.Attrs

    def highlight(self):
        self.stage = self.isSelected()
        return self.stage

    def getIndex(self):
        self.index = self.index + 1
        return self.index

    def height(self):
        self.nodeH = 25 + len(self.Attrs) * 30 + 25
        return self.nodeH

    def pen(self):
        if self.isSelected():
            return self._penSel
        else:
            return self._pen

    def applySetting(self):
        self.setObjectName(self.nodeName)

        self.setAcceptHoverEvents(True)
        self.set_flag(MOVEABLE)
        self.set_flag(SELECTABLE)

        self.margin = MARGIN
        self.nodeW = NODE_WIDTH + self.margin
        self.nodeRec = NODE_REC
        self.xpos = POSX
        self.ypos = POSY
        self.headerH = NODE_HEADER_HEIGHT
        self.footerH = NODE_FOOTER_HEIGHT
        self.border = NODE_BORDER
        self.radius = NODE_ROUND
        self.attrH = ATTR_HEIGHT
        self.headerRect = QRect(self.xpos, self.ypos, self.nodeW, self.headerH)

        self.dragOver = False
        self.tooltip = 'Dev Node'
        self.align = center

        self.nodeCenter = QPointF()
        self.nodeCenter.setX(self.nodeW / 2.0)
        self.nodeCenter.setY(self.nodeH / 2.0)

        self._brush = QBrush()
        self._brush.setStyle(PATTERN_SOLID)
        self._brush.setColor(QColor(30, 30, 30, 255))

        self._pen = QPen()
        self._pen.setStyle(LINE_SOLID)
        self._pen.setWidth(self.border)
        self._pen.setColor(QColor(50, 50, 50, 255))

        self._penSel = QPen()
        self._penSel.setStyle(LINE_SOLID)
        self._penSel.setWidth(self.border)
        self._penSel.setColor(QColor(100, 100, 100, 255))

        self._textPen = QPen()
        self._textPen.setStyle(LINE_SOLID)
        self._textPen.setColor(QColor(255, 255, 255, 255))

        self._nodeTextFont = QFont('Arial', 12, QFont.Bold)

    def paint(self, painter, option, widget=None):
        painter.setBrush(self._brush)
        painter.setPen(self.pen())
        painter.drawRoundedRect(0, 0, self.nodeW, self.nodeH, self.radius, self.radius)
        painter.setPen(self._textPen)
        painter.setFont(self._nodeTextFont)

        metrics = QFontMetrics(painter.font())
        text_width = metrics.boundingRect(self.nodeName).width() + 14
        text_height = metrics.boundingRect(self.nodeName).height() + 14
        margin = (text_width - self.nodeW) * 0.5
        textRect = QRect(-margin, -text_height, text_width, text_height)
        painter.drawText(textRect, center, self.nodeName)

    def boundingRect(self):
        self.nodeH = self.height()
        rect = QRect(self.xpos, self.ypos, self.nodeW, self.nodeH)
        rect = QRectF(rect)
        return rect

    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def itemChange(self, change, value):
        if change == POS_CHANGE:
            for edge in self.pKnobLst:
                edge.updatePath()
            self.itemMoved()
        return super(Node, self).itemChange(change, value)

    def mousePressEvent(self, event):
        self.update()
        super(Node, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.update()
        super(Node, self).mouseReleaseEvent(event)

    def _remove(self):
        self.scene().Nodes.pop(self.nodeName)
        for knob in self.Knobs.value():
            while len(knob.edges)>0:
                knob.edges[0]._remove()

        scene = self.scene()
        scene.removeItem(self)
        scene.update()

if __name__ == '__main__':

    nodeTest = QApplication(sys.argv)
    scene = QGraphicsScene(0, 0, 400, 400)

    nodeData = {'name': 'PLM'}
    node = Node(nodeData)
    node.setPos(0, 0)
    scene.addItem(node)

    view = QGraphicsView(scene)
    view.setViewportUpdateMode(UPDATE_BOUNDINGVIEW)
    view.setBackgroundBrush(COLOR_LIBS['DARKGRAY'])
    view.setWindowTitle("pNode test")
    view.show()

    nodeTest.exec_()
# -------------------------------------------------------------------------------------------------------------
# Created by panda on 5/07/2018 - 7:04 AM
# © 2017 - 2018 DAMGteam. All rights reserved