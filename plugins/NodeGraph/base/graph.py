#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, re, json

from .commands                          import NodeAddedCmd, NodeRemovedCmd, NodeMovedCmd, PortConnectedCmd
from .factory                           import NodeFactory
from .menu                              import NodeGraphMenu, NodesMenu
from .model                             import NodeGraphModel
from .node                              import NodeObject
from .port                              import Port
from plugins.NodeGraph.widgets.viewer   import NodeViewer

from bin                                import DAMG
from PyQt5.QtCore                       import pyqtSignal, QMimeData, QPoint
from PyQt5.QtWidgets                    import QUndoStack, QAction, QApplication

from appData                            import (DRAG_DROP_ID, PIPE_LAYOUT_CURVED, PIPE_LAYOUT_STRAIGHT, PIPE_LAYOUT_ANGLE,
                                                IN_PORT, OUT_PORT)
from devkit.Widgets                     import Widget, VBoxLayout

class NodeGraph(DAMG):

    node_created                        = pyqtSignal(NodeObject)
    nodes_deleted                       = pyqtSignal(list)
    node_selected                       = pyqtSignal(NodeObject)
    node_double_clicked                 = pyqtSignal(NodeObject)
    port_connected                      = pyqtSignal(Port, Port)
    port_disconnected                   = pyqtSignal(Port, Port)
    property_changed                    = pyqtSignal(NodeObject, str, object)
    data_dropped                        = pyqtSignal(QMimeData, QPoint)

    def __init__(self, parent=None):
        super(NodeGraph, self).__init__(parent)
        self.setObjectName('NodeGraphQt')
        self._widget                    = None
        self._model                     = NodeGraphModel()
        self._viewer                    = NodeViewer()
        self._node_factory              = NodeFactory()
        self._undo_stack                = QUndoStack(self)

        tab = QAction('Search Nodes', self)
        tab.setShortcut('tab')
        tab.triggered.connect(self._toggle_tab_search)
        self._viewer.addAction(tab)

        self._wire_signals()

    def __repr__(self):
        return '<{} object at {}>'.format(self.__class__.__name__, hex(id(self)))

    def _wire_signals(self):
        self._viewer.search_triggered.connect(self._on_search_triggered)
        self._viewer.connection_sliced.connect(self._on_connection_sliced)
        self._viewer.connection_changed.connect(self._on_connection_changed)
        self._viewer.moved_nodes.connect(self._on_nodes_moved)
        self._viewer.node_double_clicked.connect(self._on_node_double_clicked)
        self._viewer.node_selected.connect(self._on_node_selected)
        self._viewer.data_dropped.connect(self._on_node_data_dropped)

    def _toggle_tab_search(self):
        self._viewer.tab_search_set_nodes(self._node_factory.names)
        self._viewer.tab_search_toggle()

    def _on_property_bin_changed(self, node_id, prop_name, prop_value):
        node = self.get_node_by_id(node_id)
        if node.get_property(prop_name) != prop_value:
            node.set_property(prop_name, prop_value)

    def _on_node_double_clicked(self, node_id):
        node = self.get_node_by_id(node_id)
        self.node_double_clicked.emit(node)

    def _on_node_selected(self, node_id):
        node = self.get_node_by_id(node_id)
        self.node_selected.emit(node)

    def _on_node_data_dropped(self, data, pos):
        if data.hasFormat('text/plain'):
            if data.text().startswith('<${}>:'.format(DRAG_DROP_ID)):
                node_ids = data.text()[len('<${}>:'.format(DRAG_DROP_ID)):]
                x, y = pos.x(), pos.y()
                for node_id in node_ids.split(','):
                    self.create_node(node_id, pos=[x, y])
                x += 20
                y += 20
                return

        self.data_dropped.emit(data, pos)

    def _on_nodes_moved(self, node_data):
        self._undo_stack.beginMacro('move nodes')
        for node_view, prev_pos in node_data.items():
            node = self._model.nodes[node_view.id]
            self._undo_stack.push(NodeMovedCmd(node, node.pos(), prev_pos))
        self._undo_stack.endMacro()

    def _on_search_triggered(self, node_type, pos):
        self.create_node(node_type, pos=pos)

    def _on_connection_changed(self, disconnected, connected):
        if not (disconnected or connected):
            return

        label = 'connect node(s)' if connected else 'disconnect node(s)'
        ptypes = {IN_PORT: 'inputs', OUT_PORT: 'outputs'}

        self._undo_stack.beginMacro(label)
        for p1_view, p2_view in disconnected:
            node1 = self._model.nodes[p1_view.node.id]
            node2 = self._model.nodes[p2_view.node.id]
            port1 = getattr(node1, ptypes[p1_view.port_type])()[p1_view.name]
            port2 = getattr(node2, ptypes[p2_view.port_type])()[p2_view.name]
            port1.disconnect_from(port2)
        for p1_view, p2_view in connected:
            node1 = self._model.nodes[p1_view.node.id]
            node2 = self._model.nodes[p2_view.node.id]
            port1 = getattr(node1, ptypes[p1_view.port_type])()[p1_view.name]
            port2 = getattr(node2, ptypes[p2_view.port_type])()[p2_view.name]
            port1.connect_to(port2)
        self._undo_stack.endMacro()

    def _on_connection_sliced(self, ports):
        if not ports:
            return
        ptypes = {IN_PORT: 'inputs', OUT_PORT: 'outputs'}
        self._undo_stack.beginMacro('slice connections')
        for p1_view, p2_view in ports:
            node1 = self._model.nodes[p1_view.node.id]
            node2 = self._model.nodes[p2_view.node.id]
            port1 = getattr(node1, ptypes[p1_view.port_type])()[p1_view.name]
            port2 = getattr(node2, ptypes[p2_view.port_type])()[p2_view.name]
            port1.disconnect_from(port2)
        self._undo_stack.endMacro()

    @property
    def model(self):
        return self._model

    @property
    def widget(self):
        if self._widget is None:
            self._widget = Widget()
            layout = VBoxLayout(self._widget)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(self._viewer)
        return self._widget

    def show(self):
        self._widget.show()

    def close(self):
        self._widget.close()

    def viewer(self):
        return self._viewer

    def scene(self):
        return self._viewer.scene()

    def background_color(self):
        return self.scene().background_color

    def set_background_color(self, r, g, b):
        self.scene().background_color = (r, g, b)

    def grid_color(self):
        return self.scene().grid_color

    def set_grid_color(self, r, g, b):
        self.scene().grid_color = (r, g, b)

    def display_grid(self, display=True):
        self.scene().grid = display

    def add_properties_bin(self, prop_bin):
        prop_bin.property_changed.connect(self._on_property_bin_changed)

    def undo_stack(self):
        return self._undo_stack

    def clear_undo_stack(self):
        self._undo_stack.clear()

    def begin_undo(self, name):
        self._undo_stack.beginMacro(name)

    def end_undo(self):
        self._undo_stack.endMacro()

    def context_menu(self):
        return self.get_context_menu('graph')

    def context_nodes_menu(self):
        return self.get_context_menu('nodes')

    def get_context_menu(self, menu):
        menus = self._viewer.context_menus()
        if menus.get(menu):
            if menu == 'graph':
                return NodeGraphMenu(self, menus[menu])
            elif menu == 'nodes':
                return NodesMenu(self, menus[menu])

    def disable_context_menu(self, disabled=True, name='all'):
        if name == 'all':
            for k, menu in self._viewer.context_menus().items():
                menu.setDisabled(disabled)
                menu.setVisible(not disabled)
            return
        menus = self._viewer.context_menus()
        if menus.get(name):
            menus[name].setDisabled(disabled)
            menus[name].setVisible(not disabled)

    def acyclic(self):
        return self._model.acyclic

    def set_acyclic(self, mode=False):
        self._model.acyclic = mode
        self._viewer.acyclic = mode

    def set_pipe_style(self, style=PIPE_LAYOUT_CURVED):
        pipe_max = max([PIPE_LAYOUT_CURVED,
                        PIPE_LAYOUT_STRAIGHT,
                        PIPE_LAYOUT_ANGLE])
        style = style if 0 >= style >= pipe_max else PIPE_LAYOUT_CURVED
        self._viewer.set_pipe_layout(style)

    def fit_to_selection(self):
        nodes = self.selected_nodes() or self.all_nodes()
        if not nodes:
            return
        self._viewer.zoom_to_nodes([n.view for n in nodes])

    def reset_zoom(self):
        self._viewer.reset_zoom()

    def set_zoom(self, zoom=0):
        self._viewer.set_zoom(zoom)

    def get_zoom(self):
        return self._viewer.get_zoom()

    def center_on(self, nodes=None):
        self._viewer.center_selection(nodes)

    def center_selection(self):
        nodes = self._viewer.selected_nodes()
        self._viewer.center_selection(nodes)

    def registered_nodes(self):
        return sorted(self._node_factory.nodes.keys())

    def register_node(self, node, alias=None):
        self._node_factory.register_node(node, alias)

    def create_node(self, node_type, name=None, selected=True, color=None, text_color=None, pos=None):
        NodeCls = self._node_factory.create_node_instance(node_type)
        if NodeCls:
            node = NodeCls()

            node._graph = self
            node.model._graph_model = self.model

            wid_types = node.model.__dict__.pop('_TEMP_property_widget_types')
            prop_attrs = node.model.__dict__.pop('_TEMP_property_attrs')

            if self.model.get_node_common_properties(node.type_) is None:
                node_attrs = {node.type_: {
                    n: {'widget_type': wt} for n, wt in wid_types.items()
                }}
                for pname, pattrs in prop_attrs.items():
                    node_attrs[node.type_][pname].update(pattrs)
                self.model.set_node_common_properties(node_attrs)

            node.NODE_NAME = self.get_unique_name(name or node.NODE_NAME)
            node.model.name = node.NODE_NAME
            node.model.selected = selected

            def format_color(clr):
                if isinstance(clr, str):
                    clr = clr.strip('#')
                    return tuple(int(clr[i:i + 2], 16) for i in (0, 2, 4))
                return clr

            if color:
                node.model.color = format_color(color)
            if text_color:
                node.model.text_color = format_color(text_color)
            if pos:
                node.model.pos = [float(pos[0]), float(pos[1])]

            node.update()

            undo_cmd = NodeAddedCmd(self, node, node.model.pos)
            undo_cmd.setText('create node: "{}"'.format(node.NODE_NAME))
            self._undo_stack.push(undo_cmd)
            self.node_created.emit(node)
            return node
        raise Exception('\n\n>> Cannot find node:\t"{}"\n'.format(node_type))

    def add_node(self, node, pos=None):
        assert isinstance(node, NodeObject), 'node must be a Node instance.'

        wid_types = node.model.__dict__.pop('_TEMP_property_widget_types')
        prop_attrs = node.model.__dict__.pop('_TEMP_property_attrs')

        if self.model.get_node_common_properties(node.type_) is None:
            node_attrs = {node.type_: {
                n: {'widget_type': wt} for n, wt in wid_types.items()
            }}
            for pname, pattrs in prop_attrs.items():
                node_attrs[node.type_][pname].update(pattrs)
            self.model.set_node_common_properties(node_attrs)

        node._graph = self
        node.NODE_NAME = self.get_unique_name(node.NODE_NAME)
        node.model._graph_model = self.model
        node.model.name = node.NODE_NAME
        node.update()
        self._undo_stack.push(NodeAddedCmd(self, node, pos))

    def delete_node(self, node):
        assert isinstance(node, NodeObject), \
            'node must be a instance of a NodeObject.'
        self.nodes_deleted.emit([node.id])
        self._undo_stack.push(NodeRemovedCmd(self, node))

    def delete_nodes(self, nodes):
        self.nodes_deleted.emit([n.id for n in nodes])
        self._undo_stack.beginMacro('delete nodes')
        [self._undo_stack.push(NodeRemovedCmd(self, n)) for n in nodes]
        self._undo_stack.endMacro()

    def all_nodes(self):
        return list(self._model.nodes.values())

    def selected_nodes(self):
        nodes = []
        for item in self._viewer.selected_nodes():
            node = self._model.nodes[item.id]
            nodes.append(node)
        return nodes

    def select_all(self):
        self._undo_stack.beginMacro('select all')
        for node in self.all_nodes():
            node.set_selected(True)
        self._undo_stack.endMacro()

    def clear_selection(self):
        self._undo_stack.beginMacro('clear selection')
        for node in self.all_nodes():
            node.set_selected(False)
        self._undo_stack.endMacro()

    def get_node_by_id(self, node_id=None):
        return self._model.nodes.get(node_id)

    def get_node_by_name(self, name):
        for node_id, node in self._model.nodes.items():
            if node.name() == name:
                return node

    def get_unique_name(self, name):
        name = ' '.join(name.split())
        node_names = [n.name() for n in self.all_nodes()]
        if name not in node_names:
            return name

        regex = re.compile('[\w ]+(?: )*(\d+)')
        search = regex.search(name)
        if not search:
            for x in range(1, len(node_names) + 1):
                new_name = '{} {}'.format(name, x)
                if new_name not in node_names:
                    return new_name

        version = search.group(1)
        name = name[:len(version) * -1].strip()
        for x in range(1, len(node_names) + 1):
            new_name = '{} {}'.format(name, x)
            if new_name not in node_names:
                return new_name

    def current_session(self):
        return self._model.session

    def clear_session(self):
        for n in self.all_nodes():
            self._undo_stack.push(NodeRemovedCmd(self, n))
        self._undo_stack.clear()
        self._model.session = None

    def _serialize(self, nodes):
        serial_data = {'nodes': {}, 'connections': []}
        nodes_data = {}
        for n in nodes:
            n.update_model()
            nodes_data.update(n.model.to_dict)

        for n_id, n_data in nodes_data.items():
            serial_data['nodes'][n_id] = n_data

            inputs = n_data.pop('inputs') if n_data.get('inputs') else {}
            outputs = n_data.pop('outputs') if n_data.get('outputs') else {}

            for pname, conn_data in inputs.items():
                for conn_id, prt_names in conn_data.items():
                    for conn_prt in prt_names:
                        pipe = {IN_PORT: [n_id, pname],
                                OUT_PORT: [conn_id, conn_prt]}
                        if pipe not in serial_data['connections']:
                            serial_data['connections'].append(pipe)

            for pname, conn_data in outputs.items():
                for conn_id, prt_names in conn_data.items():
                    for conn_prt in prt_names:
                        pipe = {OUT_PORT: [n_id, pname],
                                IN_PORT: [conn_id, conn_prt]}
                        if pipe not in serial_data['connections']:
                            serial_data['connections'].append(pipe)

        if not serial_data['connections']:
            serial_data.pop('connections')

        return serial_data

    def _deserialize(self, data, relative_pos=False, pos=None):
        nodes = {}
        for n_id, n_data in data.get('nodes', {}).items():
            identifier = n_data['type_']
            NodeCls = self._node_factory.create_node_instance(identifier)
            if NodeCls:
                node = NodeCls()
                node.NODE_NAME = n_data.get('name', node.NODE_NAME)

                for prop in node.model.properties.keys():
                    if prop in n_data.keys():
                        node.model.set_property(prop, n_data[prop])

                for prop, val in n_data.get('custom', {}).items():
                    node.model.set_property(prop, val)

                nodes[n_id] = node
                self.add_node(node, n_data.get('pos'))

        for connection in data.get('connections', []):
            nid, pname = connection.get('in', ('', ''))
            in_node = nodes.get(nid)
            if not in_node:
                continue
            in_port = in_node.inputs().get(pname) if in_node else None

            nid, pname = connection.get('out', ('', ''))
            out_node = nodes.get(nid)
            if not out_node:
                continue
            out_port = out_node.outputs().get(pname) if out_node else None

            if in_port and out_port:
                self._undo_stack.push(PortConnectedCmd(in_port, out_port))

        node_objs = list(nodes.values())
        if relative_pos:
            self._viewer.move_nodes([n.view for n in node_objs])
            [setattr(n.model, 'pos', n.view.xy_pos) for n in node_objs]
        elif pos:
            self._viewer.move_nodes([n.view for n in node_objs], pos=pos)
            [setattr(n.model, 'pos', n.view.xy_pos) for n in node_objs]

        return node_objs

    def serialize_session(self):
        return self._serialize(self.all_nodes())

    def deserialize_session(self, layout_data):
        self.clear_session()
        self._deserialize(layout_data)
        self._undo_stack.clear()

    def save_session(self, file_path):
        serliazed_data = self._serialize(self.all_nodes())
        file_path = file_path.strip()
        with open(file_path, 'w') as file_out:
            json.dump(serliazed_data, file_out, indent=2, separators=(',', ':'))

    def load_session(self, file_path):
        file_path = file_path.strip()
        if not os.path.isfile(file_path):
            raise IOError('file does not exist.')

        self.clear_session()

        try:
            with open(file_path) as data_file:
                layout_data = json.load(data_file)
        except Exception as e:
            layout_data = None
            print('Cannot read data from file.\n{}'.format(e))

        if not layout_data:
            return

        self._deserialize(layout_data)
        self._undo_stack.clear()
        self._model.session = file_path

    def copy_nodes(self, nodes=None):
        nodes = nodes or self.selected_nodes()
        if not nodes:
            return False
        clipboard = QApplication.clipboard()
        serial_data = self._serialize(nodes)
        serial_str = json.dumps(serial_data)
        if serial_str:
            clipboard.setText(serial_str)
            return True
        return False

    def paste_nodes(self):
        clipboard = QApplication.clipboard()
        cb_text = clipboard.text()
        if not cb_text:
            return

        self._undo_stack.beginMacro('pasted nodes')
        serial_data = json.loads(cb_text)
        self.clear_selection()
        nodes = self._deserialize(serial_data, relative_pos=True)
        [n.set_selected(True) for n in nodes]
        self._undo_stack.endMacro()

    def duplicate_nodes(self, nodes):
        if not nodes:
            return

        self._undo_stack.beginMacro('duplicate nodes')

        self.clear_selection()
        serial = self._serialize(nodes)
        new_nodes = self._deserialize(serial)
        offset = 50
        for n in new_nodes:
            x, y = n.pos()
            n.set_pos(x + offset, y + offset)
            n.set_property('selected', True)

        self._undo_stack.endMacro()
        return new_nodes

    def disable_nodes(self, nodes, mode=None):
        if not nodes:
            return
        if mode is None:
            mode = not nodes[0].disabled()
        if len(nodes) > 1:
            text = {False: 'enable', True: 'disable'}[mode]
            text = '{} ({}) nodes'.format(text, len(nodes))
            self._undo_stack.beginMacro(text)
            [n.set_disabled(mode) for n in nodes]
            self._undo_stack.endMacro()
            return
        nodes[0].set_disabled(mode)

    def question_dialog(self, text, title='Node Graph'):
        self._viewer.question_dialog(text, title)

    def message_dialog(self, text, title='Node Graph'):
        self._viewer.message_dialog(text, title)

    def load_dialog(self, current_dir=None, ext=None):
        return self._viewer.load_dialog(current_dir, ext)

    def save_dialog(self, current_dir=None, ext=None):
        return self._viewer.save_dialog(current_dir, ext)
