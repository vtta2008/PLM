#!/usr/bin/python
from appData                        import IN_PORT, OUT_PORT
from devkit.Widgets                 import UndoCommand


class PropertyChangedCmd(UndoCommand):

    def __init__(self, node, name, value):
        UndoCommand.__init__(self)
        if name == 'name':
            self.setText('renamed "{}" to "{}"'.format(node.name(), value))
        else:
            self.setText('property "{}:{}"'.format(node.name(), name))
        self.node               = node
        self.name               = name
        self.old_val            = node.get_property(name)
        self.new_val            = value

    def set_node_prop(self, name, value):
        # set model data.
        model                   = self.node.model
        view                    = self.node.view
        model.set_property(name, value)
        # view widgets.
        if hasattr(view, 'widgets') and name in view.widgets.keys():
            if view.widgets[name].value != value:
                view.widgets[name].value = value
        # view properties.
        if name in view.properties.keys():
            # remap "pos" to "xy_pos" node view has pre-existing pos method.
            if name == 'pos':
                name = 'xy_pos'
            setattr(view, name, value)

    def undo(self):
        if self.old_val != self.new_val:
            self.set_node_prop(self.name, self.old_val)
            # emit property changed signal.
            graph = self.node.graph
            graph.property_changed.emit(self.node, self.name, self.old_val)

    def redo(self):
        if self.old_val != self.new_val:
            self.set_node_prop(self.name, self.new_val)
            # emit property changed signal.
            graph = self.node.graph
            graph.property_changed.emit(self.node, self.name, self.new_val)


class NodeMovedCmd(UndoCommand):

    def __init__(self, node, pos, prev_pos):
        UndoCommand.__init__(self)
        self.node = node
        self.pos = pos
        self.prev_pos = prev_pos

    def undo(self):
        self.node.view.xy_pos = self.prev_pos
        self.node.model.pos = self.prev_pos

    def redo(self):
        if self.pos == self.prev_pos:
            return
        self.node.view.xy_pos = self.pos
        self.node.model.pos = self.pos


class NodeAddedCmd(UndoCommand):

    def __init__(self, graph, node, pos=None):
        UndoCommand.__init__(self)
        self.setText('added node')
        self.viewer = graph.viewer()
        self.model = graph.model
        self.node = node
        self.pos = pos

    def undo(self):
        self.pos = self.pos or self.node.pos()
        self.model.nodes.pop(self.node.id)
        self.node.view.delete()

    def redo(self):
        self.model.nodes[self.node.id] = self.node
        self.viewer.add_node(self.node.view, self.pos)


class NodeRemovedCmd(UndoCommand):

    def __init__(self, graph, node):
        UndoCommand.__init__(self)
        self.setText('deleted node')
        self.scene = graph.scene()
        self.model = graph.model
        self.node = node
        self.inputs = []
        self.outputs = []
        if hasattr(self.node, 'inputs'):
            input_ports = self.node.inputs().values()
            self.inputs = [(p, p.connected_ports()) for p in input_ports]
        if hasattr(self.node, 'outputs'):
            output_ports = self.node.outputs().values()
            self.outputs = [(p, p.connected_ports()) for p in output_ports]

    def undo(self):
        self.model.nodes[self.node.id] = self.node
        self.scene.addItem(self.node.view)
        for port, connected_ports in self.inputs:
            [port.connect_to(p) for p in connected_ports]
        for port, connected_ports in self.outputs:
            [port.connect_to(p) for p in connected_ports]

    def redo(self):
        for port, connected_ports in self.inputs:
            [port.disconnect_from(p) for p in connected_ports]
        for port, connected_ports in self.outputs:
            [port.disconnect_from(p) for p in connected_ports]
        self.model.nodes.pop(self.node.id)
        self.node.view.delete()


class NodeInputConnectedCmd(UndoCommand):

    def __init__(self, src_port, trg_port):
        UndoCommand.__init__(self)
        if src_port.type_() == IN_PORT:
            self.source = src_port
            self.target = trg_port
        else:
            self.source = trg_port
            self.target = src_port

    def undo(self):
        node = self.source.node()
        node.on_input_disconnected(self.source, self.target)

    def redo(self):
        node = self.source.node()
        node.on_input_connected(self.source, self.target)


class NodeInputDisconnectedCmd(UndoCommand):

    def __init__(self, src_port, trg_port):
        UndoCommand.__init__(self)
        if src_port.type_() == IN_PORT:
            self.source = src_port
            self.target = trg_port
        else:
            self.source = trg_port
            self.target = src_port

    def undo(self):
        node = self.source.node()
        node.on_input_connected(self.source, self.target)

    def redo(self):
        node = self.source.node()
        node.on_input_disconnected(self.source, self.target)


class PortConnectedCmd(UndoCommand):

    def __init__(self, src_port, trg_port):
        UndoCommand.__init__(self)
        self.source = src_port
        self.target = trg_port

    def undo(self):
        src_model = self.source.model
        trg_model = self.target.model
        src_id = self.source.node().id
        trg_id = self.target.node().id

        port_names = src_model.connected_ports.get(trg_id)
        if port_names is []:
            del src_model.connected_ports[trg_id]
        if port_names and self.target.name() in port_names:
            port_names.remove(self.target.name())

        port_names = trg_model.connected_ports.get(src_id)
        if port_names is []:
            del trg_model.connected_ports[src_id]
        if port_names and self.source.name() in port_names:
            port_names.remove(self.source.name())

        self.source.view.disconnect_from(self.target.view)

    def redo(self):
        src_model = self.source.model
        trg_model = self.target.model
        src_id = self.source.node().id
        trg_id = self.target.node().id

        src_model.connected_ports[trg_id].append(self.target.name())
        trg_model.connected_ports[src_id].append(self.source.name())

        self.source.view.connect_to(self.target.view)


class PortDisconnectedCmd(UndoCommand):

    def __init__(self, src_port, trg_port):
        UndoCommand.__init__(self)
        self.source = src_port
        self.target = trg_port

    def undo(self):
        src_model = self.source.model
        trg_model = self.target.model
        src_id = self.source.node().id
        trg_id = self.target.node().id

        src_model.connected_ports[trg_id].append(self.target.name())
        trg_model.connected_ports[src_id].append(self.source.name())

        self.source.view.connect_to(self.target.view)

    def redo(self):
        src_model = self.source.model
        trg_model = self.target.model
        src_id = self.source.node().id
        trg_id = self.target.node().id

        port_names = src_model.connected_ports.get(trg_id)
        if port_names is []:
            del src_model.connected_ports[trg_id]
        if port_names and self.target.name() in port_names:
            port_names.remove(self.target.name())

        port_names = trg_model.connected_ports.get(src_id)
        if port_names is []:
            del trg_model.connected_ports[src_id]
        if port_names and self.source.name() in port_names:
            port_names.remove(self.source.name())

        self.source.view.disconnect_from(self.target.view)


class PortVisibleCmd(UndoCommand):

    def __init__(self, port):
        UndoCommand.__init__(self)
        self.port = port
        self.visible = port.visible()

    def set_visible(self, visible):
        self.port.model.visible = visible
        self.port.view.setVisible(visible)
        node_view = self.port.node().view
        text_item = None
        if self.port.type_() == IN_PORT:
            text_item = node_view.get_input_text_item(self.port.view)
        elif self.port.type_() == OUT_PORT:
            text_item = node_view.get_output_text_item(self.port.view)
        if text_item:
            text_item.setVisible(visible)
        node_view.post_init()

    def undo(self):
        self.set_visible(self.visible)

    def redo(self):
        self.set_visible(not self.visible)