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
import sys, requests
from functools              import partial

# PyQt5
from PyQt5.QtCore           import pyqtSignal
from PyQt5.QtWidgets        import (QApplication, QGridLayout, QCheckBox, QWidget)

from appData                import SIGNUP, PW_BLANK, USER_BLANK, PW_WRONG, __localServerCheck__, __localServerAutho__, __localServer__
from ui.UiSignals           import UiSignals
from ui.MessageBox          import MessageBox
from ui.uikits.Button       import Button
from ui.uikits.GroupBox     import GroupGrid
from ui.uikits.UiPreset     import IconPth, Label, LineEdit

# Plt
from utils                  import localSQL as usql
from utils.utils            import str2bool

# -------------------------------------------------------------------------------------------------------------
""" Sign In Layout """

class SignIn(QWidget):

    key = 'login'

    def __init__(self, parent=None):

        super(SignIn, self).__init__(parent)

        self.setWindowIcon(IconPth(32, "SignIn"))
        self.setFixedSize(400, 300)
        self.signals = UiSignals(self)

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        loginGrp, loginGrid = GroupGrid('Sign in')

        self.userTF = LineEdit()
        self.pwTF = LineEdit({'fn': 'password'})
        self.userCB = QCheckBox('Remember me?')

        forgot_pw_btn = Button({'txt': 'Forgot your password?', 'cl': partial(self.signals.showLayout.emit, 'forgotpw', 'show')})
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
        signupBtn = Button({'txt':'Sign up', 'emit2': [self.signals.showLayout.emit, ['signup', 'show']]})

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
            MessageBox(self, 'Login Failed', 'critical', USER_BLANK)
            return
        elif pass_word == "" or pass_word is None:
            MessageBox(self, 'Login Failed', 'critical', PW_BLANK)
            return

        password = str(pass_word)

        r = requests.post(__localServerAutho__, verify=False, data={'user': username, 'pwd': password})

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

            self.showLayout.emit('mainUI', 'show')
        else:
            usql.RemoveDB("curUser")
            MessageBox(self, 'Login Failed', 'critical', PW_WRONG)
            return

    def showEvent(self, event):
        # self.specs.showState.emit(True)
        self.showLayout.emit('mainUI', 'hide')
        self.showLayout.emit('sysTray', 'hide')

    def hideEvent(self, event):
        # self.specs.showState.emit(False)
        pass

    def closeEvent(self, event):
        self.showLayout.emit(self.key, 'hide')
        event.ignore()


if __name__ == '__main__':
    login = QApplication(sys.argv)
    layout = SignIn()
    layout.show()
    login.exec_()