# -*- coding: utf-8 -*-
"""

Script Name: View.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals


import os

from PyQt5.QtCore               import QPointF
from test.SlotBase import ConnectionItem
from test.ViewBase import ViewBase
from utils                      import _saveData, _loadData



class View(ViewBase):

    key                         = 'View'

    def __init__(self, parent=None):
        super(View, self).__init__()

        self.parent             = parent
        # sceneWidth              = self.config['scene_width']
        # sceneHeight             = self.config['scene_height']

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
                plugMaxConnections      = attrData['maxPlug']
                socketMaxConnections    = attrData['maxSocket']
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
# Created by panda on 3/12/2019 - 7:45 PM
# © 2017 - 2018 DAMGteam. All rights reserved