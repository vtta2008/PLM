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
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

# PLM
from ui import Widget, VBoxLayout, TabWidget
from ui import TopTab1, TopTab2, TopTab3, TopTab4, TopTab5

# -------------------------------------------------------------------------------------------------------------
""" Tab Layout """

class TopTab(Widget):

    key                 = 'TopTab'

    def __init__(self, parent=None):
        super(TopTab, self).__init__(parent)

        self.layout = VBoxLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.tabs = TabWidget()

        # self.tab1 = TopTab1()
        self.tab2 = TopTab2()
        self.tab3 = TopTab3()
        # self.tab4 = TopTab4()
        self.tab5 = TopTab5()

        self.tabLst = [
                        # self.tab1, self.tab4,
                        self.tab2, self.tab3, self.tab5
                        ]
        self.tabNames = [
                         # 'Tool', 'Testlayout',
                         'Prject', 'User', 'Cmd'
                        ]

        for layout in self.tabLst:
            layout.signals.showLayout.connect(self.signals.showLayout)
            layout.signals.executing.connect(self.signals.executing)
            layout.signals.regisLayout.connect(self.signals.regisLayout)
            layout.signals.setSetting.connect(self.signals.setSetting)
            layout.signals.openBrowser.connect(self.signals.openBrowser)

            self.tabs.addTab(layout, self.tabNames[self.tabLst.index(layout)])

        self.signals.updateAvatar.connect(self.tab3.update_avatar)

        self.tabs.setMovable(True)
        self.tabs.setElideMode(Qt.ElideRight)
        self.tabs.setUsesScrollButtons(True)

        self.layout.addWidget(self.tabs)

    def showEvent(self, event):
        self.signals.showLayout.emit(self.key, 'show')
        key = self.getValue('currentTab')
        if key is None:
            key = self.tabs.currentWidget().key
        else:
            self.signals.showLayout(key, 'show')

    def closeEvent(self, event):
        self.setValue('currentTab', self.tabs.currentWidget().key)
        self.signals.showLayout.emit(self.key, 'hide')

def main():
    app = QApplication(sys.argv)
    layout = TopTab()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018