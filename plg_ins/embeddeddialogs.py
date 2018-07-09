# -*- coding: utf-8 -*-
"""

Script Name: embeddeddialogs.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from PyQt5.QtCore import QEvent, QRectF, Qt, QTimeLine
from PyQt5.QtGui import (QBrush, QColor, QPainter, QPainterPath, QPixmap,
                         QTransform)
from PyQt5.QtWidgets import (QApplication, QDialog, QGraphicsItem,
                             QGraphicsProxyWidget, QGraphicsScene, QGraphicsView, QStyleFactory,
                             QWidget)

# from build import embeddeddialogs_rc
from plg_ins.embeddeddialog import Ui_embeddedDialog


class CustomProxy(QGraphicsProxyWidget):
    def __init__(self, parent=None, wFlags=0):
        super(CustomProxy, self).__init__(parent, wFlags)

        self.popupShown = False
        self.currentPopup = None

        self.timeLine = QTimeLine(250, self)
        self.timeLine.valueChanged.connect(self.updateStep)
        self.timeLine.stateChanged.connect(self.stateChanged)

    def boundingRect(self):
        return QGraphicsProxyWidget.boundingRect(self).adjusted(0, 0, 10, 10)

    def paintWindowFrame(self, painter, option, widget):
        color = QColor(0, 0, 0, 64)

        r = self.windowFrameRect()
        right = QRectF(r.right(), r.top() + 10, 10, r.height() - 10)
        bottom = QRectF(r.left() + 10, r.bottom(), r.width(), 10)
        intersectsRight = right.intersects(option.exposedRect)
        intersectsBottom = bottom.intersects(option.exposedRect)
        if intersectsRight and intersectsBottom:
            path = QPainterPath()
            path.addRect(right)
            path.addRect(bottom)
            painter.setPen(Qt.NoPen)
            painter.setBrush(color)
            painter.drawPath(path)
        elif intersectsBottom:
            painter.fillRect(bottom, color)
        elif intersectsRight:
            painter.fillRect(right, color)

        super(CustomProxy, self).paintWindowFrame(painter, option, widget)

    def hoverEnterEvent(self, event):
        super(CustomProxy, self).hoverEnterEvent(event)

        self.scene().setActiveWindow(self)
        if self.timeLine.currentValue != 1:
            self.zoomIn()

    def hoverLeaveEvent(self, event):
        super(CustomProxy, self).hoverLeaveEvent(event)

        if not self.popupShown and (
                self.timeLine.direction() != QTimeLine.Backward or self.timeLine.currentValue() != 0):
            self.zoomOut()

    def sceneEventFilter(self, watched, event):
        if watched.isWindow() and (event.type() == QEvent.UngrabMouse or event.type() == QEvent.GrabMouse):
            self.popupShown = watched.isVisible()
            if not self.popupShown and not self.isUnderMouse():
                self.zoomOut()

        return super(CustomProxy, self).sceneEventFilter(watched, event)

    def itemChange(self, change, value):
        if change == self.ItemChildAddedChange or change == self.ItemChildRemovedChange:
            if change == self.ItemChildAddedChange:
                self.currentPopup = value
                self.currentPopup.setCacheMode(self.ItemCoordinateCache)
                if self.scene() is not None:
                    self.currentPopup.installSceneEventFilter(self)
            elif self.scene() is not None:
                self.currentPopup.removeSceneEventFilter(self)
                self.currentPopup = None
        elif self.currentPopup is not None and change == self.ItemSceneHasChanged:
            self.currentPopup.installSceneEventFilter(self)

        return super(CustomProxy, self).itemChange(change, value)

    def updateStep(self, step):
        r = self.boundingRect()
        self.setTransform(QTransform() \
                          .translate(r.width() / 2, r.height() / 2) \
                          .rotate(step * 30, Qt.XAxis) \
                          .rotate(step * 10, Qt.YAxis) \
                          .rotate(step * 5, Qt.ZAxis) \
                          .scale(1 + 1.5 * step, 1 + 1.5 * step) \
                          .translate(-r.width() / 2, -r.height() / 2))

    def stateChanged(self, state):
        if state == QTimeLine.Running:
            if self.timeLine.direction() == QTimeLine.Forward:
                self.setCacheMode(self.NoCache)
        elif state == QTimeLine.NotRunning:
            if self.timeLine.direction() == QTimeLine.Backward:
                self.setCacheMode(self.DeviceCoordinateCache)

    def zoomIn(self):
        if self.timeLine.direction() != QTimeLine.Forward:
            self.timeLine.setDirection(QTimeLine.Forward)
        if self.timeLine.state() == QTimeLine.NotRunning:
            self.timeLine.start()

    def zoomOut(self):
        if self.timeLine.direction() != QTimeLine.Backward:
            self.timeLine.setDirection(QTimeLine.Backward)
        if self.timeLine.state() == QTimeLine.NotRunning:
            self.timeLine.start()


class EmbeddedDialog(QDialog):
    def __init__(self, parent=None):
        super(EmbeddedDialog, self).__init__(parent)

        self.ui = Ui_embeddedDialog()
        self.ui.setupUi(self)
        self.ui.layoutDirection.setCurrentIndex(self.layoutDirection() != Qt.LeftToRight)

        for styleName in QStyleFactory.keys():
            self.ui.style.addItem(styleName)
            if self.style().objectName().lower() == styleName.lower():
                self.ui.style.setCurrentIndex(self.ui.style.count() - 1)

        self.ui.layoutDirection.activated.connect(self.layoutDirectionChanged)
        self.ui.spacing.valueChanged.connect(self.spacingChanged)
        self.ui.fontComboBox.currentFontChanged.connect(self.fontChanged)
        self.ui.style.activated[str].connect(self.styleChanged)

    def layoutDirectionChanged(self, index):
        if index == 0:
            self.setLayoutDirection(Qt.LeftToRight)
        else:
            self.setLayoutDirection(Qt.RightToLeft)

    def spacingChanged(self, spacing):
        self.layout().setSpacing(spacing)
        self.adjustSize()

    def fontChanged(self, font):
        self.setFont(font)

    def setStyleHelper(self, widget, style):
        widget.setStyle(style)
        widget.setPalette(style.standardPalette())
        for child in widget.children():
            if isinstance(child, QWidget):
                self.setStyleHelper(child, style)

    def styleChanged(self, styleName):
        style = QStyleFactory.create(styleName)
        if style:
            self.setStyleHelper(self, style)

        # Keep a reference to the style.
        self._style = style


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    scene = QGraphicsScene()
    scene.setStickyFocus(True)

    for y in range(10):
        for x in range(10):
            proxy = CustomProxy(None, Qt.Window)
            proxy.setWidget(EmbeddedDialog())

            rect = proxy.boundingRect()

            proxy.setPos(x * rect.width() * 1.05, y * rect.height() * 1.05)
            proxy.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
            scene.addItem(proxy)

    scene.setSceneRect(scene.itemsBoundingRect())

    view = QGraphicsView(scene)
    view.scale(0.5, 0.5)
    view.setRenderHints(view.renderHints() | QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
    view.setBackgroundBrush(QBrush(QPixmap(':/No-Ones-Laughing-3.jpg')))
    view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
    view.show()
    view.setWindowTitle("Embedded Dialogs Demo")

    sys.exit(app.exec_())

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 17/06/2018 - 5:31 AM
# © 2017 - 2018 DAMGteam. All rights reserved