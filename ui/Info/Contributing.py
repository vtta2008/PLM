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
from PyQt5.QtWidgets import QApplication, QScrollArea

# Plm
from appData import CONTRIBUTING
from ui import Widget, GridLayout, Button, Label, AppIcon

# -------------------------------------------------------------------------------------------------------------
""" Contributing Layout """

class Contributing(Widget):

    key = 'contributing'
    showLayout = pyqtSignal(str, str)

    def __init__(self, parent=None):

        super(Contributing, self).__init__(parent)
        self.setWindowIcon(AppIcon(32, 'Contributing'))
        self.setWindowTitle('CONTRIBUTING')

        self.buildUI()

        self.resize(350, 400)

    def buildUI(self):
        self.layout = GridLayout()

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.content = Label({'txt':CONTRIBUTING, 'alg':'left', 'link': True})

        self.content.setGeometry(0, 0, 350, 400)
        self.scrollArea.setWidget(self.content)

        closeBtn = Button({'txt': 'Close', 'tt': 'Close window', 'cl': partial(self.close)})

        self.layout.addWidget(self.scrollArea, 0, 0, 8, 4)
        self.layout.addWidget(closeBtn, 8, 3, 1, 1)

        self.setLayout(self.layout)

def main():
    app = QApplication(sys.argv)
    about_layout = Contributing()
    about_layout.show()
    app.exec_()

if __name__=='__main__':
    main()