#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: TopTab4.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys

# PyQt5
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QGroupBox

# -------------------------------------------------------------------------------------------------------------
""" Plt tools """

from ui import uirc as rc
from appData import appSetting

# -------------------------------------------------------------------------------------------------------------
""" TopTab4 """

class TopTab4(QWidget):

    def __init__(self, parent=None):
        super(TopTab4, self).__init__(parent)

        # from core.Settings import Settings
        self.settings = appSetting

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        sec1Grp = QGroupBox('Library')
        sec1Grid = QGridLayout()
        sec1Grp.setLayout(sec1Grid)

        sec1Grid.addWidget(rc.Label("Update later"), 0, 0, 6, 9)

        self.layout.addWidget(sec1Grp, 0, 0, 6, 9)

        self.applySetting()

    def applySetting(self):
        pass


def main():
    app = QApplication(sys.argv)
    layout = TopTab4()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/05/2018