# -*- coding: utf-8 -*-
"""

Script Name: ui_create_account.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    ui to sign in new account

"""

# -------------------------------------------------------------------------------------------------------------
""" Import modules """
# -------------------------------------------------------------------------------------------------------------

import sys
import os
import logging
import qdarkgraystyle

# PyQt5 modules
from PyQt5.QtCore import QRegExp, QLocale
from PyQt5.QtGui import QIcon, QRegExpValidator
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLineEdit,  QDialog, QPushButton, QLabel, QMessageBox,
                             QGroupBox, QComboBox)


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
from util import variables as var
from util import utilities as func
from util import util_sql as ultis

# ----------------------------------------------------------------------------------------------------------- #
""" Sign in ui """
# ----------------------------------------------------------------------------------------------------------- #
class Sign_in(QDialog):

    def __init__(self, parent=None):

        super(Sign_in, self).__init__(parent)

        self.setWindowTitle("Sign In")
        self.setWindowIcon(QIcon(func.getIcon('Logo')))

        self.layout = QGridLayout()

        self.buildUI()

        self.setLayout(self.layout)
        self.setFixedSize(800, 300)

    def buildUI(self):

        account_section = self.account_section()
        self.layout.addWidget(account_section, 1,0,1,1)

        profile_section = self.profile_section()
        self.layout.addWidget(profile_section, 1,1,1,1)

        buttons_section = self.buttons_section()
        self.layout.addWidget(buttons_section, 3,0,1,2)

    def buttons_section(self):

        btn_groupBox = QGroupBox()
        btn_grid = QGridLayout()
        btn_groupBox.setLayout(btn_grid)

        okBtn = QPushButton('Ok')
        okBtn.clicked.connect(self.onOKclicked)
        btn_grid.addWidget(okBtn, 0, 0, 1, 1)

        cancelBtn = QPushButton('Cancel')
        cancelBtn.clicked.connect(self.close)
        btn_grid.addWidget(cancelBtn, 0, 1, 1, 1)

        return btn_groupBox

    def account_section(self):

        account_groupBox = QGroupBox()
        account_groupBox.setTitle("Account Info")
        account_grid = QGridLayout()
        account_groupBox.setLayout(account_grid)

        account_grid.addWidget(self.clabel('User Name'), 0, 0, 1, 1)
        account_grid.addWidget(self.clabel('Your Title'), 1, 0, 1, 1)
        account_grid.addWidget(self.clabel('First Name'), 2, 0, 1, 1)
        account_grid.addWidget(self.clabel('Last Name'), 3, 0, 1, 1)
        account_grid.addWidget(self.clabel('Password'), 4, 0, 1, 1)
        account_grid.addWidget(self.clabel('Re-type password'), 5, 0, 1, 1)

        self.usernameField = QLineEdit()
        self.titleField = QLineEdit()
        self.firstnameField = QLineEdit()
        self.lastnameField = QLineEdit()
        self.passwordField = QLineEdit()
        self.passwordRetypeField = QLineEdit()

        self.passwordField.setEchoMode(QLineEdit.Password)
        self.passwordRetypeField.setEchoMode(QLineEdit.Password)

        account_grid.addWidget(self.usernameField, 0, 1, 1, 3)
        account_grid.addWidget(self.titleField, 1, 1, 1, 3)
        account_grid.addWidget(self.firstnameField, 2, 1, 1, 3)
        account_grid.addWidget(self.lastnameField, 3, 1, 1, 3)
        account_grid.addWidget(self.passwordField, 4, 1, 1, 3)
        account_grid.addWidget(self.passwordRetypeField, 5, 1, 1, 3)

        return account_groupBox

    def profile_section(self):

        profile_groupBox = QGroupBox()
        profile_groupBox.setTitle("Contact details")
        profile_grid = QGridLayout()
        profile_groupBox.setLayout(profile_grid)

        profile_grid.addWidget(self.clabel("Adress Line 1"), 0,0,1,1)
        profile_grid.addWidget(self.clabel("Adress Line 2"), 1,0,1,1)
        profile_grid.addWidget(self.clabel("Postal Code"), 2,0,1,1)
        profile_grid.addWidget(self.clabel("City"), 3,0,1,1)
        profile_grid.addWidget(self.clabel("Country"), 4,0,1,1)

        self.addressLine1 = QLineEdit()
        self.addressLine2 = QLineEdit()
        self.postalCode = QLineEdit()
        self.cityLst = QComboBox()
        self.countryLst = QComboBox()

        profile_grid.addWidget(self.addressLine1, 0,1,1,1)
        self.addressLine2 = QLineEdit()

        profile_grid.addWidget(self.addressLine2, 1,1,1,1)

        regex = QRegExp("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
        self.validator = QRegExpValidator(regex, self.postalCode)
        self.postalCode.setValidator(self.validator)

        curLocaleIndex = -1
        lang_country = {}

        for lid in range(QLocale.C, QLocale.LastLanguage + 1):
            lang = (QLocale(lid).nativeLanguageName()).encode('utf-8')
            country = (QLocale(lid).nativeCountryName()).encode('utf-8')
            lang_country[country] = [lang, lid]

            lid += 1

        countries = sorted(list(set([c for c in lang_country])))
        countries.remove(countries[0])

        for c in countries:
            self.country.addItem(c)

        profile_grid.addWidget()

        return profile_groupBox



    def clabel(self, text):
        label = QLabel(text)
        label.setAlignment(var.__center__)
        label.setMinimumWidth(50)
        return label

    def onOKclicked(self):

        # Get title info
        title = self.regisTitle.text()

        if title is None or title == '':
            QMessageBox.information(var.TITLEBLANK)
            title = 'Tester'
        else:
            title = str(title)

        # Get first name info and check
        firstname = str(self.firstnameField.text())

        # Check first name and last name available
        if firstname == "" or firstname is None:
            QMessageBox.critical(self, "Warning", var.ERROR_LOG("first_name"), QMessageBox.Retry)

        # Get last name info and check
        lastname = str(self.lastnameField.text())

        if lastname == "":
            QMessageBox.critical(self, "Warning", var.ERROR_LOG("last_name"), QMessageBox.Retry)

        # Get user name and check
        username = '%s.%s' % (lastname, firstname)

        # Check username already exists
        check = ultis.check_data_exists(username)
        if check:
            USEREXISTS = 'Username %s exists, try again or you already have an account?' % username
            QMessageBox.critical(self, "Username Exists", USEREXISTS, QMessageBox.Retry)
        else:
            pass

        # Get password and retype password then check them
        password = str(self.password.text())
        passretype = str(self.passwordRetype.text())
        check = self.checkMatchPassWord(password, passretype)

        SUCCESS = "Your account has been created: %s" % username
        if not check:
            pass
        else:
            ultis.CreateNewUser(firstname, lastname, title, password)
            QMessageBox.information(self, "Your username", SUCCESS, QMessageBox.Retry)
            self.hide()
            login = self.load_login_ui()
            login.show()

    def checkMatchPassWord(self, password, passretype):
        NOTMATCH = "Password doesn't match"
        if not password == passretype:
            QMessageBox.critical(self, "Password not matches", NOTMATCH, QMessageBox.Retry)
            return False
        else:
            return True

    def load_login_ui(self):
        pass


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkgraystyle.load_stylesheet_pyqt5())
    window = Sign_in()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()