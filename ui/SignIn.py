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
import os
import sys
import requests
import logging

# PyQt5
from PyQt5.QtCore import QSettings, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QDialog, QGridLayout, QLineEdit, QPushButton, QMessageBox, QGroupBox,
                             QCheckBox, )

# Plt
import appData as app

from utilities import utils as func
from utilities import variables as var
from utilities import message as mess
from utilities import sql_local as usql

from ui import uirc as rc

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain logs """

logPth = os.path.join(app.LOGPTH)
handler = logging.FileHandler(logPth)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------------------
""" Sign In Layout """

class SignIn(QDialog):

    showMainSig = pyqtSignal(bool)
    showSignUpSig = pyqtSignal(bool)

    def __init__(self, parent=None):

        super(SignIn, self).__init__(parent)

        # Sign in layout preset
        self.setWindowTitle('Sign in')
        self.setWindowIcon(QIcon(func.get_icon('Logo')))
        self.setFixedSize(400, 300)
        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)
        self.show_hide_main(False)

        # Main layout
        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        login_groupBox = QGroupBox('Sign in')
        login_grid = QGridLayout()
        login_groupBox.setLayout(login_grid)

        self.usernameField = QLineEdit()
        self.passwordField = QLineEdit()
        self.rememberCheckBox = QCheckBox('Remember me.')
        self.passwordField.setEchoMode(QLineEdit.Password)

        forgot_pw_btn = QPushButton('Forgot your password?')
        forgot_pw_btn.clicked.connect(self.on_forgot_pw_btn_clicked)
        login_btn = QPushButton('Login')
        cancel_btn = QPushButton('Cancel')
        login_btn.clicked.connect(self.on_sign_in_btn_clicked)
        cancel_btn.clicked.connect(QApplication.quit)

        login_grid.addWidget(rc.Label(txt='Username'), 0, 0, 1, 2)
        login_grid.addWidget(rc.Label(txt='Password'), 1, 0, 1, 2)
        login_grid.addWidget(self.usernameField, 0, 2, 1, 4)
        login_grid.addWidget(self.passwordField, 1, 2, 1, 4)
        login_grid.addWidget(self.rememberCheckBox, 2, 1, 1, 2)
        login_grid.addWidget(login_btn, 2, 3, 1, 3)
        login_grid.addWidget(forgot_pw_btn, 3, 0, 1, 3)
        login_grid.addWidget(cancel_btn, 3, 3, 1, 3)

        signup_groupBox = QGroupBox('Sign up')
        signup_grid = QGridLayout()
        signup_groupBox.setLayout(signup_grid)

        sign_up_btn = QPushButton('Sign up')
        sign_up_btn.clicked.connect(self.on_sign_up_btn_clicked)

        signup_grid.addWidget(rc.Label(txt=mess.SIGN_UP), 0, 0, 1, 6)
        signup_grid.addWidget(sign_up_btn, 1, 0, 1, 6)

        self.layout.addWidget(login_groupBox, 0, 0, 1, 1)
        self.layout.addWidget(signup_groupBox, 1, 0, 1, 1)

    def on_forgot_pw_btn_clicked(self):
        from ui import ForgotPassword
        reset_pw_form = ForgotPassword.ForgotPassword()
        reset_pw_form.show()
        reset_pw_form.exec_()

    def on_sign_up_btn_clicked(self):
        self.hide()
        self.show_hihe_signup(True)

    def on_sign_in_btn_clicked(self):

        username = str(self.usernameField.text())
        pass_word = str(self.passwordField.text())

        if username == "" or username is None:
            QMessageBox.critical(self, 'Login Failed', mess.USER_BLANK)
            return
        elif pass_word == "" or pass_word is None:
            QMessageBox.critical(self, 'Login Failed', mess.PW_BLANK)
            return

        password = str(pass_word)

        r = requests.post("https://pipeline.damgteam.com/auth", verify=False,
                          data={'user': username, 'pwd': password})

        if r.status_code == 200:
            for i in r.headers['set-cookie'].split(";"):
                if 'connect.sid=' in i:
                    cookie = i.split('connect.sid=')[-1]

            token = r.json()['token']
            if func.str2bool(self.rememberCheckBox.checkState()):
                usql.update_user_token(username, token, cookie)
            else:
                usql.remove_data_table('userTokenLogin')

            self.hide()
            self.show_hide_main(True)
        else:
            QMessageBox.critical(self, 'Login Failed', mess.PW_WRONG)
            return

    def show_hide_main(self, mode):
        self.settings.setValue("showMain", mode)
        self.showMainSig.emit(mode)

    def show_hihe_signup(self, mode):
        self.settings.setValue("showSignUp", mode)
        self.showSignUpSig.emit(mode)

    def closeEvent(self, event):
        QApplication.quit()


def main():
    app = QApplication(sys.argv)
    layout = SignIn()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()