# -*- coding: utf-8 -*-
"""

Script Name: cvfdfdgfd.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class PicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(QPoint(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()


def close():
    print("xxx")

app = QApplication(sys.argv)
window = QWidget()
window.setFixedSize(740, 850) #window size.

button = PicButton(QPixmap("thinking.png"), window)
button.clicked.connect(close)
button.move(100, 100)

window.show()

sys.exit(app.exec_())
# -------------------------------------------------------------------------------------------------------------
# Created by panda on 31/07/2018 - 5:24 PM
# © 2017 - 2018 DAMGteam. All rights reserved