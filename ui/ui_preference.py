# -*- coding: utf-8 -*-
"""

Script Name: plt.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This script is master file of Pipeline Tool

"""

# -------------------------------------------------------------------------------------------------------------
""" About Plt """

__appname__ = "Pipeline Tool"
__module__ = "Plt"
__version__ = "13.0.1"
__organization__ = "DAMG team"
__website__ = "www.dot.damgteam.com"
__email__ = "dot@damgteam.com"
__author__ = "Trinh Do, a.k.a: Jimmy"
__root__ = "PLT_RT"
__db__ = "PLT_DB"
__st__ = "PLT_ST"

# -------------------------------------------------------------------------------------------------------------
import os
import sys

from PyQt5.QtCore import QSettings, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QCheckBox, QPushButton, QVBoxLayout

from utilities import utils as func
from utilities import variables as var


class Pref_layout(QDialog):

    checkboxSig = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(Pref_layout, self).__init__(parent)

        self.resize(200, 100)
        self.setWindowTitle("Preferences")
        self.setWindowIcon(QIcon(func.get_icon('Logo')))
        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

        self.checkBox = QCheckBox("Show main toolbar")
        showToolbar = func.str2bool(self.settings.value("showToolbar", True))
        self.checkBox.setChecked(showToolbar)

        closeBtn = QPushButton('Close')
        closeBtn.clicked.connect(self.close)
        self.checkBox.stateChanged.connect(self.checkBoxstateChanged)

        layout = QVBoxLayout()
        layout.addWidget(self.checkBox)
        layout.addWidget(closeBtn)
        self.setLayout(layout)

    def checkBoxstateChanged(self):
        showToolbar = func.str2bool(self.checkBox.checkState())
        self.settings.setValue("showToolbar", func.bool2str(showToolbar))
        self.checkboxSig.emit(self.checkBox.isChecked())

def main():
    app = QApplication(sys.argv)
    pref_layout = Pref_layout()
    pref_layout.show()
    app.exec_()

if __name__=='__main__':
    main()

