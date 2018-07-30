#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: Footer.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys
from functools import partial

# PyQt5
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout

# Plt
from appData import COPYRIGHT, VERSION, SiPoMin
from ui.uikits.UiPreset import Label
from core.Specs import Specs

# -------------------------------------------------------------------------------------------------------------
""" Footer """

class Footer(QWidget):

    key = 'footer'
    showLayout = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(Footer, self).__init__(parent)
        self.specs = Specs(self.key, self)
        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        version = Label({'txt': VERSION, 'alg': 'right'})
        copyR = Label({'txt': COPYRIGHT, 'alg': 'right'})

        self.layout.addWidget(version, 0, 0, 1, 9)
        self.layout.addWidget(copyR, 1, 0, 1, 9)

        self.applySetting()

    def applySetting(self):
        self.setSizePolicy(SiPoMin, SiPoMin)
        self.setContentsMargins(5, 5, 5, 5)

def main():
    app = QApplication(sys.argv)
    layout = Footer()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/06/2018 - 4:24 AM