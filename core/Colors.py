# -*- coding: utf-8 -*-
"""

Script Name: Colors.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys

# PyQt5
from PyQt5.QtCore import pyqtSignal, QObject, QResource
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QColor

# Plt
import appData as app
from ui import uirc as rc
from utilities import utils as func

# -------------------------------------------------------------------------------------------------------------
""" Colors """


class Colors(QWidget):

    def __init__(self, parent=None):
        super(Colors, self).__init__(parent)

        self.colors = dict(
                            c01 = QColor(91, 91, 91),
                            c02 = QColor(114, 108, 104),
                            c03 = QColor(0, 0, 0),
                            c04 = QColor(255, 255, 255),
                            c05 = QColor(100, 100, 100),
                            c06 = QColor(255, 0, 0),
                            c07 = QColor(255, 255, 255, 90),
                            c08 = QColor(255, 255, 255, 20),
                            c09 = QColor(255, 255, 255),
                            c10 = QColor(166, 206, 57),
                            c11 = QColor(206, 246, 117, 0),
                            c12 = QColor(190, 230, 80),
                            )

        self.layout = QHBoxLayout()

        for color in self.colors:
            btn = QLabel(color)
            self.layout.addWidget(btn)

        self.setLayout(self.layout)

def main():
    app = QApplication(sys.argv)
    layout = Colors()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 15/06/2018 - 11:05 AM
# © 2017 - 2018 DAMGteam. All rights reserved