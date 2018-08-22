# -*- coding: utf-8 -*-
"""

Script Name: pView.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python

# PyQt5
from PyQt5.QtCore import pyqtSignal, QRect, QRectF, QSize
from PyQt5.QtGui import QColor, QBrush, QPen, QCursor, QTransform, QPainterPath
from PyQt5.QtWidgets import QRubberBand, QGraphicsView

# PLM
from core.paths import (ASPEC_RATIO, CACHE_BG, SCROLLBAROFF, RUBBER_DRAG, UPDATE_VIEWRECT, UPDATE_FULLVIEW,
                        ANCHOR_VIEWCENTER,
                        ANCHOR_UNDERMICE, ANTIALIAS, ANTIALIAS_TEXT, ANTIALIAS_HIGH_QUALITY, SMOOTH_PIXMAP_TRANSFORM,
                        NON_COSMETIC_PEN, ALT_MODIFIER, MOUSE_LEFT, MOUSE_MIDDLE, MOUSE_RIGHT, KEY_SHIFT, KEY_CTRL,
                        SHIFT_MODIFIER, NO_MODIFIER, CTRL_MODIFIER, CLOSE_HAND_CUSOR, NOANCHOR, CURSOR_ARROW, KEY_DEL,
                        KEY_BACKSPACE, KEY_F, KEY_S, GRID_SIZE, RUBBER_REC)
from ui.NodeGraph.Node import Edge, Node

# -------------------------------------------------------------------------------------------------------------
""" Viewer """

class View(QGraphicsView):

    nodeCreated = pyqtSignal(object)
    nodeDeleted = pyqtSignal(object)
    nodeEdited = pyqtSignal(object, object)
    nodeSelected = pyqtSignal(object)
    nodeDoubleClick = pyqtSignal(str)
    nodeMoved = pyqtSignal(str, object)

    attrCreated = pyqtSignal(object, object)
    attrDeleted = pyqtSignal(object, object)
    attrEdited = pyqtSignal(object, object, object)

    plugConnected = pyqtSignal(object, object, object, object)
    plugDisconnected = pyqtSignal(object, object, object, object)
    socketConnected = pyqtSignal(object, object, object, object)
    socketDisconnected = pyqtSignal(object, object, object, object)

    graphSaved = pyqtSignal()
    graphLoaded = pyqtSignal()
    graphCleaned = pyqtSignal()
    graphEvaluated = pyqtSignal()

    dropped = pyqtSignal()
    keyPress = pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(View, self).__init__(*args, **kwargs)

        self.fillColor = QColor(250, 250, 250)
        self.lineColor = QColor(230, 230, 230)

        self.xStep = 20
        self.yStep = 20

        self.mtd = dict()

        self.gridVisToggle = True
        self.gridSnapToggle = False
        self._nodeSnap = False
        self.selectedNodes = None

        self.drawingConnection = False
        self.currentHoveredNode = None
        self.sourceSlot = None

        self.currentState = 'DEFAULT'
        self.pressedKeys = list()

        self.zoomInitialPos = self.cursor().pos()
        self.initMousePos = self.cursor().pos()

        self.Nodes = []
        self.nodeID = dict()

        self.currentState = 'DEFAULT'                       # Display options.
        self.pressedKeys = list()

        self.applySetting()

    def createNode(self, nodeData):
        node = Node(nodeData)
        node.nodeID = self.register_nodeID(node.nodeName)
        node.mtd['nodeID'] = node.nodeID
        self.Nodes.append(node)
        self.scene().Nodes[node.nodeName] = node

        if not nodeData['pos']:
            pos = self.mapToScene(self.viewport().rect().center())
        else:
            pos = nodeData['pos']

        self.mtd['nodes'] = self.Nodes
        self.scene().addItem(node)
        node.setPos(pos[0], pos[1])
        self.nodeCreated.emit(node.nodeName)

        return node

    def deleteNode(self, node):
        if not node in self.sceneView.Nodes.values():
            return
        else:
            nodeName = node.nodeName
            node._remove()
            self.nodeDeleted.emit(nodeName)

    def editNode(self, node, newData):
        if not node in self.scene().nodes.values():
            print('Node object does not exist! Attribute creation aborted !')
            return

        if newData['name']:
            if newData['name'] in self.sceneView.Nodes.keys():
                print('A node with the same name already exists : {0}, Node edition aborted!'.format(newData['name']))
                return
            else:
                node.nodeName = newData['name']
        elif newData['pos']:
            if newData['pos'] == node.pos():
                return
            else:
                node.setPos(newData['pos'][0], newData['pos'][1])

    def createAttribute(self, node, attrData):
        if not node in self.sceneView.Nodes.values():
            print('Node object does not exist! Attribute creation aborted !')
            return

        for attr in node.Attrs:
            if attrData['key'] == attr.key:
                print('Node object does not exist! Attribute creation aborted !')
                return

        attr = node.createAttribute(attrData)
        self.attrCreated.emit(node.nodeName, attr.index)

    def deleteAttribute(self, node, index):
        if not node in self.sceneView.Nodes.values():
            print('Node object does not exist!, Attribute deletion aborted !')
            return

        node._deleteAttribute(index)
        self.attrDeleted.emit(node.nodeName, index)

    def getNodes(self):
        return self.Nodes

    def reDrawEdge(self):
        for edge in self.edges():
            edge.updatePath()

    def createConnection(self, sourceNode, sourceAttr, targetNode, targetAttr):

        plug = self.scene().nodes[sourceNode].plugs[sourceAttr]
        socket = self.scene().nodes[targetNode].sockets[targetAttr]
        edge = Edge(plug.center(), socket.center(), plug, socket)

        edge.plugNode = plug.parentItem().name
        edge.plugAttr = plug.attribute
        edge.socketNode = socket.parentItem().name
        edge.socketAttr = socket.attribute

        plug.connect(socket, edge)
        socket.connect(plug, edge)
        edge.updatePath()
        self.scene().addItem(edge)

    def _initRubberband(self, position):
        self.rubberBandStart = position
        self.origin = position
        self.rubberband.setGeometry(QRect(self.origin, QSize()))
        self.rubberband.show()

    def _releaseRubberband(self):
        painterPath = QPainterPath()
        rect = self.mapToScene(self.rubberband.geometry())
        painterPath.addPolygon(rect)
        self.rubberband.hide()
        return painterPath

    def _focus(self):
        if self.scene().selectedItems():
            itemsArea = self._getSelectionBoundingbox()
            self.fitInView(itemsArea, ASPEC_RATIO)
        else:
            itemsArea = self.scene().itemsBoundingRect()
            self.fitInView(itemsArea, ASPEC_RATIO)

    def _getSelectionBoundingbox(self):
        bbx_min = None
        bbx_max = None
        bby_min = None
        bby_max = None
        bbw = 0
        bbh = 0
        for item in self.scene().selectedItems():
            pos = item.scenePos()
            x = pos.x()
            y = pos.y()
            w = x + item.boundingRect().width()
            h = y + item.boundingRect().height()

            if bbx_min is None:
                bbx_min = x
            elif x < bbx_min:
                bbx_min = x

            if bbx_max is None:
                bbx_max = w
            elif w > bbx_max:
                bbx_max = w

            if bby_min is None:
                bby_min = y
            elif y < bby_min:
                bby_min = y

            if bby_max is None:
                bby_max = h
            elif h > bby_max:
                bby_max = h

        bbw = bbx_max - bbx_min
        bbh = bby_max - bby_min
        return QRectF(QRect(bbx_min, bby_min, bbw, bbh))

    def _deleteSelectedNodes(self):
        selected_nodes = list()
        for node in self.scene().selectedItems():
            selected_nodes.append(node.name)
            node._remove()

        self.nodeDeleted.emit(selected_nodes)

    def _returnSelection(self):
        selected_nodes = list()
        if self.scene().selectedItems():
            for node in self.scene().selectedItems():
                selected_nodes.append(node.nodeName)

        self.nodeSelected.emit(selected_nodes)

    def register_nodeID(self, nodeName):
        if self.nodeID == {} or nodeName not in self.nodeID.keys():
            id = 1
            self.nodeID[nodeName] = [id]
        else:
            id = len(self.nodeID[nodeName])
            self.nodeID[nodeName].appent(id)
        return '{0}_{1}'.format(nodeName, str(id))

    def applySetting(self):

        self.previousMouseOffset = 0                                    # Tablet zoom.
        self.zoomDirection = 0
        self.zoomIncr = 0

        self.setHorizontalScrollBarPolicy(SCROLLBAROFF)
        self.setVerticalScrollBarPolicy(SCROLLBAROFF)
        self.setDragMode(RUBBER_DRAG)
        self.setCacheMode(CACHE_BG)
        self.setViewportUpdateMode(UPDATE_VIEWRECT)
        self.setViewportUpdateMode(UPDATE_FULLVIEW)
        self.setResizeAnchor(ANCHOR_VIEWCENTER)
        self.setRenderHint(ANTIALIAS, True)
        self.setRenderHint(ANTIALIAS_TEXT, True)
        self.setRenderHint(ANTIALIAS_HIGH_QUALITY, True)
        self.setRenderHint(SMOOTH_PIXMAP_TRANSFORM, True)
        self.setRenderHint(NON_COSMETIC_PEN, True)
        self.setTransformationAnchor(ANCHOR_UNDERMICE)
        self.setTransformationAnchor(ANCHOR_VIEWCENTER)
        self.setHorizontalScrollBarPolicy(SCROLLBAROFF)
        self.setVerticalScrollBarPolicy(SCROLLBAROFF)

        self.rubberband = QRubberBand(RUBBER_REC, self)

    def wheelEvent(self, event):
        moose = event.angleDelta().y() / 120
        if moose > 0:
            zoomFactor = 1.1
        elif moose < 0:
            zoomFactor = 0.9
        else:
            zoomFactor = 1

        self.scale(zoomFactor, zoomFactor)
        self.currentState = 'DEFAULT'

    def mousePressEvent(self, event):
        if (event.button() == MOUSE_RIGHT and event.modifiers() == ALT_MODIFIER):          # Tablet zoom
            self.currentState = 'ZOOM_VIEW'
            self.initMousePos = event.pos()
            self.zoomInitialPos = event.pos()
            self.initMouse = QCursor.pos()
            self.setInteractive(False)
        elif (event.button() == MOUSE_MIDDLE and event.modifiers() == ALT_MODIFIER):       # Drag view
            self.currentState = 'DRAG_VIEW'
            self.prevPos = event.pos()
            self.setCursor(CLOSE_HAND_CUSOR)
            self.setInteractive(False)
        elif (event.button() == MOUSE_LEFT and event.modifiers() == ALT_MODIFIER and self.scene().itemAt(self.mapToScene(event.pos()), QTransform()) is None):         # Rubber band selection
            self.currentState = 'SELECTION'
            self._initRubberband(event.pos())
            self.setInteractive(False)
        elif (event.button() == MOUSE_LEFT and event.modifiers() ==  NO_MODIFIER and self.scene().itemAt(self.mapToScene(event.pos()), QTransform()) is not None):     # Drag Item
            self.currentState = 'DRAG_ITEM'
            self.setInteractive(True)
        elif (event.button() == MOUSE_LEFT and KEY_SHIFT in self.pressedKeys and
              KEY_CTRL in self.pressedKeys):                                              # Add selection
            self.currentState = 'ADD_SELECTION'
            self._initRubberband(event.pos())
            self.setInteractive(False)
        elif (event.button() == MOUSE_LEFT and event.modifiers() == CTRL_MODIFIER):
            self._initRubberband(event.pos())
            self.setInteractive(False)
        elif (event.button() == MOUSE_LEFT and event.modifiers() == SHIFT_MODIFIER):       # Toggle selection
            self.currentState = 'TOGGLE_SELECTION'
            self._initRubberband(event.pos())
            self.setInteractive(False)
        else:
            self.currentState = 'DEFAULT'
        super(View, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):                                # Zoom.
        if self.currentState == 'ZOOM_VIEW':
            offset = self.zoomInitialPos.x() - event.pos().x()
            if offset > self.previousMouseOffset:
                self.previousMouseOffset = offset
                self.zoomDirection = -1
                self.zoomIncr -= 1
            elif offset == self.previousMouseOffset:
                self.previousMouseOffset = offset
                if self.zoomDirection == -1:
                    self.zoomDirection = -1
                else:
                    self.zoomDirection = 1
            else:
                self.previousMouseOffset = offset
                self.zoomDirection = 1
                self.zoomIncr += 1
            if self.zoomDirection == 1:
                zoomFactor = 1.03
            else:
                zoomFactor = 1 / 1.03

            pBefore = self.mapToScene(self.initMousePos)                    # Perform zoom and re-center on initial click position.
            self.setTransformationAnchor(ANCHOR_VIEWCENTER)
            self.scale(zoomFactor, zoomFactor)
            pAfter = self.mapToScene(self.initMousePos)
            diff = pAfter - pBefore

            self.setTransformationAnchor(NOANCHOR)
            self.translate(diff.x(), diff.y())
        elif self.currentState == 'DRAG_VIEW':                              # Drag canvas.
            offset = self.prevPos - event.pos()
            self.prevPos = event.pos()
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() + offset.y())
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + offset.x())
        elif (self.currentState == 'SELECTION' or self.currentState == 'ADD_SELECTION' or
              self.currentState == 'SUBTRACT_SELECTION' or self.currentState == 'TOGGLE_SELECTION'):   # RuberBand selection.
            self.rubberband.setGeometry(QRect(self.origin, event.pos()).normalized())

        super(View, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.currentState == 'ZOOM_VIEW':                                            # Zoom the View.
            self.offset = 0
            self.zoomDirection = 0
            self.zoomIncr = 0
            self.setInteractive(True)
        elif self.currentState == 'DRAG_VIEW':                                          # Drag View.
            self.setCursor(CURSOR_ARROW)
            self.setInteractive(True)
        elif self.currentState == 'SELECTION':
            self.rubberband.setGeometry(QRect(self.origin, event.pos()).normalized())   # Selection.
            painterPath = self._releaseRubberband()
            self.setInteractive(True)
            self.scene().setSelectionArea(painterPath)
        elif self.currentState == 'ADD_SELECTION':                                      # Add Selection.
            self.rubberband.setGeometry(QRect(self.origin, event.pos()).normalized())
            painterPath = self._releaseRubberband()
            self.setInteractive(True)
            for item in self.scene().items(painterPath):
                item.setSelected(True)

        elif self.currentState == 'SUBTRACT_SELECTION':                                 # Subtract Selection.
            self.rubberband.setGeometry(QRect(self.origin, event.pos()).normalized())
            painterPath = self._releaseRubberband()
            self.setInteractive(True)
            for item in self.scene().items(painterPath):
                item.setSelected(False)
        elif self.currentState == 'TOGGLE_SELECTION':                                   # Toggle Selection
            self.rubberband.setGeometry(QRect(self.origin, event.pos()).normalized())
            painterPath = self._releaseRubberband()
            self.setInteractive(True)
            for item in self.scene().items(painterPath):
                if item.isSelected():
                    item.setSelected(False)
                else:
                    item.setSelected(True)

        self.currentState = 'DEFAULT'
        super(View, self).mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        if event.key() not in self.pressedKeys:
            self.pressedKeys.append(event.key())
        if event.key() in (KEY_DEL, KEY_BACKSPACE):
            self._deleteSelectedNodes()
        if event.key() == KEY_F:
            self._focus()
        if event.key() == KEY_S:
            self._nodeSnap = True

        self.keyPress.emit(event.key())

    def keyReleaseEvent(self, event):
        if event.key() == KEY_S:
            self._nodeSnap = False

        if event.key() in self.pressedKeys:
            self.pressedKeys.remove(event.key())

    def drawBackground(self, painter, rect):
        gr = rect.toRect()

        painter.setBrush(QBrush(self.fillColor))
        painter.setPen(QPen(self.lineColor))

        startX = gr.left() + GRID_SIZE - (gr.left() % GRID_SIZE)
        startY = gr.top() + GRID_SIZE - (gr.top() % GRID_SIZE)
        painter.save()

        for x in range(startX, gr.right(), GRID_SIZE):
            painter.drawLine(x, gr.top(), x, gr.bottom())

        for y in range(startY, gr.bottom(), GRID_SIZE):
            painter.drawLine(gr.left(), y, gr.right(), y)

        painter.restore()
        super(View, self).drawBackground(painter, rect)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 5/07/2018 - 7:03 AM
# © 2017 - 2018 DAMGteam. All rights reserved