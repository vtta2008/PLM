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

# -------------------------------------------------------------------------------------------------------------
""" Tab Layout """

class TopTab(QWidget):

    key = 'topTab'
    executing = pyqtSignal(str)
    showLayout = pyqtSignal(str, str)
    regLayout = pyqtSignal(object)
    updateAvatar = pyqtSignal(bool)


    def __init__(self, parent=None):
        super(TopTab, self).__init__(parent)
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

        self.tabLst = [self.tab1, self.tab2, self.tab3, self.tab4, self.tab5]
        self.tabNames = ['Tool', 'Prj', 'User', 'Testlayout', 'Cmd']

        for layout in self.tabLst:
            layout.showLayout.connect(self.showLayout)
            layout.executing.connect(self.executing)
            layout.addLayout.connect(self.regLayout)
            self.tabs.addTab(layout, self.tabNames[self.tabLst.index(layout)])

        self.updateAvatar.connect(self.tab3.update_avatar)
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