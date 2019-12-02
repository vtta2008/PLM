# -*- coding: utf-8 -*-
"""

Script Name: SlotBase.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QColor

from toolkits.Core import RectF, Rect
from toolkits.Gui   import Brush, Pen, Transform, PainterPath
from toolkits.Widgets import GraphicItem, GraphicPathItem
from appData import PATTERN_SOLID, LINE_SOLID, MOUSE_LEFT
from utils import _get_pointer_bounding_box, _convert_to_QColor



class SlotBase(GraphicItem):

    Type                        = 'DAMGSLOTITEM'
    key                         = 'SlotItem'
    _name                       = 'DAMG SLot Item'
    slotType                    = None
    connected_slots             = list()
    newConnection               = None
    connections                 = list()

    def __init__(self, parent, attribute, preset, index, dataType, maxConnections):
        super(SlotBase, self).__init__(parent)

        # Status.
        self.setAcceptHoverEvents(True)

        # Storage.
        self.attribute          = attribute
        self.preset             = preset
        self.index              = index
        self.dataType           = dataType
        self.maxConnections     = maxConnections

        # Style.
        self.brush = Brush()
        self.brush.setStyle(PATTERN_SOLID)
        self.pen = Pen()
        self.pen.setStyle(LINE_SOLID)

    def accepts(self, slot_item):
        # no plug on plug or socket on socket
        hasPlugItem = isinstance(self, PlugItem) or isinstance(slot_item, PlugItem)
        hasSocketItem = isinstance(self, SocketItem) or isinstance(slot_item, SocketItem)
        if not (hasPlugItem and hasSocketItem):
            return False
        # no self connection
        if self.parentItem() == slot_item.parentItem():
            return False
        #no more than maxConnections
        if self.maxConnections>0 and len(self.connected_slots) >= self.maxConnections:
            return False
        #no connection with different types
        if slot_item.dataType != self.dataType:
            return False
        #otherwize, all fine.
        return True

    def mousePressEvent(self, event):
        if event.button() == MOUSE_LEFT:
            self.newConnection = ConnectionItem(self.center(), self.mapToScene(event.pos()), self, None)
            self.connections.append(self.newConnection)
            self.scene().addItem(self.newConnection)
            nodzInst = self.scene().views()[0]
            nodzInst.drawingConnection = True
            nodzInst.sourceSlot = self
            nodzInst.currentDataType = self.dataType
        else:
            super(SlotBase, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        nodzInst = self.scene().views()[0]
        config = nodzInst.config
        if nodzInst.drawingConnection:
            mbb = _get_pointer_bounding_box(pointerPos=event.scenePos().toPoint(), bbSize=config['mouse_bounding_box'])
            # Get nodes in pointer's bounding box.
            targets = self.scene().items(mbb)
            if any(isinstance(target, NodeItem) for target in targets):
                if self.parentItem() not in targets:
                    for target in targets:
                        if isinstance(target, NodeItem):
                            nodzInst.currentHoveredNode = target
            else:
                nodzInst.currentHoveredNode = None
            # Set connection's end point.
            self.newConnection.target_point = self.mapToScene(event.pos())
            self.newConnection.updatePath()
        else:
            super(SlotBase, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        nodzInst = self.scene().views()[0]
        if event.button() == MOUSE_LEFT:
            nodzInst.drawingConnection = False
            nodzInst.currentDataType = None
            target = self.scene().itemAt(event.scenePos().toPoint(), Transform())
            if not isinstance(target, SlotBase):
                self.newConnection._remove()
                super(SlotBase, self).mouseReleaseEvent(event)
                return
            if target.accepts(self):
                self.newConnection.target = target
                self.newConnection.source = self
                self.newConnection.target_point = target.center()
                self.newConnection.source_point = self.center()
                # Perform the ConnectionItem.
                self.connect(target, self.newConnection)
                target.connect(self, self.newConnection)
                self.newConnection.updatePath()
            else:
                self.newConnection._remove()
        else:
            super(SlotBase, self).mouseReleaseEvent(event)
        nodzInst.currentHoveredNode = None

    def shape(self):
        path = PainterPath()
        path.addRect(self.boundingRect())
        return path

    def paint(self, painter, option, widget):
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        nodzInst = self.scene().views()[0]
        config = nodzInst.config
        if nodzInst.drawingConnection:
            if self.parentItem() == nodzInst.currentHoveredNode:
                painter.setBrush(_convert_to_QColor(config['non_connectable_color']))
                if (self.slotType == nodzInst.sourceSlot.slotType or (self.slotType != nodzInst.sourceSlot.slotType and self.dataType != nodzInst.sourceSlot.dataType)):
                    painter.setBrush(_convert_to_QColor(config['non_connectable_color']))
                else:
                    _penValid = Pen()
                    _penValid.setStyle(LINE_SOLID)
                    _penValid.setWidth(2)
                    _penValid.setColor(QColor(255, 255, 255, 255))
                    painter.setPen(_penValid)
                    painter.setBrush(self.brush)
        painter.drawEllipse(self.boundingRect())

    def center(self):
        rect = self.boundingRect()
        center = QPointF(rect.x() + rect.width() * 0.5, rect.y() + rect.height() * 0.5)
        return self.mapToScene(center)


class SocketItem(SlotBase):

    def __init__(self, parent, attribute, index, preset, dataType, maxConnections):
        super(SocketItem, self).__init__(parent, attribute, preset, index, dataType, maxConnections)
        # Storage.
        self.attributte = attribute
        self.preset = preset
        self.slotType = 'socket'
        # Methods.
        self._createStyle(parent)

    def _createStyle(self, parent):
        config = parent.scene().views()[0].config
        self.brush = Brush()
        self.brush.setStyle(PATTERN_SOLID)
        self.brush.setColor(_convert_to_QColor(config[self.preset]['socket']))

    def boundingRect(self):
        width = height = self.parentItem().attrHeight / 2.0
        nodzInst = self.scene().views()[0]
        config = nodzInst.config
        x = - width / 2.0
        y = (self.parentItem().baseHeight - config['node_radius'] + (self.parentItem().attrHeight/4) +
             self.parentItem().attrs.index(self.attribute) * self.parentItem().attrHeight )
        rect = RectF(Rect(x, y, width, height))
        return rect

    def connect(self, plug_item, connection):

        if self.maxConnections>0 and len(self.connected_slots) >= self.maxConnections:
            # Already connected.
            self.connections[self.maxConnections-1]._remove()
        # Populate connection.
        connection.plugItem = plug_item
        connection.socketNode = self.parentItem().name
        connection.socketAttr = self.attribute
        # Add plug to connected slots.
        self.connected_slots.append(plug_item)
        # Add connection.
        if connection not in self.connections:
            self.connections.append(connection)
        # Emit signal.
        nodzInst = self.scene().views()[0]
        nodzInst.signal_SocketConnected.emit(connection.plugNode, connection.plugAttr, connection.socketNode, connection.socketAttr)

    def disconnect(self, connection):
        # Emit signal.
        nodzInst = self.scene().views()[0]
        nodzInst.signal_SocketDisconnected.emit(connection.plugNode, connection.plugAttr, connection.socketNode, connection.socketAttr)
        # Remove connected plugs
        if connection.plugItem in self.connected_slots:
            self.connected_slots.remove(connection.plugItem)
        # Remove connections
        self.connections.remove(connection)


class PlugItem(SlotBase):

    key                             = 'PlugItem'
    slotType                        = 'plug'

    def __init__(self, parent, attribute, index, preset, dataType, maxConnections):
        super(PlugItem, self).__init__(parent, attribute, preset, index, dataType, maxConnections)

        # Storage.
        self.attributte             = attribute
        self.preset                 = preset
        config = parent.scene().views()[0].config

        self.brush = Brush()
        self.brush.setStyle(PATTERN_SOLID)
        self.brush.setColor(_convert_to_QColor(config[self.preset]['plug']))

    def boundingRect(self):
        width = height = self.parentItem().attrHeight / 2.0
        nodzInst = self.scene().views()[0]
        config = nodzInst.config

        x = self.parentItem().baseWidth - (width / 2.0)
        y = (self.parentItem().baseHeight - config['node_radius'] + self.parentItem().attrHeight / 4 +
             self.parentItem().attrs.index(self.attribute) * self.parentItem().attrHeight)
        rect = RectF(Rect(x, y, width, height))
        return rect

    def connect(self, socket_item, connection):
        if self.maxConnections>0 and len(self.connected_slots) >= self.maxConnections:
            self.connections[self.maxConnections-1]._remove()
        # Populate connection.
        connection.socketItem = socket_item
        connection.plugNode = self.parentItem().name
        connection.plugAttr = self.attribute
        # Add socket to connected slots.
        if socket_item in self.connected_slots:
            self.connected_slots.remove(socket_item)
        self.connected_slots.append(socket_item)
        # Add connection.
        if connection not in self.connections:
            self.connections.append(connection)
        # Emit signal.
        nodzInst = self.scene().views()[0]
        nodzInst.signal_PlugConnected.emit(connection.plugNode, connection.plugAttr, connection.socketNode, connection.socketAttr)

    def disconnect(self, connection):
        # Emit signal.
        nodzInst = self.scene().views()[0]
        nodzInst.signal_PlugDisconnected.emit(connection.plugNode, connection.plugAttr, connection.socketNode, connection.socketAttr)
        # Remove connected socket from plug
        if connection.socketItem in self.connected_slots:
            self.connected_slots.remove(connection.socketItem)
        # Remove connection
        self.connections.remove(connection)


class ConnectionItem(GraphicPathItem):

    key = 'ConnectionItem'

    socketNode                              = None
    socketAttr                              = None
    plugNode                                = None
    plugAttr                                = None
    plugItem                                = None
    socketItem                              = None
    movable_point                           = None

    data = tuple()

    def __init__(self, source_point, target_point, source, target):

        super(ConnectionItem, self).__init__()

        self.setZValue(1)

        # Storage.
        self.source_point = source_point
        self.target_point = target_point
        self.source = source
        self.target = target

        config = self.source.scene().views()[0].config
        self.setAcceptHoverEvents(True)
        self.setZValue(-1)
        self._pen = Pen(_convert_to_QColor(config['connection_color']))
        self._pen.setWidth(config['connection_width'])

    def _outputConnectionData(self):
        return ("{0}.{1}".format(self.plugNode, self.plugAttr),
                "{0}.{1}".format(self.socketNode, self.socketAttr))

    def mousePressEvent(self, event):
        nodzInst = self.scene().views()[0]
        for item in nodzInst.scene().items():
            if isinstance(item, ConnectionItem):
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
        config = nodzInst.config
        mbb = _get_pointer_bounding_box(pointerPos=event.scenePos().toPoint(), bbSize=config['mouse_bounding_box'])
        # Get nodes in pointer's bounding box.
        targets = self.scene().items(mbb)
        if any(isinstance(target, NodeItem) for target in targets):
            if nodzInst.sourceSlot.parentItem() not in targets:
                for target in targets:
                    if isinstance(target, NodeItem):
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
        slot = self.scene().itemAt(event.scenePos().toPoint(), Transform())
        if not isinstance(slot, SlotBase):
            self._remove()
            self.updatePath()
            super(ConnectionItem, self).mouseReleaseEvent(event)
            return
        if self.movable_point == 'target_point':
            if slot.accepts(self.source):
                # Plug reconnection.
                self.target = slot
                self.target_point = slot.center()
                plug = self.source
                socket = self.target
                # Reconnect.
                socket.connect(plug, self)
                self.updatePath()
            else:
                self._remove()
        else:
            if slot.accepts(self.target):
                # Socket Reconnection
                self.source = slot
                self.source_point = slot.center()
                socket = self.target
                plug = self.source
                # Reconnect.
                plug.connect(socket, self)
                self.updatePath()
            else:
                self._remove()

    def _remove(self):
        if self.source is not None:
            self.source.disconnect(self)
        if self.target is not None:
            self.target.disconnect(self)
        scene = self.scene()
        scene.removeItem(self)
        scene.update()

    def updatePath(self):
        self.setPen(self._pen)
        path = PainterPath()
        path.moveTo(self.source_point)
        dx = (self.target_point.x() - self.source_point.x()) * 0.5
        dy = self.target_point.y() - self.source_point.y()
        ctrl1 = QPointF(self.source_point.x() + dx, self.source_point.y() + dy * 0)
        ctrl2 = QPointF(self.source_point.x() + dx, self.source_point.y() + dy * 1)
        path.cubicTo(ctrl1, ctrl2, self.target_point)
        self.setPath(path)



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/12/2019 - 4:40 AM
# © 2017 - 2018 DAMGteam. All rights reserved