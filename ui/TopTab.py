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
from damg                       import DAMGLIST

# PyQt5
from PyQt5.QtWidgets            import QApplication

# PLM
from ui.uikits.Widget           import Widget
from ui.uikits.BoxLayout        import VBoxLayout
from ui.uikits.TabWidget        import TabWidget
from ui                         import (TopTab1, TopTab2, TopTab3)

# -------------------------------------------------------------------------------------------------------------
""" Tab Layout """

class TopTab(Widget):

    key                         = 'TopTab'

    def __init__(self, parent=None):
        super(TopTab, self).__init__(parent)

        self.layout             = VBoxLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.tabs               = TabWidget()

        self.tab1               = TopTab1.TopTab1()
        self.tab2               = TopTab2.TopTab2()
        self.tab3               = TopTab3.TopTab3()

        self.tabLst             = DAMGLIST(listData=[self.tab1, self.tab2, self.tab3])
        self.tabNames           = DAMGLIST(listData=['Project', 'User', 'Cmd'])

        for layout in self.tabLst:
            layout.signals.showLayout.connect(self.signals.showLayout)
            layout.signals.executing.connect(self.signals.executing)
            layout.signals.regisLayout.connect(self.signals.regisLayout)
            layout.signals.setSetting.connect(self.signals.setSetting)
            layout.signals.openBrowser.connect(self.signals.openBrowser)

            self.tabs.addTab(layout, self.tabNames[self.tabLst.index(layout)])

        self.signals.updateAvatar.connect(self.tab2.update_avatar)

        self.layout.addWidget(self.tabs)

    def getCurrentTab(self):
        return self.tabLst[self.tabs.currentIndex()]

    def getCurrentKey(self):
        return self.getCurrentTab().key

    def showEvent(self, event):

        try:
            key                 = self.getValue('currentTab')
        except None:
            key                 = self.tab1.key
        else:
            self.signals.showLayout.emit(key, 'show')
        finally:
            self.signals.showLayout.emit(self.key, 'show')

    def hideEvent(self, event):
        self.setValue('currentTab', self.getCurrentKey())

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