# -*- coding: utf-8 -*-
"""

Script Name: ui_sign_up.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    ui to log in

"""

# -------------------------------------------------------------------------------------------------------------
""" Import modules """
# -------------------------------------------------------------------------------------------------------------

import sys
import os
import logging
import qdarkgraystyle

# PyQt5 modules
from PyQt5.QtCore import QRegExp, QLocale, Qt
from PyQt5.QtGui import QIcon, QRegExpValidator, QFont, QTextLine, QPalette
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLineEdit,  QDialog, QPushButton, QLabel, QMessageBox,
                             QGroupBox, QComboBox, QCheckBox, QHBoxLayout)

__center__ = Qt.AlignCenter

# Setting logfing info
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

check_pth = os.getenv('PIPELINE_TOOL')

if check_pth is None:
    logging.warning("environment variable have not set yet.")

    SCR_PATH = os.getcwd().split('ui')[0]
    KEY = "PIPELINE_TOOL"

    # Set key, path into environment variable.
    logging.info("Set up environment variable")
    os.environ[KEY] = SCR_PATH

# import Pipeline tool modules
from utilities import variables as var
from utilities import utils as func
from utilities import utils_sql as ultis
from utilities import message as mess


def query_user_info():
    currentUserData = ultis.query_current_user()
    curUser = currentUserData[2]
    unix = currentUserData[0]
    token = currentUserData[1]
    rememberLogin = currentUserData[3]
    status = currentUserData[-1]
    ultis.check_sys_configuration(curUser)
    return unix, token, curUser, rememberLogin, status

# -------------------------------------------------------------------------------------------------------------
""" Login Layout """
# -------------------------------------------------------------------------------------------------------------
class Sign_in(QDialog):

    unix, token, curUser, rememberLogin, status = query_user_info()

    def __init__(self, parent=None):

        super(Sign_in, self).__init__(parent)

        self.setWindowTitle('Sign in')
        self.setWindowIcon(QIcon(func.getIcon('Logo')))
        self.setContentsMargins(0,0,0,0)

        self.layout = QGridLayout()

        self.buildUI()

        self.setLayout(self.layout)

    def buildUI(self):

        login_groupBox = QGroupBox()
        login_groupBox.setTitle('Sign in')
        login_grid = QGridLayout()
        login_groupBox.setLayout(login_grid)

        self.usernameField = QLineEdit(self.curUser)
        self.passwordField = QLineEdit()
        self.rememberCheckBox = QCheckBox('Remember me.')
        self.passwordField.setEchoMode(QLineEdit.Password)

        login_btn = QPushButton('Login')
        cancel_btn = QPushButton('Cancel')
        sign_up_btn = QPushButton('Sign up')

        login_btn.clicked.connect(self.on_sign_in_but_clicked)
        cancel_btn.clicked.connect(self.on_cancel_btn_clicked)
        sign_up_btn.clicked.connect(self.on_sign_up_btn_clicked)

        login_grid.addWidget(self.clabel('Username'), 1, 0, 1, 2)
        login_grid.addWidget(self.clabel('Password'), 2, 0, 1, 2)
        login_grid.addWidget(self.usernameField, 1, 2, 1, 4)
        login_grid.addWidget(self.passwordField, 2, 2, 1, 4)

        login_grid.addWidget(self.rememberCheckBox, 3, 3, 1, 2)

        login_grid.addWidget(login_btn, 4, 0, 1, 3)
        login_grid.addWidget(cancel_btn, 4, 3, 1, 3)

        login_grid.addWidget(self.clabel(mess.SIGN_UP), 5, 0, 1, 3)
        login_grid.addWidget(sign_up_btn, 5, 3, 1, 3)

        self.layout.addWidget(login_groupBox, 0, 0, 1, 1)

    def clabel(self, text):
        label = QLabel(text)
        label.setAlignment(var.__center__)
        label.setMinimumWidth(50)
        return label

    def on_sign_up_btn_clicked(self):
        from ui import ui_sign_up
        reload(ui_sign_up)
        signup = ui_sign_up.main()
        signup.exec_()

    def on_cancel_btn_clicked(self):
        self.close()

    def on_sign_in_but_clicked(self):
        username = self.usernameField.text()
        password = self.passwordField.text()

        if username == "" or username is None:
            QMessageBox.critical(self, 'Login Failed', mess.USERNAME_BLANK)
            return
        elif password == "" or password is None:
            QMessageBox.critical(self, 'Login Failed', mess.PASSWORD_BLANK)
            return

        # Check username exists
        checkUserExists = ultis.check_data_exists(username)

        if not checkUserExists:
            QMessageBox.critical(self, 'Login Failed', "Username not exists")
            return

        # Check status of username
        checkUserStatus = ultis.query_user_status(username)

        if checkUserStatus == 'disabled':
            QMessageBox.critical(self, 'Login Failed', mess.USER_BLOCK)
            return

        # Check password correct
        password = str(func.encoding(password))
        checkPasswordMatch = ultis.check_password_match(username, password)

        if not checkPasswordMatch:
            QMessageBox.critical(self, 'Login Failed', "Password not match")
            return
        else:
            QMessageBox.information(self, 'Login Successful', "Welcome %s" % username)
            checkSettingState = self.rememberCheckBox.checkState()
            if checkSettingState:
                setting = 'True'
            else:
                setting = 'False'

            user_profile = ultis.query_user_profile(username)
            token = user_profile[1]
            unix = user_profile[0]

            ultis.update_user_remember_login(token, setting)
            ultis.update_current_user(unix, token, username, setting)

            self.hide()
            window = main.Main()
            window.show()

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkgraystyle.load_stylesheet_pyqt5())
    window = Sign_in()
    window.setFixedSize(360, 240)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()