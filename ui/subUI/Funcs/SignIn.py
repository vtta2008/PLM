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

# PLM
from appData                import SIGNUP, PW_BLANK, USER_BLANK, PW_WRONG, __localServerAutho__
from ui.uikits.Widget       import Widget
from ui.uikits.Icon         import AppIcon
from ui.uikits.CheckBox     import CheckBox
from ui.uikits.Button       import Button
from ui.uikits.MessageBox   import MessageBox
from ui.uikits.Label        import Label, usernameLabel, passwordLabel
from ui.uikits.GridLayout   import GridLayout
from ui.uikits.LineEdit     import LineEdit
from ui.uikits.GroupBox     import GroupGrid
from utils                  import str2bool, RemoveDB, UpdateDB

# -------------------------------------------------------------------------------------------------------------
""" Sign In Layout """

class SignIn(Widget):

    key = 'SignIn'
    _login = False

    def __init__(self, parent=None):

        super(SignIn, self).__init__(parent)

        self.setWindowIcon(AppIcon(32, "SignIn"))
        self.setFixedSize(400, 300)
        self.setWindowTitle('Sign In')

        self.layout             = GridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        loginGrp, loginGrid     = GroupGrid('Sign in')

        self.userTF             = LineEdit()
        self.pwTF               = LineEdit({'fn': 'password'})
        self.userCB             = CheckBox('Remember me?')

        forgot_pw_btn           = Button({'txt': 'Forgot your password?', 'cl': partial(self.signals.emit, 'showLayout', 'ForgotPassword', 'show')})
        login_btn               = Button({'txt': 'Log in', 'cl': self.signInClicked})
        cancel_btn              = Button({'txt': 'Cancel', 'cl': sys.exit})

        signupGrp, signupGrid   = GroupGrid('Sign up')
        signupBtn               = Button({'txt':'Sign up', 'cl': partial(self.signals.emit, 'showLayout', 'SignUp', 'show')})

        loginGrid.addWidget(usernameLabel, 0, 0, 1, 2)
        loginGrid.addWidget(passwordLabel, 1, 0, 1, 2)
        loginGrid.addWidget(self.userTF, 0, 2, 1, 4)
        loginGrid.addWidget(self.pwTF, 1, 2, 1, 4)
        loginGrid.addWidget(self.userCB, 2, 1, 1, 2)
        loginGrid.addWidget(login_btn, 2, 3, 1, 3)
        loginGrid.addWidget(forgot_pw_btn, 3, 0, 1, 3)
        loginGrid.addWidget(cancel_btn, 3, 3, 1, 3)

        signupGrid.addWidget(Label({'txt': SIGNUP}), 0, 0, 1, 6)
        signupGrid.addWidget(signupBtn, 1, 0, 1, 6)

        self.layout.addWidget(loginGrp, 0, 0, 1, 1)
        self.layout.addWidget(signupGrp, 1, 0, 1, 1)

    def forgetPwClicked(self):
        if __name__ == '__main__':
            from ui.subUI.Funcs.ForgotPassword import ForgotPassword
            self.forgotPW = ForgotPassword()
            self.forgotPW.show()
        else:
            self.signals.showLayout('ForgotPassword', 'show')

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

            RemoveDB("curUser")
            UpdateDB("curUser", [username, token, cookie, str2bool(check)])
            self.signals.emit('loginChanged', True)
        else:
            RemoveDB("curUser")
            MessageBox(self, 'Login Failed', 'critical', PW_WRONG)
            return

    def loginChanged(self, login):
        self._login = login

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, newVal):
        self._login = newVal