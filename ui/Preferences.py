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
from PyQt5.QtCore import QSettings, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QCheckBox, QPushButton, QGridLayout, QGroupBox

# Plt
import appData as app
from utilities import utils as func

# -------------------------------------------------------------------------------------------------------------
""" Preferences window """

class Preferences(QDialog):

    checkboxTDSig = pyqtSignal(bool)
    checkboxCompSig = pyqtSignal(bool)
    checkboxArtSig = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(Preferences, self).__init__(parent)

        self.resize(200, 100)
        self.setWindowTitle("Preferences")
        self.setWindowIcon(QIcon(func.getIcon32('Logo')))

        self.settings = app.appSetting

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        tbGrpBox = QGroupBox("Tool Bar")
        tbGrid = QGridLayout()
        tbGrpBox.setLayout(tbGrid)

        self.toolBarTD_checkBox = QCheckBox("Show/hide TD toolbar")
        showTDToolbar = func.str2bool(self.settings.value("showTDToolbar", True))
        self.toolBarTD_checkBox.setChecked(showTDToolbar)
        self.toolBarTD_checkBox.stateChanged.connect(self.checkBoxTDStateChanged)

        self.toolBarComp_checkBox = QCheckBox("Show/hide Comp toolbar")
        showCompToolbar = func.str2bool(self.settings.value("showCompToolbar", True))
        self.toolBarComp_checkBox.setChecked(showCompToolbar)
        self.toolBarComp_checkBox.stateChanged.connect(self.checkBoxCompStateChanged)

        self.toolBarArt_checkBox = QCheckBox("Show/hide Art toolbar")
        showArtToolbar = func.str2bool(self.settings.value("showArtToolbar", True))
        self.toolBarArt_checkBox.setChecked(showArtToolbar)
        self.toolBarArt_checkBox.stateChanged.connect(self.checkBoxArtStateChanged)

        self.allToolBar_checkBox = QCheckBox("Show/hide all toolbar")
        showAllToolbar = func.str2bool(self.settings.value("showAllToolbar", True))
        self.allToolBar_checkBox.setChecked(showAllToolbar)
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
        showAllToolbar = func.str2bool(self.allToolBar_checkBox.checkState())
        self.toolBarTD_checkBox.setChecked(showAllToolbar)
        self.toolBarComp_checkBox.setChecked(showAllToolbar)
        self.toolBarArt_checkBox.setChecked(showAllToolbar)
        self.settings.setValue("showAllToolbar", func.bool2str(showAllToolbar))

    def checkBoxTDStateChanged(self):
        showTDToolbar = func.str2bool(self.toolBarTD_checkBox.checkState())
        self.settings.setValue("showTDToolbar", func.bool2str(showTDToolbar))
        self.checkboxTDSig.emit(self.toolBarTD_checkBox.isChecked())

    def checkBoxCompStateChanged(self):
        showCompToolbar = func.str2bool(self.toolBarComp_checkBox.checkState())
        self.settings.setValue("showCompToolbar", func.bool2str(showCompToolbar))
        self.checkboxCompSig.emit(self.toolBarComp_checkBox.isChecked())

    def checkBoxArtStateChanged(self):
        showArtToolbar = func.str2bool(self.toolBarArt_checkBox.checkState())
        self.settings.setValue("showArtToolbar", func.bool2str(showArtToolbar))
        self.checkboxArtSig.emit(self.toolBarArt_checkBox.isChecked())

def main():
    app = QApplication(sys.argv)
    pref_layout = Preferences()
    pref_layout.show()
    app.exec_()

if __name__=='__main__':
    main()

