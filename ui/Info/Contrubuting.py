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
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QScrollArea

# Plm
from appData import CONTRIBUTING
from ui.uikits.UiPreset import Label, IconPth
from ui.uikits.Button import Button
from core.Specs import Specs

# -------------------------------------------------------------------------------------------------------------
""" Contributing Layout """

class Contributing(QWidget):

    key = 'contributing'
    showLayout = pyqtSignal(str, str)

    def __init__(self, parent=None):

        super(Contributing, self).__init__(parent)
        self.specs = Specs(self.key, self)
        self.setWindowIcon(IconPth(32, 'Contributing'))

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)
        self.resize(350, 400)

    def buildUI(self):
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.content = Label({'txt':CONTRIBUTING, 'alg':'left', 'link': True})

        self.content.setGeometry(0, 0, 350, 400)
        self.scrollArea.setWidget(self.content)

        closeBtn = Button({'txt': 'Close', 'tt': 'Close window', 'cl': partial(self.showLayout.emit, self.key, 'hide')})

        self.layout.addWidget(self.scrollArea, 0, 0, 8, 4)
        self.layout.addWidget(closeBtn, 8, 3, 1, 1)

    def closeEvent(self, event):
        self.showLayout.emit(self.key, 'hide')
        event.ignore()

def main():
    app = QApplication(sys.argv)
    about_layout = Contributing()
    about_layout.show()
    app.exec_()

if __name__=='__main__':
    main()