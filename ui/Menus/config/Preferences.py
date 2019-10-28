#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: Plt.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This script is master file of Pipeline Tool

"""

# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys

# PyQt5
from PyQt5.QtWidgets import QApplication, QCheckBox, QPushButton, QGridLayout, QGroupBox

# Plt
from utils.utils import str2bool, bool2str
from ui import Widget, AppIcon, GridLayout, GroupBox, CheckBox, Button

# -------------------------------------------------------------------------------------------------------------
""" Preferences window """

class Preferences(Widget):

    key = 'Preferences'

    _msg_user_not_set = "Not configured yet, will be set with the first message received"

    def __init__(self, parent=None):
        super(Preferences, self).__init__(parent)

        self.resize(200, 100)
        self.setWindowIcon(AppIcon(32, self.key))
        self.setWindowTitle(self.key)

        self.layout = GridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        tbGrpBox = QGroupBox("Tool Bar")
        tbGrid = GridLayout()
        tbGrpBox.setLayout(tbGrid)

        self.toolBarTD_checkBox = CheckBox({'txt': "Show/hide TD toolbar"})
        self.toolBarTD_checkBox.stateChanged.connect(self.checkBoxTDStateChanged)

        self.toolBarComp_checkBox = CheckBox({'txt': "Show/hide Comp toolbar"})
        self.toolBarComp_checkBox.stateChanged.connect(self.checkBoxCompStateChanged)

        self.toolBarArt_checkBox = CheckBox({'txt': "Show/hide Art toolbar"})
        self.toolBarArt_checkBox.stateChanged.connect(self.checkBoxArtStateChanged)

        self.allToolBar_checkBox = CheckBox({'txt': "Show/hide all toolbar"})
        self.allToolBar_checkBox.stateChanged.connect(self.checkBoxMasterStateChanged)

        closeBtn = Button({'txt': 'Close', 'cl': self.close})

        tbGrid.addWidget(self.toolBarTD_checkBox, 0, 0, 1, 1)
        tbGrid.addWidget(self.toolBarComp_checkBox, 1, 0, 1, 1)
        tbGrid.addWidget(self.toolBarArt_checkBox, 2, 0, 1, 1)
        tbGrid.addWidget(self.allToolBar_checkBox, 3, 0, 1, 1)

        self.layout.addWidget(tbGrpBox, 0,0,1,2)
        self.layout.addWidget(closeBtn, 1, 0, 1, 2)

    def checkBoxMasterStateChanged(self):
        showAllToolbar = str2bool(self.allToolBar_checkBox.checkState())
        self.toolBarTD_checkBox.setChecked(showAllToolbar)
        self.toolBarComp_checkBox.setChecked(showAllToolbar)
        self.toolBarArt_checkBox.setChecked(showAllToolbar)
        self.settings.setValue("showAllToolbar", bool2str(showAllToolbar))

    def checkBoxTDStateChanged(self):
        return str2bool(self.toolBarTD_checkBox.checkState())

    def checkBoxCompStateChanged(self):
        return str2bool(self.toolBarComp_checkBox.checkState())

    def checkBoxArtStateChanged(self):
        return str2bool(self.toolBarArt_checkBox.checkState())


def main():
    app = QApplication(sys.argv)
    pref_layout = Preferences()
    pref_layout.show()
    app.exec_()

if __name__=='__main__':
    main()

