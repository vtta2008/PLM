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
import sys

# PtQt5
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QScrollArea

# Plt
from appData import CREDIT, left
from utilities.utils import getAppIcon
from ui.uirc import Label, Button
from core.Specs import Specs

# -------------------------------------------------------------------------------------------------------------
""" About Layout """

class Credit(QWidget):

    key = 'credit'

    def __init__(self, parent=None):

        super(Credit, self).__init__(parent)
        self.specs = Specs(self.key, self)
        self.setWindowIcon(QIcon(getAppIcon(32, 'Credit')))

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.content = Label(CREDIT, left)

        self.content.setGeometry(0, 0, 650, 400)
        self.scrollArea.setWidget(self.content)

        okBtn = Button(['Ok', 'Close credit window'])
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