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
from appData import REFERENCE
from ui.Libs.UiPreset import Label, IconPth
from ui.Libs.Button import Button
from core.Specs import Specs

# -------------------------------------------------------------------------------------------------------------
""" Contributing Layout """

class Reference(QWidget):

    key = 'reference'
    showLayout = pyqtSignal(str, str)

    def __init__(self, parent=None):

        super(Reference, self).__init__(parent)
        self.specs = Specs(self.key, self)
        self.setWindowIcon(IconPth(32, 'Reference'))

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)
        self.resize(450, 400)

    def buildUI(self):
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.content = Label({'txt':REFERENCE, 'alg':'left', 'link': True})

        self.content.setGeometry(0, 0, 450, 400)
        self.scrollArea.setWidget(self.content)

        closeBtn = Button({'txt': 'Close', 'tt': 'Close window', 'cl': partial(self.showLayout.emit, self.key, 'hide')})

        self.layout.addWidget(self.scrollArea, 0, 0, 8, 4)
        self.layout.addWidget(closeBtn, 8, 3, 1, 1)

    def closeEvent(self, event):
        self.showLayout.emit(self.key, 'hide')
        event.ignore()

def main():
    app = QApplication(sys.argv)
    about_layout = Reference()
    about_layout.show()
    app.exec_()

if __name__=='__main__':
    main()