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
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox, QPushButton, QGridLayout, QGroupBox

from core.Loggers import SetLogger
# Plt
from utilities.utils import str2bool, bool2str, get_app_icon

# -------------------------------------------------------------------------------------------------------------
""" Preferences window """

class Preferences(QWidget):

    key = 'preferences'
    showLayout = pyqtSignal(str, str)
    checkboxTDSig = pyqtSignal(bool)
    checkboxCompSig = pyqtSignal(bool)
    checkboxArtSig = pyqtSignal(bool)

    _msg_user_not_set = "Not configured yet, will be set with the first message received"

    def __init__(self, parent=None):
        super(Preferences, self).__init__(parent)
        self.logger = SetLogger(self)
        self.resize(200, 100)
        self.setWindowIcon(QIcon(get_app_icon(32, 'Configuration')))

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        tbGrpBox = QGroupBox("Tool Bar")
        tbGrid = QGridLayout()
        tbGrpBox.setLayout(tbGrid)

        self.toolBarTD_checkBox = QCheckBox("Show/hide TD toolbar")
        self.toolBarTD_checkBox.stateChanged.connect(self.checkBoxTDStateChanged)

        self.toolBarComp_checkBox = QCheckBox("Show/hide Comp toolbar")
        self.toolBarComp_checkBox.stateChanged.connect(self.checkBoxCompStateChanged)

        self.toolBarArt_checkBox = QCheckBox("Show/hide Art toolbar")
        self.toolBarArt_checkBox.stateChanged.connect(self.checkBoxArtStateChanged)

        self.allToolBar_checkBox = QCheckBox("Show/hide all toolbar")
        self.allToolBar_checkBox.stateChanged.connect(self.checkBoxMasterStateChanged)


        closeBtn = QPushButton('Close')
        closeBtn.clicked.connect(self.close)

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

    def hideEvent(self, event):
        # self.specs.showState.emit(False)
        pass

    def closeEvent(self, event):
        self.showLayout.emit(self.key, 'hide')
        event.ignore()

def main():
    app = QApplication(sys.argv)
    pref_layout = Preferences()
    pref_layout.show()
    app.exec_()

if __name__=='__main__':
    main()

