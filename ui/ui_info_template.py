#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Name: ui_info_template.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This is a layout which have info about pipeline tools

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
""" Import modules """

# Python
import sys

# PtQt5
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QGridLayout, QLabel, QPushButton

# Plt
from utilities import utils as func

class About_plt_layout(QDialog):
    def __init__(self, id='About', message=None, icon=func.get_icon('Logo'), parent=None):
        super(About_plt_layout, self).__init__(parent)

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
    about_layout = About_plt_layout()
    about_layout.show()
    sys.exit(app.exec_())