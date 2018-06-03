#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: SignIn.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

    Sign In layout.

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys
import requests

# PyQt5
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QApplication, QDialog, QGridLayout, QLineEdit, QPushButton, QMessageBox, QGroupBox,
                             QCheckBox, )

# Plt
from utilities import localSQL as usql
import appData as app
from ui import uirc as rc
from utilities import utils as func

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logger = app.set_log()

# -------------------------------------------------------------------------------------------------------------
""" Sign In Layout """

class SignIn(QDialog):

    showSignup = pyqtSignal(bool)
    showPlt = pyqtSignal(bool)

    def __init__(self, parent=None):

        super(SignIn, self).__init__(parent)

        self.setWindowTitle('Sign in')
        self.setWindowIcon(rc.IconPth(32, "SignIn"))
        self.setFixedSize(400, 300)
        self.settings = app.APPSETTING

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        loginGrp = QGroupBox('Sign in')
        loginGrid = QGridLayout()
        loginGrp.setLayout(loginGrid)

        self.userTF = QLineEdit()
        self.pwTF = QLineEdit()
        self.pwTF.setEchoMode(QLineEdit.Password)

        self.userCB = QCheckBox('Remember me.')

        forgot_pw_btn = QPushButton('Forgot your password?')
        forgot_pw_btn.clicked.connect(self.on_forgot_pw_btn_clicked)
        login_btn = QPushButton('Login')
        cancel_btn = QPushButton('Cancel')
        login_btn.clicked.connect(self.on_sign_in_btn_clicked)
        cancel_btn.clicked.connect(QApplication.quit)

        loginGrid.addWidget(rc.Label('Username'), 0, 0, 1, 2)
        loginGrid.addWidget(rc.Label('Password'), 1, 0, 1, 2)
        loginGrid.addWidget(self.userTF, 0, 2, 1, 4)
        loginGrid.addWidget(self.pwTF, 1, 2, 1, 4)
        loginGrid.addWidget(self.userCB, 2, 1, 1, 2)
        loginGrid.addWidget(login_btn, 2, 3, 1, 3)
        loginGrid.addWidget(forgot_pw_btn, 3, 0, 1, 3)
        loginGrid.addWidget(cancel_btn, 3, 3, 1, 3)

        signupGrp = QGroupBox('Sign up')
        signupGrid = QGridLayout()
        signupGrp.setLayout(signupGrid)

        signupBtn = QPushButton('Sign up')
        signupBtn.clicked.connect(self.on_sign_up_btn_clicked)

        signupGrid.addWidget(rc.Label(txt=app.SIGNUP), 0, 0, 1, 6)
        signupGrid.addWidget(signupBtn, 1, 0, 1, 6)

        self.layout.addWidget(loginGrp, 0, 0, 1, 1)
        self.layout.addWidget(signupGrp, 1, 0, 1, 1)

    def on_forgot_pw_btn_clicked(self):
        from ui import ForgotPassword
        app.reload(ForgotPassword)
        forgetPW = ForgotPassword.ForgotPassword()
        forgetPW.show()
        forgetPW.exec_()

    def on_sign_up_btn_clicked(self):
        self.showLogin.emit(False)
        self.show_hide_sign_up(True)

    def on_sign_in_btn_clicked(self):
        username = str(self.userTF.text())
        pass_word = str(self.pwTF.text())

        if username == "" or username is None:
            QMessageBox.critical(self, 'Login Failed', app.USERBLANK)
            return
        elif pass_word == "" or pass_word is None:
            QMessageBox.critical(self, 'Login Failed', app.PWBLANK)
            return

        password = str(pass_word)

        r = requests.post(app.__serverAutho__, verify=False, data={'user': username, 'pwd': password})

        if r.status_code == 200:
            for i in r.headers['set-cookie'].split(";"):
                if 'connect.sid=' in i:
                    cookie = i.split('connect.sid=')[-1]
                    break
                else:
                    cookie="No value"
                    continue

            token = r.json()['token']
            check = self.userCB.checkState()
            usql.RemoveDB("curUser")
            usql.UpdateDB("curUser", [username, token, cookie, func.str2bool(check)])

            self.showPlt.emit(True)
        else:
            usql.RemoveDB("curUser")
            QMessageBox.critical(self, 'Login Failed', app.PWWRONG)
            return

    def closeEvent(self, event):
        QApplication.quit()


def main():
    login = QApplication(sys.argv)
    layout = SignIn()
    layout.show()
    login.exec_()


if __name__ == '__main__':
    main()