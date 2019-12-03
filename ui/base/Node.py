# -*- coding: utf-8 -*-
"""

Script Name: Node.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from .NodeBase import NodeBase
from .SlotBase import PlugItem, SocketItem


class Node(NodeBase):

    key                             = 'Node'

    def __init__(self, name, preset, alternate):
        super(Node, self).__init__(self)

        self.setZValue(1)
        self._name                  = name
        self.preset                 = preset
        self.alternate              = alternate

    def _createAttribute(self, name, index, preset, plug, socket, dataType, maxPlug, maxSocket):
        if name in self.attrs:
            print('AttributeNameError: attribute name already exists on this node : {0}'.format(name))
            return
        self.attrPreset = preset
        # Create a plug connection item.
        if plug:
            plugInst = PlugItem(parent=self, attribute=name, index=self.attrCount, preset=preset, dataType=dataType, maxConn=maxPlug)
            self.plugs[name] = plugInst
        # Create a socket connection item.
        if socket:
            socketInst = SocketItem(parent=self, attribute=name, index=self.attrCount, preset=preset, dataType=dataType, maxConn=maxSocket)
            self.sockets[name] = socketInst
        self.attrCount += 1
        # Add the attribute based on its index.
        if index == -1 or index > self.attrCount:
            self.attrs.append(name)
        else:
            self.attrs.insert(index, name)
        # Store attr data.
        self.attrsData[name] = {'name': name, 'socket': socket, 'plug': plug, 'preset': preset, 'dataType': dataType, 'maxPlug': maxPlug, 'maxSocket': maxSocket}
        # Update node height.
        self.update()

    def _deleteAttribute(self, index):
        name = self.attrs[index]
        # Remove socket and its connections.
        if name in self.sockets.keys():
            for connection in self.sockets[name].connections:
                connection._remove()
            self.scene().removeItem(self.sockets[name])
            self.sockets.pop(name)
        # Remove plug and its connections.
        if name in self.plugs.keys():
            for connection in self.plugs[name].connections:
                connection._remove()
            self.scene().removeItem(self.plugs[name])
            self.plugs.pop(name)
        # Reduce node height.
        if self.attrCount > 0:
            self.attrCount -= 1
        # Remove attribute from node.
        if name in self.attrs:
            self.attrs.remove(name)
        self.update()

    def _remove(self):
        self.scene().nodes.pop(self.name)
        # Remove all sockets connections.
        for socket in self.sockets.values():
            while len(socket.connections)>0:
                socket.connections[0]._remove()
        # Remove all plugs connections.
        for plug in self.plugs.values():
            while len(plug.connections)>0:
                plug.connections[0]._remove()
        # Remove node.
        scene = self.scene()
        scene.removeItem(self)
        scene.update()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/12/2019 - 8:07 PM
# © 2017 - 2018 DAMGteam. All rights reserved