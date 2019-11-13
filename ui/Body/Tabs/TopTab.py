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
from bin.data.damg              import DAMGLIST

# PyQt5
from PyQt5.QtWidgets            import QApplication
from PyQt5.QtGui                import QResizeEvent

# PLM
from ui.uikits.Icon             import AppIcon
from ui.uikits.BoxLayout        import VBoxLayout
from ui.uikits.TabWidget        import TabWidget
from ui.Body.Tabs               import TopTab1, TopTap3, TopTab2

# -------------------------------------------------------------------------------------------------------------
""" Tab Layout """

class TopTab(TabWidget):

    key                         = 'TopTab'

    def __init__(self, buttonManager, parent=None):
        super(TopTab, self).__init__(parent)

        self.layout             = VBoxLayout()
        self.buttonManager      = buttonManager
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.tab1               = TopTab1.TopTab1(self.buttonManager, self.parent)
        self.tab2               = TopTab2.TopTab2(self.buttonManager, self.parent)
        self.tab3               = TopTap3.TopTap3(self.buttonManager, self.parent)

        self.tabs               = DAMGLIST(listData=[self.tab1, self.tab2, self.tab3])
        self.tabNames           = DAMGLIST(listData=['Project', 'User', 'Cmd'])

        for layout in self.tabs:
            # layout.signals.connect('executing', self.signals.executing)
            # layout.signals.connect('regisLayout', self.signals.regisLayout)
            # layout.signals.connect('openBrowser', self.signals.openBrowser)
            # layout.signals.connect('setSetting', self.signals.setSetting)
            # layout.signals.connect('showLayout', self.signals.showLayout)
            # layout.settings._settingEnable = True

            self.addTab(layout, self.tabNames[self.tabs.index(layout)])
            self.setTabIcon(self.tabs.index(layout), AppIcon(32, self.tabNames[self.tabs.index(layout)]))

        self.signals.updateAvatar.connect(self.tab2.update_avatar)

    def resizeEvent(self, event):
        w = self.width()
        h = self.height()
        for tab in self.tabs:
            tab.resize(w-4, h-4)


def main():
    app = QApplication(sys.argv)
    layout = TopTab()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018