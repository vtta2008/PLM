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

import sys, logging

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

TXT = "Test String"
ALG = Qt.AlignCenter
WMIN = 50

class pltLabel(QDialog):

    def __init__(self, txt=TXT, align=None, parent=None):
        super(pltLabel, self).__init__(parent)

        layout = QVBoxLayout()
        text = QLabel(txt)
        layout.addWidget(text)

        text.setMinimumWidth(WMIN)
        if align == None:
            align = Qt.AlignCenter
        text.setAlignment(align)

        self.setLayout(layout)

class TestWindow(QMainWindow):

    def __init__(self, parent=None):
        super(TestWindow, self).__init__(parent)

        self.setWindowTitle(TXT)
        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        widget = pltLabel("What the hex is this ???")
        self.layout.addWidget(widget, 0,0,1,1)

def main():
    app = QApplication(sys.argv)
    testWindow = TestWindow()
    testWindow.show()
    app.exec_()

if __name__=='__main__':
    main()