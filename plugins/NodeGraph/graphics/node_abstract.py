# -*- coding: utf-8 -*-
"""

Script Name: node_abstract.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals


from appData import Z_VAL_NODE, NODE_WIDTH, NODE_HEIGHT

from toolkits.Widgets import GraphicObject
from PyQt5.QtCore import QRectF

class AbstractNodeItem(GraphicObject):

    def __init__(self, name='node', parent=None):
        super(AbstractNodeItem, self).__init__(parent)
        self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
        self.setZValue(Z_VAL_NODE)
        self._properties = {
            'id': None,
            'name': name.strip(),
            'color': (13, 18, 23, 255),
            'border_color': (46, 57, 66, 255),
            'text_color': (255, 255, 255, 180),
            'type_': 'AbstractBaseNode',
            'selected': False,
            'disabled': False,
        }
        self._width = NODE_WIDTH
        self._height = NODE_HEIGHT

    def __repr__(self):
        return '{}.{}(\'{}\')'.format(
            self.__module__, self.__class__.__name__, self.name)

    def boundingRect(self):
        return QRectF(0.0, 0.0, self._width, self._height)

    def mousePressEvent(self, event):
        self._properties['selected'] = True
        super(AbstractNodeItem, self).mousePressEvent(event)

    def setSelected(self, selected):
        self._properties['selected'] = selected
        super(AbstractNodeItem, self).setSelected(selected)

    def pre_init(self, viewer, pos=None):

        pass

    def post_init(self, viewer, pos=None):

        pass

    @property
    def id(self):
        return self._properties['id']

    @id.setter
    def id(self, unique_id=''):
        self._properties['id'] = unique_id

    @property
    def type_(self):
        return self._properties['type_']

    @type_.setter
    def type_(self, node_type='NODE'):
        self._properties['type_'] = node_type

    @property
    def size(self):
        return self._width, self._height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width=0.0):
        self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height=0.0):
        self._height = height

    @property
    def color(self):
        return self._properties['color']

    @color.setter
    def color(self, color=(0, 0, 0, 255)):
        self._properties['color'] = color

    @property
    def text_color(self):
        return self._properties['text_color']

    @text_color.setter
    def text_color(self, color=(100, 100, 100, 255)):
        self._properties['text_color'] = color

    @property
    def border_color(self):
        return self._properties['border_color']

    @border_color.setter
    def border_color(self, color=(0, 0, 0, 255)):
        self._properties['border_color'] = color

    @property
    def disabled(self):
        return self._properties['disabled']

    @disabled.setter
    def disabled(self, state=False):
        self._properties['disabled'] = state

    @property
    def selected(self):
        return self.isSelected()

    @selected.setter
    def selected(self, selected=False):
        self.setSelected(selected)

    @property
    def xy_pos(self):
        return [float(self.scenePos().x()), float(self.scenePos().y())]

    @xy_pos.setter
    def xy_pos(self, pos=None):
        pos = pos or [0.0, 0.0]
        self.setPos(pos[0], pos[1])

    @property
    def name(self):
        return self._properties['name']

    @name.setter
    def name(self, name=''):
        self._properties['name'] = name
        self.setToolTip('node: {}'.format(name))

    @property
    def properties(self):

        props = {'width': self.width,
                 'height': self.height,
                 'pos':  self.xy_pos}
        props.update(self._properties)
        return props

    def viewer(self):

        if self.scene():
            return self.scene().viewer()

    def delete(self):

        if self.scene():
            self.scene().removeItem(self)

    def from_dict(self, node_dict):

        node_attrs = list(self._properties.keys()) + ['width', 'height', 'pos']
        for name, value in node_dict.items():
            if name in node_attrs:
                if name == 'pos':
                    name = 'xy_pos'
                setattr(self, name, value)



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 4/12/2019 - 1:47 AM
# © 2017 - 2018 DAMGteam. All rights reserved