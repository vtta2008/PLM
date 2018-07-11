#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: TopTab4.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys, random
from functools import partial

# PyQt5
from PyQt5.QtCore import pyqtSignal, pyqtSlot, pyqtProperty, Qt, QPointF, QTimer, QSize, QRectF, QSizeF
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QGroupBox
from PyQt5.QtGui import QRadialGradient, QColor, QPainter, QBrush, QPen

# Plt
from ui import uirc as rc
from core.Specs import Specs

# -------------------------------------------------------------------------------------------------------------
""" TopTab4 """

class TopTab4(QWidget):

    key = 'topTab4'
    executing = pyqtSignal(str)
    showLayout = pyqtSignal(str, str)
    addLayout = pyqtSignal(object)

    def __init__(self, parent=None):
        super(TopTab4, self).__init__(parent)
        self.specs = Specs(self.key, self)
        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)
        self.addLayout.emit(self)

    def buildUI(self):

        sec1Grp = QGroupBox('Test Layout')
        sec1Grid = QGridLayout()
        sec1Grp.setLayout(sec1Grid)

        # sec1Grid.addWidget(rc.Label("Update later"), 0, 0, 6, 9)
        sec1Grid.addWidget(BubblesWidget(), 0, 0, 6, 9)

        self.layout.addWidget(sec1Grp, 0, 0, 6, 9)

        self.applySetting()

    def applySetting(self):
        pass

class BaseClass(QWidget):
    def __init__(self, parent=None):
        super(BaseClass, self).__init__(parent)
        self.resetAuthor()

    def getAuthor(self):
        return self._author

    def setAuthor(self, name):
        self._author = name

    def resetAuthor(self):
        self._author = "David Boddie"

    author = pyqtProperty(str, getAuthor, setAuthor, resetAuthor)

class Bubble:
    def __init__(self, position, radius, speed, innerColor, outerColor):
        self.position = position
        self.radius = radius
        self.speed = speed
        self.innerColor = innerColor
        self.outerColor = outerColor
        self.updateBrush()

    def updateBrush(self):
        gradient = QRadialGradient(
            QPointF(self.radius, self.radius), self.radius,
            QPointF(self.radius * 0.5, self.radius * 0.5))

        gradient.setColorAt(0, QColor(255, 255, 255, 255))
        gradient.setColorAt(0.25, self.innerColor)
        gradient.setColorAt(1, self.outerColor)
        self.brush = QBrush(gradient)

    def drawBubble(self, painter):
        painter.save()
        painter.translate(self.position.x() - self.radius,
                          self.position.y() - self.radius)
        painter.setBrush(self.brush)
        painter.drawEllipse(0.0, 0.0, 2 * self.radius, 2 * self.radius)
        painter.restore()

class BubblesWidget(BaseClass):
    bubbleLeft = pyqtSignal()
    bubblesRemaining = pyqtSignal(int)

    def __init__(self, parent=None):
        super(BubblesWidget, self).__init__(parent)
        self.pen = QPen(QColor("#cccccc"))
        self.bubbles = []
        self.backgroundColor1 = self.randomColor()
        self.backgroundColor2 = self.randomColor().darker(150)
        self.newBubble = None
        random.seed()
        self.animation_timer = QTimer(self)
        self.animation_timer.setSingleShot(False)
        self.animation_timer.timeout.connect(self.animate)
        self.animation_timer.start(25)
        self.bubbleTimer = QTimer()
        self.bubbleTimer.setSingleShot(False)
        self.bubbleTimer.timeout.connect(self.expandBubble)
        self.setMouseTracking(True)
        self.setMinimumSize(QSize(200, 200))
        self.setWindowTitle("Bubble Maker")

    def paintEvent(self, event):
        background = QRadialGradient(QPointF(self.rect().topLeft()), 500, QPointF(self.rect().bottomRight()))
        background.setColorAt(0, self.backgroundColor1)
        background.setColorAt(1, self.backgroundColor2)
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QBrush(background))
        painter.setPen(self.pen)
        for bubble in self.bubbles:
            if QRectF(bubble.position - QPointF(bubble.radius, bubble.radius),
                      QSizeF(2 * bubble.radius, 2 * bubble.radius)).intersects(QRectF(event.rect())):
                bubble.drawBubble(painter)
        if self.newBubble:
            self.newBubble.drawBubble(painter)
        painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.newBubble is None:
            self.newBubble = Bubble(QPointF(event.pos()), 4.0, 1.0 + random.random() * 7, self.randomColor(),
                                    self.randomColor())
            self.bubbleTimer.start(50)
            event.accept()

    def mouseMoveEvent(self, event):
        if self.newBubble:
            self.update(QRectF(self.newBubble.position - QPointF(self.newBubble.radius + 1, self.newBubble.radius + 1),
                               QSizeF(2 * self.newBubble.radius + 2, 2 * self.newBubble.radius + 2)).toRect())
            self.newBubble.position = QPointF(event.pos())
            self.update(
                QRectF(self.newBubble.position - QPointF(self.newBubble.radius + 1, self.newBubble.radius + 1),
                       QSizeF(2 * self.newBubble.radius + 2, 2 * self.newBubble.radius + 2)).toRect())
        event.accept()

    def mouseReleaseEvent(self, event):
        if self.newBubble:
            self.bubbles.append(self.newBubble)
            self.newBubble = None
            self.bubbleTimer.stop()
            self.bubblesRemaining.emit(len(self.bubbles))
        event.accept()

    def expandBubble(self):
        if self.newBubble:
            self.newBubble.radius = min(self.newBubble.radius + 4.0, self.width() / 8.0, self.height() / 8.0)
            self.update(QRectF(self.newBubble.position - QPointF(self.newBubble.radius + 1, self.newBubble.radius + 1),
                               QSizeF(2 * self.newBubble.radius + 2, 2 * self.newBubble.radius + 2)).toRect())
            self.newBubble.updateBrush()

    def randomColor(self):
        red = 205 + random.random() * 50
        green = 205 + random.random() * 50
        blue = 205 + random.random() * 50
        alpha = 91 + random.random() * 100
        return QColor(red, green, blue, alpha)

    def animate(self):
        bubbles = []
        left = False
        for bubble in self.bubbles:
            bubble.position = bubble.position + QPointF(0, -bubble.speed)
            self.update(QRectF(bubble.position - QPointF(bubble.radius + 1, bubble.radius + 1),
                               QSizeF(2 * bubble.radius + 2, 2 * bubble.radius + 2 + bubble.speed)).toRect())
            if bubble.position.y() + bubble.radius > 0:
                bubbles.append(bubble)
            else:
                self.bubbleLeft.emit()
                left = True
        if self.newBubble:
            self.update(
                QRectF(self.newBubble.position - QPointF(
                    self.newBubble.radius + 1,
                    self.newBubble.radius + 1),
                       QSizeF(2 * self.newBubble.radius + 2, 2 * self.newBubble.radius + 2)).toRect())
        self.bubbles = bubbles
        if left:
            self.bubblesRemaining.emit(len(self.bubbles))

    def sizeHint(self):
        return QSize(200, 200)

    def getBubbles(self):
        return len(self.bubbles)

    @pyqtSlot(int)
    def setBubbles(self, value):

        value = max(0, value)
        while len(self.bubbles) < value:
            newBubble = Bubble(QPointF(random.random() * self.width(), random.random() * self.height()),
                               4.0 + random.random() * 20, 1.0 + random.random() * 7, self.randomColor(),
                               self.randomColor())
            newBubble.updateBrush()
            self.bubbles.append(newBubble)
        self.bubbles = self.bubbles[:value]
        self.bubblesRemaining.emit(value)
        self.update()

    numberOfBubbles = pyqtProperty(int, getBubbles, setBubbles)

    def getColor1(self):
        return self.backgroundColor1

    def setColor1(self, value):
        self.backgroundColor1 = QColor(value)
        self.update()

    color1 = pyqtProperty(QColor, getColor1, setColor1)

    def getColor2(self):
        return self.backgroundColor2

    def setColor2(self, value):
        self.backgroundColor2 = QColor(value)
        self.update()

    color2 = pyqtProperty(QColor, getColor2, setColor2)

    @pyqtSlot()
    def stop(self):
        self.animation_timer.stop()

    @pyqtSlot()
    def start(self):
        self.animation_timer.start(25)

def main():
    app = QApplication(sys.argv)
    layout = TopTab4()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018