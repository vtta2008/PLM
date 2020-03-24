# -*- coding: utf-8 -*-
"""

Script Name: screen.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------


class reader(property):
    def __init__(self, varname):
        _reader = lambda obj: getattr(obj, varname)
        super(reader, self).__init__(_reader)

class accessor(property):
    def __init__(self, varname, set_validation=None):
        _reader = lambda obj: getattr(obj, varname)
        def _writer(obj, value):
            if set_validation is not None:
                if set_validation(value):
                    setattr(obj, varname, value)
        super(accessor, self).__init__(_reader, _writer)

#example
class MyClass(object):
    def __init__(self):
        self._attr = None

    attr = reader('_attr')


import math, sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QPalette, QBrush, QColor, QPen
from PyQt5.QtWidgets import QWidget, QApplication, QTextEdit, QMainWindow, QGridLayout, QPushButton


class Overlay(QWidget):


    _num = 12
    _radius = 10
    _innerRadius = 60


    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        palette = QPalette(self.palette())
        palette.setColor(palette.Background, Qt.transparent)
        self.setPalette(palette)

    def paintEvent(self, event):

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QBrush(QColor(255, 255, 255, 127)))
        painter.setPen(QPen(Qt.NoPen))

        for i in range(self.num):
            if (self.counter / (self.num - 1)) % self.num == i:
                painter.setBrush(QBrush(QColor(127 + (self.counter % 5)*32, 127, 127)))
            else:
                painter.setBrush(QBrush(QColor(127, 127, 127)))

            painter.drawEllipse(self.width()/2 + (self.innerRadius) * math.cos(2 * math.pi * i / float(self.num)) - (self.radius/2),
                                self.height()/2 + (self.innerRadius) * math.sin(2 * math.pi * i / float(self.num)) - (self.radius/2),
                                self.radius, self.radius)

        painter.end()

    def showEvent(self, event):

        self.timer = self.startTimer(50)
        self.counter = 0

    def timerEvent(self, event):
        self.counter += 1
        self.update()
        # if self.counter == 60:
        #     self.killTimer(self.timer)
        #     self.hide()

    @property
    def num(self):
        return self._num

    @property
    def radius(self):
        return self._radius

    @property
    def innerRadius(self):
        return self._innerRadius

    @innerRadius.setter
    def innerRadius(self, val):
        self._innerRadius = val

    @radius.setter
    def radius(self, val):
        self._radius = val

    @num.setter
    def num(self, val):
        self._num = val


class MainWindow(QMainWindow):

    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        widget = QWidget(self)
        self.editor = QTextEdit()
        self.editor.setPlainText("0123456789"*100)
        layout = QGridLayout(widget)
        layout.addWidget(self.editor, 0, 0, 1, 3)
        button = QPushButton("Wait")
        layout.addWidget(button, 1, 1, 1, 1)

        self.setCentralWidget(widget)
        self.overlay = Overlay(self.centralWidget())
        self.overlay.hide()
        button.clicked.connect(self.overlay.show)

    def resizeEvent(self, event):
        self.overlay.resize(event.size())
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/21/2020 - 8:59 AM
# © 2017 - 2019 DAMGteam. All rights reserved