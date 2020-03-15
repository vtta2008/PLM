# -*- coding: utf-8 -*-
"""

Script Name: NodeManager.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PLM.ui import SocketItem, PlugItem, Node
from bin                        import DAMGDICT
from PLM.utils import _swapListIndices


class NodeManager(DAMGDICT):

    key = 'nodeManager'

    def __init__(self):
        super(NodeManager, self).__init__(self)
        self.update()

    def createNode(self, view, name='default', preset='node_default', position=None, alternate=True):
        if name in view.scene().nodes.keys():
            name = '{0}1'.format(name)
        nodeItem = Node(name=name, alternate=alternate, preset=preset)
        if not position:
            position = self.mapToScene(self.viewport().rect().center())
        view.scene().addItem(nodeItem)
        nodeItem.setPos(position - nodeItem.nodeCenter)
        self.add(nodeItem.name, nodeItem)
        return nodeItem

    def deleteNode(self, node):
        if node in self.values():
            node._remove()
            self.pop(node.name)

    def changeNodeName(self, newName=None, node=None):
        oldName = node.name
        if newName != None:
            if not newName in self.keys():
                node.name = newName
                self.add(newName, node)
                self.pop(oldName)
        if node.sockets:
            for socket in node.sockets.values():
                for connection in socket.connections:
                    connection.socketNode = newName
        if node.plugs:
            for plug in node.plugs.values():
                for connection in plug.connections:
                    connection.plugNode = newName
        node.update()

    def createAttribute(self, node, name='default', index=-1, preset='attr_default', plug=True, socket=True,
                                    dataType=None, maxPlug=-1, maxSocket=1):
        if not node in self.values():
            print('NodeNotExistsError: Node object does not exist !')
            return
        if name in node.attrs:
            print('AttributeNameError: An attribute with the same name already exists : {0}'.format(name))
            return
        node._createAttribute(name, index, preset, plug, socket, dataType, maxPlug, maxSocket)

    def deleteAttribute(self, node, index):
        if not node in self.values():
            print('NodeNotExistsError: Node object does not exist !')
            return
        node._deleteAttribute(index)

    def editAttribute(self, node, index, newName=None, newIndex=None):
        if not node in self.values():
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
            self.update()
        node.update()


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/12/2019 - 7:57 PM
# © 2017 - 2018 DAMGteam. All rights reserved