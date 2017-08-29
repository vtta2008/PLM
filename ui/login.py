# -*- coding: utf-8 -*-

"""
Script Name: login.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is a login UI for user.

"""
# -------------------------------------------------------------------------------------------------------------
# IMPORT PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
import logging

from PyQt5.QtCore import *
from PyQt5.QtGui import *
# -------------------------------------------------------------------------------------------------------------
# IMPORT PTQT5 ELEMENT TO MAKE UI
# -------------------------------------------------------------------------------------------------------------
from PyQt5.QtWidgets import *

from tk import appFuncs as func
from tk import defaultVariable as var
from tk import message

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

# ------------------------------------------------------
# GET INFO DATA BEFORE START
# Update local pc info

func.updateInfo()
# logger.info('Updating data')

# ------------------------------------------------------
# DEFAULT VARIABLES
# ------------------------------------------------------
MESSAGE = message.LOGIN_NOTE
TITLE = var.MAIN_ID['LogIn']

# UI variables preset for layout customizing
# Dimension
W = 400
H = 260

# Margin
M = [0,5,5,5,5]

class Login(QDialog):

    def __init__(self, parent=None):

        super(Login, self).__init__()

        self.setWindowTitle(TITLE)
        self.setWindowIcon(QIcon(func.getIcon('Logo')))
        self.setFixedSize(W, H)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(M[1], M[2], M[3], M[4])

        self.buildUI()

    def buildUI(self):

        # Login Details section
        self.widgetLogin = QGroupBox()
        self.widgetLogin.setTitle('Login Details')
        self.widgetLogin.setContentsMargins(M[1], M[2], M[3], M[4])

        hboxLogin = QHBoxLayout()
        loginLayout = QGridLayout()

        # User name text field
        self.userTf = QLineEdit()

        # Password text field
        self.pwdTf = QLineEdit()
        self.pwdTf.setEchoMode(QLineEdit.Password)

        # Username and password label
        userLabel = QLabel('User Name')
        userLabel.setAlignment(Qt.AlignCenter)
        pwdLabel = QLabel('Password')
        pwdLabel.setAlignment(Qt.AlignCenter)

        # Login and close buttons
        loginBtn = QPushButton('Login')

        closeBtn = QPushButton('Close')
        closeBtn.clicked.connect(self.closeEvent)

        # Check box remember setting login for next time
        self.rememberCb = QCheckBox('Remeber Me')

        # Add content to grid layout
        loginLayout.addWidget(userLabel, 0,0,1,1)
        loginLayout.addWidget(self.userTf, 0,1,1,2)
        loginLayout.addWidget(pwdLabel, 1,0,1,1)
        loginLayout.addWidget(self.pwdTf, 1,1,1,2)
        loginLayout.addWidget(self.rememberCb, 2,0,1,1)
        loginLayout.addWidget(loginBtn, 2,1,1,1)
        loginLayout.addWidget(closeBtn, 2,2,1,1)

        # Add grid layout into group box layout
        hboxLogin.addLayout(loginLayout)
        self.widgetLogin.setLayout(hboxLogin)

        # Add layout to main
        self.layout.addWidget(self.widgetLogin)

        # Important Note
        self.widgetNote = QGroupBox()
        self.widgetNote.setTitle('Important Note')
        self.widgetNote.setContentsMargins(M[1], M[2], M[3], M[4])

        hboxNote = QHBoxLayout()
        noteLayout = QGridLayout()

        noteLabel = QLabel(MESSAGE)
        noteLabel.setAlignment(Qt.AlignLeft)

        noteLayout.addWidget(noteLabel, 0,0,1,3)

        # Add grid layout into group box layout
        hboxNote.addLayout(noteLayout)
        self.widgetNote.setLayout(hboxNote)

        # Add layout to main
        self.layout.addWidget(self.widgetNote)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Warning', "Are you sure?", QMessageBox.Yes|QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def LoginCheck(self):
        # Check if it is the first time of log in in local machine
        pass


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = Login()
    ui.show()
    sys.exit(app.exec_())

