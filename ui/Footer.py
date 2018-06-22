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
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton

# Plt
from appData import COPYRIGHT, appSetting
from utilities import utils as func

# -------------------------------------------------------------------------------------------------------------
""" Footer """

class Footer(QWidget):

    footerSig = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Footer, self).__init__(parent)

        from core.SettingManager import Settings
        self.settings = Settings()
        self.layout = QGridLayout()

        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.logoBtn = QPushButton()
        self.logoBtn.setToolTip(COPYRIGHT)
        self.logoBtn.setIcon(QIcon(func.getLogo(24, 'DAMG')))
        self.logoBtn.clicked.connect(partial(self.footerSig.emit, "Credit"))

        self.browserBtn = QPushButton()
        self.browserBtn.setToolTip("PLM web browser")
        self.browserBtn.setIcon(QIcon(func.getAppIcon(32, 'PLMBrowser')))
        self.browserBtn.clicked.connect(partial(self.footerSig.emit, "PLMBrowser"))

        for i in range(7):
            self.layout.addWidget(QLabel(), 0, i, 1, 1)

        self.layout.addWidget(self.browserBtn, 0, 8, 1, 1)
        self.layout.addWidget(self.logoBtn, 0, 9, 1, 1)

        self.applySetting()

    def applySetting(self):
        self.layout.setSpacing(0)

        self.logoBtn.setFixedSize(QSize(25, 25))
        self.logoBtn.setIconSize(QSize(24, 24))
        # self.logoBtn.setMouseTracking(True)

        self.browserBtn.setFixedSize(QSize(25, 25))
        self.browserBtn.setIconSize(QSize(24, 24))
        # self.browserBtn.setMouseTracking(True)

def main():
    app = QApplication(sys.argv)
    layout = Footer()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/06/2018 - 4:24 AM