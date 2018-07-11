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

# PtQt5
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QGridLayout, QScrollArea, QWidget, QMenuBar

# Plt
from utilities.utils import getAppIcon
from appData import README, left
from ui.lib.LayoutPreset import Button, Label
from core.Specs import Specs

# -------------------------------------------------------------------------------------------------------------
""" About Layout """

class About(QWidget):

    key = 'about'

    def __init__(self, parent=None):

        super(About, self).__init__(parent)
        self.specs = Specs(self.key, self)
        self.setWindowIcon(QIcon(getAppIcon(32, 'About')))
        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)
        self.resize(650, 300)

    def buildUI(self):
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.content = Label({'txt':README, 'alg':'left'})

        self.content.setGeometry(0, 0, 650, 400)
        self.scrollArea.setWidget(self.content)

        closeBtn = Button({'txt':'Close', 'tt':'Close about window', 'cl': self.close})

        self.layout.addWidget(self.scrollArea, 0, 0, 8, 4)
        self.layout.addWidget(closeBtn, 8, 3, 1, 1)

def main():
    app = QApplication(sys.argv)
    about_layout = About()
    about_layout.show()
    app.exec_()

if __name__=='__main__':
    main()