#!/usr/bin/python
from .properties import NodePropWidget

from PyQt5.QtWidgets import QStyledItemDelegate, QHeaderView, QTableWidget, QSpinBox, QTableWidgetItem, QApplication
from PyQt5.QtGui import QPen
from PyQt5.QtCore import QRect, pyqtSignal

from appData import ANTIALIAS, PEN_NONE, State_Selected, BRUSH_NONE, MATCH_EXACTLY
from devkit.Widgets import Widget, Button, HBoxLayout, VBoxLayout, GridLayout, GroupBox

class PropertiesDelegate(QStyledItemDelegate):

    def paint(self, painter, option, index):

        painter.save()
        painter.setRenderHint(ANTIALIAS, False)
        painter.setPen(PEN_NONE)
        painter.setBrush(option.palette.midlight())
        painter.drawRect(option.rect)

        if option.state & State_Selected:
            bdr_clr = option.palette.highlight().color()
            painter.setPen(QPen(bdr_clr, 1.5))
        else:
            bdr_clr = option.palette.alternateBase().color()
            painter.setPen(QPen(bdr_clr, 1))

        painter.setBrush(BRUSH_NONE)
        painter.drawRect(QRect(option.rect.x() + 1, option.rect.y() + 1, option.rect.width() - 2, option.rect.height() - 2))
        painter.restore()


class PropertiesList(QTableWidget):

    def __init__(self, parent=None):
        super(PropertiesList, self).__init__(parent)
        self.setItemDelegate(PropertiesDelegate())
        self.setColumnCount(1)
        self.setShowGrid(False)
        QHeaderView.setSectionResizeMode(self.verticalHeader(), QHeaderView.ResizeToContents)
        self.verticalHeader().hide()
        QHeaderView.setSectionResizeMode(self.horizontalHeader(), 0, QHeaderView.Stretch)
        self.horizontalHeader().hide()


class PropertiesBinWidget(Widget):

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

        btn_clr = Button({'txt': 'clear'})
        btn_clr.setToolTip('Clear the properties bin.')
        btn_clr.clicked.connect(self.clear_bin)

        top_layout = HBoxLayout()
        top_layout.addWidget(self._limit)
        top_layout.addStretch(1)
        top_layout.addWidget(btn_clr)

        layout = VBoxLayout(self)
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
        items = self._prop_list.findItems(node_id, MATCH_EXACTLY)
        [self._prop_list.removeRow(i.row()) for i in items]

    def __on_limit_changed(self, value):
        rows = self._prop_list.rowCount()
        if rows > value:
            self._prop_list.removeRow(rows - 1)

    def __on_nodes_deleted(self, nodes):
        [self.__on_prop_close(n) for n in nodes]

    def __on_graph_property_changed(self, node, prop_name, prop_value):
        properties_widget = self.prop_widget(node)
        if not properties_widget:
            return

        property_window = properties_widget.get_widget(prop_name)
        if prop_value != property_window.get_value():
            self._block_signal = True
            property_window.set_value(prop_value)
            self._block_signal = False

    def __on_property_widget_changed(self, node_id, prop_name, prop_value):
        if not self._block_signal:
            self.property_changed.emit(node_id, prop_name, prop_value)

    def limit(self):
        return int(self._limit.value())

    def set_limit(self, limit):
        self._limit.setValue(limit)

    def add_node(self, node):
        if self.limit() == 0:
            return

        rows = self._prop_list.rowCount()
        if rows >= self.limit():
            self._prop_list.removeRow(rows - 1)

        itm_find = self._prop_list.findItems(node.id, MATCH_EXACTLY)
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
        node_id = node if isinstance(node, str) else node.id
        self.__on_prop_close(node_id)

    def clear_bin(self):
        self._prop_list.setRowCount(0)

    def prop_widget(self, node):
        node_id = node if isinstance(node, str) else node.id
        itm_find = self._prop_list.findItems(node_id, MATCH_EXACTLY)
        if itm_find:
            item = itm_find[0]
            return self._prop_list.cellWidget(item.row(), 0)


if __name__ == '__main__':
    import sys
    from plugins.NodeGraph import BaseNode, NodeGraph
    from appData import (NODE_PROP_QLABEL, NODE_PROP_QLINEEDIT, NODE_PROP_QCOMBO, NODE_PROP_QSPINBOX, NODE_PROP_COLORPICKER, NODE_PROP_SLIDER)


    class TestNode(BaseNode):
        NODE_NAME = 'test node'

        def __init__(self):
            super(TestNode, self).__init__()
            self.create_property('label_test', 'foo bar',
                                 widget_type=NODE_PROP_QLABEL)
            self.create_property('text_edit', 'hello',
                                 widget_type=NODE_PROP_QLINEEDIT)
            self.create_property('color_picker', (0, 0, 255),
                                 widget_type=NODE_PROP_COLORPICKER)
            self.create_property('integer', 10,
                                 widget_type=NODE_PROP_QSPINBOX)
            self.create_property('list', 'foo',
                                 items=['foo', 'bar'],
                                 widget_type=NODE_PROP_QCOMBO)
            self.create_property('range', 50,
                                 range=(45, 55),
                                 widget_type=NODE_PROP_SLIDER)

    def prop_changed(node_id, prop_name, prop_value):
        print('-'*100)
        print(node_id, prop_name, prop_value)


    app = QApplication(sys.argv)

    graph = NodeGraph()
    graph.register_node(TestNode)

    prop_bin = PropertiesBinWidget()
    prop_bin.property_changed.connect(prop_changed)

    node = graph.create_node('nodeGraphQt.nodes.TestNode')

    prop_bin.add_node(node)
    prop_bin.show()

    app.exec_()
