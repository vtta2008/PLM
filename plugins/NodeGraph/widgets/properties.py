# -*- coding: utf-8 -*-
"""

Script Name: properties.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals


from collections import defaultdict

from appData import (NODE_PROP_QLABEL, NODE_PROP_QLINEEDIT, NODE_PROP_QTEXTEDIT, NODE_PROP_QCOMBO, NODE_PROP_QCHECKBOX,
                     NODE_PROP_QSPINBOX, NODE_PROP_COLORPICKER, NODE_PROP_SLIDER)

from toolkits.Widgets import Widget, TabWidget

from PyQt5.QtCore import pyqtSignal, QRect, QRectF, Qt
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QColorDialog, QSlider, QSizePolicy, QSpinBox, QLineEdit, QAbstractSpinBox, QTextEdit, QComboBox, QCheckBox, QGridLayout

class BaseProperty(Widget):

    value_changed = pyqtSignal(str, object)

    def set_value(self, value):
        raise NotImplementedError

    def get_value(self):
        raise NotImplementedError


class _ColorSolid(Widget):

    def __init__(self, parent=None, color=None):
        super(_ColorSolid, self).__init__(parent)
        self.setMinimumSize(15, 15)
        self.setMaximumSize(15, 15)
        self.color = color or (0, 0, 0)

    def paintEvent(self, event):
        size = self.geometry()
        rect = QRect(1, 1, size.width() - 2, size.height() - 2)
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(*self._color))
        painter.drawRoundedRect(rect, 4, 4)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        hex = '#{0:02x}{1:02x}{2:02x}'.format(*self._color)
        self.setToolTip('rgb: {}\nhex: {}'.format(self._color[0:3], hex))
        self.update()


class PropColorPicker(BaseProperty):

    def __init__(self, parent=None):
        super(PropColorPicker, self).__init__(parent)
        self._solid = _ColorSolid(self)
        self._solid.setMaximumHeight(15)
        self._label = QLabel()
        self._update_label()

        button = QPushButton('select color')
        button.clicked.connect(self._on_select_color)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 8, 0)
        layout.setSpacing(4)
        layout.addWidget(self._solid, 0, Qt.AlignCenter)
        layout.addWidget(self._label, 0, Qt.AlignCenter)
        layout.addWidget(button, 1, Qt.AlignLeft)

    def _on_select_color(self):
        color = QColorDialog.getColor(QColor(*self.get_value()))
        if color.isValid():
            self.set_value(color.getRgb())

    def _update_label(self):
        self._label.setStyleSheet(
            'QLabel {{color: rgba({}, {}, {}, 255);}}'
            .format(*self._solid.color))
        self._label.setText(self.hex_color())
        self._label.setAlignment(Qt.AlignCenter)
        self._label.setMinimumWidth(60)

    def hex_color(self):
        return '#{0:02x}{1:02x}{2:02x}'.format(*self._solid.color)

    def get_value(self):
        return self._solid.color

    def set_value(self, value):
        if value != self.get_value():
            self._solid.color = value
            self._update_label()
            self.value_changed.emit(self.toolTip(), value)


class PropSlider(BaseProperty):

    def __init__(self, parent=None):
        super(PropSlider, self).__init__(parent)
        self._block = False
        self._slider = QSlider()
        self._spnbox = QSpinBox()
        self._init()

    def _init(self):
        self._slider.setOrientation(Qt.Horizontal)
        self._slider.setTickPosition(QSlider.TicksBelow)
        self._slider.setSizePolicy(QSizePolicy.Expanding,
                                   QSizePolicy.Preferred)
        self._spnbox.setButtonSymbols(QAbstractSpinBox.NoButtons)
        layout = QHBoxLayout(self)
        layout.addWidget(self._spnbox)
        layout.addWidget(self._slider)
        self._spnbox.valueChanged.connect(self._on_spnbox_changed)
        self._slider.valueChanged.connect(self._on_slider_changed)
        # store the original press event.
        self._slider_press_event = self._slider.mousePressEvent
        self._slider.mousePressEvent = self.sliderMousePressEvent
        self._slider.mouseReleaseEvent = self.sliderMouseReleaseEvent

    def sliderMousePressEvent(self, event):
        self._block = True
        self._slider_press_event(event)

    def sliderMouseReleaseEvent(self, event):
        self.value_changed.emit(self.toolTip(), self.get_value())
        self._block = False

    def _on_slider_changed(self, value):
        self._spnbox.setValue(value)

    def _on_spnbox_changed(self, value):
        if value != self._slider.value():
            self._slider.setValue(value)
            if not self._block:
                self.value_changed.emit(self.toolTip(), self.get_value())

    def get_value(self):
        return self._spnbox.value()

    def set_value(self, value):
        if value != self.get_value():
            self._block = True
            self._spnbox.setValue(value)
            self.value_changed.emit(self.toolTip(), value)
            self._block = False

    def set_min(self, value=0):
        self._spnbox.setMinimum(value)
        self._slider.setMinimum(value)

    def set_max(self, value=0):
        self._spnbox.setMaximum(value)
        self._slider.setMaximum(value)


class PropLabel(QLabel):

    value_changed = pyqtSignal(str, object)

    def get_value(self):
        return self.text()

    def set_value(self, value):
        if value != self.get_value():
            self.setText(value)
            self.value_changed.emit(self.toolTip(), value)


class PropLineEdit(QLineEdit):

    value_changed = pyqtSignal(str, object)

    def __init__(self, parent=None):
        super(PropLineEdit, self).__init__(parent)
        self.__prev_text = ''
        self.returnPressed.connect(self._on_return_pressed)

    def focusInEvent(self, event):
        super(PropLineEdit, self).focusInEvent(event)
        self.__prev_text = self.text()

    def focusOutEvent(self, event):
        super(PropLineEdit, self).focusOutEvent(event)
        if self.__prev_text != self.text():
            self.value_changed.emit(self.toolTip(), self.text())
        self.__prev_text = ''

    def _on_return_pressed(self):
        if self.__prev_text != self.text():
            self.value_changed.emit(self.toolTip(), self.text())

    def get_value(self):
        return self.text()

    def set_value(self, value):
        if value != self.get_value():
            self.setText(value)
            self.value_changed.emit(self.toolTip(), value)


class PropTextEdit(QTextEdit):

    value_changed = pyqtSignal(str, object)

    def __init__(self, parent=None):
        super(PropTextEdit, self).__init__(parent)
        self.__prev_text = ''

    def focusInEvent(self, event):
        super(PropTextEdit, self).focusInEvent(event)
        self.__prev_text = self.toPlainText()

    def focusOutEvent(self, event):
        super(PropTextEdit, self).focusOutEvent(event)
        if self.__prev_text != self.toPlainText():
            self.value_changed.emit(self.toolTip(), self.toPlainText())
        self.__prev_text = ''

    def _on_return_pressed(self):
        self.value_changed.emit(self.toolTip(), self.get_value())

    def get_value(self):
        return self.toPlainText()

    def set_value(self, value):
        if value != self.get_value():
            self.setPlainText(value)
            self.value_changed.emit(self.toolTip(), value)


class PropComboBox(QComboBox):

    value_changed = pyqtSignal(str, object)

    def __init__(self, parent=None):
        super(PropComboBox, self).__init__(parent)
        self.currentIndexChanged.connect(self._on_index_changed)

    def _on_index_changed(self):
        self.value_changed.emit(self.toolTip(), self.get_value())

    def items(self):
        return [self.itemText(i) for i in range(self.count())]

    def set_items(self, items):
        self.clear()
        self.addItems(items)

    def get_value(self):
        return self.currentText()

    def set_value(self, value):
        if value != self.get_value():
            idx = self.findText(value, Qt.MatchExactly)
            self.setCurrentIndex(idx)
            if idx >= 0:
                self.value_changed.emit(self.toolTip(), value)


class PropCheckBox(QCheckBox):

    value_changed = pyqtSignal(str, object)

    def __init__(self, parent=None):
        super(PropCheckBox, self).__init__(parent)
        self.clicked.connect(self._on_clicked)

    def _on_clicked(self):
        self.value_changed.emit(self.toolTip(), self.get_value())

    def get_value(self):
        return self.isChecked()

    def set_value(self, value):
        if value != self.get_value():
            self.setChecked(value)
            self.value_changed.emit(self.toolTip(), value)


class PropSpinBox(QSpinBox):

    value_changed = pyqtSignal(str, object)

    def __init__(self, parent=None):
        super(PropSpinBox, self).__init__(parent)
        self.setButtonSymbols(self.NoButtons)
        self.valueChanged.connect(self._on_value_change)

    def _on_value_change(self, value):
        self.value_changed.emit(self.toolTip(), value)

    def get_value(self):
        return self.value()

    def set_value(self, value):
        if value != self.get_value():
            self.setValue(value)


WIDGET_MAP = {
    NODE_PROP_QLABEL:       PropLabel,
    NODE_PROP_QLINEEDIT:    PropLineEdit,
    NODE_PROP_QTEXTEDIT:    PropTextEdit,
    NODE_PROP_QCOMBO:       PropComboBox,
    NODE_PROP_QCHECKBOX:    PropCheckBox,
    NODE_PROP_QSPINBOX:     PropSpinBox,
    NODE_PROP_COLORPICKER:  PropColorPicker,
    NODE_PROP_SLIDER:       PropSlider,
}


# main property widgets.


class PropWindow(Widget):

    def __init__(self, parent=None):
        super(PropWindow, self).__init__(parent)
        self.__layout = QGridLayout()
        self.__layout.setColumnStretch(1, 1)
        self.__layout.setSpacing(6)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.addLayout(self.__layout)

    def __repr__(self):
        return '<PropWindow object at {}>'.format(hex(id(self)))

    def add_widget(self, name, widget, value, label=None):
        """
        Add a property widget to the window.
        Args:
            name (str): property name to be displayed.
            widget (BaseProperty): property widget.
            value (object): property value.
            label (str): custom label to display.
        """
        widget.setToolTip(name)
        widget.set_value(value)
        if label is None:
            label = name
        row = self.__layout.rowCount()
        if row > 0:
            row += 1

        label_flags = Qt.AlignCenter | Qt.AlignRight
        if widget.__class__.__name__ == 'PropTextEdit':
            label_flags = label_flags | Qt.AlignTop

        self.__layout.addWidget(QLabel(label), row, 0, label_flags)
        self.__layout.addWidget(widget, row, 1)

    def get_widget(self, name):
        """
        Returns the property widget from the name.
        Args:
            name (str): property name.
        Returns:
            Widget: property widget.
        """
        for row in range(self.__layout.rowCount()):
            item = self.__layout.itemAtPosition(row, 1)
            if item and name == item.widget().toolTip():
                return item.widget()


class NodePropWidget(Widget):

    property_changed = pyqtSignal(str, str, object)
    property_closed = pyqtSignal(str)

    def __init__(self, parent=None, node=None):
        super(NodePropWidget, self).__init__(parent)
        self.__node_id = node.id
        self.__tab_windows = {}
        self.__tab = TabWidget()

        close_btn = QPushButton('X')
        close_btn.setToolTip('close property')
        close_btn.clicked.connect(self._on_close)

        self.name_wgt = PropLineEdit()
        self.name_wgt.setToolTip('name')
        self.name_wgt.set_value(node.name())
        self.name_wgt.value_changed.connect(self._on_property_changed)

        self.type_wgt = QLabel(node.type_)
        self.type_wgt.setAlignment(Qt.AlignRight)
        self.type_wgt.setToolTip('type_')
        font = self.type_wgt.font()
        font.setPointSize(10)
        self.type_wgt.setFont(font)

        name_layout = QHBoxLayout()
        name_layout.setContentsMargins(0, 0, 0, 0)
        name_layout.addWidget(QLabel('name'))
        name_layout.addWidget(self.name_wgt)
        name_layout.addWidget(close_btn)
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.addLayout(name_layout)
        layout.addWidget(self.__tab)
        layout.addWidget(self.type_wgt)
        self._read_node(node)

    def __repr__(self):
        return '<NodePropWidget object at {}>'.format(hex(id(self)))

    def _on_close(self):
        """
        called by the close button.
        """
        self.property_closed.emit(self.__node_id)

    def _on_property_changed(self, name, value):
        """
        slot function called when a property widget has changed.
        Args:
            name (str): property name.
            value (object): new value.
        """
        self.property_changed.emit(self.__node_id, name, value)

    def _read_node(self, node):
        """
        Populate widget from a node.
        Args:
            node (NodeGraphQt.BaseNode): node class.
        """
        model = node.model
        graph_model = node.graph.model

        common_props = graph_model.get_node_common_properties(node.type_)

        # sort tabs and properties.
        tab_mapping = defaultdict(list)
        for prop_name, prop_val in model.custom_properties.items():
            tab_name = model.get_tab_name(prop_name)
            tab_mapping[tab_name].append((prop_name, prop_val))

        # add tabs.
        for tab in sorted(tab_mapping.keys()):
            if tab != 'Node':
                self.add_tab(tab)

        # populate tab properties.
        for tab in sorted(tab_mapping.keys()):
            prop_window = self.__tab_windows[tab]
            for prop_name, value in tab_mapping[tab]:
                wid_type = model.get_widget_type(prop_name)
                if wid_type == 0:
                    continue

                WidClass = WIDGET_MAP.get(wid_type)
                widget = WidClass()
                if prop_name in common_props.keys():
                    if 'items' in common_props[prop_name].keys():
                        widget.set_items(common_props[prop_name]['items'])
                    if 'range' in common_props[prop_name].keys():
                        prop_range = common_props[prop_name]['range']
                        widget.set_min(prop_range[0])
                        widget.set_max(prop_range[1])

                prop_window.add_widget(prop_name, widget, value,
                                       prop_name.replace('_', ' '))
                widget.value_changed.connect(self._on_property_changed)

        # add "Node" tab properties.
        self.add_tab('Node')
        default_props = ['color', 'text_color', 'disabled', 'id']
        prop_window = self.__tab_windows['Node']
        for prop_name in default_props:
            wid_type = model.get_widget_type(prop_name)
            WidClass = WIDGET_MAP.get(wid_type)

            widget = WidClass()
            prop_window.add_widget(prop_name,
                                   widget,
                                   model.get_property(prop_name),
                                   prop_name.replace('_', ' '))

            widget.value_changed.connect(self._on_property_changed)

        self.type_wgt.setText(model.get_property('type_'))

    def node_id(self):
        """
        Returns the node id linked to the widget.
        Returns:
            str: node id
        """
        return self.__node_id

    def add_widget(self, name, widget, tab='Properties'):
        """
        add new node property widget.
        Args:
            name (str): property name.
            widget (BaseProperty): property widget.
            tab (str): tab name.
        """
        if tab not in self._widgets.keys():
            tab = 'Properties'
        window = self.__tab_windows[tab]
        window.add_widget(name, widget)
        widget.value_changed.connect(self._on_property_changed)

    def add_tab(self, name):
        """
        add a new tab.
        Args:
            name (str): tab name.
        Returns:
            PropWindow: tab child widget.
        """
        if name in self.__tab_windows.keys():
            raise AssertionError('Tab name {} already taken!'.format(name))
        self.__tab_windows[name] = PropWindow(self)
        self.__tab.addTab(self.__tab_windows[name], name)
        return self.__tab_windows[name]

    def get_widget(self, name):
        """
        get property widget.
        Args:
            name (str): property name.
        Returns:
            Widget: property widget.
        """
        if name == 'name':
            return self.name_wgt
        for tab_name, prop_win in self.__tab_windows.items():
            widget = prop_win.get_widget(name)
            if widget:
                return widget



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 4/12/2019 - 2:07 AM
# © 2017 - 2018 DAMGteam. All rights reserved