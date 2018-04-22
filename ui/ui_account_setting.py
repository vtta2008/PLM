# -*- coding: utf-8 -*-
"""
Script Name: ui_about.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is main file to store everything for the pipeline app

"""

# -------------------------------------------------------------------------------------------------------------
# IMPORT PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
import logging
import os
import shutil
import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QImage, QIcon, QPixmap
from PyQt5.QtWidgets import *

from utilities import utils_sql as ultis
# ------------------------------------------------------
# IMPORT FROM PIPELINE TOOLS APP
# ------------------------------------------------------
from utilities import utils as func

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

def query_user_info():

    currentUserData = ultis.query_current_user()
    curUser = currentUserData[2]
    unix = currentUserData[0]
    token = currentUserData[1]
    rememberLogin = currentUserData[3]
    status = currentUserData[-1]
    ultis.check_sys_configuration(curUser)
    return unix, token, curUser, rememberLogin, status

class WindowDialog(QDialog):

    changAvatarSignal = pyqtSignal(str)

    def __init__(self, parent=None, username=None, id='User Setting', icon=func.get_icon('Logo')):
        super(WindowDialog, self).__init__(parent)

        self.username = username

        self.setWindowTitle(id)
        self.setWindowIcon(QIcon(icon))
        central_widget = QWidget(self)
        self.layout = QGridLayout(self)
        central_widget.setLayout(self.layout)

        self.buildUI()

    def buildUI(self):

        oldPasswordGroupBox = QGroupBox('Old Password')
        oldPasswordGridLayout = QGridLayout()
        oldPasswordLabel = QLabel('Old Password: ')
        self.oldPassword = QLineEdit()
        self.oldPassword.setEchoMode(QLineEdit.Password)
        oldPasswordGridLayout.addWidget(oldPasswordLabel, 0,0,1,1)
        oldPasswordGridLayout.addWidget(self.oldPassword, 0,1,1,1)
        oldPasswordGroupBox.setLayout(oldPasswordGridLayout)

        newPasswordGroupBox = QGroupBox('New Password')
        newPasswordGridLayout = QGridLayout()
        newPasswordLabel = QLabel('New Password: ')
        self.newPassword = QLineEdit()
        self.newPassword.setEchoMode(QLineEdit.Password)
        newConfirmLable = QLabel('Confirm')
        self.confirmPassword = QLineEdit()
        self.confirmPassword.setEchoMode(QLineEdit.Password)

        newPasswordGridLayout.addWidget(newPasswordLabel, 0,0,1,1)
        newPasswordGridLayout.addWidget(self.newPassword, 0,1,1,1)
        newPasswordGridLayout.addWidget(newConfirmLable, 1,0,1,1)
        newPasswordGridLayout.addWidget(self.confirmPassword, 1,1,1,1)
        newPasswordGroupBox.setLayout(newPasswordGridLayout)

        changePasswordBtnGroupBox = QGroupBox('Set Change password')
        changePasswordBtnLayout = QHBoxLayout()
        okBtn = QPushButton('Change Password')
        okBtn.setMinimumWidth(100)
        okBtn.clicked.connect(self.onOkBtnClicked)
        cancelBtn = QPushButton('Cancel')
        cancelBtn.setMinimumWidth(100)
        cancelBtn.clicked.connect(self.onCancelBtnClicked)
        changePasswordBtnLayout.addWidget(okBtn)
        changePasswordBtnLayout.addWidget(cancelBtn)
        changePasswordBtnGroupBox.setLayout(changePasswordBtnLayout)

        avatarGroupBox = QGroupBox('User Avatar')
        avatarGroupLayout = QHBoxLayout()
        imagePth = func.get_avatar(self.username.split(".")[0] + self.username.split(".")[-1])
        image = QPixmap.fromImage(QImage(imagePth))
        self.avatar = QLabel()
        self.avatar.setPixmap(image)
        self.avatar.setScaledContents(True)
        self.avatar.setFixedSize(100, 100)
        avatarGroupLayout.addWidget(self.avatar)
        avatarGroupBox.setLayout(avatarGroupLayout)

        changeAvatarBtnGroupBox = QGroupBox('Set Change Avatar')
        changeAvatarBtnLayout = QHBoxLayout()
        changeAvatarBtn = QPushButton('Change Avatar')
        changeAvatarBtn.setMinimumWidth(100)
        changeAvatarBtn.clicked.connect(self.onChangeAvatarBtnClicked)
        changeAvatarBtnLayout.addWidget(changeAvatarBtn)
        changeAvatarBtnGroupBox.setLayout(changeAvatarBtnLayout)

        self.layout.addWidget(oldPasswordGroupBox, 0,0,1,2)
        self.layout.addWidget(newPasswordGroupBox, 1,0,2,2)
        self.layout.addWidget(changePasswordBtnGroupBox, 3,0,1,2)
        self.layout.addWidget(avatarGroupBox, 0,2,3,3)
        self.layout.addWidget(changeAvatarBtnGroupBox, 3,2,1,3)

        self.setLayout(self.layout)

    def onOkBtnClicked(self):
        unix, token, curUser, rememberLogin, status = query_user_info()
        password = func.encode(self.oldPassword.text())

        if password=="":
            QMessageBox.critical(self, 'Failed', "Please type your password")
            return

        checkPass = ultis.check_password_match(curUser, password)

        if not checkPass:
            QMessageBox.critical(self, 'Failed', "Password not match")
            return
        else:
            newpass = func.encode(self.newPassword.text())
            confirm = func.encode(self.confirmPassword.text())
            if newpass == "" or confirm == "":
                QMessageBox.critical(self, 'Failed', "Please type your new password")
                return
            elif newpass==confirm:
                ultis.update_password_user(unix, newpass)
                QMessageBox.information(self, 'Update password', "Your password has changed")
                self.close()
            else:
                QMessageBox.critical(self, 'Failed', "Password not match")

    def onCancelBtnClicked(self):
        self.close()

    def onChangeAvatarBtnClicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        imgsDir = os.path.join(os.getenv('PIPELINE_TOOL'), 'imgs')
        fileName, _ = QFileDialog.getOpenFileName(self, "Your Avatar", imgsDir, "All Files (*);;Img Files (*.jpg)",
                                                  options=options)
        if fileName:
            unix, token, curUser, rememberLogin, status = query_user_info()
            baseFileName = curUser.split('.')[0] + curUser.split('.')[-1] + '.avatar.jpg'
            desPth = os.path.join(imgsDir, baseFileName)

            pths = [fileName, desPth]

            if fileName in pths:
                if desPth == fileName:
                    return
                else:
                    func.resize_image(fileName, desPth)
                    os.rename(desPth, desPth + '.old')
                    shutil.copy2(fileName, desPth)
                    image = QPixmap.fromImage(QImage(desPth))
                    self.avatar.setPixmap(image)
                    self.avatar.update()
            else:
                shutil.copy2(fileName, desPth)
                self.avatar.setPixmap(desPth)
                self.avatar.update()

            self.changAvatarSignal.emit(desPth)
            ultis.dynamic_insert_timelog('Change Avatar')


if __name__=='__main__':
    app = QApplication(sys.argv)
    window = WindowDialog('TrinhDo')
    window.show()
    sys.exit(app.exec_())