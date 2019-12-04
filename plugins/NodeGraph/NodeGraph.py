# -*- coding: utf-8 -*-
"""

Script Name: NodeGraph.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from .base import NodeGraph, Node, Backdrop, setup_context_menu


# create a example node object with a input/output port.
class MyNode(Node):
    """example test node."""

    # unique node identifier domain. ("com.chantasticvfx.MyNode")
    __identifier__ = 'com.chantasticvfx'

    # initial default node name.
    NODE_NAME = 'My Node'

    def __init__(self):
        super(MyNode, self).__init__()
        self.add_input('foo', color=(180, 80, 0))
        self.add_output('bar')



# create the node graph controller.
graph = NodeGraph()

# set up default menu and commands.
setup_context_menu(graph)

# register backdrop node. (included in the NodeGraphQt module)
graph.register_node(Backdrop)

# register example node into the node graph.
graph.register_node(MyNode)

# create nodes.
backdrop = graph.create_node('nodeGraphQt.nodes.Backdrop', name='Backdrop')
node_a = graph.create_node('com.chantasticvfx.MyNode', name='Node A')
node_b = graph.create_node('com.chantasticvfx.MyNode', name='Node B', color='#5b162f')

# connect node a input to node b output.
node_a.set_input(0, node_b.output(0))

# show widget.
viewer = graph.viewer()


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 4/12/2019 - 7:14 PM
# © 2017 - 2018 DAMGteam. All rights reserved