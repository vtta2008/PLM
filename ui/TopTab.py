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
import sys
import sqlite3 as lite

# PyQt5
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (QApplication, QSizePolicy, QWidget, QVBoxLayout, QTabWidget)

# Plt
import appData as app

from ui import (TopTab1, TopTab2, TopTab3, TopTab4, TopTab5)
from utilities import utils as func

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logger = app.set_log()

# -------------------------------------------------------------------------------------------------------------
""" Tab Layout """

class TopTab(QWidget):

    dbConn = lite.connect(app.DBPTH)
    showMainSig = pyqtSignal(bool)
    showLoginSig = pyqtSignal(bool)
    tabSizeSig = pyqtSignal(int, int)

    def __init__(self, username, parent=None):
        super(TopTab, self).__init__(parent)

        self.username = username
        self.settings = app.APPSETTING

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
        self.tabs.addTab(TopTab5.TopTab5(), 'Cmd')

        self.layout.addWidget(self.tabs)
        self.applySetting()

    def applySetting(self):
        # self.tabs.setTabBar(rc.TabBar())
        # self.tabs.setDocumentMode(True)
        self.tabs.setMovable(True)
        self.tabs.setElideMode(Qt.ElideRight)
        self.tabs.setUsesScrollButtons(True)
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