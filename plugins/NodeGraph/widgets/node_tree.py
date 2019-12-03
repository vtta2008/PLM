# -*- coding: utf-8 -*-
"""

Script Name: node_tree.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals


from appData import DRAG_DROP_ID

from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidget, QAbstractItemView
from PyQt5.QtCore import Qt

TYPE_NODE = QTreeWidgetItem.UserType + 1
TYPE_CATEGORY = QTreeWidgetItem.UserType + 2


class BaseNodeTreeItem(QTreeWidgetItem):

    def __eq__(self, other):
        return id(self) == id(other)


class NodeTreeWidget(QTreeWidget):

    def __init__(self, parent=None, node_graph=None):
        super(NodeTreeWidget, self).__init__(parent)
        self.setDragDropMode(QAbstractItemView.DragOnly)
        self.setHeaderHidden(True)
        self._factory = None
        self._custom_labels = {}
        self._set_node_factory(node_graph._node_factory)

    def __repr__(self):
        return '<{} object at {}>'.format(self.__class__.__name__, hex(id(self)))

    def mimeData(self, items):
        node_ids = ','.join(i.toolTip(0) for i in items)
        mime_data = super(NodeTreeWidget, self).mimeData(items)
        mime_data.setText('<${}>:{}'.format(DRAG_DROP_ID, node_ids))
        return mime_data

    def _build_tree(self):
        self.clear()
        categories = set()
        node_types = {}
        for name, node_ids in self._factory.names.items():
            for nid in node_ids:
                categories.add('.'.join(nid.split('.')[:-1]))
                node_types[nid] = name

        category_items = {}
        for category in sorted(categories):
            if category in self._custom_labels.keys():
                label = self._custom_labels[category]
            else:
                label = '- {}'.format(category)
            cat_item = BaseNodeTreeItem(self, [label], type=TYPE_CATEGORY)
            cat_item.setFirstColumnSpanned(True)
            cat_item.setFlags(Qt.ImEnabled)
            self.addTopLevelItem(cat_item)
            cat_item.setExpanded(True)
            category_items[category] = cat_item

        for node_id, node_name in node_types.items():
            category = '.'.join(node_id.split('.')[:-1])
            category_item = category_items[category]

            item = BaseNodeTreeItem(category_item, [node_name], type=TYPE_NODE)
            item.setToolTip(0, node_id)

            category_item.addChild(item)

    def _set_node_factory(self, factory):
        self._factory = factory

    def set_category_label(self, category, label):
        self._custom_labels[category] = label

    def update(self):
        self._build_tree()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 4/12/2019 - 2:07 AM
# © 2017 - 2018 DAMGteam. All rights reserved