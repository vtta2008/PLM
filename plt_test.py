#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: plt_test.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
        This is the place to test layout script
"""
# -------------------------------------------------------------------------------------------------------------
""" Check data flowing """
import os
print("Start running test file: {file}".format(file=__name__))
print("Directory: {path}".format(path=__file__.split(__name__)[0]))
__root__ = "PLT_RT"
# -------------------------------------------------------------------------------------------------------------
""" Import """
import versioneer
import sys, logging

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

TXT = "Test String"
ALG = Qt.AlignCenter
WMIN = 50

class Clabel(QWidget):
    def __init__(self,txt=TXT, wmin=WMIN, alg = None, font=None, parent=None):
        super(Clabel, self).__init__(parent)
        if alg == None:
            alg = Qt.AlignCenter
        if font == None:
            font = QFont("Arial, 10")
        label = QLabel(txt)
        label.setMinimumWidth(wmin)
        label.setAlignment(alg)
        label.setFont(font)

        layout = QHBoxLayout()
        layout.addWidget(label)

class TestWindow(QMainWindow):

    def __init__(self, parent=None):
        super(TestWindow, self).__init__(parent)

        self.setWindowTitle(TXT)
        self.widget = QWidget()
        self.buildUI()
        self.setCentralWidget(self.widget)

    def buildUI(self):
        layout = QVBoxLayout()
        layout.addWidget(Clabel("What the hex is this ???"))
        self.widget.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    testWindow = TestWindow()
    testWindow.show()
    app.exec_()

if __name__=='__main__':
    main()