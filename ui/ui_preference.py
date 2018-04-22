# -*- coding: utf-8 -*-
import os

from PyQt5.QtCore import QSettings, pyqtSignal
from PyQt5.QtWidgets import QDialog, QCheckBox, QPushButton, QVBoxLayout

from utilities import utils as func

SETTING_PATH = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'settings', 'PipelineTool_settings.ini')

class Preferences(QDialog):

    checkboxSig = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(Preferences, self).__init__(parent)

        self.resize(200, 100)
        self.setWindowTitle("Preferences")

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



