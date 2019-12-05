# -*- coding: utf-8 -*-
"""

Script Name: node.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from appData                    import (NODE_PROP, NODE_PROP_QLINEEDIT, NODE_PROP_QTEXTEDIT, NODE_PROP_QCOMBO,
                                        NODE_PROP_QCHECKBOX, IN_PORT, OUT_PORT)
from cores.errors               import PortRegistrationError

from plugins.NodeGraph.graphics import NodeItem, BackdropNodeItem
from plugins.NodeGraph.widgets  import NodeComboBox, NodeLineEdit, NodeCheckBox

from .command                   import PropertyChangedCmd
from .model                     import NodeModel
from .port                      import Port

class classproperty(object):

    def __init__(self, f):
        self.f = f

    def __get__(self, instance, owner):
        return self.f(owner)


class NodeObject(object):
    #: (str) unique node identifier domain.
    __identifier__ = 'nodeGraphQt.nodes'

    #: (str) base node name.
    NODE_NAME = None

    def __init__(self, qgraphics_item=None):
        assert qgraphics_item, 'qgraphics item cannot be None.'
        self._graph = None
        self._model = NodeModel()
        self._model.type_ = self.type_
        self._model.name = self.NODE_NAME
        self._view = qgraphics_item
        self._view.type_ = self.type_
        self._view.name = self.model.name
        self._view.id = self._model.id

    def __repr__(self):
        return '<{}("{}") object at {}>'.format(
            self.__class__.__name__, self.NODE_NAME, hex(id(self)))

    @classproperty
    def type_(cls):
        return cls.__identifier__ + '.' + cls.__name__

    @property
    def id(self):
        return self.model.id

    @property
    def graph(self):
        return self._graph

    @property
    def view(self):
        return self._view

    def set_view(self, item):
        self._view = item
        self._view.id = self.model.id
        self.NODE_NAME = self._view.name

    @property
    def model(self):
        return self._model

    def set_model(self, model):
        self._model = model
        self._model.type_ = self.type_
        self._model.id = self.view.id

    def update_model(self):

        for name, val in self.view.properties.items():
            if name in self.model.properties.keys():
                setattr(self.model, name, val)
            if name in self.model.custom_properties.keys():
                self.model.custom_properties[name] = val

    def update(self):

        settings = self.model.to_dict[self.model.id]
        settings['id'] = self.model.id
        if settings.get('custom'):
            settings['widgets'] = settings.pop('custom')

        self.view.from_dict(settings)

    def name(self):

        return self.model.name

    def set_name(self, name=''):

        self.set_property('name', name)

    def color(self):

        r, g, b, a = self.model.color
        return r, g, b

    def set_color(self, r=0, g=0, b=0):

        self.set_property('color', (r, g, b, 255))

    def disabled(self):

        return self.model.disabled

    def set_disabled(self, mode=False):

        self.set_property('disabled', mode)

    def selected(self):

        self.model.selected = self.view.isSelected()
        return self.model.selected

    def set_selected(self, selected=True):

        self.set_property('selected', selected)

    def create_property(self, name, value, items=None, range=None,
                        widget_type=NODE_PROP, tab=None):

        self.model.add_property(name, value, items, range, widget_type, tab)

    def properties(self):

        props = self.model.to_dict[self.id].copy()
        props['id'] = self.id
        return props

    def get_property(self, name):

        if self.graph and name == 'selected':
            self.model.set_property(self.view.selected)

        return self.model.get_property(name)

    def set_property(self, name, value):

        # prevent signals from causing a infinite loop.
        if self.get_property(name) == value:
            return

        if self.graph and name == 'name':
            value = self.graph.get_unique_name(value)
            self.NODE_NAME = value

        if self.graph:
            undo_stack = self.graph.undo_stack()
            undo_stack.push(PropertyChangedCmd(self, name, value))
        else:
            if hasattr(self.view, name):
                setattr(self.view, name, value)
            self.model.set_property(name, value)

    def has_property(self, name):

        return name in self.model.properties.keys()

    def set_x_pos(self, x):

        y = self.pos()[1]
        self.set_pos(float(x), y)

    def set_y_pos(self, y):

        x = self.pos()[0]
        self.set_pos(x, float(y))

    def set_pos(self, x, y):

        self.set_property('pos', [float(x), float(y)])

    def x_pos(self):

        return self.model.pos[0]

    def y_pos(self):

        return self.model.pos[1]

    def pos(self):

        if self.view.xy_pos and self.view.xy_pos != self.model.pos:
            self.model.pos = self.view.xy_pos

        return self.model.pos


class BaseNode(NodeObject):

    NODE_NAME = 'Base Node'

    def __init__(self):
        super(BaseNode, self).__init__(NodeItem())
        self._inputs = []
        self._outputs = []

    def update_model(self):

        for name, val in self.view.properties.items():
            if name in ['inputs', 'outputs']:
                continue
            self.model.set_property(name, val)

        for name, widget in self.view.widgets.items():
            self.model.set_property(name, widget.value)

    def set_icon(self, icon=None):

        self.set_property('icon', icon)

    def icon(self):

        return self.model.icon

    def add_combo_menu(self, name='', label='', items=None, tab=None):

        items = items or []
        self.create_property(
            name, items[0], items=items, widget_type=NODE_PROP_QCOMBO, tab=tab)

        widget = NodeComboBox(self.view, name, label, items)
        widget.value_changed.connect(lambda k, v: self.set_property(k, v))
        self.view.add_widget(widget)

    def add_text_input(self, name='', label='', text='', tab=None):

        self.create_property(
            name, text, widget_type=NODE_PROP_QLINEEDIT, tab=tab)
        widget = NodeLineEdit(self.view, name, label, text)
        widget.value_changed.connect(lambda k, v: self.set_property(k, v))
        self.view.add_widget(widget)

    def add_checkbox(self, name='', label='', text='', state=False, tab=None):

        self.create_property(
            name, state, widget_type=NODE_PROP_QCHECKBOX, tab=tab)
        widget = NodeCheckBox(self.view, name, label, text, state)
        widget.value_changed.connect(lambda k, v: self.set_property(k, v))
        self.view.add_widget(widget)

    def add_input(self, name='input', multi_input=False, display_name=True,
                  color=None):

        if name in self.inputs().keys():
            raise PortRegistrationError(
                'port name "{}" already registered.'.format(name))
        view = self.view.add_input(name, multi_input, display_name)
        if color:
            view.color = color
            view.border_color = [min([255, max([0, i + 80])]) for i in color]
        port = Port(self, view)
        port.model.type_ = IN_PORT
        port.model.name = name
        port.model.display_name = display_name
        port.model.multi_connection = multi_input
        self._inputs.append(port)
        self.model.inputs[port.name()] = port.model
        return port

    def add_output(self, name='output', multi_output=True, display_name=True, color=None):

        if name in self.outputs().keys():
            raise PortRegistrationError(
                'port name "{}" already registered.'.format(name))
        view = self.view.add_output(name, multi_output, display_name)
        if color:
            view.color = color
            view.border_color = [min([255, max([0, i + 80])]) for i in color]
        port = Port(self, view)
        port.model.type_ = OUT_PORT
        port.model.name = name
        port.model.display_name = display_name
        port.model.multi_connection = multi_output
        self._outputs.append(port)
        self.model.outputs[port.name()] = port.model
        return port

    def inputs(self):

        return {p.name(): p for p in self._inputs}

    def outputs(self):

        return {p.name(): p for p in self._outputs}

    def input(self, index):

        return self._inputs[index]

    def set_input(self, index, port):

        src_port = self.input(index)
        src_port.connect_to(port)

    def output(self, index):

        return self._outputs[index]

    def set_output(self, index, port):

        src_port = self.output(index)
        src_port.connect_to(port)


class BackdropNode(NodeObject):

    NODE_NAME = 'Backdrop'

    def __init__(self):
        super(BackdropNode, self).__init__(BackdropNodeItem())
        # override base default color.
        self.model.color = (5, 129, 138, 255)
        self.create_property('backdrop_text', '',
                             widget_type=NODE_PROP_QTEXTEDIT, tab='Backdrop')

    def auto_size(self):

        self.view.auto_resize()

    def nodes(self):

        node_ids = [n.id for n in self.view.get_nodes()]
        return [self.graph.get_node_by_id(nid) for nid in node_ids]

    def set_text(self, text=''):

        self.set_property('backdrop_text', text)

    def text(self):

        return self.get_property('backdrop_text')

    def set_size(self, width, height):

        if self.graph:
            self.graph.begin_undo('backdrop size')
            self.set_property('width', width)
            self.set_property('height', height)
            self.graph.end_undo()
            return
        self.view.width, self.view.height = width, height
        self.model.width, self.model.height = width, height

    def size(self):

        self.model.width = self.view.width
        self.model.height = self.view.height
        return self.model.width, self.model.height

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 4/12/2019 - 1:35 AM
# © 2017 - 2018 DAMGteam. All rights reserved