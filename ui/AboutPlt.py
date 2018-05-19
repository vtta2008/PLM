#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Name: AboutPlt.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This is a layout which have info about pipeline tools

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys, os
import appData as app

# PtQt5
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QScrollArea, QLabel, QPushButton

# Plt
from utilities import utils as func
# from ui import uirc as rc

# -------------------------------------------------------------------------------------------------------------
""" About Layout """

class AboutPlt(QDialog):

    def __init__(self, parent=None):

        super(AboutPlt, self).__init__(parent)

        self.setWindowTitle("About PLt")
        self.setWindowIcon(QIcon(func.get_icon('Logo')))

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        with open(os.path.join(os.getenv(app.__envKey__), 'appData', 'ABOUT'), 'r') as f:
            readme = f.read()

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.content = QLabel(readme)

        self.content.setGeometry(0, 0, 650, 400)
        self.scrollArea.setWidget(self.content)

        okBtn = QPushButton('Ok')
        okBtn.clicked.connect(self.close)

        self.layout.addWidget(self.scrollArea, 0, 0, 8, 4)
        self.layout.addWidget(okBtn, 8, 3, 1, 1)

def main():
    app = QApplication(sys.argv)
    about_layout = AboutPlt()
    about_layout.show()
    app.exec_()


if __name__=='__main__':
    main()