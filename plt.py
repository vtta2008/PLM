#!/usr/bin/env python
# -*- coding: utf-8 -*-

# http://13.55.214.163/check
# http://13.55.214.163/auth
"""

Script Name: plt.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This script is master file of Pipeline Tool

"""

# -------------------------------------------------------------------------------------------------------------
""" Import modules """

# Python
import logging
import os
import subprocess
import sys
import webbrowser
import requests

import sqlite3 as lite
from functools import partial

# PyQt5
from PyQt5.QtCore import Qt, QSize, QCoreApplication, QSettings, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFrame, QDialog, QWidget, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QSizePolicy, QLineEdit, QLabel, QPushButton, QMessageBox, QGroupBox,
                             QCheckBox, QTabWidget, QSystemTrayIcon, QAction, QMenu, QFileDialog, QComboBox, QTabBar)

from __init__ import (__root__, __appname__, __version__, __organization__, __website__)

# -------------------------------------------------------------------------------------------------------------
""" Set up env variable path """
# Main path
os.environ[__root__] = os.getcwd()

# subprocess.Popen("python setup.py build", cwd=os.getcwd())

# Preset
import plt_presets as pltp

pltp.preset2_install_extra_python_package()
pltp.preset3_maya_intergrate()

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logPth = os.path.join(os.getenv(__root__), 'appData', 'logs', 'plt.log')
logger = logging.getLogger('plt')
handler = logging.FileHandler(logPth)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------------------
""" Plt tools """

import qdarkgraystyle

from ui import ui_acc_setting
from ui import ui_preference

from utilities import utils as func
from utilities import sql_local as usql
from utilities import message as mess
from utilities import variables as var

# -------------------------------------------------------------------------------------------------------------
""" Variables """

# PyQt5 ui elements
__center__ = Qt.AlignCenter
__right__ = Qt.AlignRight
__left__ = Qt.AlignLeft
frameStyle = QFrame.Sunken | QFrame.Panel

# Get apps info config
APPINFO = pltp.preset4_gather_configure_info()

# -------------------------------------------------------------------------------------------------------------

def clabel(text):
    label = QLabel(text)
    label.setAlignment(__center__)
    label.setMinimumWidth(50)
    return label

# -------------------------------------------------------------------------------------------------------------
""" Sign up layout """

class Plt_sign_up(QDialog):

    showLoginSig1 = pyqtSignal(bool)

    def __init__(self, parent=None):

        super(Plt_sign_up, self).__init__(parent)

        self.setWindowTitle("Sign Up")
        self.setWindowIcon(QIcon(func.get_icon('Logo')))
        self.setContentsMargins(0,0,0,0)
        self.setFixedSize(450, 900)

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        avatar_section = self.avatar_section()
        account_section = self.account_section()
        profile_section = self.profile_section()
        contact_section = self.location_section()
        security_section = self.security_section()
        buttons_section = self.buttons_section()

        self.layout.addWidget(clabel("ALL FIELD ARE REQUIRED."), 0, 0, 1, 6)
        self.layout.addWidget(avatar_section, 1, 0, 1, 2)
        self.layout.addWidget(account_section, 1, 2, 1, 4)
        self.layout.addWidget(profile_section, 2, 0, 1, 6)
        self.layout.addWidget(contact_section, 3, 0, 1, 6)
        self.layout.addWidget(security_section, 4, 0, 1, 6)
        self.layout.addWidget(buttons_section, 5, 0, 1, 6)

    def avatar_section(self):
        avatar_groupBox = QGroupBox("Avatar")
        avatar_grid = QGridLayout()
        avatar_groupBox.setLayout(avatar_grid)

        defaultImg = QPixmap.fromImage(QImage(func.get_avatar('default')))
        self.userAvatar = QLabel()
        self.userAvatar.setPixmap(defaultImg)
        self.userAvatar.setScaledContents(True)
        self.userAvatar.setFixedSize(100, 100)

        set_avatarBtn = QPushButton("Set Avatar")
        set_avatarBtn.clicked.connect(self.on_set_avatar_btn_clicked)

        avatar_grid.addWidget(self.userAvatar, 0, 0, 2, 2)
        avatar_grid.addWidget(set_avatarBtn, 2, 0, 1, 2)

        return avatar_groupBox

    def account_section(self):

        account_groupBox = QGroupBox("Account")
        account_grid = QGridLayout()
        account_groupBox.setLayout(account_grid)

        account_grid.addWidget(clabel('User Name'), 0, 0, 1, 2)
        account_grid.addWidget(clabel('Password'), 1, 0, 1, 2)
        account_grid.addWidget(clabel('Confirm Password'), 2, 0, 1, 2)

        self.usernameField = QLineEdit()
        self.passwordField = QLineEdit()
        self.confirmPassField = QLineEdit()

        self.passwordField.setEchoMode(QLineEdit.Password)
        self.confirmPassField.setEchoMode(QLineEdit.Password)

        account_grid.addWidget(self.usernameField, 0, 3, 1, 4)
        account_grid.addWidget(self.passwordField, 1, 3, 1, 4)
        account_grid.addWidget(self.confirmPassField, 2, 3, 1, 4)

        return account_groupBox

    def profile_section(self):

        profile_groupBox = QGroupBox("Profile")
        profile_grid = QGridLayout()
        profile_groupBox.setLayout(profile_grid)

        profile_grid.addWidget(clabel('First Name'), 0, 0, 1, 2)
        profile_grid.addWidget(clabel('Last Name'), 1, 0, 1, 2)
        profile_grid.addWidget(clabel('Your Title'), 2, 0, 1, 2)
        profile_grid.addWidget(clabel('Email'), 3, 0, 1, 2)
        profile_grid.addWidget(clabel('Phone Number'), 4, 0, 1, 2)

        self.titleField = QLineEdit()
        self.firstnameField = QLineEdit()
        self.lastnameField = QLineEdit()
        self.emailField = QLineEdit()
        self.phoneField = QLineEdit()

        profile_grid.addWidget(self.firstnameField, 0, 2, 1, 4)
        profile_grid.addWidget(self.lastnameField, 1, 2, 1, 4)
        profile_grid.addWidget(self.titleField, 2, 2, 1, 4)
        profile_grid.addWidget(self.emailField, 3, 2, 1, 4)
        profile_grid.addWidget(self.phoneField, 4, 2, 1, 4)

        return profile_groupBox

    def location_section(self):

        contact_groupBox = QGroupBox("Location")
        contact_grid = QGridLayout()
        contact_groupBox.setLayout(contact_grid)

        contact_grid.addWidget(clabel("Address Line 1"), 0, 0, 1, 2)
        contact_grid.addWidget(clabel("Address Line 2"), 1, 0, 1, 2)
        contact_grid.addWidget(clabel("Postal"), 2, 0, 1, 2)
        contact_grid.addWidget(clabel("City"), 3, 0, 1, 2)
        contact_grid.addWidget(clabel("Country"), 4, 0, 1, 2)

        self.addressLine1 = QLineEdit()
        self.addressLine2 = QLineEdit()
        self.postalCode = QLineEdit()
        self.city = QLineEdit()
        self.country = QLineEdit()

        contact_grid.addWidget(self.addressLine1, 0, 2, 1, 4)
        contact_grid.addWidget(self.addressLine2, 1, 2, 1, 4)
        contact_grid.addWidget(self.city, 2, 2, 1, 4)
        contact_grid.addWidget(self.postalCode, 3, 2, 1, 4)
        contact_grid.addWidget(self.country, 4, 2, 1, 4)

        return contact_groupBox

    def security_section(self):

        questions_groupBox = QGroupBox("Security Question")
        questions_grid = QGridLayout()
        questions_groupBox.setLayout(questions_grid)

        self.question1 = QComboBox()
        self.question1.setMaximumWidth(300)
        self.answer2 = QLineEdit()
        self.question2 = QComboBox()
        self.question2.setMaximumWidth(300)
        self.answer1 = QLineEdit()

        questions = usql.query_all_questions()
        for i in questions:
            self.question1.addItem(str(i[0]))
            self.question2.addItem(str(i[0]))

        questions_grid.addWidget(clabel('Question 1'), 0, 0, 1, 3)
        questions_grid.addWidget(clabel('Answer 1'), 1, 0, 1, 3)
        questions_grid.addWidget(clabel('Question 2'), 2, 0, 1, 3)
        questions_grid.addWidget(clabel('Answer 2'), 3, 0, 1, 3)

        questions_grid.addWidget(self.question1, 0, 3, 1, 6)
        questions_grid.addWidget(self.answer1, 1, 3, 1, 6)
        questions_grid.addWidget(self.question2, 2, 3, 1, 6)
        questions_grid.addWidget(self.answer2, 3, 3, 1, 6)

        return questions_groupBox

    def buttons_section(self):
        btn_groupBox = QGroupBox()
        btn_grid = QGridLayout()
        btn_groupBox.setLayout(btn_grid)

        self.user_agree_checkBox = QCheckBox(mess.USER_CHECK_REQUIRED)
        btn_grid.addWidget(self.user_agree_checkBox, 0, 0, 1, 6)

        okBtn = QPushButton('Create Account')
        okBtn.clicked.connect(self.on_create_btn_clicked)
        btn_grid.addWidget(okBtn, 1, 0, 1, 2)

        cancelBtn = QPushButton('Cancel')
        cancelBtn.clicked.connect(self.on_cancel_btn_clicked)
        btn_grid.addWidget(cancelBtn, 1, 2, 1, 2)

        quitBtn = QPushButton('Quit')
        quitBtn.clicked.connect(QApplication.quit)
        btn_grid.addWidget(quitBtn, 1,4,1,2)

        return btn_groupBox

    def on_set_avatar_btn_clicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        imgsDir = os.path.join(os.getenv(__root__), 'avatar')
        self.rawAvatarPth, _ = QFileDialog.getOpenFileName(self, "Your Avatar", imgsDir, "All Files (*);;Img Files (*.jpg)",
                                                           options=options)
        if self.rawAvatarPth:
            self.userAvatar.setPixmap(QPixmap.fromImage(QImage(self.rawAvatarPth)))
            self.userAvatar.update()

    def on_create_btn_clicked(self):

        username = str(self.usernameField.text())
        password = str(self.passwordField.text())
        confirm = str(self.confirmPassField.text())
        firstname = str(self.firstnameField.text())
        lastname = str(self.lastnameField.text())
        email = str(self.emailField.text())
        phone = str(self.phoneField.text())
        address1 = str(self.addressLine1.text())
        address2 = str(self.addressLine2.text())
        postal = str(self.postalCode.text())
        city = str(self.city.text())
        country = str(self.country.text())
        answer1 = str(self.answer1.text())
        answer2 = str(self.answer2.text())

        reg = [username, password, confirm, firstname, lastname, email, phone, address1, address2, postal, city, country,
               answer1, answer2]

        if self.check_all_conditions(confirm, password, reg):

            data = self.create_user_data()

            usql.create_new_user_data(data)

    def create_user_data(self):

        username = str(self.usernameField.text())
        password = str(self.passwordField.text())
        firstname = str(self.firstnameField.text())
        lastname = str(self.lastnameField.text())
        email = str(self.emailField.text())
        phone = str(self.phoneField.text())
        address1 = str(self.addressLine1.text())
        address2 = str(self.addressLine2.text())
        postal = str(self.postalCode.text())
        city = str(self.city.text())
        country = str(self.country.text())
        question1 = str(self.question1.currentText())
        answer1 = str(self.answer1.text())
        question2 = str(self.question2.currentText())
        answer2 = str(self.answer2.text())
        title = str(self.titleField.text())
        token = func.get_token()
        timelog = func.get_time()
        sysInfo = func.get_local_pc()
        productID = sysInfo['Product ID']
        ip, cityIP, countryIP = func.get_location()
        unix = func.get_unix()
        datelog = func.get_date()
        pcOS = sysInfo['os']
        pcUser = sysInfo['pcUser']
        pcPython = sysInfo['python']

        if not os.path.exists(self.rawAvatarPth):
            rawAvatarPth = func.get_avatar('default')
        else:
            rawAvatarPth = self.rawAvatarPth

        data = [username, password, firstname, lastname, title, email, phone, address1, address2, postal, city,
                    country, token, timelog, productID, ip, cityIP, countryIP, unix, question1, answer1, question2,
                    answer2, datelog, pcOS, pcUser, pcPython, rawAvatarPth]

        return data

    def on_cancel_btn_clicked(self):
        self.close()
        self.settings.setValue("showLogin", True)
        self.showLoginSig1.emit(True)

    def check_all_conditions(self, confirm, password, reg):

        if self.check_all_field_blank(reg):
            if self.check_pw_matching(confirm, password):
                if self.check_user_agreement():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def check_user_agreement(self):
        state = self.user_agree_checkBox.checkState()
        if not state:
            QMessageBox.critical(self, "Warning", mess.USER_NOT_CHECK, QMessageBox.Retry)
            return False
        else:
            return True

    def check_pw_matching(self, confirm, password):
        check_pass = func.check_match(password, confirm)
        if not check_pass:
            QMessageBox.critical(self, "Warning", mess.PW_UNMATCH, QMessageBox.Retry)
            return False
        else:
            return True

    def check_all_field_blank(self, reg):
        secName = ['Username', 'Password', 'Confirm Password', 'Firstname', 'Lastname', 'Email', 'Phone', 'Address line 1',
                   'Address line 2', 'Postal', 'City', 'Country', 'Answer 1', 'Answer 2']

        check = []

        for i in reg:
            if not func.check_blank(i):
                index = reg.index(i)
                QMessageBox.critical(self, "Warning", secName[index] + mess.SEC_BLANK, QMessageBox.Retry)
                check.append(secName[index])
                break
            else:
                continue

        if len(check) == 0:
            return True
        else:
            return False

    def check_password_matching(self, password, passretype):

        if not password == passretype:
            QMessageBox.critical(self, "Warning", mess.PW_UNMATCH, QMessageBox.Retry)
            return False
        else:
            return True

    def closeEvent(self, event):
        self.on_cancel_btn_clicked()

# -------------------------------------------------------------------------------------------------------------
""" Login Layout """

class Plt_sign_in(QDialog):

    def __init__(self, parent=None):

        super(Plt_sign_in, self).__init__(parent)

        # Sign in layout preset
        self.setWindowTitle('Sign in')
        self.setWindowIcon(QIcon(func.get_icon('Logo')))
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedSize(400, 300)

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)
        self.signup = Plt_sign_up()
        showLoginSig1 = self.signup.showLoginSig1
        showLoginSig1.connect(self.show_hide_login)

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

        login_grid.addWidget(clabel('Username'), 1, 0, 1, 2)
        login_grid.addWidget(clabel('Password'), 2, 0, 1, 2)
        login_grid.addWidget(self.usernameField, 1, 2, 1, 4)
        login_grid.addWidget(self.passwordField, 2, 2, 1, 4)
        login_grid.addWidget(self.rememberCheckBox, 3, 1, 1, 2)
        login_grid.addWidget(login_btn, 3, 3, 1, 3)
        login_grid.addWidget(forgot_pw_btn, 4, 0, 1, 3)
        login_grid.addWidget(cancel_btn, 4, 3, 1, 3)

        signup_groupBox = QGroupBox('Sign up')
        signup_grid = QGridLayout()
        signup_groupBox.setLayout(signup_grid)

        sign_up_btn = QPushButton('Sign up')
        sign_up_btn.clicked.connect(self.on_sign_up_btn_clicked)

        signup_grid.addWidget(clabel(mess.SIGN_UP), 0, 0, 1, 6)
        signup_grid.addWidget(sign_up_btn, 1, 0, 1, 6)

        self.layout.addWidget(login_groupBox, 0, 0, 1, 1)
        self.layout.addWidget(signup_groupBox, 1, 0, 1, 1)

    def show_hide_login(self, param):
        param = func.str2bool(param)
        if param:
            self.show()
        else:
            self.hide()

    def on_forgot_pw_btn_clicked(self):
        from ui import ui_pw_reset_form
        reset_pw_form = ui_pw_reset_form.Reset_password_form()
        reset_pw_form.show()
        reset_pw_form.exec_()

    def on_sign_up_btn_clicked(self):
        self.hide()
        self.signup.show()
        self.signup.exec_()

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
            self.settings.setValue("showMain", True)

            window = Plt_application()
            showLoginSig2 = window.showLoginSig2
            showLoginSig2.connect(self.show_hide_login)
            window.show()
        else:
            QMessageBox.critical(self, 'Login Failed', mess.PW_WRONG)
            return

    def closeEvent(self, event):
        QApplication.quit()

# -------------------------------------------------------------------------------------------------------------
""" Tab Layout """

class TabWidget(QWidget):

    dbConn = lite.connect(var.DB_PATH)
    showMainSig = pyqtSignal(bool)
    showLoginSig = pyqtSignal(bool)

    def __init__(self, username, package, parent=None):

        super(TabWidget, self).__init__(parent)

        self.username = username
        self.package = package

        self.setContentsMargins(0,0,0,0)
        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

        self.layout = QVBoxLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        # Create tab layout
        # ------------------------------------------------------
        self.tabs = QTabWidget()

        self.tab1 = self.tab1Layout()
        self.tabs.addTab(self.tab1, 'Tool')

        self.tab2 = self.tab2Layout()
        self.tabs.addTab(self.tab2, 'Prj')

        self.tab3 = self.tab3Layout()
        self.tabs.addTab(self.tab3, 'User')

        self.tab4 = QGroupBox()
        self.tab4Layout()
        self.tabs.addTab(self.tab4, 'Lib')

        userClass = usql.query_userClass(self.username)
        if userClass == 'Administrator Privilege':
            self.tab5 = QGroupBox()
            self.tab5Layout()
            self.tabs.addTab(self.tab5, 'DB')

        self.layout.addWidget(self.tabs)

    def tab1Layout(self):
        tab1Widget = QWidget()
        tab1layout = QHBoxLayout()
        tab1Widget.setLayout(tab1layout)

        tab1Section1GrpBox = QGroupBox('Dev')
        tab1Section1Grid = QGridLayout()
        tab1Section1GrpBox.setLayout(tab1Section1Grid)

        for key in APPINFO:
            if key == 'PyCharm':
                pycharmBtn = self.make_icon_btn2('PyCharm')
                tab1Section1Grid.addWidget(pycharmBtn, 0, 0, 1, 1)
            if key == 'SublimeText 3':
                sublimeBtn = self.make_icon_btn2('SublimeText 3')
                tab1Section1Grid.addWidget(sublimeBtn, 1, 0, 1, 1)
            if key == 'QtDesigner':
                qtdesignerBtn = self.make_icon_btn2('QtDesigner')
                tab1Section1Grid.addWidget(qtdesignerBtn, 2, 0, 1, 1)

        tab1Section2GrpBox = QGroupBox('Extra')
        tab1Section2Grid = QGridLayout()
        tab1Section2GrpBox.setLayout(tab1Section2Grid)

        arIconBtn = self.make_icon_btn2('Advance Renamer')
        noteReminderBtn = self.make_icon_btn1('QtNote', 'Note Reminder', self.note_reminder)
        textEditorBtn = self.make_icon_btn1('Text Editor', 'Text Editor', self.text_editor)
        dictBtn = self.make_icon_btn1('English Dictionary', 'English Dictionary', self.english_dictionary)
        screenshotBtn = self.make_icon_btn1('Screenshot', 'Screenshot', self.make_screen_shot)
        calendarBtn = self.make_icon_btn1('Calendar', 'Calendar', self.calendar)
        calculatorBtn = self.make_icon_btn1('Calculator', 'Calculator', self.calculator)
        fileFinderBtn = self.make_icon_btn1('Finder', 'Find files', self.findFiles)

        tab1Section2Grid.addWidget(arIconBtn, 0, 0, 1, 1)
        tab1Section2Grid.addWidget(noteReminderBtn, 0, 1, 1, 1)
        tab1Section2Grid.addWidget(textEditorBtn, 0, 2, 1, 1)
        tab1Section2Grid.addWidget(dictBtn, 1, 0, 1, 1)
        tab1Section2Grid.addWidget(screenshotBtn, 1, 1, 1, 1)
        tab1Section2Grid.addWidget(calendarBtn, 1, 2, 1, 1)
        tab1Section2Grid.addWidget(calculatorBtn, 2, 0, 1, 1)
        tab1Section2Grid.addWidget(fileFinderBtn, 2, 1, 1, 1)

        tab1Section3GrpBox = QGroupBox('CGI')
        tab1Section3Grid = QGridLayout()
        tab1Section3GrpBox.setLayout(tab1Section3Grid)

        if key == 'Mudbox 2018':
            mudbox18Btn = self.make_icon_btn2(key)
            tab1Section3Grid.addWidget(mudbox18Btn, 2, 0, 1, 1)
        if key == 'Mudbox 2017':
            mudbox17Btn = self.make_icon_btn2(key)
            tab1Section3Grid.addWidget(mudbox17Btn, 2, 1, 1, 1)
        if key == '3ds Max 2018':
            max18Btn = self.make_icon_btn2(key)
            tab1Section3Grid.addWidget(max18Btn, 2, 2, 1, 1)
        if key == '3ds Max 2017':
            max17Btn = self.make_icon_btn2(key)
            tab1Section3Grid.addWidget(max17Btn, 3, 0, 1, 1)

        tab1layout.addWidget(tab1Section1GrpBox)
        tab1layout.addWidget(tab1Section2GrpBox)
        tab1layout.addWidget(tab1Section3GrpBox)

        return tab1Widget

    def tab2Layout(self):
        # Create Layout for Tab 2.
        tab2Widget = QWidget()
        tab2layout = QHBoxLayout()
        tab2Widget.setLayout(tab2layout)

        tab2Section1GrpBox = QGroupBox('Proj')
        tab2Section1Grid = QGridLayout()
        tab2Section1GrpBox.setLayout(tab2Section1Grid)

        newProjBtn = QPushButton('New Project')
        newProjBtn.clicked.connect(self.on_newProjBtbn_clicked)
        newGrpBtn = QPushButton('New Group')
        newGrpBtn.clicked.connect(self.on_newGrpBtn_clicked)
        prjLstBtn = QPushButton('Your Projects')
        prjLstBtn.clicked.connect(self.on_prjLstBtn_clicked)

        tab2Section1Grid.addWidget(newProjBtn, 0, 0, 1, 2)
        tab2Section1Grid.addWidget(newGrpBtn, 1, 0, 1, 2)
        tab2Section1Grid.addWidget(prjLstBtn, 2, 0, 1, 2)

        tab2Section2GrpBox = QGroupBox('Crew')
        tab2Section2Grid = QGridLayout()
        tab2Section2GrpBox.setLayout(tab2Section2Grid)

        recruitBtn = QPushButton('Find crew')
        recruitBtn.clicked.connect(self.on_recruitBtn_clicked)
        getCrewBtn = QPushButton('Get crew')
        getCrewBtn.clicked.connect(self.on_getCrewBtn_clicked)
        crewLstBtn = QPushButton('Your crew')
        crewLstBtn.clicked.connect(self.on_crewLstBtn_clicked)
        tab2Section2Grid.addWidget(recruitBtn, 0, 0, 1, 2)
        tab2Section2Grid.addWidget(getCrewBtn, 1, 0, 1, 2)
        tab2Section2Grid.addWidget(crewLstBtn, 2, 0, 1, 2)

        tab2Section3GrpBox = QGroupBox('Com')
        tab2Section3Grid = QGridLayout()
        tab2Section3GrpBox.setLayout(tab2Section3Grid)

        tab2Section3Grid.addWidget(QLabel(""), 0, 0, 1, 2)

        tab2layout.addWidget(tab2Section1GrpBox)
        tab2layout.addWidget(tab2Section2GrpBox)
        tab2layout.addWidget(tab2Section3GrpBox)

        return tab2Widget

    def tab3Layout(self):
        # Create Layout for Tab 3.
        tab3Widget = QWidget()
        tab3layout = QHBoxLayout()
        tab3Widget.setLayout(tab3layout)

        tab3Section1GrpBox = QGroupBox(self.username)
        tab3Section1Grid = QGridLayout()
        tab3Section1GrpBox.setLayout(tab3Section1Grid)

        self.userAvatar = QLabel()
        self.userAvatar.setPixmap(QPixmap.fromImage(QImage(func.get_avatar(self.username))))
        self.userAvatar.setScaledContents(True)
        self.userAvatar.setFixedSize(100, 100)
        tab3Section1Grid.addWidget(self.userAvatar, 0, 0, 2, 2)

        tab3Section2GrpBox = QGroupBox("Account Setting")
        tab3Section2Grid = QGridLayout()
        tab3Section2GrpBox.setLayout(tab3Section2Grid)

        userSettingBtn = QPushButton('Account Setting')
        userSettingBtn.clicked.connect(self.on_userSettingBtn_clicked)

        signOutBtn = QPushButton('Log Out')
        signOutBtn.clicked.connect(self.on_signOutBtn_clicked)

        tab3Section2Grid.addWidget(userSettingBtn, 0, 2, 1, 4)
        tab3Section2Grid.addWidget(signOutBtn, 1, 2, 1, 4)

        tab3layout.addWidget(tab3Section1GrpBox)
        tab3layout.addWidget(tab3Section2GrpBox)

        return tab3Widget

    def tab4Layout(self):
        # Create Layout for Tab 4.
        self.tab4.setTitle('Library')

        hboxLayout = QHBoxLayout()
        tab4ridLayout = QGridLayout()

        tab4ridLayout.addWidget(QLabel('Update later'), 0, 0)

        hboxLayout.addLayout(tab4ridLayout)
        self.tab4.setLayout(hboxLayout)

    def tab5Layout(self):
        # Create Layout for Tab 4
        self.tab5.setTitle('SQL')
        hboxLayout = QHBoxLayout()
        tab5GridLayout = QGridLayout()

        dataBrowserIconBtn = self.make_icon_btn2('Database Browser')
        tab5GridLayout.addWidget(dataBrowserIconBtn)

        hboxLayout.addLayout(tab5GridLayout)
        self.tab5.setLayout(hboxLayout)

    def update_avatar(self, param):
        self.userAvatar.setPixmap(QPixmap.fromImage(QImage(param)))
        self.userAvatar.update()

    def make_icon_btn1(self, iconName, tooltip, func_tool):
        icon = QIcon(func.get_icon(iconName))
        iconBtn = QPushButton()
        iconBtn.setToolTip(tooltip)
        iconBtn.setIcon(icon)
        iconBtn.setFixedSize(30, 30)
        iconBtn.setIconSize(QSize(30 - 3, 30 - 3))
        iconBtn.clicked.connect(func_tool)
        return iconBtn

    def make_icon_btn2(self, name):
        icon = QIcon(APPINFO[name][1])
        iconBtn = QPushButton()
        iconBtn.setToolTip(APPINFO[name][0])
        iconBtn.setIcon(icon)
        iconBtn.setFixedSize(30, 30)
        iconBtn.setIconSize(QSize(30 - 3, 30 - 3))
        iconBtn.clicked.connect(partial(self.open_applicaton, APPINFO[name][2]))
        return iconBtn

    def open_applicaton(self, pth):
        subprocess.Popen(pth)

    def english_dictionary(self):
        from ui import ui_english_dict
        EngDict = ui_english_dict.EnglishDict()
        EngDict.exec_()

    def make_screen_shot(self):
        from ui import ui_screenshot
        dlg = ui_screenshot.Screenshot()
        dlg.exec_()

    def calendar(self):
        from ui import ui_calendar
        dlg = ui_calendar.Calendar()
        dlg.exec_()

    def calculator(self):
        from ui import ui_calculator
        dlg = ui_calculator.Calculator()
        dlg.exec_()

    def findFiles(self):
        from ui import ui_find_files
        dlg = ui_find_files.Findfiles()
        dlg.exec_()

    def note_reminder(self):
        from ui import ui_note_reminder
        window = ui_note_reminder.WindowDialog()
        window.exec_()

    def text_editor(self):
        from ui.textedit import textedit
        window = textedit.WindowDialog()
        window.exec_()

    def on_newProjBtbn_clicked(self):
        from ui import ui_new_project
        window = ui_new_project.NewProject()
        window.exec_()

    def on_newGrpBtn_clicked(self):
        pass

    def on_prjLstBtn_clicked(self):
        pass

    def on_recruitBtn_clicked(self):
        pass

    def on_getCrewBtn_clicked(self):
        pass

    def on_crewLstBtn_clicked(self):
        pass

    def on_userSettingBtn_clicked(self):
        user_setting_layout = ui_acc_setting.Account_setting()
        user_setting_layout.show()
        sig = user_setting_layout.changeAvatarSignal
        sig.connect(self.update_avatar)
        user_setting_layout.exec_()

    def on_signOutBtn_clicked(self):
        self.settings.setValue("showMain", False)
        self.showMainSig.emit(False)
        self.showLoginSig.emit(True)

# -------------------------------------------------------------------------------------------------------------
""" Pipeline Tool main layout """

class Plt_application(QMainWindow):

    showLoginSig2 = pyqtSignal(bool)

    def __init__(self, login=None, parent=None):

        super(Plt_application, self).__init__(parent)

        username, rememberLogin = pltp.preset5_query_user_info()

        self.mainID = var.PLT_ID
        self.appInfo = APPINFO
        self.package = var.PLT_PKG
        self.message = var.PLT_MESS
        self.url = var.PLT_URL

        self.setWindowTitle(self.mainID['Main'])
        self.setWindowIcon(QIcon(func.get_icon('Logo')))
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setContentsMargins(0, 0, 0, 0)

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

        self.trayIcon = self.sys_tray_icon_menu()
        self.trayIcon.setToolTip(__appname__)
        self.trayIcon.show()
        self.trayIcon.activated.connect(self.sys_tray_icon_activated)

        if login == 'Auto login':
            icon = QSystemTrayIcon.Information
            self.trayIcon.showMessage('Welcome', "Log in as %s" % username, icon, 1000)
        else:
            icon = QSystemTrayIcon.Information
            self.trayIcon.showMessage('Welcome', "Log in as %s" % username, icon, 1000)

        # Build UI
        self.buildUI()

        # Tabs build
        self.tabWidget = TabWidget(username, self.package)
        showMainSig = self.tabWidget.showMainSig
        showLoginSig = self.tabWidget.showLoginSig

        showMainSig.connect(self.show_hide_main)
        showLoginSig.connect(self.send_to_login)

        self.setCentralWidget(self.tabWidget)

        self.showMainUI = func.str2bool(self.settings.value("showMain", True))
        self.show_hide_main(self.showMainUI)

        # Log record
        # self.procedures('log in')

    def buildUI(self):

        self.layout = self.setGeometry(300, 300, 400, 350)

        # Status bar viewing message
        self.statusBar().showMessage(self.message['status'])
        # ----------------------------------------------
        # Menu Tool Bar sections
        menubar = self.menuBar()

        # ----------------------------------------------
        # File menu
        fileMenu = menubar.addMenu('File')
        exitAction, prefAction = self.fileMenuToolBar()
        separator1 = self.createSeparatorAction()
        fileMenu.addAction(prefAction)
        fileMenu.addAction(separator1)
        fileMenu.addAction(exitAction)

        # ----------------------------------------------
        # Tools menu
        toolMenu = menubar.addMenu('Tools')
        cleanPycAction, reconfigaction = self.toolMenuToolBar()
        toolMenu.addAction(cleanPycAction)
        toolMenu.addAction(reconfigaction)

        # ----------------------------------------------
        # Help menu
        helpMenu = menubar.addMenu('Help')
        aboutAction, creditAction, helpAction = self.helpMenuToolBar()
        helpMenu.addAction(aboutAction)
        helpMenu.addAction(creditAction)
        helpMenu.addAction(helpAction)

        # ----------------------------------------------

        self.tdToolBar = self.toolBarTD()
        self.compToolBar = self.toolBarComp()
        self.artToolBar = self.toolBarArt()
        # self.addToolBar(Qt.LeftToolBarArea, self.tdToolBar)
        # self.addToolBar(Qt.LeftToolBarArea, self.artToolBar)

        # Load Setting
        self.showTDToolBar = func.str2bool(self.settings.value("showTDToolbar", True))
        self.showCompToolBar = func.str2bool(self.settings.value("showCompToolbar", True))
        self.showArtToolBar = func.str2bool(self.settings.value("showArtToolbar", True))

        self.tdToolBar.setVisible(self.showTDToolBar)
        self.compToolBar.setVisible(self.showCompToolBar)
        self.artToolBar.setVisible(self.showArtToolBar)

    def sys_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.showNormal()

    def sys_tray_icon_menu(self):
        trayIconMenu = QMenu(self)

        snippingAction = self.createAction(self.appInfo, 'Snipping Tool')
        trayIconMenu.addAction(snippingAction)

        screenshoticon = QIcon(func.get_icon('Screenshot'))
        screenshotAction = QAction(screenshoticon, "Screenshot", self)
        screenshotAction.triggered.connect(func.screenshot)
        trayIconMenu.addAction(screenshotAction)

        maximizeIcon = QIcon(func.get_icon("Maximize"))
        maximizeAction = QAction(maximizeIcon, "Maximize", self)
        maximizeAction.triggered.connect(self.showMaximized)
        trayIconMenu.addSeparator()
        trayIconMenu.addAction(maximizeAction)

        minimizeIcon = QIcon(func.get_icon('Minimize'))
        minimizeAction = QAction(minimizeIcon, "Minimize", self)
        minimizeAction.triggered.connect(self.hide)
        trayIconMenu.addAction(minimizeAction)

        restoreIcon = QIcon(func.get_icon('Restore'))
        restoreAction = QAction(restoreIcon, "Restore", self)
        restoreAction.triggered.connect(self.showNormal)
        trayIconMenu.addAction(restoreAction)

        quitIcon = QIcon(func.get_icon('Close'))
        quitAction = QAction(quitIcon, "Quit", self)
        quitAction.triggered.connect(self.exit_action_trigger)
        trayIconMenu.addSeparator()
        trayIconMenu.addAction(quitAction)

        trayIcon = QSystemTrayIcon(self)
        trayIcon.setIcon(QIcon(func.get_icon('Logo')))
        trayIcon.setContextMenu(trayIconMenu)

        return trayIcon

    def fileMenuToolBar(self):
        # Preferences
        prefAction = QAction(QIcon(func.get_icon('Preferences')), 'Preferences', self)
        prefAction.setStatusTip('Preferences')
        prefAction.triggered.connect(self.preferences_action_triggered)

        # Exit action
        exitAction = QAction(QIcon(self.appInfo['Exit'][1]), self.appInfo['Exit'][0], self)
        exitAction.setStatusTip(self.appInfo['Exit'][0])
        exitAction.triggered.connect(self.exit_action_trigger)
        return exitAction, prefAction

    def toolMenuToolBar(self):
        cleanaction = QAction(QIcon(self.appInfo['CleanPyc'][1]), self.appInfo['CleanPyc'][0], self)
        cleanaction.setStatusTip(self.appInfo['CleanPyc'][0])
        cleanaction.triggered.connect(partial(func.clean_unnecessary_file, '.pyc'))

        reconfigaction = QAction(QIcon(self.appInfo['ReConfig'][1]), self.appInfo['ReConfig'][0], self)
        reconfigaction.setStatusTip(self.appInfo['ReConfig'][0])
        reconfigaction.triggered.connect(func.Collect_info)

        return cleanaction, reconfigaction

    def helpMenuToolBar(self):
        # About action
        about = QAction(QIcon(self.appInfo['About'][1]), self.appInfo['About'][0], self)
        about.setStatusTip(self.appInfo['About'][0])
        about.triggered.connect(partial(self.info_layout, self.mainID['About'], self.message['About'], self.appInfo['About'][1]))
        # Credit action
        credit = QAction(QIcon(self.appInfo['Credit'][1]), self.appInfo['Credit'][0], self)
        credit.setStatusTip(self.appInfo['Credit'][0])
        credit.triggered.connect(partial(self.info_layout, self.mainID['Credit'], self.message['Credit'], self.appInfo['Credit'][1]))
        # Help action
        helpAction = QAction(QIcon(self.appInfo['Help'][1]), self.appInfo['Help'][0], self)
        helpAction.setStatusTip((self.appInfo['Help'][0]))
        helpAction.triggered.connect(partial(self.open_browser, self.url['Help']))
        return about, credit, helpAction

    def toolBarTD(self):
        # TD Tool Bar
        toolBarTD = self.addToolBar('TD')

        # Maya_tk 2017
        if 'Maya 2018' in self.appInfo:
            maya2017 = self.createAction(self.appInfo, 'Maya 2017')
            toolBarTD.addAction(maya2017)
        # Maya_tk 2017
        if 'Maya 2017' in self.appInfo:
            maya2017 = self.createAction(self.appInfo, 'Maya 2017')
            toolBarTD.addAction(maya2017)

        # ZBrush 4R8
        if 'ZBrush 4R8' in self.appInfo:
            zbrush4R8 = self.createAction(self.appInfo, 'ZBrush 4R8')
            toolBarTD.addAction(zbrush4R8)
        # ZBrush 4R7
        if 'ZBrush 4R7' in self.appInfo:
            zbrush4R7 = self.createAction(self.appInfo, 'ZBrush 4R7')
            toolBarTD.addAction(zbrush4R7)

        # Houdini FX
        if 'Houdini FX' in self.appInfo:
            houdiniFX = self.createAction(self.appInfo, 'Houdini FX')
            toolBarTD.addAction(houdiniFX)

        # Mari
        if 'Mari' in self.appInfo:
            mari = self.createAction(self.appInfo, 'Mari')
            toolBarTD.addAction(mari)

        # return Tool Bar
        return toolBarTD

    def toolBarComp(self):
        # VFX toolBar
        toolBarComp = self.addToolBar('VFX')

        # Davinci
        if 'Resolve' in self.appInfo:
            davinci = self.createAction(self.appInfo, 'Resolve')
            toolBarComp.addAction(davinci)

        # NukeX
        if 'NukeX' in self.appInfo:
            nukeX = self.createAction(self.appInfo, 'NukeX')
            toolBarComp.addAction(nukeX)

        # Hiero
        if 'Hiero' in self.appInfo:
            hiero = self.createAction(self.appInfo, 'Hiero')
            toolBarComp.addAction(hiero)

        # After Effect CC
        if 'After Effects CC' in self.appInfo:
            aeCC = self.createAction(self.appInfo, 'After Effects CC')
            toolBarComp.addAction(aeCC)

        # After Effect CS6
        if 'After Effects CS6' in self.appInfo:
            aeCS6 = self.createAction(self.appInfo, 'After Effects CS6')
            toolBarComp.addAction(aeCS6)

        # Premiere CC
        if 'Premiere Pro CC' in self.appInfo:
            prCC = self.createAction(self.appInfo, 'Premiere Pro CC')
            toolBarComp.addAction(prCC)

        # Premiere CS6
        if 'Premiere Pro CS6' in self.appInfo:
            prCS6 = self.createAction(self.appInfo, 'Premiere Pro CS6')
            toolBarComp.addAction(prCS6)

        # Return Tool Bar
        return toolBarComp

    def toolBarArt(self):
        toolbarArt = self.addToolBar('Art')

        if 'Photoshop CC' in self.appInfo:
            ptsCS6 = self.createAction(self.appInfo, 'Photoshop CC')
            toolbarArt.addAction(ptsCS6)

        # Photoshop CS6
        if 'Photoshop CS6' in self.appInfo:
            ptsCC = self.createAction(self.appInfo, 'Photoshop CS6')
            toolbarArt.addAction(ptsCC)

        # Illustrator CC
        if 'Illustrator CC' in self.appInfo:
            illusCC = self.createAction(self.appInfo, 'Illustrator CC')
            toolbarArt.addAction(illusCC)

        # Illustrator CS6
        if 'Illustrator CS6' in self.appInfo:
            illusCS6 = self.createActioin(self.appInfo, 'Illustrator CS6')
            toolbarArt.addAction(illusCS6)

        return toolbarArt

    def procedures(self, eventlog):
        pass
        # usql.insert_timeLog(eventlog)

    def createAction(self, appInfo, key):
        action = QAction(QIcon(appInfo[key][1]), appInfo[key][0], self)
        action.setStatusTip(appInfo[key][0])
        action.triggered.connect(partial(self.openApplication, appInfo[key][2]))
        return action

    def createSeparatorAction(self):
        separator = QAction(QIcon(self.appInfo['Sep'][0]), self.appInfo['Sep'][1], self)
        separator.setSeparator(True)
        return separator

    def openApplication(self, path):
        subprocess.Popen(path)

    def info_layout(self, id='Note', message=" ", icon=func.get_icon('Logo')):
        from ui import ui_info_template
        dlg = ui_info_template.About_plt_layout(id=id, message=message, icon=icon)
        dlg.exec_()

    def open_browser(self, url):
        webbrowser.open(url)

    def preferences_action_triggered(self):
        dlg = ui_preference.Pref_layout()
        dlg.show()
        sigTD = dlg.checkboxTDSig
        sigComp = dlg.checkboxCompSig
        sigArt = dlg.checkboxArtSig
        sigTD.connect(self.show_hide_TDtoolBar)
        sigComp.connect(self.show_hide_ComptoolBar)
        sigArt.connect(self.show_hide_ArttoolBar)
        dlg.exec_()

    def show_hide_TDtoolBar(self, param):
        self.tdToolBar.setVisible(param)
        self.settings.setValue("showTDToolbar", func.bool2str(param))

    def show_hide_ComptoolBar(self, param):
        self.compToolBar.setVisible(param)
        self.settings.setValue("showCompToolbar", func.bool2str(param))

    def show_hide_ArttoolBar(self, param):
        self.artToolBar.setVisible(param)
        self.settings.setValue("showArtToolbar", func.bool2str(param))

    def show_hide_main(self, param):
        param = func.str2bool(param)
        if not param:
            self.trayIcon.hide()
            self.close()
        else:
            self.trayIcon.show()
            self.show()

    def send_to_login(self, param):
        self.settings.setValue("showLogin", param)
        self.showLoginSig2.emit(param)

    def exit_action_trigger(self):
        # self.procedures("Log out")
        logger.debug("LOG OUT")
        QApplication.instance().quit()

    def closeEvent(self, event):
        icon = QSystemTrayIcon.Information
        self.trayIcon.showMessage('Notice', "Pipeline Tool will keep running in the system tray.", icon, 1000)
        self.hide()
        event.ignore()

# -------------------------------------------------------------------------------------------------------------
""" Operation """

def main():

    usql.query_userData()

    QCoreApplication.setApplicationName(__appname__)
    QCoreApplication.setApplicationVersion(__version__)
    QCoreApplication.setOrganizationName(__organization__)
    QCoreApplication.setOrganizationDomain(__website__)

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(func.get_icon('Logo')))
    app.setStyleSheet(qdarkgraystyle.load_stylesheet_pyqt5())

    username, token, cookie = usql.query_user_session()

    r = requests.get("https://pipeline.damgteam.com/check", verify = False,
                     headers={'Authorization': 'Bearer {token}'.format(token=token)}, cookies={'connect.sid': cookie})

    if r.status_code == 200:
        window = Plt_application()
        window.show()
        if not QSystemTrayIcon.isSystemTrayAvailable():
            QMessageBox.critical(None, mess.SYSTRAY_UNAVAI)
            sys.exit(1)
    else:
        login = Plt_sign_in()
        login.show()

    QApplication.setQuitOnLastWindowClosed(False)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

# ----------------------------------------------------------------------------