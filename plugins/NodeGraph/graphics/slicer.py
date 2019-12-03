# -*- coding: utf-8 -*-
"""

Script Name: slicer.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from appData                import Z_VAL_NODE_WIDGET, PIPE_SLICER_COLOR, LINE_SOLID, LINE_DASH
from toolkits.Gui           import Pen, PainterPath
from toolkits.Widgets       import GraphicPathItem
from PyQt5.QtCore           import QRectF
from PyQt5.QtGui            import QColor
from PyQt5.QtCore           import QPointF

class SlicerPipe(GraphicPathItem):

    def __init__(self):
        super(SlicerPipe, self).__init__()
        self.setZValue(Z_VAL_NODE_WIDGET + 2)

    def paint(self, painter, option, widget):

        color = QColor(*PIPE_SLICER_COLOR)
        p1 = self.path().pointAtPercent(0)
        p2 = self.path().pointAtPercent(1)
        size = 6.0
        offset = size / 2

        painter.save()
        painter.setRenderHint(painter.Antialiasing, True)

        font = painter.font()
        font.setPointSize(12)
        painter.setFont(font)
        text = 'slice'
        text_x = painter.fontMetrics().width(text) / 2
        text_y = painter.fontMetrics().height() / 1.5
        text_pos = QPointF(p1.x() - text_x, p1.y() - text_y)
        text_color = QColor(*PIPE_SLICER_COLOR)
        text_color.setAlpha(80)
        painter.setPen(Pen(text_color, 1.5, LINE_SOLID))
        painter.drawText(text_pos, text)

        painter.setPen(Pen(color, 1.5, LINE_DASH))
        painter.drawPath(self.path())

        painter.setPen(Pen(color, 1.5, LINE_SOLID))
        painter.setBrush(color)

        rect = QRectF(p1.x() - offset, p1.y() - offset, size, size)
        painter.drawEllipse(rect)

        rect = QRectF(p2.x() - offset, p2.y() - offset, size, size)
        painter.drawEllipse(rect)
        painter.restore()

    def draw_path(self, p1, p2):
        path = PainterPath()
        path.moveTo(p1)
        path.lineTo(p2)
        self.setPath(path)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 4/12/2019 - 1:44 AM
# © 2017 - 2018 DAMGteam. All rights reserved