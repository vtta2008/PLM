# -*- coding: utf-8 -*-
import os
import sys

from PyQt5.QtCore import QSettings, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QCheckBox, QPushButton, QVBoxLayout

from utilities import utils as func

SETTING_PATH = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'settings', 'plt_setting.ini')

class Pref_layout(QDialog):

    checkboxSig = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(Pref_layout, self).__init__(parent)

        self.resize(200, 100)
        self.setWindowTitle("Preferences")
        self.setWindowIcon(QIcon(func.get_icon('Logo')))
        self.settings = QSettings(SETTING_PATH, QSettings.IniFormat)

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
    app = QApplication
    pref_layout = Pref_layout()
    pref_layout.show()
    app.exec_()

if __name__=='__main__':
    main()

