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
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (QApplication, QGridLayout, QMessageBox, QCheckBox, QWidget)

# Plt
from utilities import localSQL as usql
from appData import SIGNUP, PW_BLANK, USER_BLANK, PW_WRONG, __serverAutho__
from ui.uikits.UiPreset import IconPth, Label, LineEdit
from ui.uikits.GroupBox import GroupGrid
from ui.uikits.Button import Button
from utilities.utils import str2bool
from core.Specs import Specs

# -------------------------------------------------------------------------------------------------------------
""" Sign In Layout """

class SignIn(QWidget):

    key = 'login'
    showLayout = pyqtSignal(str, str)
    setSetting = pyqtSignal(str, str)

    def __init__(self, parent=None):

        super(SignIn, self).__init__(parent)

        self.specs = Specs(self.key, self)
        self.setWindowIcon(IconPth(32, "SignIn"))
        self.setFixedSize(400, 250)

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        loginGrp, loginGrid = GroupGrid('Sign in')

        self.userTF = LineEdit()
        self.pwTF = LineEdit({'fm': 'password'})
        self.userCB = QCheckBox('Remember me?')

        forgot_pw_btn = Button({'txt': 'Forgot your password?', 'cl': self.forgetPwClicked})
        login_btn = Button({'txt': 'Log in', 'cl': self.signInClicked})
        cancel_btn = Button({'txt': 'Cancel', 'cl': QApplication.quit})

        loginGrid.addWidget(Label({'txt': 'Username'}), 0, 0, 1, 2)
        loginGrid.addWidget(Label({'txt': 'Password'}), 1, 0, 1, 2)
        loginGrid.addWidget(self.userTF, 0, 2, 1, 4)
        loginGrid.addWidget(self.pwTF, 1, 2, 1, 4)
        loginGrid.addWidget(self.userCB, 2, 1, 1, 2)
        loginGrid.addWidget(login_btn, 2, 3, 1, 3)
        loginGrid.addWidget(forgot_pw_btn, 3, 0, 1, 3)
        loginGrid.addWidget(cancel_btn, 3, 3, 1, 3)

        signupGrp, signupGrid = GroupGrid('Sign up')
        signupBtn = Button({'txt':'Sign up', 'emit2': [self.showLayout.emit, ['signup', 'show']]})

        signupGrid.addWidget(Label({'txt': SIGNUP}), 0, 0, 1, 6)
        signupGrid.addWidget(signupBtn, 1, 0, 1, 6)

        self.layout.addWidget(loginGrp, 0, 0, 1, 1)
        self.layout.addWidget(signupGrp, 1, 0, 1, 1)

    def forgetPwClicked(self):
        from ui.Funcs import ForgotPassword
        forgetPW = ForgotPassword.ForgotPassword()
        forgetPW.show()

    def signInClicked(self):
        username = str(self.userTF.text())
        pass_word = str(self.pwTF.text())

        if username == "" or username is None:
            QMessageBox.critical(self, 'Login Failed', USER_BLANK)
            return
        elif pass_word == "" or pass_word is None:
            QMessageBox.critical(self, 'Login Failed', PW_BLANK)
            return

        password = str(pass_word)

        r = requests.post(__serverAutho__, verify=False, data={'user': username, 'pwd': password})

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
            usql.UpdateDB("curUser", [username, token, cookie, str2bool(check)])
            print('show main ui')
            self.showLayout.emit('mainUI', 'show')
            # self.hide()
        else:
            usql.RemoveDB("curUser")
            QMessageBox.critical(self, 'Login Failed', PW_WRONG)
            return

    def showEvent(self, event):
        self.specs.showState.emit(True)
        self.showLayout.emit('mainUI', 'hide')
        self.showLayout.emit('sysTray', 'hide')

    def hideEvent(self, event):
        self.specs.showState.emit(False)

    def closeEvent(self, event):
        self.showLayout.emit(self.key, 'hide')
        event.ignore()


def main():
    login = QApplication(sys.argv)
    layout = SignIn()
    layout.show()
    login.exec_()


if __name__ == '__main__':
    main()