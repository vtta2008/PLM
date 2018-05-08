# -*- coding: utf-8 -*-
"""

Script Name: plt.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This script is master file of Pipeline Tool

"""

# -------------------------------------------------------------------------------------------------------------
import sys

from PyQt5.QtCore import QSettings, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QCheckBox, QPushButton, QVBoxLayout, QGridLayout

from utilities import utils as func
from utilities import variables as var


class Pref_layout(QDialog):

    checkboxTDSig = pyqtSignal(bool)
    checkboxCompSig = pyqtSignal(bool)
    checkboxArtSig = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(Pref_layout, self).__init__(parent)

        self.resize(200, 100)
        self.setWindowTitle("Preferences")
        self.setWindowIcon(QIcon(func.get_icon('Logo')))
        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.toolBarTD_checkBox = QCheckBox("Show TD toolbar")
        showTDToolbar = func.str2bool(self.settings.value("showTDToolbar", True))
        self.toolBarTD_checkBox.setChecked(showTDToolbar)
        self.toolBarTD_checkBox.stateChanged.connect(self.checkBoxTDstateChanged)

        self.toolBarComp_checkBox = QCheckBox("Show Comp toolbar")
        showCompToolbar = func.str2bool(self.settings.value("showCompToolbar", True))
        self.toolBarComp_checkBox.setChecked(showCompToolbar)
        self.toolBarComp_checkBox.stateChanged.connect(self.checkBoxCompstateChanged)

        self.toolBarArt_checkBox = QCheckBox("Show Art toolbar")
        showArtToolbar = func.str2bool(self.settings.value("showArtToolbar", True))
        self.toolBarArt_checkBox.setChecked(showArtToolbar)
        self.toolBarArt_checkBox.stateChanged.connect(self.checkBoxArtstateChanged)

        closeBtn = QPushButton('Close')
        closeBtn.clicked.connect(self.close)

        self.layout.addWidget(self.toolBarTD_checkBox, 0, 0, 1, 1)
        self.layout.addWidget(self.toolBarComp_checkBox, 1, 0, 1, 1)
        self.layout.addWidget(self.toolBarArt_checkBox, 2, 0, 1, 1)

        self.layout.addWidget(closeBtn, 4, 0, 1, 1)

    def checkBoxTDstateChanged(self):
        showTDToolbar = func.str2bool(self.toolBarTD_checkBox.checkState())
        self.settings.setValue("showTDToolbar", func.bool2str(showTDToolbar))
        self.checkboxTDSig.emit(self.toolBarTD_checkBox.isChecked())

    def checkBoxCompstateChanged(self):
        showCompToolbar = func.str2bool(self.toolBarComp_checkBox.checkState())
        self.settings.setValue("showCompToolbar", func.bool2str(showCompToolbar))
        self.checkboxCompSig.emit(self.toolBarComp_checkBox.isChecked())

    def checkBoxArtstateChanged(self):
        showArtToolbar = func.str2bool(self.toolBarArt_checkBox.checkState())
        self.settings.setValue("showArtToolbar", func.bool2str(showArtToolbar))
        self.checkboxCompSig.emit(self.toolBarArt_checkBox.isChecked())

def main():
    app = QApplication(sys.argv)
    pref_layout = Pref_layout()
    pref_layout.show()
    app.exec_()

if __name__=='__main__':
    main()

