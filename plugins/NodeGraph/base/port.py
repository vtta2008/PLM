#!/usr/bin/python
from .commands import (PortConnectedCmd, PortDisconnectedCmd, PortVisibleCmd, NodeInputConnectedCmd,
                       NodeInputDisconnectedCmd)
from .model import PortModel
from appData import IN_PORT, OUT_PORT


class Port(object):

    def __init__(self, node, port):
        self.__view = port
        self.__model = PortModel(node)

    def __repr__(self):
        port = str(self.__class__.__name__)
        return '<{}("{}") object at {}>'.format(port, self.name(), hex(id(self)))

    @property
    def view(self):
        return self.__view

    @property
    def model(self):
        return self.__model

    def type_(self):
        return self.model.type_

    def multi_connection(self):
        return self.model.multi_connection

    def node(self):
        return self.model.node

    def name(self):
        return self.model.name

    def visible(self):
        return self.model.visible

    def set_visible(self, visible=True):
        label = 'show' if visible else 'hide'
        undo_stack = self.node().graph.undo_stack()
        undo_stack.beginMacro('{} port {}'.format(label, self.name()))

        connected_ports = self.connected_ports()
        if connected_ports:
            for port in connected_ports:
                undo_stack.push(PortDisconnectedCmd(self, port))

        undo_stack.push(PortVisibleCmd(self))
        undo_stack.endMacro()

    def connected_ports(self):
        ports = []
        graph = self.node().graph
        for node_id, port_names in self.model.connected_ports.items():
            for port_name in port_names:
                node = graph.get_node_by_id(node_id)
                if self.type_() == IN_PORT:
                    ports.append(node.outputs()[port_name])
                elif self.type_() == OUT_PORT:
                    ports.append(node.inputs()[port_name])
        return ports

    def connect_to(self, port=None):
        if not port:
            return

        graph = self.node().graph
        viewer = graph.viewer()

        undo_stack = graph.undo_stack()
        undo_stack.beginMacro('connect port')

        pre_conn_port = None
        src_conn_ports = self.connected_ports()
        if not self.multi_connection() and src_conn_ports:
            pre_conn_port = src_conn_ports[0]

        if not port:
            if pre_conn_port:
                undo_stack.push(NodeInputDisconnectedCmd(self, port))
                undo_stack.push(PortDisconnectedCmd(self, port))
            return

        if graph.acyclic() and viewer.acyclic_check(self.view, port.view):
            if pre_conn_port:
                undo_stack.push(NodeInputDisconnectedCmd(self, pre_conn_port))
                undo_stack.push(PortDisconnectedCmd(self, pre_conn_port))
                return

        trg_conn_ports = port.connected_ports()
        if not port.multi_connection() and trg_conn_ports:
            dettached_port = trg_conn_ports[0]
            undo_stack.push(NodeInputDisconnectedCmd(port, dettached_port))
            undo_stack.push(PortDisconnectedCmd(port, dettached_port))
        if pre_conn_port:
            undo_stack.push(NodeInputDisconnectedCmd(self, pre_conn_port))
            undo_stack.push(PortDisconnectedCmd(self, pre_conn_port))

        undo_stack.push(NodeInputConnectedCmd(self, port))
        undo_stack.push(PortConnectedCmd(self, port))
        undo_stack.endMacro()
        ports = {p.type_(): p for p in [self, port]}
        graph.port_connected.emit(ports[IN_PORT], ports[OUT_PORT])

    def disconnect_from(self, port=None):
        if not port:
            return
        graph = self.node().graph
        graph.undo_stack().beginMacro('disconnect port')
        graph.undo_stack().push(NodeInputDisconnectedCmd(self, port))
        graph.undo_stack().push(PortDisconnectedCmd(self, port))
        graph.undo_stack().endMacro()

        # emit "port_disconnected" signal from the parent graph.
        ports = {p.type_(): p for p in [self, port]}
        graph.port_disconnected.emit(ports[IN_PORT], ports[OUT_PORT])
