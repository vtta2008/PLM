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
from functools import partial

# PtQt5
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QGridLayout, QScrollArea

# Plm
from appData import CREDIT
from ui.uikits.Widget import Widget
from ui.uikits.GridLayout import GridLayout
from ui.uikits.Button import Button
from ui.uikits.UiPreset import Label, IconPth

# -------------------------------------------------------------------------------------------------------------
""" Credit Layout """

class Credit(Widget):

    key = 'credit'
    showLayout = pyqtSignal(str, str)

    def __init__(self, parent=None):

        super(Credit, self).__init__(parent)

        self.setWindowIcon(IconPth(32, 'Credit'))
        self.setWindowTitle('CREDIT')

        self.buildUI()

        self.resize(500, 600)

    def buildUI(self):
        self.layout = GridLayout()

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.content = Label({'txt':CREDIT, 'alg':'left', 'link': True})

        self.content.setGeometry(0, 0, 500, 600)
        self.scrollArea.setWidget(self.content)

        closeBtn = Button({'txt': 'Close', 'tt': 'Close window', 'cl': self.close})

        self.layout.addWidget(self.scrollArea, 0, 0, 8, 4)
        self.layout.addWidget(closeBtn, 8, 3, 1, 1)

        self.setLayout(self.layout)

def main():
    app = QApplication(sys.argv)
    about_layout = Credit()
    about_layout.show()
    app.exec_()

if __name__=='__main__':
    main()