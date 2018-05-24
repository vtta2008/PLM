#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: TopTabWidget.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys, logging
import sqlite3 as lite

# PyQt5
from PyQt5.QtCore import pyqtSignal, QSettings
from PyQt5.QtWidgets import (QApplication, QSizePolicy, QWidget, QVBoxLayout, QTabWidget)

# Plt
import appData as app

from ui import (TopTab1, TopTab2, TopTab3, TopTab4)

from utilities import utils as func
from utilities import variables as var

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logPth = os.path.join(app.LOGPTH)
handler = logging.FileHandler(logPth)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------------------
# Get apps info config
ICONINFO = func.preset_load_iconInfo()

# -------------------------------------------------------------------------------------------------------------
""" Variables """

# -------------------------------------------------------------------------------------------------------------
""" Tab Layout """

class TopTab(QWidget):

    dbConn = lite.connect(var.DB_PATH)
    showMainSig = pyqtSignal(bool)
    showLoginSig = pyqtSignal(bool)
    tabSizeSig = pyqtSignal(int, int)

    def __init__(self, username, parent=None):
        super(TopTab, self).__init__(parent)

        self.username = username
        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

        self.layout = QVBoxLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        self.tabs = QTabWidget()

        tab3 = TopTab3.TopTab3()
        tab3.showMainSig.connect(self.showMainSig.emit)
        tab3.showLoginSig.connect(self.showLoginSig.emit)

        self.tabs.addTab(TopTab1.TopTab1(), 'Tool')
        self.tabs.addTab(TopTab2.TopTab2(), 'Prj')
        self.tabs.addTab(tab3, 'User')
        self.tabs.addTab(TopTab4.TopTab4(), 'Library')

        self.layout.addWidget(self.tabs)
        self.applySetting()

    def applySetting(self):
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.tabs.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)


def main():
    app = QApplication(sys.argv)
    layout = TopTab()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018