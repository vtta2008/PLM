# -*- coding: utf-8 -*-
"""

Script Name: properties_bin.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from .properties import NodePropWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QStyledItemDelegate, QStyle, QHeaderView, QTableWidget, QWidget, QSpinBox, QPushButton, QHBoxLayout, QVBoxLayout, QTableWidgetItem
from PyQt5.QtCore import Qt, QRect, pyqtSignal

class PropertiesDelegate(QStyledItemDelegate):

    def paint(self, painter, option, index):
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, False)
        painter.setPen(Qt.NoPen)
        painter.setBrush(option.palette.midlight())
        painter.drawRect(option.rect)

        if option.state & QStyle.State_Selected:
            bdr_clr = option.palette.highlight().color()
            painter.setPen(QPen(bdr_clr, 1.5))
        else:
            bdr_clr = option.palette.alternateBase().color()
            painter.setPen(QPen(bdr_clr, 1))

        painter.setBrush(Qt.NoBrush)
        painter.drawRect(QRect(option.rect.x() + 1,
                                      option.rect.y() + 1,
                                      option.rect.width() - 2,
                                      option.rect.height() - 2))
        painter.restore()


class PropertiesList(QTableWidget):

    def __init__(self, parent=None):
        super(PropertiesList, self).__init__(parent)
        self.setItemDelegate(PropertiesDelegate())
        self.setColumnCount(1)
        self.setShowGrid(False)
        QHeaderView.setSectionResizeMode(
            self.verticalHeader(), QHeaderView.ResizeToContents)
        self.verticalHeader().hide()
        QHeaderView.setSectionResizeMode(
            self.horizontalHeader(), 0, QHeaderView.Stretch)
        self.horizontalHeader().hide()


class PropertiesBinWidget(QWidget):

    #: Signal emitted (node_id, prop_name, prop_value)
    property_changed = pyqtSignal(str, str, object)

    def __init__(self, parent=None, node_graph=None):
        super(PropertiesBinWidget, self).__init__(parent)
        self.setWindowTitle('Properties Bin')
        self._prop_list = PropertiesList()
        self._limit = QSpinBox()
        self._limit.setToolTip('Set display nodes limit.')
        self._limit.setMaximum(10)
        self._limit.setMinimum(0)
        self._limit.setValue(5)
        self._limit.valueChanged.connect(self.__on_limit_changed)
        self.resize(400, 400)

        self._block_signal = False

        btn_clr = QPushButton('clear')
        btn_clr.setToolTip('Clear the properties bin.')
        btn_clr.clicked.connect(self.clear_bin)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self._limit)
        top_layout.addStretch(1)
        top_layout.addWidget(btn_clr)

        layout = QVBoxLayout(self)
        layout.addLayout(top_layout)
        layout.addWidget(self._prop_list, 1)

        # wire up node graph.
        node_graph.add_properties_bin(self)
        node_graph.node_double_clicked.connect(self.add_node)
        node_graph.nodes_deleted.connect(self.__on_nodes_deleted)
        node_graph.property_changed.connect(self.__on_graph_property_changed)

    def __repr__(self):
        return '<{} object at {}>'.format(self.__class__.__name__, hex(id(self)))

    def __on_prop_close(self, node_id):
        items = self._prop_list.findItems(node_id, Qt.MatchExactly)
        [self._prop_list.removeRow(i.row()) for i in items]

    def __on_limit_changed(self, value):
        rows = self._prop_list.rowCount()
        if rows > value:
            self._prop_list.removeRow(rows - 1)

    def __on_nodes_deleted(self, nodes):
        """
        Slot function when a node has been deleted.
        Args:
            nodes (list[str]): list of node ids.
        """
        [self.__on_prop_close(n) for n in nodes]

    def __on_graph_property_changed(self, node, prop_name, prop_value):
        """
        Slot function that updates the property bin from the node graph signal.
        Args:
            node (NodeGraphQt.NodeObject):
            prop_name (str):
            prop_value (object):
        """
        properties_widget = self.prop_widget(node)
        if not properties_widget:
            return

        property_window = properties_widget.get_widget(prop_name)
        if prop_value != property_window.get_value():
            self._block_signal = True
            property_window.set_value(prop_value)
            self._block_signal = False

    def __on_property_widget_changed(self, node_id, prop_name, prop_value):
        """
        Slot function triggered when a property widget value has changed.
        Args:
            node_id (str):
            prop_name (str):
            prop_value (object):
        """
        if not self._block_signal:
            self.property_changed.emit(node_id, prop_name, prop_value)

    def limit(self):
        """
        Returns the limit for how many nodes can be loaded into the bin.
        Returns:
            int: node limit.
        """
        return int(self._limit.value())

    def set_limit(self, limit):
        """
        Set limit of nodes to display.
        Args:
            limit (int): node limit.
        """
        self._limit.setValue(limit)

    def add_node(self, node):
        """
        Add node to the properties bin.
        Args:
            node (NodeGraphQt.NodeObject): node object.
        """
        if self.limit() == 0:
            return

        rows = self._prop_list.rowCount()
        if rows >= self.limit():
            self._prop_list.removeRow(rows - 1)

        itm_find = self._prop_list.findItems(node.id, Qt.MatchExactly)
        if itm_find:
            self._prop_list.removeRow(itm_find[0].row())

        self._prop_list.insertRow(0)
        prop_widget = NodePropWidget(node=node)
        prop_widget.property_changed.connect(self.__on_property_widget_changed)
        prop_widget.property_closed.connect(self.__on_prop_close)
        self._prop_list.setCellWidget(0, 0, prop_widget)

        item = QTableWidgetItem(node.id)
        self._prop_list.setItem(0, 0, item)
        self._prop_list.selectRow(0)

    def remove_node(self, node):
        """
        Remove node from the properties bin.
        Args:
            node (str or NodeGraphQt.BaseNode): node id or node object.
        """
        node_id = node if isinstance(node, str) else node.id
        self.__on_prop_close(node_id)

    def clear_bin(self):
        """
        Clear the properties bin.
        """
        self._prop_list.setRowCount(0)

    def prop_widget(self, node):
        """
        Returns the node property widget.
        Args:
            node (str or NodeGraphQt.NodeObject): node id or node object.
        Returns:
            NodePropWidget: node property widget.
        """
        node_id = node if isinstance(node, str) else node.id
        itm_find = self._prop_list.findItems(node_id, Qt.MatchExactly)
        if itm_find:
            item = itm_find[0]
            return self._prop_list.cellWidget(item.row(), 0)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 4/12/2019 - 2:06 AM
# © 2017 - 2018 DAMGteam. All rights reserved