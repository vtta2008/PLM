# -*- coding: utf-8 -*-
"""

Script Name: node_base.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics, QColor
from PyQt5.QtWidgets import QGraphicsTextItem

from appData import (IN_PORT, OUT_PORT, NODE_WIDTH, NODE_HEIGHT, NODE_ICON_SIZE, ICON_NODE_BASE, NODE_SEL_COLOR, NODE_SEL_BORDER_COLOR,
                     PORT_FALLOFF, Z_VAL_NODE, Z_VAL_NODE_WIDGET)
from cores.errors import NodeWidgetError
from .node_abstract import AbstractNodeItem
from plugins.NodeGraph.base.port import PortItem
from toolkits.Widgets import GraphicObject, GraphicPathItem
from toolkits.Gui import Pen, Pixmap, PainterPath
from PyQt5.QtCore import QRectF


class XDisabledItem(GraphicObject):

    def __init__(self, parent=None, text=None):
        super(XDisabledItem, self).__init__(parent)
        self.setZValue(Z_VAL_NODE_WIDGET + 2)
        self.setVisible(False)
        self.color = (0, 0, 0, 255)
        self.text = text

    def boundingRect(self):
        return self.parentItem().boundingRect()

    def paint(self, painter, option, widget):

        painter.save()

        margin = 20
        rect = self.boundingRect()
        dis_rect = (rect.left() - (margin / 2),
                                 rect.top() - (margin / 2),
                                 rect.width() + margin,
                                 rect.height() + margin)
        pen = Pen(QColor(*self.color), 8)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawLine(dis_rect.topLeft(), dis_rect.bottomRight())
        painter.drawLine(dis_rect.topRight(), dis_rect.bottomLeft())

        bg_color = QColor(*self.color)
        bg_color.setAlpha(100)
        bg_margin = -0.5
        bg_rect = QRectF(dis_rect.left() - (bg_margin / 2),
                         dis_rect.top() - (bg_margin / 2),
                         dis_rect.width() + bg_margin,
                         dis_rect.height() + bg_margin)
        painter.setPen(Pen(QColor(0, 0, 0, 0)))
        painter.setBrush(bg_color)
        painter.drawRoundedRect(bg_rect, 5, 5)

        pen = Pen(QColor(155, 0, 0, 255), 0.7)
        painter.setPen(pen)
        painter.drawLine(dis_rect.topLeft(), dis_rect.bottomRight())
        painter.drawLine(dis_rect.topRight(), dis_rect.bottomLeft())

        point_size = 4.0
        point_pos = (dis_rect.topLeft(), dis_rect.topRight(),
                     dis_rect.bottomLeft(), dis_rect.bottomRight())
        painter.setBrush(QColor(255, 0, 0, 255))
        for p in point_pos:
            p.setX(p.x() - (point_size / 2))
            p.setY(p.y() - (point_size / 2))
            point_rect = QRectF(
                p, QRectF(point_size, point_size))
            painter.drawEllipse(point_rect)

        if self.text:
            font = painter.font()
            font.setPointSize(10)

            painter.setFont(font)
            font_metrics = QFontMetrics(font)
            font_width = font_metrics.width(self.text)
            font_height = font_metrics.height()
            txt_w = font_width * 1.25
            txt_h = font_height * 2.25
            text_bg_rect = QRectF((rect.width() / 2) - (txt_w / 2),
                                  (rect.height() / 2) - (txt_h / 2),
                                  txt_w, txt_h)
            painter.setPen(Pen(QColor(255, 0, 0), 0.5))
            painter.setBrush(QColor(*self.color))
            painter.drawRoundedRect(text_bg_rect, 2, 2)

            text_rect = QRectF((rect.width() / 2) - (font_width / 2),
                               (rect.height() / 2) - (font_height / 2),
                               txt_w * 2, font_height * 2)

            painter.setPen(Pen(QColor(255, 0, 0), 1))
            painter.drawText(text_rect, self.text)

        painter.restore()


class NodeItem(AbstractNodeItem):


    def __init__(self, name='node', parent=None):
        super(NodeItem, self).__init__(name, parent)
        pixmap = Pixmap(ICON_NODE_BASE)
        if pixmap.size().height() > NODE_ICON_SIZE:
            pixmap = pixmap.scaledToHeight(NODE_ICON_SIZE,Qt.SmoothTransformation)
        self._properties['icon'] = ICON_NODE_BASE
        self._icon_item = Pixmap(pixmap, self)
        self._icon_item.setTransformationMode(Qt.SmoothTransformation)
        self._text_item = QGraphicsTextItem(self.name, self)
        self._x_item = XDisabledItem(self, 'DISABLED')
        self._input_items = {}
        self._output_items = {}
        self._widgets = {}

    def paint(self, painter, option, widget):

        painter.save()
        bg_border = 1.0
        rect = QRectF(0.5 - (bg_border / 2),
                      0.5 - (bg_border / 2),
                      self._width + bg_border,
                      self._height + bg_border)
        radius = 2
        border_color = QColor(*self.border_color)

        path = GraphicPathItem()
        path.addRoundedRect(rect, radius, radius)

        rect = self.boundingRect()
        bg_color = QColor(*self.color)
        painter.setBrush(bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

        if self.selected and NODE_SEL_COLOR:
            painter.setBrush(QColor(*NODE_SEL_COLOR))
            painter.drawRoundedRect(rect, radius, radius)

        label_rect = QRectF(rect.left() + (radius / 2),
                            rect.top() + (radius / 2),
                            self._width - (radius / 1.25),
                            28)
        path = PainterPath()
        path.addRoundedRect(label_rect, radius / 1.5, radius / 1.5)
        painter.setBrush(QColor(0, 0, 0, 50))
        painter.fillPath(path, painter.brush())

        border_width = 0.8
        if self.selected and NODE_SEL_BORDER_COLOR:
            border_width = 1.2
            border_color = QColor(*NODE_SEL_BORDER_COLOR)
        border_rect = QRectF(rect.left() - (border_width / 2),
                             rect.top() - (border_width / 2),
                             rect.width() + border_width,
                             rect.height() + border_width)

        pen = Pen(border_color, border_width)
        pen.setCosmetic(self.viewer().get_zoom() < 0.0)
        path = PainterPath()
        path.addRoundedRect(border_rect, radius, radius)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(pen)
        painter.drawPath(path)

        painter.restore()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            start = PortItem().boundingRect().width() - PORT_FALLOFF
            end = self.boundingRect().width() - start
            x_pos = event.pos().x()
            if not start <= x_pos <= end:
                event.ignore()
        super(NodeItem, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.modifiers() == Qt.AltModifier:
            event.ignore()
            return
        super(NodeItem, self).mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        viewer = self.viewer()
        if viewer:
            viewer.node_double_clicked.emit(self.id)
        super(NodeItem, self).mouseDoubleClickEvent(event)

    def itemChange(self, change, value):
        if change == self.ItemSelectedChange and self.scene():
            self.reset_pipes()
            if value:
                self.hightlight_pipes()
            self.setZValue(Z_VAL_NODE)
            if not self.selected:
                self.setZValue(Z_VAL_NODE + 1)

        return super(NodeItem, self).itemChange(change, value)

    def _tooltip_disable(self, state):
        tooltip = '<b>{}</b>'.format(self.name)
        if state:
            tooltip += ' <font color="red"><b>(DISABLED)</b></font>'
        tooltip += '<br/>{}<br/>'.format(self.type_)
        self.setToolTip(tooltip)

    def _set_base_size(self, add_w=0.0, add_h=0.0):
        self._width = NODE_WIDTH
        self._height = NODE_HEIGHT
        width, height = self.calc_size(add_w, add_h)
        if width > self._width:
            self._width = width
        if height > self._height:
            self._height = height

    def _set_text_color(self, color):

        text_color = QColor(*color)
        for port, text in self._input_items.items():
            text.setDefaultTextColor(text_color)
        for port, text in self._output_items.items():
            text.setDefaultTextColor(text_color)
        self._text_item.setDefaultTextColor(text_color)

    def activate_pipes(self):
        """
        active pipe color.
        """
        ports = self.inputs + self.outputs
        for port in ports:
            for pipe in port.connected_pipes:
                pipe.activate()

    def hightlight_pipes(self):
        """
        highlight pipe color.
        """
        ports = self.inputs + self.outputs
        for port in ports:
            for pipe in port.connected_pipes:
                pipe.highlight()

    def reset_pipes(self):
        """
        reset the pipe color.
        """
        ports = self.inputs + self.outputs
        for port in ports:
            for pipe in port.connected_pipes:
                pipe.reset()

    def calc_size(self, add_w=0.0, add_h=0.0):
        """
        calculate minimum node size.
        Args:
            add_w (float): additional width.
            add_h (float): additional height.
        """
        width = self._text_item.boundingRect().width()
        height = self._text_item.boundingRect().height()

        if self._widgets:
            wid_width = max([
                w.boundingRect().width() for w in self._widgets.values()
            ])
            if width < wid_width:
                width = wid_width

        port_height = 0.0
        if self._input_items:
            input_widths = []
            for port, text in self._input_items.items():
                input_width = port.boundingRect().width() - PORT_FALLOFF
                if text.isVisible():
                    input_width += text.boundingRect().width() / 1.5
                input_widths.append(input_width)
            width += max(input_widths)
            port_height = port.boundingRect().height()

        if self._output_items:
            output_widths = []
            for port, text in self._output_items.items():
                output_width = port.boundingRect().width()
                if text.isVisible():
                    output_width += text.boundingRect().width() / 1.5
                output_widths.append(output_width)
            width += max(output_widths)
            port_height = port.boundingRect().height()

        in_count = len([p for p in self.inputs if p.isVisible()])
        out_count = len([p for p in self.outputs if p.isVisible()])
        height += port_height * max([in_count, out_count])
        if self._widgets:
            wid_height = 0.0
            for w in self._widgets.values():
                wid_height += w.boundingRect().height()
            wid_height += wid_height / len(self._widgets.values())
            if wid_height > height:
                height = wid_height

        width += add_w
        height += add_h

        return width, height

    def arrange_icon(self, h_offset=0.0, v_offset=0.0):

        x = 2.0 + h_offset
        y = 2.0 + v_offset
        self._icon_item.setPos(x, y)

    def arrange_label(self, h_offset=0.0, v_offset=0.0):
        text_rect = self._text_item.boundingRect()
        text_x = (self._width / 2) - (text_rect.width() / 2)
        text_x += h_offset
        text_y = 1.0 + v_offset
        self._text_item.setPos(text_x, text_y)

    def arrange_widgets(self, v_offset=0.0):

        if not self._widgets:
            return
        wid_heights = sum(
            [w.boundingRect().height() for w in self._widgets.values()])
        pos_y = self._height / 2
        pos_y -= wid_heights / 2
        pos_y += v_offset
        for widget in self._widgets.values():
            rect = widget.boundingRect()
            pos_x = (self._width / 2) - (rect.width() / 2)
            widget.setPos(pos_x, pos_y)
            pos_y += rect.height()

    def arrange_ports(self, v_offset=0.0):

        width = self._width
        txt_offset = PORT_FALLOFF - 2
        spacing = 1

        # adjust input position
        inputs = [p for p in self.inputs if p.isVisible()]
        if inputs:
            port_width = inputs[0].boundingRect().width()
            port_height = inputs[0].boundingRect().height()
            port_x = (port_width / 2) * -1
            port_y = v_offset
            for port in inputs:
                port.setPos(port_x, port_y)
                port_y += port_height + spacing
        # adjust input text position
        for port, text in self._input_items.items():
            if port.isVisible():
                txt_x = port.boundingRect().width() / 2 - txt_offset
                text.setPos(txt_x, port.y() - 1.5)

        # adjust output position
        outputs = [p for p in self.outputs if p.isVisible()]
        if outputs:
            port_width = outputs[0].boundingRect().width()
            port_height = outputs[0].boundingRect().height()
            port_x = width - (port_width / 2)
            port_y = v_offset
            for port in outputs:
                port.setPos(port_x, port_y)
                port_y += port_height + spacing
        # adjust output text position
        for port, text in self._output_items.items():
            if port.isVisible():
                txt_width = text.boundingRect().width() - txt_offset
                txt_x = port.x() - txt_width
                text.setPos(txt_x, port.y() - 1.5)

    def offset_label(self, x=0.0, y=0.0):

        icon_x = self._text_item.pos().x() + x
        icon_y = self._text_item.pos().y() + y
        self._text_item.setPos(icon_x, icon_y)

    def draw_node(self):

        height = self._text_item.boundingRect().height()

        # setup initial base size.
        self._set_base_size(add_w=0.0, add_h=height)
        # set text color when node is initialized.
        self._set_text_color(self.text_color)
        # set the tooltip
        self._tooltip_disable(self.disabled)

        # --- setup node layout ---

        # arrange label text
        self.arrange_label(h_offset=0.0, v_offset=0.0)
        # arrange icon
        self.arrange_icon(h_offset=0.0, v_offset=0.0)
        # arrange input and output ports.
        self.arrange_ports(v_offset=height + (height / 2))
        # arrange node widgets
        self.arrange_widgets(v_offset=height / 2)

    def post_init(self, viewer=None, pos=None):

        self.draw_node()

        if pos:
            self.xy_pos = pos

    @property
    def icon(self):
        return self._properties['icon']

    @icon.setter
    def icon(self, path=None):
        self._properties['icon'] = path
        path = path or ICON_NODE_BASE
        pixmap = Pixmap(path)
        if pixmap.size().height() > NODE_ICON_SIZE:
            pixmap = pixmap.scaledToHeight(NODE_ICON_SIZE,
                                           Qt.SmoothTransformation)
        self._icon_item.setPixmap(pixmap)
        if self.scene():
            self.post_init()

    @AbstractNodeItem.width.setter
    def width(self, width=0.0):
        w, h = self.calc_size()
        width = width if width > w else w
        AbstractNodeItem.width.fset(self, width)

    @AbstractNodeItem.height.setter
    def height(self, height=0.0):
        w, h = self.calc_size()
        h = 70 if h < 70 else h
        height = height if height > h else h
        AbstractNodeItem.height.fset(self, height)

    @AbstractNodeItem.disabled.setter
    def disabled(self, state=False):
        AbstractNodeItem.disabled.fset(self, state)
        for n, w in self._widgets.items():
            w.widget.setDisabled(state)
        self._tooltip_disable(state)
        self._x_item.setVisible(state)

    @AbstractNodeItem.selected.setter
    def selected(self, selected=False):
        AbstractNodeItem.selected.fset(self, selected)
        if selected:
            self.hightlight_pipes()

    @AbstractNodeItem.name.setter
    def name(self, name=''):
        AbstractNodeItem.name.fset(self, name)
        self._text_item.setPlainText(name)
        if self.scene():
            self.draw_node()

    @AbstractNodeItem.color.setter
    def color(self, color=(100, 100, 100, 255)):
        AbstractNodeItem.color.fset(self, color)
        if self.scene():
            self.scene().update()

    @AbstractNodeItem.text_color.setter
    def text_color(self, color=(100, 100, 100, 255)):
        AbstractNodeItem.text_color.fset(self, color)
        self._set_text_color(color)

    @property
    def inputs(self):

        return list(self._input_items.keys())

    @property
    def outputs(self):

        return list(self._output_items.keys())

    def add_input(self, name='input', multi_port=False, display_name=True):

        port = PortItem(self)
        port.name = name
        port.port_type = IN_PORT
        port.multi_connection = multi_port
        port.display_name = display_name
        text = QGraphicsTextItem(port.name, self)
        text.font().setPointSize(8)
        text.setFont(text.font())
        text.setVisible(display_name)
        self._input_items[port] = text
        if self.scene():
            self.post_init()
        return port

    def add_output(self, name='output', multi_port=False, display_name=True):

        port = PortItem(self)
        port.name = name
        port.port_type = OUT_PORT
        port.multi_connection = multi_port
        port = display_name
        text = QGraphicsTextItem(port.name, self)
        text.font().setPointSize(8)
        text.setFont(text.font())
        text.setVisible(display_name)
        self._output_items[port] = text
        if self.scene():
            self.post_init()
        return port

    def get_input_text_item(self, port_item):

        return self._input_items[port_item]

    def get_output_text_item(self, port_item):

        return self._output_items[port_item]

    @property
    def widgets(self):
        return self._widgets.copy()

    def add_widget(self, widget):
        self._widgets[widget.name] = widget

    def get_widget(self, name):
        widget = self._widgets.get(name)
        if widget:
            return widget
        raise NodeWidgetError('node has no widget "{}"'.format(name))

    def delete(self):
        for port, text in self._input_items.items():
            port.delete()
        for port, text in self._output_items.items():
            port.delete()
        super(NodeItem, self).delete()

    def from_dict(self, node_dict):
        super(NodeItem, self).from_dict(node_dict)
        widgets = node_dict.pop('widgets', {})
        for name, value in widgets.items():
            if self._widgets.get(name):
                self._widgets[name] = value

            # -------------------------------------------------------------------------------------------------------------


# Created by panda on 4/12/2019 - 1:46 AM
# © 2017 - 2018 DAMGteam. All rights reserved