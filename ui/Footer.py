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
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout

# Plt
from appData import COPYRIGHT
from ui.Libs.Button import Button
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

        self.logoBtn = Button({'stt':COPYRIGHT, 'icon':'TeamLogo', 'cl':partial(self.showLayout.emit, "credit", "show")})
        # self.logoBtn.setToolTip(COPYRIGHT)
        # self.logoBtn.setIcon(QIcon(getLogo(24, 'DAMG')))
        # self.logoBtn.clicked.connect(partial(self.showLayout.emit, "credit", "show"))

        self.browserBtn = Button({'stt':'Browser', 'icon':'PLMBrowser', 'cl':partial(self.showLayout.emit, "browser", "show")})
        # self.browserBtn.setToolTip("PLM web browser")
        # self.browserBtn.setIcon(QIcon(getAppIcon(32, 'PLMBrowser')))
        # self.browserBtn.clicked.connect(partial(self.showLayout.emit, "browser", "show"))

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