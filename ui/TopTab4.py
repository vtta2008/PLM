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
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QGroupBox

# -------------------------------------------------------------------------------------------------------------
""" Plt tools """
import appData as app

from ui import uirc as rc

from utilities import utils as func
from utilities import variables as var

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logger = app.set_log()

# -------------------------------------------------------------------------------------------------------------
# Get apps info config
APPINFO = func.preset_load_appInfo()

# -------------------------------------------------------------------------------------------------------------
""" Variables """

# -------------------------------------------------------------------------------------------------------------
""" TopTab4 """


class TopTab4(QWidget):

    def __init__(self, parent=None):
        super(TopTab4, self).__init__(parent)

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

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