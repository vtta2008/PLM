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
import sys
import appData as app

# PtQt5
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QScrollArea, QLabel, QPushButton

# Plt
from utilities import utils as func

# -------------------------------------------------------------------------------------------------------------
""" About Layout """

class About(QDialog):

    def __init__(self, parent=None):

        super(About, self).__init__(parent)

        self.setWindowTitle("About PLt")
        self.setWindowIcon(QIcon(func.getAppIcon(32, 'About')))

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        readme = app.README

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
    about_layout = About()
    about_layout.show()
    app.exec_()


if __name__=='__main__':
    main()