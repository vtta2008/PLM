# -*- coding: utf-8 -*-
"""

Script Name: animatedtiles.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PyQt5.QtCore import (pyqtProperty, pyqtSignal, QEasingCurve, QObject,
                          QParallelAnimationGroup, QPointF, QPropertyAnimation, qrand, QRectF,
                          QState, QStateMachine, Qt, QTimer)
from PyQt5.QtGui import (QBrush, QLinearGradient, QPainter, QPainterPath,
                         QPixmap)
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsPixmapItem,
                             QGraphicsRectItem, QGraphicsScene, QGraphicsView, QGraphicsWidget,
                             QStyle)

from build import animatedtiles_rc


# PyQt doesn't support deriving from more than one wrapped class so we use
# composition and delegate the property.
class Pixmap(QObject):
    def __init__(self, pix):
        super(Pixmap, self).__init__()

        self.pixmap_item = QGraphicsPixmapItem(pix)
        self.pixmap_item.setCacheMode(QGraphicsItem.DeviceCoordinateCache)

    def _set_pos(self, pos):
        self.pixmap_item.setPos(pos)

    pos = pyqtProperty(QPointF, fset=_set_pos)


class Button(QGraphicsWidget):
    pressed = pyqtSignal()

    def __init__(self, pixmap, parent=None):
        super(Button, self).__init__(parent)

        self._pix = pixmap

        self.setAcceptHoverEvents(True)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)

    def boundingRect(self):
        return QRectF(-65, -65, 130, 130)

    def shape(self):
        path = QPainterPath()
        path.addEllipse(self.boundingRect())

        return path

    def paint(self, painter, option, widget):
        down = option.state & QStyle.State_Sunken
        r = self.boundingRect()

        grad = QLinearGradient(r.topLeft(), r.bottomRight())
        if option.state & QStyle.State_MouseOver:
            color_0 = Qt.white
        else:
            color_0 = Qt.lightGray

        color_1 = Qt.darkGray

        if down:
            color_0, color_1 = color_1, color_0

        grad.setColorAt(0, color_0)
        grad.setColorAt(1, color_1)

        painter.setPen(Qt.darkGray)
        painter.setBrush(grad)
        painter.drawEllipse(r)

        color_0 = Qt.darkGray
        color_1 = Qt.lightGray

        if down:
            color_0, color_1 = color_1, color_0

        grad.setColorAt(0, color_0)
        grad.setColorAt(1, color_1)

        painter.setPen(Qt.NoPen)
        painter.setBrush(grad)

        if down:
            painter.translate(2, 2)

        painter.drawEllipse(r.adjusted(5, 5, -5, -5))
        painter.drawPixmap(-self._pix.width() / 2, -self._pix.height() / 2,
                           self._pix)

    def mousePressEvent(self, ev):
        self.pressed.emit()
        self.update()

    def mouseReleaseEvent(self, ev):
        self.update()


class View(QGraphicsView):
    def resizeEvent(self, event):
        super(View, self).resizeEvent(event)
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)


if __name__ == '__main__':

    import sys
    import math

    app = QApplication(sys.argv)

    kineticPix = QPixmap(':/images/kinetic.png')
    bgPix = QPixmap(':/images/Time-For-Lunch-2.jpg')

    scene = QGraphicsScene(-350, -350, 700, 700)

    items = []
    for i in range(64):
        item = Pixmap(kineticPix)
        item.pixmap_item.setOffset(-kineticPix.width() / 2,
                                   -kineticPix.height() / 2)
        item.pixmap_item.setZValue(i)
        items.append(item)
        scene.addItem(item.pixmap_item)

    # Buttons.
    buttonParent = QGraphicsRectItem()
    ellipseButton = Button(QPixmap(':/images/ellipse.png'), buttonParent)
    figure8Button = Button(QPixmap(':/images/figure8.png'), buttonParent)
    randomButton = Button(QPixmap(':/images/random.png'), buttonParent)
    tiledButton = Button(QPixmap(':/images/tile.png'), buttonParent)
    centeredButton = Button(QPixmap(':/images/centered.png'), buttonParent)

    ellipseButton.setPos(-100, -100)
    figure8Button.setPos(100, -100)
    randomButton.setPos(0, 0)
    tiledButton.setPos(-100, 100)
    centeredButton.setPos(100, 100)

    scene.addItem(buttonParent)
    buttonParent.setScale(0.75)
    buttonParent.setPos(200, 200)
    buttonParent.setZValue(65)

    # States.
    rootState = QState()
    ellipseState = QState(rootState)
    figure8State = QState(rootState)
    randomState = QState(rootState)
    tiledState = QState(rootState)
    centeredState = QState(rootState)

    # Values.
    for i, item in enumerate(items):
        # Ellipse.
        ellipseState.assignProperty(item, 'pos',
                                    QPointF(math.cos((i / 63.0) * 6.28) * 250,
                                            math.sin((i / 63.0) * 6.28) * 250))

        # Figure 8.
        figure8State.assignProperty(item, 'pos',
                                    QPointF(math.sin((i / 63.0) * 6.28) * 250,
                                            math.sin(((i * 2) / 63.0) * 6.28) * 250))

        # Random.
        randomState.assignProperty(item, 'pos',
                                   QPointF(-250 + qrand() % 500, -250 + qrand() % 500))

        # Tiled.
        tiledState.assignProperty(item, 'pos',
                                  QPointF(((i % 8) - 4) * kineticPix.width() + kineticPix.width() / 2,
                                          ((i // 8) - 4) * kineticPix.height() + kineticPix.height() / 2))

        # Centered.
        centeredState.assignProperty(item, 'pos', QPointF())

    # Ui.
    view = View(scene)
    view.setWindowTitle("Animated Tiles")
    view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
    view.setBackgroundBrush(QBrush(bgPix))
    view.setCacheMode(QGraphicsView.CacheBackground)
    view.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
    view.show()

    states = QStateMachine()
    states.addState(rootState)
    states.setInitialState(rootState)
    rootState.setInitialState(centeredState)

    group = QParallelAnimationGroup()
    for i, item in enumerate(items):
        anim = QPropertyAnimation(item, b'pos')
        anim.setDuration(750 + i * 25)
        anim.setEasingCurve(QEasingCurve.InOutBack)
        group.addAnimation(anim)

    trans = rootState.addTransition(ellipseButton.pressed, ellipseState)
    trans.addAnimation(group)

    trans = rootState.addTransition(figure8Button.pressed, figure8State)
    trans.addAnimation(group)

    trans = rootState.addTransition(randomButton.pressed, randomState)
    trans.addAnimation(group)

    trans = rootState.addTransition(tiledButton.pressed, tiledState)
    trans.addAnimation(group)

    trans = rootState.addTransition(centeredButton.pressed, centeredState)
    trans.addAnimation(group)

    timer = QTimer()
    timer.start(125)
    timer.setSingleShot(True)
    trans = rootState.addTransition(timer.timeout, ellipseState)
    trans.addAnimation(group)

    states.start()

    sys.exit(app.exec_())
# -------------------------------------------------------------------------------------------------------------
# Created by panda on 12/07/2018 - 7:55 PM
# © 2017 - 2018 DAMGteam. All rights reserved