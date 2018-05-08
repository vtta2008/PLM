# -*- coding: utf-8 -*-
"""

Script Name: plt.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    Setting your account.

"""

# -------------------------------------------------------------------------------------------------------------
""" About Plt """

__appname__ = "Pipeline Tool"
__module__ = "Plt"
__version__ = "13.0.1"
__organization__ = "DAMG team"
__website__ = "www.dot.damgteam.com"
__email__ = "dot@damgteam.com"
__author__ = "Trinh Do, a.k.a: Jimmy"
__root__ = "PLT_RT"
__db__ = "PLT_DB"
__st__ = "PLT_ST"

# -------------------------------------------------------------------------------------------------------------
""" Import modules """

# Python
import os
import shutil
import sys
import logging

# PtQt5
from PyQt5.QtCore import pyqtSignal, QSettings, Qt
from PyQt5.QtGui import QImage, QIcon, QPixmap
from PyQt5.QtWidgets import (QDialog, QGridLayout, QLabel, QLineEdit, QGroupBox, QHBoxLayout, QPushButton, QFileDialog,
                             QMessageBox, QApplication)

# Plt
from utilities import sql_local as usql
from utilities import utils as func
from utilities import message as mess
from utilities import variables as var

# -------------------------------------------------------------------------------------------------------------
""" Declare variables """

__center__ = Qt.AlignCenter

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain logs """

logPth = os.path.join(os.getenv(__root__), 'appData', 'logs', 'acc_setting.log')
logger = logging.getLogger('acc_setting')
handler = logging.FileHandler(logPth)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def clabel(text, *args):
    label = QLabel(text)
    label.setAlignment(__center__)
    label.setMinimumWidth(50)
    return label

# ----------------------------------------------------------------------------------------------------------- #
""" User setting layout """
# ----------------------------------------------------------------------------------------------------------- #
class Account_setting(QDialog):

    changeAvatarSignal = pyqtSignal(str)
    curUser = usql.query_curUser()

    def __init__(self, parent=None):

        super(Account_setting, self).__init__(parent)

        self.username = self.curUser[0]
        self.setWindowTitle('User Setting')
        self.setWindowIcon(QIcon(func.get_icon('Logo')))

        self.settings = QSettings(var.USER_SETTING, QSettings.IniFormat)

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        password_section = self.change_pass_section()
        avatar_section = self.change_avatar_section()
        profile_section = self.change_profile_section()
        location_setion = self.change_location_section()

        self.layout.addWidget(avatar_section, 0, 0, 1, 1)
        self.layout.addWidget(password_section, 0, 1 , 1, 1)
        self.layout.addWidget(profile_section, 1, 0, 1, 1)
        self.layout.addWidget(location_setion, 1, 1, 1, 1)

    def change_avatar_section(self):

        avatar_groupBox = QGroupBox('Change Avatar')
        avatar_layout = QHBoxLayout()
        avatar_groupBox.setLayout(avatar_layout)

        self.avatar = QLabel()
        self.avatar.setPixmap(QPixmap.fromImage(QImage(func.get_avatar(self.username))))
        self.avatar.setScaledContents(True)
        self.avatar.setFixedSize(100, 100)

        change_avatar_btn = QPushButton('Change Avatar')
        change_avatar_btn.clicked.connect(self.update_avatar)
        avatar_layout.addWidget(self.avatar)
        avatar_layout.addWidget(change_avatar_btn)

        return avatar_groupBox

    def change_pass_section(self):

        password_groupBox = QGroupBox('Change Password')
        password_layout = QGridLayout()
        password_groupBox.setLayout(password_layout)

        self.old_pass = QLineEdit()
        self.old_pass.setEchoMode(QLineEdit.Password)
        self.new_pass = QLineEdit()
        self.new_pass.setEchoMode(QLineEdit.Password)
        self.confirm_pass = QLineEdit()
        self.confirm_pass.setEchoMode(QLineEdit.Password)

        change_pass_btn = QPushButton('Change Password')
        change_pass_btn.clicked.connect(self.update_password)

        password_layout.addWidget(QLabel('Old Password'), 0, 0, 1, 2)
        password_layout.addWidget(QLabel('New Password'), 1, 0, 1, 2)
        password_layout.addWidget(QLabel('Confirm Password'), 2, 0, 1, 2)

        password_layout.addWidget(self.old_pass, 0, 2, 1, 4)
        password_layout.addWidget(self.new_pass, 1, 2, 1, 4)
        password_layout.addWidget(self.confirm_pass, 2, 2, 1, 4)
        password_layout.addWidget(change_pass_btn, 3, 0, 1, 6)

        return password_groupBox

    def change_profile_section(self):

        profile_groupBox = QGroupBox("Change Profile")
        profile_layout = QGridLayout()
        profile_groupBox.setLayout(profile_layout)

        profile_layout.addWidget(QLabel('First Name'), 0, 0, 1, 2)
        profile_layout.addWidget(QLabel('Last Name'), 1, 0, 1, 2)
        profile_layout.addWidget(QLabel('Your Title'), 2, 0, 1, 2)
        profile_layout.addWidget(QLabel('Emial'), 3, 0, 1, 2)
        profile_layout.addWidget(QLabel('Phone Number'), 4, 0, 1, 2)

        self.firstnameField = QLineEdit()
        self.lastnameField = QLineEdit()
        self.titleField = QLineEdit()
        self.emailField = QLineEdit()
        self.phoneField = QLineEdit()

        change_profile_btn = QPushButton("Update Profile")
        change_profile_btn.clicked.connect(self.update_profile)

        profile_layout.addWidget(self.firstnameField, 0, 2, 1, 4)
        profile_layout.addWidget(self.lastnameField, 1, 2, 1, 4)
        profile_layout.addWidget(self.titleField, 2, 2, 1, 4)
        profile_layout.addWidget(self.emailField, 3, 2, 1, 4)
        profile_layout.addWidget(self.phoneField, 4, 2, 1, 4)
        profile_layout.addWidget(change_profile_btn, 5, 0, 1, 6)

        return profile_groupBox

    def change_location_section(self):

        location_groupBox = QGroupBox("Change Location")
        location_layout = QGridLayout()
        location_groupBox.setLayout(location_layout)

        location_layout.addWidget(QLabel('Address Line 1'), 0, 0, 1, 2)
        location_layout.addWidget(QLabel('Address Line 2'), 1, 0, 1, 2)
        location_layout.addWidget(QLabel('Postal'), 2, 0, 1, 2)
        location_layout.addWidget(QLabel('City'), 3, 0, 1, 2)
        location_layout.addWidget(QLabel('Country'), 4, 0, 1, 2)

        self.address1Field = QLineEdit()
        self.address2Field = QLineEdit()
        self.postalField = QLineEdit()
        self.cityField = QLineEdit()
        self.countryField = QLineEdit()

        change_location_btn = QPushButton("Update Location")
        change_location_btn.clicked.connect(self.update_location)

        location_layout.addWidget(self.address1Field, 0, 2, 1, 4)
        location_layout.addWidget(self.address2Field, 1, 2, 1, 4)
        location_layout.addWidget(self.postalField, 2, 2, 1, 4)
        location_layout.addWidget(self.cityField, 3, 2, 1, 4)
        location_layout.addWidget(self.countryField, 4, 2, 1, 4)
        location_layout.addWidget(change_location_btn, 5, 0, 1, 6)

        return location_groupBox

    def update_password(self):

        old_pass = func.text_to_hex(self.old_pass.text())
        new_pass = func.text_to_hex(self.new_pass.text())
        confirm_pass = func.text_to_hex(self.confirm_pass.text())

        if len(old_pass) == 0 or len(new_pass) == 0 or len(confirm_pass) == 0:
            QMessageBox.critical(self, 'Failed', mess.PW_BLANK)
            return
        elif new_pass is not confirm_pass:
            QMessageBox.critical(self, 'Failed', mess.PW_UNMATCH)
            return
        else:
            checkPass = func.check_pw_match(self.curUser, old_pass)
            if not checkPass:
                QMessageBox.critical(self, 'Failed', "Password not match")
                return
            else:
                newpass = func.encode(self.newPassword.text())
                func.update_password(self.unix, newpass)
                QMessageBox.information(self, 'Updated', mess.PW_CHANGED)

    def update_avatar(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        imgsDir = os.path.join(os.getenv(__root__), 'avatar')
        fileName, _ = QFileDialog.getOpenFileName(self, "Your Avatar", imgsDir, "All Files (*);;Img Files (*.jpg)",
                                                  options=options)
        if fileName:
            baseFileName = self.username + '.avatar.jpg'
            desPth = os.path.join(imgsDir, baseFileName)

            if desPth == fileName:
                pass
            elif os.path.exists(desPth):
                if os.path.exists(desPth + '.old'):
                    os.remove(desPth + '.old')

                os.rename(desPth, desPth + '.old')
                func.resize_image(fileName, desPth)
                shutil.copy2(fileName, desPth)
                image = QPixmap.fromImage(QImage(desPth))
                self.avatar.setPixmap(image)
                self.avatar.update()
                self.settings.setValue(self.username, desPth)
                self.changeAvatarSignal.emit(desPth)

    def update_profile(self):
        pass

    def update_location(self):
        pass


def main():
    app = QApplication(sys.argv)
    acc_setting = Account_setting()
    acc_setting.show()
    app.exec_()

if __name__=='__main__':
    main()