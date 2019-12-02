# -*- coding: utf-8 -*-
"""

Script Name: ScenceGraph.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
""" Import """

# PyThon
import os

# PyQt5
from PyQt5.QtCore               import pyqtSignal, QPointF, QLineF

# PLM
from ui.base import ViewBase, SocketItem, PlugItem, ConnectionItem, NodeItem
from utils                      import _loadConfig, _saveData, _loadData, _swapListIndices, _convert_to_QColor
from toolkits.Widgets           import GraphicScene, RubberBand
from toolkits.Gui               import Brush, Pen
from appData                    import (sceneGraphCfg, ANCHOR_UNDERMICE, ANTIALIAS, ANTIALIAS_HIGH_QUALITY, ANTIALIAS_TEXT,
                                        SMOOTH_PIXMAP_TRANSFORM, NON_COSMETIC_PEN, UPDATE_FULLVIEW, SCROLLBAROFF,
                                        RUBBER_REC, ACTION_MOVE, PATTERN_SOLID)
from appData.config import sceneGraphCfg


class Scene(GraphicScene):

    signal_NodeMoved = pyqtSignal(str, object)

    def __init__(self, parent):
        super(Scene, self).__init__(parent)

        self.gridSize               = parent.config['grid_size']
        self.nodes                  = dict()

    def dragEnterEvent(self, event):
        event.setDropAction(ACTION_MOVE)
        event.accept()

    def dragMoveEvent(self, event):
        event.setDropAction(ACTION_MOVE)
        event.accept()

    def dropEvent(self, event):
        self.signal_Dropped.emit(event.scenePos())
        event.accept()

    def drawBackground(self, painter, rect):

        config = _loadConfig(sceneGraphCfg)
        self._brush = Brush()
        self._brush.setStyle(PATTERN_SOLID)
        self._brush.setColor(_convert_to_QColor(config['bg_color']))
        painter.fillRect(rect, self._brush)
        if self.views()[0].gridVisToggle:
            leftLine = rect.left() - rect.left() % self.gridSize
            topLine = rect.top() - rect.top() % self.gridSize
            lines = list()
            i = int(leftLine)
            while i < int(rect.right()):
                lines.append(QLineF(i, rect.top(), i, rect.bottom()))
                i += self.gridSize
            u = int(topLine)
            while u < int(rect.bottom()):
                lines.append(QLineF(rect.left(), u, rect.right(), u))
                u += self.gridSize
            self.pen = Pen()
            self.pen.setColor(_convert_to_QColor(config['grid_color']))
            self.pen.setWidth(0)
            painter.setPen(self.pen)
            painter.drawLines(lines)

    def updateScene(self):
        for connection in [i for i in self.items() if isinstance(i, ConnectionItem)]:
            connection.target_point = connection.target.center()
            connection.source_point = connection.source.center()
            connection.updatePath()


class View(ViewBase):

    key                         = 'View'

    def __init__(self, parent, configPath=sceneGraphCfg):
        super(View, self).__init__(parent)

        self.config             = _loadConfig(configPath)

        self.setRenderHint(ANTIALIAS, self.config['antialiasing'])
        self.setRenderHint(ANTIALIAS_TEXT, self.config['antialiasing'])
        self.setRenderHint(ANTIALIAS_HIGH_QUALITY, self.config['antialiasing_boost'])
        self.setRenderHint(SMOOTH_PIXMAP_TRANSFORM, self.config['smooth_pixmap'])
        self.setRenderHint(NON_COSMETIC_PEN, True)

        self.setViewportUpdateMode(UPDATE_FULLVIEW)
        self.setTransformationAnchor(ANCHOR_UNDERMICE)
        self.setHorizontalScrollBarPolicy(SCROLLBAROFF)
        self.setVerticalScrollBarPolicy(SCROLLBAROFF)

        self.rubberband         = RubberBand(RUBBER_REC, self)

        # Setup scene.
        scene                   = Scene(self)
        sceneWidth              = self.config['scene_width']
        sceneHeight             = self.config['scene_height']

        scene.setSceneRect(0, 0, sceneWidth, sceneHeight)
        scene.signal_NodeMoved.connect(self.signal_NodeMoved)                           # Connect scene node moved signal
        self.setScene(scene)

        self.previousMouseOffset = 0
        self.zoomDirection       = 0
        self.zoomIncr            = 0

        # Connect signals.
        self.scene().selectionChanged.connect(self._returnSelection)

    # NODES
    def createNode(self, name='default', preset='node_default', position=None, alternate=True):
        if name in self.scene().nodes.keys():
            print('A node with the same name already exists : {0}'.format(name))
            return
        else:
            nodeItem = NodeItem(name=name, alternate=alternate, preset=preset)
            self.scene().nodes[name] = nodeItem
            if not position:
                # Get the center of the view.
                position = self.mapToScene(self.viewport().rect().center())
            # Set node position.
            self.scene().addItem(nodeItem)
            nodeItem.setPos(position - nodeItem.nodeCenter)
            # Emit signal.
            self.signal_NodeCreated.emit(name)
            return nodeItem

    def deleteNode(self, node):
        if not node in self.scene().nodes.values():
            print('Node object does not exist !')
            return
        if node in self.scene().nodes.values():
            nodeName = node.name
            node._remove()
            self.signal_NodeDeleted.emit([nodeName])

    def editNode(self, node, newName=None):
        if not node in self.scene().nodes.values():
            print('NodeNotExistsError: Node object does not exist !')
            return
        oldName = node.name

        if newName != None:
            if newName in self.scene().nodes.keys():
                print('NodeNameError: A node with the same name already exists : {0}'.format(newName))
                return
            else:
                node.name = newName

        self.scene().nodes[newName] = self.scene().nodes[oldName]
        self.scene().nodes.pop(oldName)

        if node.sockets:
            for socket in node.sockets.values():
                for connection in socket.connections:
                    connection.socketNode = newName
        if node.plugs:
            for plug in node.plugs.values():
                for connection in plug.connections:
                    connection.plugNode = newName
        node.update()
        # Emit signal.
        self.signal_NodeEdited.emit(oldName, newName)

    def createAttribute(self, node, name='default', index=-1, preset='attr_default', plug=True, socket=True, dataType=None, plugMaxConnections=-1, socketMaxConnections=1):
        if not node in self.scene().nodes.values():
            print('NodeNotExistsError: Node object does not exist !')
            return
        if name in node.attrs:
            print('AttributeNameError: An attribute with the same name already exists : {0}'.format(name))
            return
        node._createAttribute(name=name, index=index, preset=preset, plug=plug, socket=socket, dataType=dataType, plugMaxConnections=plugMaxConnections, socketMaxConnections=socketMaxConnections)
        # Emit signal.
        self.signal_AttrCreated.emit(node.name, index)

    def deleteAttribute(self, node, index):
        if not node in self.scene().nodes.values():
            print('NodeNotExistsError: Node object does not exist !')
            return
        node._deleteAttribute(index)
        # Emit signal.
        self.signal_AttrDeleted.emit(node.name, index)

    def editAttribute(self, node, index, newName=None, newIndex=None):
        if not node in self.scene().nodes.values():
            print('NodeNotExistsError: Node object does not exist !')
            return
        if newName != None:
            if newName in node.attrs:
                print('AttributeNameError: An attribute with the same name already exists : {0}'.format(newName))
                return
            else:
                oldName = node.attrs[index]
            # Rename in the slot item(s).
            if node.attrsData[oldName]['plug']:
                node.plugs[oldName].attribute = newName
                node.plugs[newName] = node.plugs[oldName]
                node.plugs.pop(oldName)
                for connection in node.plugs[newName].connections:
                    connection.plugAttr = newName
            if node.attrsData[oldName]['socket']:
                node.sockets[oldName].attribute = newName
                node.sockets[newName] = node.sockets[oldName]
                node.sockets.pop(oldName)
                for connection in node.sockets[newName].connections:
                    connection.socketAttr = newName
            # Replace attribute data.
            node.attrsData[oldName]['name'] = newName
            node.attrsData[newName] = node.attrsData[oldName]
            node.attrsData.pop(oldName)
            node.attrs[index] = newName

        if isinstance(newIndex, int):
            attrName = node.attrs[index]
            _swapListIndices(node.attrs, index, newIndex)
            # Refresh connections.
            for plug in node.plugs.values():
                plug.update()
                if plug.connections:
                    for connection in plug.connections:
                        if isinstance(connection.source, PlugItem):
                            connection.source = plug
                            connection.source_point = plug.center()
                        else:
                            connection.target = plug
                            connection.target_point = plug.center()
                        if newName:
                            connection.plugAttr = newName
                        connection.updatePath()

            for socket in node.sockets.values():
                socket.update()
                if socket.connections:
                    for connection in socket.connections:
                        if isinstance(connection.source, SocketItem):
                            connection.source = socket
                            connection.source_point = socket.center()
                        else:
                            connection.target = socket
                            connection.target_point = socket.center()
                        if newName:
                            connection.socketAttr = newName
                        connection.updatePath()
            self.scene().update()
        node.update()

        # Emit signal.
        if newIndex:
            self.signal_AttrEdited.emit(node.name, index, newIndex)
        else:
            self.signal_AttrEdited.emit(node.name, index, index)

    def saveGraph(self, filePath='path'):
        data = dict()
        # Store nodes data.
        data['NODES'] = dict()
        nodes = self.scene().nodes.keys()
        for node in nodes:
            nodeInst = self.scene().nodes[node]
            preset = nodeInst.nodePreset
            nodeAlternate = nodeInst.alternate
            data['NODES'][node] = {'preset'     : preset       , 'position'    : [nodeInst.pos().x(), nodeInst.pos().y()],
                                   'alternate'  : nodeAlternate, 'attributes'  : []}
            attrs = nodeInst.attrs
            for attr in attrs:
                attrData = nodeInst.attrsData[attr]
                # serialize dataType if needed.
                if isinstance(attrData['dataType'], type):
                    attrData['dataType'] = str(attrData['dataType'])
                data['NODES'][node]['attributes'].append(attrData)
        # Store connections data.
        data['CONNECTIONS'] = self.evaluateGraph()


        # Save data.
        try:
            _saveData(filePath=filePath, data=data)
        except:
            print('Invalid path : {0}'.format(filePath))
            print('Save aborted !')
            return False

        # Emit signal.
        self.signal_GraphSaved.emit()

    def loadGraph(self, filePath='path'):
        # Load data.
        if os.path.exists(filePath):
            data                        = _loadData(filePath=filePath)
        else:
            print('Invalid path : {0}'.format(filePath))
            print('Load aborted !')
            return False
        # Apply nodes data.
        nodesData                       = data['NODES']
        nodesName                       = nodesData.keys()
        for name in nodesName:
            preset                      = nodesData[name]['preset']
            position                    = nodesData[name]['position']
            position                    = QPointF(position[0], position[1])
            alternate                   = nodesData[name]['alternate']
            node                        = self.createNode(name=name, preset=preset, position=position, alternate=alternate)
            # Apply attributes data.
            attrsData                   = nodesData[name]['attributes']
            for attrData in attrsData:
                index                   = attrsData.index(attrData)
                name                    = attrData['name']
                plug                    = attrData['plug']
                socket                  = attrData['socket']
                preset                  = attrData['preset']
                dataType                = attrData['dataType']
                plugMaxConnections      = attrData['plugMaxConnections']
                socketMaxConnections    = attrData['socketMaxConnections']
                # un-serialize data type if needed
                if (isinstance(dataType, str) and dataType.find('<') == 0):
                    dataType = eval(str(dataType.split('\'')[1]))
                self.createAttribute(node=node, name=name, index=index, preset=preset, plug=plug, socket=socket,
                                     dataType=dataType, plugMaxConnections=plugMaxConnections,
                                     socketMaxConnections=socketMaxConnections )
        # Apply connections data.
        connectionsData                 = data['CONNECTIONS']
        for connection in connectionsData:
            source                      = connection[0]
            sourceNode                  = source.split('.')[0]
            sourceAttr                  = source.split('.')[1]
            target                      = connection[1]
            targetNode                  = target.split('.')[0]
            targetAttr                  = target.split('.')[1]
            self.createConnection(sourceNode, sourceAttr, targetNode, targetAttr)
        self.scene().update()
        # Emit signal.
        self.signal_GraphLoaded.emit()

    def createConnection(self, sourceNode, sourceAttr, targetNode, targetAttr):
        plug                    = self.scene().nodes[sourceNode].plugs[sourceAttr]
        socket                  = self.scene().nodes[targetNode].sockets[targetAttr]
        connection              = ConnectionItem(plug.center(), socket.center(), plug, socket)

        connection.plugNode     = plug.parentItem().name
        connection.plugAttr     = plug.attribute
        connection.socketNode   = socket.parentItem().name
        connection.socketAttr   = socket.attribute

        plug.connect(socket, connection)
        socket.connect(plug, connection)
        connection.updatePath()
        self.scene().addItem(connection)
        return connection

    def evaluateGraph(self):
        scene                   = self.scene()
        data                    = list()
        for item in scene.items():
            if isinstance(item, ConnectionItem):
                connection = item
                data.append(connection._outputConnectionData())
        # Emit Signal
        self.signal_GraphEvaluated.emit()
        return data

    def clearGraph(self):
        self.scene().clear()
        self.scene().nodes = dict()
        # Emit signal.
        self.signal_GraphCleared.emit()






# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/12/2019 - 1:18 AM
# © 2017 - 2018 DAMGteam. All rights reserved