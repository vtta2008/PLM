#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Name: Credit.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    Credit infomation.

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

# -------------------------------------------------------------------------------------------------------------
""" About Layout """

class Credit(QDialog):

    def __init__(self, parent=None):

        super(Credit, self).__init__(parent)

        self.setWindowTitle("Credit")
        self.setWindowIcon(QIcon(func.get_icon('Logo')))

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        with open(os.path.join(os.getenv(app.__envKey__), 'appData', 'CREDIT'), 'r') as f:
            credit = f.read()

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.content = QLabel(credit)

        self.content.setGeometry(0, 0, 650, 400)
        self.scrollArea.setWidget(self.content)

        okBtn = QPushButton('Ok')
        okBtn.clicked.connect(self.close)

        self.layout.addWidget(self.scrollArea, 0, 0, 8, 4)
        self.layout.addWidget(okBtn, 8, 3, 1, 1)

def main():
    app = QApplication(sys.argv)
    about_layout = Credit()
    about_layout.show()
    app.exec_()


if __name__=='__main__':
    main()