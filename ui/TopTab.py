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
from bin.data.damg                       import DAMGLIST

# PyQt5
from PyQt5.QtWidgets            import QApplication

# PLM
from ui.uikits.Icon             import AppIcon
from ui.uikits.BoxLayout        import VBoxLayout
from ui.uikits.TabWidget        import TabWidget
from ui.Tabs                    import TopTab1, TopTab2, TopTap3

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

        self.tabLst             = DAMGLIST(listData=[self.tab1, self.tab2, self.tab3])
        self.tabNames           = DAMGLIST(listData=['Project', 'User', 'Cmd'])

        for layout in self.tabLst:
            layout.signals.showLayout.connect(self.signals.showLayout)
            layout.signals.executing.connect(self.signals.executing)
            layout.signals.regisLayout.connect(self.signals.regisLayout)
            layout.signals.setSetting.connect(self.signals.setSetting)
            layout.signals.openBrowser.connect(self.signals.openBrowser)

            self.addTab(layout, self.tabNames[self.tabLst.index(layout)])
            self.setTabIcon(self.tabLst.index(layout), AppIcon(32, self.tabNames[self.tabLst.index(layout)]))

        self.signals.updateAvatar.connect(self.tab2.update_avatar)

def main():
    app = QApplication(sys.argv)
    layout = TopTab()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018