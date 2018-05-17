#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Name: ui_info_template.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This is a layout which have info about pipeline tools

"""
# -------------------------------------------------------------------------------------------------------------
""" Import plt_modules """

# Python
import sys

# PtQt5
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QGridLayout, QLabel, QPushButton, QScrollArea

# Plt
from utilities import utils as func

class AboutPlt(QDialog):
    def __init__(self, id='About', message=None, icon=func.get_icon('Logo'), parent=None):
        super(AboutPlt, self).__init__(parent)

        self.setWindowTitle(id)
        self.setWindowIcon(QIcon(icon))
        central_widget = QWidget(self)
        self.layout = QGridLayout(self)
        central_widget.setLayout(self.layout)
        self.buildUI(message)
        self.setLayout(self.layout)

    def buildUI(self, message):
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.content = QLabel(message)
        self.content.setGeometry(0, 0, 400, 650)
        self.scrollArea.setWidget(self.content)

        yesBtn = QPushButton('OK')
        yesBtn.clicked.connect(self.close)

        self.layout.addWidget(self.scrollArea, 0, 0, 8, 4)
        self.layout.addWidget(yesBtn, 8, 2, 1, 2)

def main():
    app = QApplication(sys.argv)
    about_layout = AboutPlt()
    about_layout.show()
    app.exec_()


if __name__=='__main__':
    main()