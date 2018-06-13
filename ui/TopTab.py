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

# -------------------------------------------------------------------------------------------------------------
""" Tab Layout """

class TopTab(QWidget):

    showPlt = pyqtSignal(bool)
    showLogin = pyqtSignal(bool)
    tabSizeSig = pyqtSignal(int, int)
    updateAvatar = pyqtSignal(bool)
    execute = pyqtSignal(str)

    def __init__(self, parent=None):
        super(TopTab, self).__init__(parent)

        self.settings = app.appSetting

        self.layout = QVBoxLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        self.tabs = QTabWidget()

        tab3 = TopTab3.TopTab3()
        tab3.showPlt.connect(self.showPlt.emit)
        tab3.showLogin.connect(self.showLogin.emit)
        self.updateAvatar.connect(tab3.update_avatar)

        tab1 = TopTab1.TopTab1()
        tab1.execute.connect(self.execute.emit)

        self.tabs.addTab(tab1, 'Tool')
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