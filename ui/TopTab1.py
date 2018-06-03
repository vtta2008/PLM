#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: topTab1.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys
from functools import partial

# PyQt5
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QGroupBox, QLineEdit, QPushButton

# Plt
import appData as app
from ui import uirc as rc
from utilities import utils as func

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logger = app.set_log()

# -------------------------------------------------------------------------------------------------------------
""" topTab1 """

class TopTab1(QWidget):

    loadLayout = pyqtSignal(str)
    execute = pyqtSignal(str)

    def __init__(self, parent=None):
        super(TopTab1, self).__init__(parent)

        self.settings = app.APPSETTING

        for i in app.CONFIG_TOOLS:
            self.settings.setValue(i, False)

        self.appInfo = func.preset_load_appInfo()
        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        officeBtns = []
        keys = ['TextEditor', 'NoteReminder']
        for key in keys:
            if key in self.appInfo:
                btn = rc.IconBtnLoadLayout(key)
                btn.consoleSig.connect(self.loadLayout.emit)
                officeBtns.append(btn)

        for key in app.CONFIG_OFFICE:
            if key in self.appInfo:
                btn = rc.IconBtnProcess(key)
                btn.consoleSig.connect(self.execute.emit)
                officeBtns.append(btn)

        sec1Grp = rc.AutoSectionBtnGrp("Office", officeBtns, "IconGrid")

        devBtns = []
        for key in app.CONFIG_DEV:
            if key in self.appInfo:
                btn = rc.IconBtnProcess(key)
                btn.consoleSig.connect(self.execute.emit)
                devBtns.append(btn)

        sec2Grp = rc.AutoSectionBtnGrp("Dev", devBtns, "IconGrid")

        pyuiBtn = []
        for key in app.CONFIG_TOOLS:
            if key in self.appInfo:
                btn = rc.IconBtnLoadLayout(key)
                btn.consoleSig.connect(self.loadLayout.emit)
                pyuiBtn.append(btn)

        sec3Grp = rc.AutoSectionBtnGrp("Tools", pyuiBtn, "IconGrid")

        extraBtns = []
        for key in app.CONFIG_EXTRA:
            if key in self.appInfo:
                btn = rc.IconBtnProcess(key)
                btn.consoleSig.connect(self.loadLayout.emit)
                extraBtns.append(btn)

        sec4Grp = rc.AutoSectionBtnGrp("Extra", extraBtns, "IconGrid")

        self.findEdit = QLineEdit()
        findBtn = QPushButton("Find Tool")

        sec5Grp = QGroupBox("Find Tool")
        sec5Grid = QGridLayout()
        sec5Grid.addWidget(self.findEdit, 0, 0, 1, 7)
        sec5Grid.addWidget(findBtn, 0, 7, 1, 2)
        sec5Grp.setLayout(sec5Grid)

        self.layout.addWidget(sec1Grp, 0, 0, 2, 3)
        self.layout.addWidget(sec2Grp, 2, 0, 2, 3)
        self.layout.addWidget(sec3Grp, 0, 3, 4, 3)
        self.layout.addWidget(sec4Grp, 0, 6, 4, 3)
        self.layout.addWidget(sec5Grp, 4, 0, 1, 9)

        self.applySetting()

    def applySetting(self):
        self.layout.setSpacing(2)


def main():
    app = QApplication(sys.argv)
    layout = TopTab1()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 24/05/2018