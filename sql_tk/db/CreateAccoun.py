# -*- coding: utf-8 -*-
"""
Script Name: desktopUI.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is main file to store everything for the pipeline app

"""

# -------------------------------------------------------------------------------------------------------------
# IMPORT PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
import logging
import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
# ------------------------------------------------------
# IMPORT PTQT5 ELEMENT TO MAKE UI
# ------------------------------------------------------
from PyQt5.QtWidgets import *

# ------------------------------------------------------
# IMPORT FROM PIPELINE TOOLS APP
# ------------------------------------------------------
from tk import appFuncs as func
from tk import message as mes

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

# ------------------------------------------------------
# GET INFO DATA BEFORE START
# Update local pc info
# getData.initialize()

# logger.info('Updating data')

# ------------------------------------------------------
# DEFAULT VARIABLES
# ------------------------------------------------------
# UI variables preset for layout customizing
# Dimension
W = 350
H = 260
AVATAR_SIZE = 100
ICON_SIZE = 30
BUFFER = 3

# Margin
M1 = [0, 5, 5, 5, 5]

# Base unit of position to be using in QGridlayout
X = 0
Y = 0
XW = 1
XH = 1
GRID_TOTAL = 9

# Alignment attribute from PyQt5
__center__ = Qt.AlignCenter
__right__ = Qt.AlignRight
__left__ = Qt.AlignLeft
frameStyle = QFrame.Sunken | QFrame.Panel

# Get icon path
# pthInfo = PACKAGE['appData']
# infoData = NAMES['info']

# getData.initialize()
#
# filePath = os.path.join(os.getenv('PIPELINE_TOOL'), 'sql_tk\db\main.config.yml')
#
# with open(filePath, 'r') as f:
#     APPINFO = yaml.load(f)

class Button(QToolButton):

    def __init__(self, text, parent=None):
        super(Button, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 5)
        size.setWidth(max(size.width(), size.height()))
        return size

# ----------------------------------------------------------------------------------------------------------- #
"""                                       SUB CLASS: REGISTER UI                                            """
# ----------------------------------------------------------------------------------------------------------- #
class NewAccount(QDialog):
    TITLEBLANK = 'If title is blank, it will be considered as a "Tester"'

    def __init__(self, parent=None):
        super(NewAccount, self).__init__(parent)
        self.setWindowTitle("Create New Account")
        self.setWindowIcon(QIcon(func.getIcon('Logo')))
        self.layout = QGridLayout()
        # self.layout.setColumnStretch(1, 1)
        # self.layout.setColumnMinimumWidth(1, 250)
        self.firstnameField = QLineEdit()
        self.lastnameField = QLineEdit()
        self.regisTitle = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.passwordRetype = QLineEdit()
        self.passwordRetype.setEchoMode(QLineEdit.Password)
        self.buildUI()

    def buildUI(self):

        self.layout.addWidget(self.clabel('Register!'), 0, 0, 1, 4)
        self.layout.addWidget(self.clabel('Title(modeler, artist, etc.)'), 1, 0, 1, 1)
        self.layout.addWidget(self.clabel('First Name'), 2, 0, 1, 1)
        self.layout.addWidget(self.clabel('Last Name'), 3, 0, 1, 1)
        self.layout.addWidget(self.clabel(self.TITLEBLANK), 4, 0, 1, 4)
        self.layout.addWidget(self.clabel('Password'), 5, 0, 1, 1)
        self.layout.addWidget(self.clabel('Re-type password'), 6, 0, 1, 1)
        self.layout.addWidget(self.regisTitle, 1, 1, 1, 3)
        self.layout.addWidget(self.firstnameField, 2, 1, 1, 3)
        self.layout.addWidget(self.lastnameField, 3, 1, 1, 3)
        self.layout.addWidget(self.password, 5, 1, 1, 3)
        self.layout.addWidget(self.passwordRetype, 6, 1, 1, 3)
        self.layout.addWidget(self.clabel(''), 7, 0, 1, 4)
        okBtn = QPushButton('Ok')
        okBtn.clicked.connect(self.setOKclciked)
        cancelBtn = QPushButton('Cancel')
        cancelBtn.clicked.connect(self.cancelClicked)

        self.layout.addWidget(okBtn, 8, 0, 1, 2)
        self.layout.addWidget(cancelBtn, 8, 2, 1, 2)
        self.setLayout(self.layout)

    def clabel(self, text):
        label = QLabel(text)
        label.setAlignment(__center__)
        label.setMinimumWidth(50)
        return label

    def cancelClicked(self):

        login = LoginUI()
        login.show()
        self.hide()


    def setOKclciked(self):
        title = self.regisTitle.text()
        firstname = self.firstnameField.text()
        lastname = self.lastnameField.text()
        password = self.password.text()
        passretype = self.passwordRetype.text()
        check = self.checkMatchPassWord(firstname, lastname, title, password, passretype)
        if not check:
            pass
        else:
            SUCCESS = "%s.%s" % (lastname, firstname)
            self.processNewAcountData(lastname, firstname, title, password)
            QMessageBox.information(self, "Error", SUCCESS, QMessageBox.Retry)
            self.hide()
            login = LoginUI()
            login.show()

    def checkMatchPassWord(self, firstname, lastname, title, password, passretype):
        NOTMATCH = "Password doesn't match"
        FIRSTNAME = "Firstname cannot be blank"
        LASTNAME = "Lastname cannot be blank"
        if title == "":
            title = 'Tester'
        if firstname == "":
            QMessageBox.critical(self, "Error", FIRSTNAME, QMessageBox.Retry)
            return False
        else:
            pass
        if lastname == "":
            QMessageBox.critical(self, "Error", LASTNAME, QMessageBox.Retry)
            return False
        else:
            pass
        if not password == passretype:
            QMessageBox.critical(self, "Password not matches", NOTMATCH, QMessageBox.Retry)
            return False
        else:
            return True

    def processNewAcountData(self, lastname, firstname, title, password):
        from sql_tk.db import ultilitis_user
        reload(ultilitis_user)
        ultilitis_user.CreateNewUser(lastname, firstname, title, password)

# ----------------------------------------------------------------------------------------------------------- #
"""                                       SUB CLASS: USER LOGIN UI                                          """
# ----------------------------------------------------------------------------------------------------------- #
class LoginUI(QDialog):
    appDataPth = os.path.join(os.getenv('PIPELINE_TOOL'), 'sql_tk/db/main.config')

    def __init__(self, parent=None):

        super(LoginUI, self).__init__()

        self.setWindowTitle('Log in')
        self.setWindowIcon(QIcon(func.getIcon('Logo')))
        self.prevUserLogin = os.path.join(os.getenv('PIPELINE_TOOL'), 'sql_tk/db/user.config')
        self.buildUI()

    def buildUI(self):

        self.mainFrame = QGroupBox(self)
        self.mainFrame.setTitle('User Account')
        self.mainFrame.setFixedSize(W, H)
        hboxLogin = QHBoxLayout()
        self.layout = QGridLayout()
        self.layout.setContentsMargins(5, 5, 5, 5)
        loginText = QLabel('User Name: ')
        loginText.setAlignment(__center__)
        self.layout.addWidget(loginText, 0, 0, 1, 2)
        self.userName = QLineEdit()
        self.layout.addWidget(self.userName, 0, 2, 1, 7)
        passText = QLabel('Password: ')
        passText.setAlignment(__center__)
        self.layout.addWidget(passText, 1, 0, 1, 2)
        self.passWord = QLineEdit()
        self.passWord.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.passWord, 1, 2, 1, 7)
        rememberCheck = QLabel('Remember Me')
        rememberCheck.setAlignment(__center__)
        self.layout.addWidget(rememberCheck, 2, 0, 1, 2)
        self.rememberCheckBox = QCheckBox()
        self.layout.addWidget(self.rememberCheckBox, 2, 2, 1, 1)
        self.loginBtn = QPushButton('Login')
        self.loginBtn.clicked.connect(self.Login_btn)
        self.layout.addWidget(self.loginBtn, 2, 3, 1, 3)
        self.cancelBtn = QPushButton('Cancel')
        self.cancelBtn.clicked.connect(self.Cancel_btn)
        self.layout.addWidget(self.cancelBtn, 2, 6, 1, 3)
        noteLabel = QLabel(mes.LOGIN_NOTE)
        self.layout.addWidget(noteLabel, 3, 0, 1, 3)
        createAccount = QPushButton('Create Account')
        createAccount.clicked.connect(self.createAccUI)
        self.layout.addWidget(createAccount, 3,3,1,6)

        hboxLogin.addLayout(self.layout)
        self.mainFrame.setLayout(hboxLogin)

    def createAccUI(self):
        createAcc = NewAccount()
        createAcc.exec_()

    def Cancel_btn(self):
        self.close()

    def Login_btn(self, *args):
        user_name = str(self.userName.text())
        pass_word = str(func.encoding(self.passWord.text()))

        if user_name == "":
            QMessageBox.information(self, 'Login Failed', 'Username can not be blank')
        elif pass_word == "":
            QMessageBox.information(self, 'Login Failed', 'No password')
        else:
            self.AttemptLogin(user_name, pass_word)

    def AttemptLogin(self, username, password):
        userData = func.checkUserLogin(username)
        userLogin = {}
        if userData == {}:
            QMessageBox.information(self, 'Login Failed', "Username not exists")
            return
        else:
            if not password == userData[username][7]:
                QMessageBox.information(self, 'Login Failed', "Wrong password")
                return
            else:
                QMessageBox.information(self, 'Login Successful', "Welcome %s" % username)
                userLogin['remember login'] = self.rememberCheckBox.checkState()
                userLogin['username'] = username
                userLogin['group'] = userData[username][8]
                userLogin['avatar'] = userData[username][9]
                userLogin['aka'] = userData[username][6]
                userLogin['title'] = userData[username][5]
                userLogin['fullname'] = userData[username][4]
                func.saveCurrentUserLogin(userLogin)
                self.hide()
                window = DesktopUI()
                window.show()

def initialize():
    app = QApplication(sys.argv)
    login = LoginUI()
    login.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    initialize()
