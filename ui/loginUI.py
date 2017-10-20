# -*- coding: utf-8 -*-

"""
Script Name: loginUI.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is a login UI for user.

"""
# -------------------------------------------------------------------------------------------------------------
# IMPORT PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
import json, logging, os, subprocess, sys, webbrowser
from functools import partial
from tk import appFuncs as func
from tk import defaultVariable as var
from tk import getData, message

# -------------------------------------------------------------------------------------------------------------
# IMPORT PTQT5 ELEMENT TO MAKE UI
# -------------------------------------------------------------------------------------------------------------
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

# ------------------------------------------------------
# GET INFO DATA BEFORE START
# Update local pc info
getData.initialize()

# ------------------------------------------------------
# DEFAULT VARIABLES
# ------------------------------------------------------
MESSAGE = message.LOGIN_NOTE
TITLE = var.MAIN_ID['LogIn']
NAMES = var.MAIN_NAMES
MAINID = var.MAIN_ID
PACKAGE = var.MAIN_PACKPAGE

# UI variables preset for layout customizing
# Dimension
W = 400
H = 260
AVATAR_SIZE = 100
ICON_SIZE = 30
BUFFER = 3

# Margin
M = [0,5,5,5,5]

# Alignment attribute from PyQt5
__center__ = Qt.AlignCenter
__right__ = Qt.AlignRight
__left__ = Qt.AlignLeft

# Get icon path
pthInfo = PACKAGE['appData']
infoData = NAMES['info']
filePath = os.path.join(pthInfo, infoData)
info = func.dataHandle(filePath, 'r')

# Get app path
logger.info('Loading information...')
APPINFO = info['pipeline']
logger.info('Loading pipeline manager UI')

userDataPth = os.path.join(os.getenv(NAMES['key']), os.path.join('scrInfo', 'user.info'))

userData = func.dataHandle(userDataPth, 'r')

prodInfoFolder = os.path.join(os.getenv(NAMES['key']), os.path.join(NAMES['appdata'][1], 'prodInfo'))

prodContent = [f for f in os.listdir(prodInfoFolder) if f.endswith('.prod')]

prodLst = []

for f in prodContent:
    with open(os.path.join(prodInfoFolder, f), 'r') as f:
        info = json.load(f)
    prodLst.append(info['name'])

class LoginUI(QDialog):

    tempPth = os.path.join(os.getenv('PIPELINE_TOOL'), 'user.temp')
    appDataPth = os.path.join(os.getenv('PIPELINE_TOOL'), 'scrInfo/apps.pipeline')

    def __init__(self, parent=None):

        super(LoginUI, self).__init__()

        self.setWindowTitle(TITLE)
        self.setWindowIcon(QIcon(func.getIcon('Logo')))
        self.setFixedSize(W, H)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(M[1], M[2], M[3], M[4])

        self.checkTempUser()

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
        loginBtn.clicked.connect(self.checkLogin)

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

    def checkTempUser(self):
        if not os.path.exists(self.tempPth):

            logger.info('This is the first time user login')

            infoData = func.dataHandle(self.appDataPth, 'r')
            self.userUid = infoData['sys']['Product ID']
            self.userToken = func.createToken()

            self.buildUI()
        else:
            userLogin = func.dataHandle(self.tempPth, 'r')
            userName = [f for f in userLogin][0]

            if userLogin[userName][3] == 0:
                self.buildUI()
            else:
                pass

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Warning', "Are you sure?", QMessageBox.Yes|QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def checkLogin(self, *args):

        # Check if it is the first time of log in in local machine
        user_name = str(self.userName.text())
        pass_word = str(func.encoding(self.passWord.text()))

        print 'start here'

        # if user_name == "":
        #     logger.info('username blank')
        #
        #     QMessageBox.information(self, 'Login Failed', 'Username can not be blank')
        #
        # elif userData[user_name] != None and pass_word == userData[user_name][0]:
        #     QMessageBox.information(self, 'Login Successful', "Welcome back %s\n "
        #                                                       "Now it's the time to make amazing thing to the world !!!" % user_name)
        #     self.close()
        #     func.saveCurrentUserLogin(user_name, self.rememberCheckBox.checkState())
        # else:
        #     QMessageBox.information(self, 'Login Failed', 'Username or Password is incorrected')

def initialize():
    app = QApplication(sys.argv)
    loginUI = LoginUI()
    loginUI.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    initialize()