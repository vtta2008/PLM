# -*- coding: utf-8 -*-
"""
Script Name: ui_about.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is main file to store everything for the pipeline app

"""

# -------------------------------------------------------------------------------------------------------------
# IMPORT PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
import logging
import sys

from PyQt5.QtGui import *
# ------------------------------------------------------
# IMPORT PTQT5 ELEMENT TO MAKE UI
# ------------------------------------------------------
from PyQt5.QtWidgets import *

# ------------------------------------------------------
# IMPORT FROM PIPELINE TOOLS APP
# ------------------------------------------------------
from util import utilities as func

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

class WindowDialog(QDialog):
    def __init__(self, id='About', message=None, icon=func.getIcon('Logo'), parent=None):
        super(WindowDialog, self).__init__(parent)

        self.setWindowTitle(id)
        self.setWindowIcon(QIcon(icon))
        central_widget = QWidget(self)
        self.layout = QGridLayout(self)
        central_widget.setLayout(self.layout)
        self.buildUI(message)

    def buildUI(self, message):
        self.layout.addWidget(QLabel(message),0,0)

        yesBtn = QPushButton('OK')
        yesBtn.clicked.connect(self.close)
        self.layout.addWidget(yesBtn,1,1,1,2)

        self.setLayout(self.layout)

if __name__=='__main__':
    app = QApplication(sys.argv)
    window = WindowDialog()
    window.show()
    sys.exit(app.exec_())