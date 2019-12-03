# -*- coding: utf-8 -*-
"""

Script Name: NodeBase.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals


from PyQt5.QtCore                   import QPointF

from .SlotBase                      import ConnectionItem
from toolkits.Gui                   import Brush, Pen, Font, FontMetric, PainterPath
from toolkits.Widgets               import GraphicObject
from toolkits.Core                  import Rect, RectF
from appData                        import MOVEABLE, LINE_SOLID, PATTERN_SOLID, BOLD, NORMAL, SELECTABLE, sceneGraphCfg, center
from utils                          import _convert_to_QColor, _loadConfig
from bin                            import DAMGLIST, DAMGDICT



class NodeBase(GraphicObject):

    key                             = 'NodeBase'

    attrPreset                      = None
    attrCount                       = 0
    currentDataType                 = None

    attrs                           = DAMGLIST()

    plugs                           = DAMGDICT()
    sockets                         = DAMGDICT()
    attrsData                       = DAMGDICT()

    def __init__(self, name, preset, alternate):
        super(NodeBase, self).__init__(self)

        self.config = _loadConfig(sceneGraphCfg)
        self.nodePreset             = preset
        self.alternate              = alternate
        self.name                   = name

        # Dimensions.
        self.baseWidth              = self.config['node_width']
        self.baseHeight             = self.config['node_height']
        self.attrHeight             = self.config['node_attr_height']
        self.border                 = self.config['node_border']
        self.radius                 = self.config['node_radius']

        self.setAcceptHoverEvents(True)
        self.setFlag(MOVEABLE)
        self.setFlag(SELECTABLE)

        self.nodeCenter = QPointF()
        self.nodeCenter.setX(self.baseWidth / 2.0)
        self.nodeCenter.setY(self.height / 2.0)

        self._brush = Brush()
        self._brush.setStyle(PATTERN_SOLID)
        self._brush.setColor(_convert_to_QColor(self.config[self.nodePreset]['bg']))

        self._pen = Pen()
        self._pen.setStyle(LINE_SOLID)
        self._pen.setWidth(self.border)
        self._pen.setColor(_convert_to_QColor(self.config[self.nodePreset]['border']))

        self._penSel = Pen()
        self._penSel.setStyle(LINE_SOLID)
        self._penSel.setWidth(self.border)
        self._penSel.setColor(_convert_to_QColor(self.config[self.nodePreset]['border_sel']))

        self._textPen = Pen()
        self._textPen.setStyle(LINE_SOLID)
        self._textPen.setColor(_convert_to_QColor(self.config[self.nodePreset]['text']))

        self._nodeTextFont = Font(self.config['node_font'], self.config['node_font_size'], BOLD)
        self._attrTextFont = Font(self.config['attr_font'], self.config['attr_font_size'], NORMAL)

        self._attrBrush = Brush()
        self._attrBrush.setStyle(PATTERN_SOLID)

        self._attrBrushAlt = Brush()
        self._attrBrushAlt.setStyle(PATTERN_SOLID)

        self._attrPen = Pen()
        self._attrPen.setStyle(LINE_SOLID)

    def mouseDoubleClickEvent(self, event):
        super(NodeBase, self).mouseDoubleClickEvent(event)
        self.scene().parent().signal_NodeDoubleClicked.emit(self.name)

    def mouseMoveEvent(self, event):
        if self.scene().views()[0].gridVisToggle:
            if self.scene().views()[0].gridSnapToggle or self.scene().views()[0]._nodeSnap:
                gridSize = self.scene().gridSize
                currentPos = self.mapToScene(event.pos().x() - self.baseWidth / 2, event.pos().y() - self.height / 2)
                snap_x = (round(currentPos.x() / gridSize) * gridSize) - gridSize / 4
                snap_y = (round(currentPos.y() / gridSize) * gridSize) - gridSize / 4
                snap_pos = QPointF(snap_x, snap_y)
                self.setPos(snap_pos)
                self.scene().updateScene()
            else:
                self.scene().updateScene()
                super(NodeBase, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        # Emit node moved signal.
        self.scene().signal_NodeMoved.emit(self.name, self.pos())
        super(NodeBase, self).mouseReleaseEvent(event)

    def mousePressEvent(self, event):
        nodes = self.scene().nodes
        for node in nodes.values():
            node.setZValue(1)
        for item in self.scene().items():
            if isinstance(item, ConnectionItem):
                item.setZValue(1)
        self.setZValue(2)
        super(NodeBase, self).mousePressEvent(event)

    def hoverLeaveEvent(self, event):
        nodzInst = self.scene().views()[0]
        for item in nodzInst.scene().items():
            if isinstance(item, ConnectionItem):
                item.setZValue(0)
        super(NodeBase, self).hoverLeaveEvent(event)

    def boundingRect(self):
        rect = RectF(0, 0, self.baseWidth, self.height)
        rect = RectF(rect)
        return rect

    def shape(self):
        path = PainterPath()
        path.addRect(self.boundingRect())
        return path

    def paint(self, painter, option, widget):
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawRoundedRect(0, 0, self.baseWidth, self.height, self.radius, self.radius)
        # Node label.
        painter.setPen(self._textPen)
        painter.setFont(self._nodeTextFont)
        metrics = FontMetric(painter.font())
        text_width = metrics.boundingRect(self.name).width() + 14
        text_height = metrics.boundingRect(self.name).height() + 14
        margin = (text_width - self.baseWidth) * 0.5
        textRect = Rect(-margin, -text_height, text_width, text_height)
        painter.drawText(textRect, center, self.name)
        # Attributes.
        offset = 0
        for attr in self.attrs:
            nodzInst                = self.scene().views()[0]
            config                  = nodzInst.config
            # Attribute rect.
            rect                    = Rect(self.border / 2, self.baseHeight - self.radius + offset, self.baseWidth - self.border, self.attrHeight)
            attrData                = self.attrsData[attr]
            name                    = attr
            preset                  = attrData['preset']
            # Attribute base.
            self._attrBrush.setColor(_convert_to_QColor(config[preset]['bg']))
            if self.alternate:
                self._attrBrushAlt.setColor(_convert_to_QColor(config[preset]['bg'], True, config['alternate_value']))
            self._attrPen.setColor(_convert_to_QColor([0, 0, 0, 0]))

            painter.setPen(self._attrPen)
            painter.setBrush(self._attrBrush)
            if (offset / self.attrHeight) % 2:
                painter.setBrush(self._attrBrushAlt)

            painter.drawRect(rect)

            # Attribute label.
            painter.setPen(_convert_to_QColor(config[preset]['text']))
            painter.setFont(self._attrTextFont)

            # Search non-connectable attributes.
            if nodzInst.drawingConnection:
                if self == nodzInst.currentHoveredNode:
                    if (attrData['dataType'] != nodzInst.sourceSlot.dataType or
                        (nodzInst.sourceSlot.slotType == 'plug' and attrData['socket'] == False or
                         nodzInst.sourceSlot.slotType == 'socket' and attrData['plug'] == False)):
                        # Set non-connectable attributes color.
                        painter.setPen(_convert_to_QColor(config['non_connectable_color']))

            textRect = Rect(rect.left() + self.radius, rect.top(), rect.width() - 2*self.radius, rect.height())
            painter.drawText(textRect, center, name)

            offset += self.attrHeight

    @property
    def height(self):
        if self.attrCount > 0:
            return (self.baseHeight + self.attrHeight * self.attrCount + self.border + 0.5 * self.radius)
        else:
            return self.baseHeight

    @property
    def pen(self):
        if self.isSelected():
            return self._penSel
        else:
            return self._pen


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/12/2019 - 4:37 AM
# © 2017 - 2018 DAMGteam. All rights reserved