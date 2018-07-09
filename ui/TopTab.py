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

# PyQt5
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QTabWidget)

# Plt
from appData import SiPoMin
from ui import (TopTab1, TopTab2, TopTab3, TopTab4, TopTab5)
from core.Specs import Specs

# -------------------------------------------------------------------------------------------------------------
""" Tab Layout """

class TopTab(QWidget):

    key = 'topTab'
    executing = pyqtSignal(str)
    showLayout = pyqtSignal(str, str)
    regLayout = pyqtSignal(str, object)
    updateAvatar = pyqtSignal(str)


    def __init__(self, parent=None):
        super(TopTab, self).__init__(parent)
        self.specs = Specs(self.key, self)
        self.layout = QVBoxLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        self.tabs = QTabWidget()

        self.tab1 = TopTab1.TopTab1()
        self.tab2 = TopTab2.TopTab2()
        self.tab3 = TopTab3.TopTab3()
        self.tab4 = TopTab4.TopTab4()
        self.tab5 = TopTab5.TopTab5()

        self.tab1.showLayout.connect(self.showLayout)
        self.tab2.showLayout.connect(self.showLayout)
        self.tab3.showLayout.connect(self.showLayout)
        self.tab4.showLayout.connect(self.showLayout)
        self.tab5.showLayout.connect(self.showLayout)

        self.tab1.executing.connect(self.executing)
        self.tab2.executing.connect(self.executing)
        self.tab3.executing.connect(self.executing)
        self.tab4.executing.connect(self.executing)
        self.tab5.executing.connect(self.executing)

        self.tab1.regLayout.connect(self.regLayout)
        self.tab2.regLayout.connect(self.regLayout)
        self.tab3.regLayout.connect(self.regLayout)
        self.tab4.regLayout.connect(self.regLayout)
        self.tab5.regLayout.connect(self.regLayout)

        self.updateAvatar.connect(self.tab3.update_avatar)

        self.tabs.addTab(self.tab1, 'Tool')
        self.tabs.addTab(self.tab2, 'Prj')
        self.tabs.addTab(self.tab3, 'User')
        self.tabs.addTab(self.tab4, 'Library')
        self.tabs.addTab(self.tab5, 'Cmd')

        self.layout.addWidget(self.tabs)
        self.applySetting()

    def applySetting(self):
        self.tabs.setMovable(True)
        self.tabs.setElideMode(Qt.ElideRight)
        self.tabs.setUsesScrollButtons(True)
        self.setSizePolicy(SiPoMin, SiPoMin)
        self.tabs.setSizePolicy(SiPoMin, SiPoMin)

def main():
    app = QApplication(sys.argv)
    layout = TopTab()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018