# -*- coding: utf-8 -*-
"""

Script Name: ui_sign_up.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    Create new account

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
                             QGroupBox, QComboBox, QCheckBox)


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

# ----------------------------------------------------------------------------------------------------------- #
""" Sign in ui """
# ----------------------------------------------------------------------------------------------------------- #
class Sign_up(QDialog):

    def __init__(self, parent=None):

        super(Sign_up, self).__init__(parent)

        self.setWindowTitle("Sign Up")
        self.setWindowIcon(QIcon(func.getIcon('Logo')))
        self.setContentsMargins(0,0,0,0)
        self.setFixedSize(400, 800)

        self.layout = QGridLayout()

        self.buildUI()

        self.setLayout(self.layout)

    def buildUI(self):

        self.layout.addWidget(self.clabel("All fields are required."), 0,0,1,6)

        account_section = self.account_section()
        self.layout.addWidget(account_section, 1, 0, 1, 6)

        profile_section = self.profile_section()
        self.layout.addWidget(profile_section, 2, 0, 1, 6)

        contact_section = self.contact_section()
        self.layout.addWidget(contact_section, 3, 0, 1, 6)

        buttons_section = self.buttons_section()
        self.layout.addWidget(buttons_section, 5, 0, 1, 6)

    def account_section(self):

        account_groupBox = QGroupBox()
        account_groupBox.setTitle("Account")
        account_grid = QGridLayout()
        account_groupBox.setLayout(account_grid)

        account_grid.addWidget(self.clabel('User Name'), 0, 0, 1, 2)
        account_grid.addWidget(self.clabel('Password'), 1, 0, 1, 2)
        account_grid.addWidget(self.clabel('Re-type'), 2, 0, 1, 2)

        self.usernameField = QLineEdit()
        self.passwordField = QLineEdit()
        self.retypeField = QLineEdit()

        self.passwordField.setEchoMode(QLineEdit.Password)
        self.retypeField.setEchoMode(QLineEdit.Password)

        account_grid.addWidget(self.usernameField, 0, 3, 1, 4)
        account_grid.addWidget(self.passwordField, 1, 3, 1, 4)
        account_grid.addWidget(self.retypeField, 2, 3, 1, 4)

        return account_groupBox

    def profile_section(self):

        profile_groupBox = QGroupBox()
        profile_groupBox.setTitle("Profile")
        profile_grid = QGridLayout()
        profile_groupBox.setLayout(profile_grid)

        profile_grid.addWidget(self.clabel('Your Title'), 0, 0, 1, 2)
        profile_grid.addWidget(self.clabel('First Name'), 1, 0, 1, 2)
        profile_grid.addWidget(self.clabel('Last Name'), 2, 0, 1, 2)

        self.titleField = QLineEdit()
        self.firstnameField = QLineEdit()
        self.lastnameField = QLineEdit()

        profile_grid.addWidget(self.titleField, 0, 3, 1, 4)
        profile_grid.addWidget(self.firstnameField, 1, 3, 1, 4)
        profile_grid.addWidget(self.lastnameField, 2, 3, 1, 4)

        return profile_groupBox

    def contact_section(self):

        contact_groupBox = QGroupBox()
        contact_groupBox.setTitle("Contact")
        contact_grid = QGridLayout()
        contact_groupBox.setLayout(contact_grid)

        contact_grid.addWidget(self.clabel("Line 1"), 0, 0, 1, 2)
        contact_grid.addWidget(self.clabel("Line 2"), 1, 0, 1, 2)
        contact_grid.addWidget(self.clabel("Postal"), 2, 0, 1, 2)
        contact_grid.addWidget(self.clabel("City"), 3, 0, 1, 2)
        contact_grid.addWidget(self.clabel("Country"), 4, 0, 1, 2)

        self.addressLine1 = QLineEdit()
        self.addressLine2 = QLineEdit()
        self.postalCode = QLineEdit()
        self.city = QLineEdit()
        self.countryLst = QComboBox()


        regex = QRegExp("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
        self.validator = QRegExpValidator(regex, self.postalCode)
        self.postalCode.setValidator(self.validator)

        lang_country = {}

        for i in range(QLocale.C, QLocale.LastLanguage + 1):
            lang = (QLocale(i).nativeLanguageName()).encode('utf-8')
            country = (QLocale(i).nativeCountryName()).encode('utf-8')
            lang_country[country] = [lang, i]
            i += 1

        countries = sorted(list(set([c for c in lang_country])))

        countries.remove(countries[0])

        for country in countries:
            self.countryLst.addItem(country)

        contact_grid.addWidget(self.addressLine1, 0, 3, 1, 4)
        contact_grid.addWidget(self.addressLine2, 1, 3, 1, 4)
        contact_grid.addWidget(self.cityLst, 2, 3, 1, 4)
        contact_grid.addWidget(self.postalCode, 3, 3, 1, 4)
        contact_grid.addWidget(self.countryLst, 4, 3, 1, 4)

        return contact_groupBox

    def buttons_section(self):

        btn_groupBox = QGroupBox()
        btn_grid = QGridLayout()
        btn_groupBox.setLayout(btn_grid)

        self.checkBox = QCheckBox(mess.CHECK_AGREEMENT)
        self.checkBox.setStyleSheet("fontName='Timé'")
        btn_grid.addWidget(self.checkBox, 0, 0, 1, 1)

        okBtn = QPushButton('Ok')
        okBtn.clicked.connect(self.onOKclicked)
        btn_grid.addWidget(okBtn, 1, 0, 1, 1)

        cancelBtn = QPushButton('Cancel')
        cancelBtn.clicked.connect(self.close)
        btn_grid.addWidget(cancelBtn, 1, 1, 1, 1)

        return btn_groupBox

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
    window = Sign_up()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()