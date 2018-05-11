#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: Plt.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This script is master file of Pipeline Tool

"""
# -------------------------------------------------------------------------------------------------------------
""" Check data flowing """
# print("Import from modules: {file}".format(file=__name__))
# print("Directory: {path}".format(path=__file__.split(__name__)[0]))
__root__ = "PLT_RT"
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import pychecker
import os, sys, logging, subprocess, webbrowser, requests
import sqlite3 as lite
from functools import partial

# PyQt5
from PyQt5.QtCore import Qt, QSize, QCoreApplication, QSettings, pyqtSignal, QByteArray
from PyQt5.QtGui import QIcon, QPixmap, QImage, QIntValidator, QFont
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFrame, QDialog, QWidget, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QLineEdit, QLabel, QPushButton, QMessageBox, QGroupBox,
                             QCheckBox, QTabWidget, QSystemTrayIcon, QAction, QMenu, QFileDialog, QComboBox,
                             QDockWidget, QSlider, QSizePolicy, QStackedWidget, QStackedLayout)

# -------------------------------------------------------------------------------------------------------------
""" Set up env variable path """

os.environ[__root__] = os.getcwd()

# -------------------------------------------------------------------------------------------------------------
""" Stylesheet plugin """
import qdarkgraystyle

from __init__ import (__root__, __appname__, __version__, __organization__, __website__)

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
from ui import (ui_acc_setting, ui_preference)

from utilities import utils as func
from utilities import sql_local as usql
from utilities import message as mess
from utilities import variables as var

func.preset_maya_intergrate()

# -------------------------------------------------------------------------------------------------------------
""" Variables """

# String
TXT = "No Text" # String by default

# Value, Nummber, Float, Int ...
UNIT = 60   # Base Unit
MARG = 5    # Content margin
BUFF = 10   # Buffer size
SCAL = 1    # Scale value
STEP = 1    # Step value changing
VAL = 1     # Default value
MIN = 0     # Minimum value
MAX = 1000  # Maximum value
WMIN = 50   # Minimum width
HMIN = 20   # Minimum height

# Alignment
ALGC = Qt.AlignCenter
ALGR = Qt.AlignRight
ALGL = Qt.AlignLeft
HORZ = Qt.Horizontal
VERT = Qt.Vertical

# Style
frameStyle = QFrame.Sunken | QFrame.Panel


# -------------------------------------------------------------------------------------------------------------
# Get apps info config
APPINFO = func.preset_load_appInfo()
ICONINFO = func.preset_load_iconInfo()

def Clabel(txt=TXT, wmin=WMIN, alg = None, font=None):
    if alg == None:
        alg = Qt.AlignCenter

    if font == None:
        font = QFont({"Arial, 10"})

    label = QLabel(txt)
    label.setMinimumWidth(wmin)
    label.setAlignment(alg)
    label.setFont(font)
    return label

class pltSlider(QVBoxLayout):

    def __init__(self, txt=TXT, val=VAL, axe=None, parent=None):
        super(pltSlider, self).__init__(parent)

        if axe == None:
            axe = HORZ

        self.val = val
        self.slider = QSlider(axe)
        self.slider.setWindowTitle(txt)
        self.addWidget(self.slider)

    def slider_value(self):
        self.slider.setMinimum(MIN)
        self.slider.setMaximum(MAX)
        self.slider.setSingleStep(STEP)
        self.slider.setValue(self.val)

class SliderWidget(QWidget):

    valueChangeSig = pyqtSignal(float)

    def __init__(self, txt=TXT, val=VAL, axe=HORZ, parent=None):
        super(SliderWidget, self).__init__(parent)

        self.val = val
        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

        self.layout = QGridLayout()

        self.slider = QSlider(axe)
        self.slider.setWindowTitle(txt)

        self.slider.setMinimum(MIN)
        self.slider.setMaximum(MAX)
        self.slider.setSingleStep(STEP)
        self.slider.setValue(self.val)

        self.numField = QLineEdit()
        self.numField.setValidator(QIntValidator(0, 999, self))
        self.numField.setText("0")
        self.numField.setText(str(self.val))

        self.slider.valueChanged.connect(self.set_value)
        self.numField.textChanged.connect(self.set_slider)

        # self.layout.addWidget(pltLabel("Unit: "), 0, 0, 1, 1)
        self.layout.addWidget(self.numField, 0, 0, 1, 1)
        self.layout.addWidget(self.slider, 0, 1, 1, 2)

        self.setLayout(self.layout)

    def set_value(self):
        val = self.slider.value()
        self.numField.setText(str(val))

    def set_slider(self):
        val = self.numField.text()
        if val == "" or val == None:
            val = "0"
        self.slider.setValue(float(val))

    def changeEvent(self, event):
        self.settings.setValue("{name}Value".format(name=self.txt), float)
        self.valueChangeSig.emit(self.slider.value())

class UnitSetting(QWidget):

    stepChangeSig = pyqtSignal(float)
    valueChangeSig = pyqtSignal(float)
    minChangeSig = pyqtSignal(float)
    maxChangeSig = pyqtSignal(float)

    def __init__(self, parent=None):
        super(UnitSetting, self).__init__(parent)

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.stepVal = QLineEdit("1")
        self.valueVal = QLineEdit("1")
        self.minVal = QLineEdit("0")
        self.maxVal = QLineEdit("1000")

        self.stepVal.setValidator(QIntValidator(0, 999, self))
        self.valueVal.setValidator(QIntValidator(0, 999, self))
        self.minVal.setValidator(QIntValidator(0, 999, self))
        self.maxVal.setValidator(QIntValidator(0, 999, self))

        self.stepVal.textChanged.connect(self.set_step)
        self.valueVal.textChanged.connect(self.set_value)
        self.minVal.textChanged.connect(self.set_min)
        self.maxVal.textChanged.connect(self.set_max)

        self.layout.addWidget(Clabel("STEP: "), 0,0,1,1)
        self.layout.addWidget(Clabel("VALUE: "), 1,0,1,1)
        self.layout.addWidget(Clabel("MIN: "), 2,0,1,1)
        self.layout.addWidget(Clabel("MAX: "), 3,0,1,1)

        self.layout.addWidget(self.stepVal, 0, 1, 1, 1)
        self.layout.addWidget(self.valueVal, 1, 1, 1, 1)
        self.layout.addWidget(self.minVal, 2, 1, 1, 1)
        self.layout.addWidget(self.maxVal, 3, 1, 1, 1)

    def set_step(self):
        val = float(self.stepVal.text())
        self.stepChangeSig.emit(val)
        self.settings.setValue("stepSetting", float)

    def set_value(self):
        val = float(self.valueVal.text())
        self.valueChangeSig.emit(float(val))
        self.settings.setValue("valueSetting", float)

    def set_min(self):
        val = float(self.minVal.text())
        self.minChangeSig.emit(float(val))
        self.settings.setValue("minSetting", float)

    def set_max(self):
        val = float(self.maxVal.text())
        self.maxChangeSig.emit(float(val))
        self.settings.setValue("maxSetting", float)

    def changeEvent(self, event):
        pass

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
        self.avatar_section()
        self.account_section()
        self.profile_section()
        self.location_section()
        self.security_section()
        self.buttons_section()

        self.layout.addWidget(Clabel("ALL FIELD ARE REQUIRED!!!"), 0, 0, 1, 6)
        self.layout.addWidget(self.avaSection, 1, 0, 1, 2)
        self.layout.addWidget(self.accSection, 1, 2, 1, 4)
        self.layout.addWidget(self.prfSection, 2, 0, 1, 6)
        self.layout.addWidget(self.conSection, 3, 0, 1, 6)
        self.layout.addWidget(self.serSection, 4, 0, 1, 6)
        self.layout.addWidget(self.btnSection, 5, 0, 1, 6)

    def avatar_section(self):
        self.avaSection = QGroupBox("Avatar")
        avatar_grid = QGridLayout()
        self.avaSection.setLayout(avatar_grid)

        defaultImg = QPixmap.fromImage(QImage(func.get_avatar('default')))
        self.userAvatar = QLabel()
        self.userAvatar.setPixmap(defaultImg)
        self.userAvatar.setScaledContents(True)
        self.userAvatar.setFixedSize(100, 100)

        set_avatarBtn = QPushButton("Set Avatar")
        set_avatarBtn.clicked.connect(self.on_set_avatar_btn_clicked)

        avatar_grid.addWidget(self.userAvatar, 0, 0, 2, 2)
        avatar_grid.addWidget(set_avatarBtn, 2, 0, 1, 2)

    def account_section(self):
        self.accSection = QGroupBox("Account")
        account_grid = QGridLayout()
        self.accSection.setLayout(account_grid)

        account_grid.addWidget(Clabel('User Name'), 0, 0, 1, 2)
        account_grid.addWidget(Clabel('Password'), 1, 0, 1, 2)
        account_grid.addWidget(Clabel('Confirm Password'), 2, 0, 1, 2)

        self.userField = QLineEdit()
        self.pwField = QLineEdit()
        self.cfpwField = QLineEdit()

        self.pwField.setEchoMode(QLineEdit.Password)
        self.cfpwField.setEchoMode(QLineEdit.Password)

        account_grid.addWidget(self.userField, 0, 3, 1, 4)
        account_grid.addWidget(self.pwField, 1, 3, 1, 4)
        account_grid.addWidget(self.cfpwField, 2, 3, 1, 4)

    def profile_section(self):
        self.prfSection = QGroupBox("Profile")
        profile_grid = QGridLayout()
        self.prfSection.setLayout(profile_grid)

        profile_grid.addWidget(Clabel('First Name'), 0, 0, 1, 2)
        profile_grid.addWidget(Clabel('Last Name'), 1, 0, 1, 2)
        profile_grid.addWidget(Clabel('Your Title'), 2, 0, 1, 2)
        profile_grid.addWidget(Clabel('Email'), 3, 0, 1, 2)
        profile_grid.addWidget(Clabel('Phone Number'), 4, 0, 1, 2)

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

    def location_section(self):
        self.conSection = QGroupBox("Location")
        conGrid = QGridLayout()
        self.conSection.setLayout(conGrid)

        conGrid.addWidget(Clabel("Address Line 1"), 0, 0, 1, 2)
        conGrid.addWidget(Clabel("Address Line 2"), 1, 0, 1, 2)
        conGrid.addWidget(Clabel("Postal"), 2, 0, 1, 2)
        conGrid.addWidget(Clabel("City"), 3, 0, 1, 2)
        conGrid.addWidget(Clabel("Country"), 4, 0, 1, 2)

        self.addressLine1 = QLineEdit()
        self.addressLine2 = QLineEdit()
        self.postalCode = QLineEdit()
        self.city = QLineEdit()
        self.country = QLineEdit()

        conGrid.addWidget(self.addressLine1, 0, 2, 1, 4)
        conGrid.addWidget(self.addressLine2, 1, 2, 1, 4)
        conGrid.addWidget(self.city, 2, 2, 1, 4)
        conGrid.addWidget(self.postalCode, 3, 2, 1, 4)
        conGrid.addWidget(self.country, 4, 2, 1, 4)

    def security_section(self):

        self.serSection = QGroupBox("Security Question")
        questions_grid = QGridLayout()
        self.serSection.setLayout(questions_grid)

        self.ques1 = QComboBox()
        self.answ2 = QLineEdit()
        self.ques2 = QComboBox()
        self.answ1 = QLineEdit()

        questions = usql.query_all_questions()

        for i in questions:
            self.ques1.addItem(str(i[0]))
            self.ques2.addItem(str(i[0]))

        questions_grid.addWidget(Clabel('Question 1'), 0, 0, 1, 3)
        questions_grid.addWidget(Clabel('Answer 1'), 1, 0, 1, 3)
        questions_grid.addWidget(Clabel('Question 2'), 2, 0, 1, 3)
        questions_grid.addWidget(Clabel('Answer 2'), 3, 0, 1, 3)

        questions_grid.addWidget(self.ques1, 0, 3, 1, 6)
        questions_grid.addWidget(self.answ1, 1, 3, 1, 6)
        questions_grid.addWidget(self.ques2, 2, 3, 1, 6)
        questions_grid.addWidget(self.answ2, 3, 3, 1, 6)

    def buttons_section(self):
        self.btnSection = QGroupBox()
        btn_grid = QGridLayout()
        self.btnSection.setLayout(btn_grid)

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
        regInput = self.collect_input()
        if self.check_all_conditions(regInput):
            data = self.generate_user_data()
            usql.create_new_user_data(data)

    def collect_input(self):
        username = str(self.userField.text())
        password = str(self.pwField.text())
        confirm = str(self.cfpwField.text())
        firstname = str(self.firstnameField.text())
        lastname = str(self.lastnameField.text())
        email = str(self.emailField.text())
        phone = str(self.phoneField.text())
        address1 = str(self.addressLine1.text())
        address2 = str(self.addressLine2.text())
        postal = str(self.postalCode.text())
        city = str(self.city.text())
        country = str(self.country.text())
        answer1 = str(self.answ1.text())
        answer2 = str(self.answ2.text())
        return [username, password, confirm, firstname, lastname, email, phone, address1, address2, postal, city,
                country, answer1, answer2]

    def generate_user_data(self):
        regInput = self.collect_input()
        question1 = str(self.ques1.currentText())
        question2 = str(self.ques2.currentText())
        title = str(self.titleField.text()) or "Guess"

        token = func.get_token()
        timelog = func.get_time()
        sysInfo = func.get_local_pc()
        productID = sysInfo['Product ID']
        ip, cityIP, countryIP = func.get_pc_location()
        unix = func.get_unix()
        datelog = func.get_date()
        pcOS = sysInfo['os']
        pcUser = sysInfo['pcUser']
        pcPython = sysInfo['python']

        if not os.path.exists(self.rawAvatarPth):
            avatar = func.get_avatar('default')
        else:
            avatar = self.rawAvatarPth

        data = [regInput[0], regInput[1], regInput[3], regInput[4], title, regInput[5], regInput[6], regInput[7],
                regInput[8], regInput[9], regInput[10], regInput[11], token, timelog, productID, ip, cityIP, countryIP, unix, question1, regInput[12], question2,
                regInput[13], datelog, pcOS, pcUser, pcPython, avatar]
        return data

    def on_cancel_btn_clicked(self):
        self.close()
        self.settings.setValue("showLogin", True)
        self.showLoginSig1.emit(True)

    def check_all_conditions(self):
        if self.check_all_field_blank():
            if self.check_user_agreement():
                if self.check_pw_matching():
                    return True
        return False

    def check_all_field_blank(self):
        regInput = self.collect_input()
        secName = ["Username", "Password", "Confirm Password", "Firstname", "Lastname", "Email", "Phone",
                   "Address line 1", "Address line 2", "Postal", "City", "Country", "Answer 1", "Answer 2"]
        for section in regInput:
            if not func.check_blank(section):
                QMessageBox.critical(self, "Fail", secName[regInput.index(section)] + mess.SEC_BLANK, QMessageBox.Retry)
                return False
        return True

    def check_user_agreement(self):
        return self.user_agree_checkBox.checkState()

    def check_pw_matching(self):
        password = str(self.pwField.text())
        confirm = str(self.cfpwField.text())
        check_pass = func.check_match(password, confirm)
        if not check_pass:
            QMessageBox.critical(self, "Warning", mess.PW_UNMATCH, QMessageBox.Retry)
            return False
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

        login_grid.addWidget(Clabel(text='Username'), 0, 0, 1, 2)
        login_grid.addWidget(Clabel(text='Password'), 1, 0, 1, 2)
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

        signup_grid.addWidget(Clabel(text=mess.SIGN_UP), 0, 0, 1, 6)
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
            if not QSystemTrayIcon.isSystemTrayAvailable():
                QMessageBox.critical(None, mess.SYSTRAY_UNAVAI)
                sys.exit(1)
        else:
            QMessageBox.critical(self, 'Login Failed', mess.PW_WRONG)
            return

    def closeEvent(self, event):
        QApplication.quit()

# -------------------------------------------------------------------------------------------------------------
""" Menu bar Layout """

class MenuBarLayout(QMainWindow):

    showTDSig2 = pyqtSignal(bool)
    showCompSig2 = pyqtSignal(bool)
    showArtSig2 = pyqtSignal(bool)

    def __init__(self, parent=None):

        super(MenuBarLayout, self).__init__(parent)

        self.appInfo = APPINFO
        self.mainID = var.PLT_ID
        self.message = var.PLT_MESS
        self.url = var.PLT_URL

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)
        self.setFixedHeight(30)

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        self.createAction()

        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.prefAct)
        self.fileMenu.addAction(self.separator1)
        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = self.menuBar().addMenu("&View")
        self.viewMenu.addAction(self.viewTDAct)
        self.viewMenu.addAction(self.viewCompAct)
        self.viewMenu.addAction(self.viewArtAct)
        self.viewMenu.addAction(self.viewAllAct)

        self.toolMenu = self.menuBar().addMenu("&Tools")
        self.toolMenu.addAction(self.cleanAct)
        self.toolMenu.addAction(self.reconfigAct)

        self.aboutMenu = self.menuBar().addMenu("&About")
        self.aboutMenu.addAction(self.aboutAct)

        self.creditMenu = self.menuBar().addMenu("&Credit")
        self.creditMenu.addAction(self.creditAct)

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.helpAct)

    def createAction(self):
        # Preferences
        self.prefAct = QAction(QIcon(func.get_icon('Preferences')), 'Preferences', self)
        self.prefAct.setStatusTip('Preferences')
        self.prefAct.triggered.connect(self.preferences_action_triggered)

        # Exit
        self.exitAct = QAction(QIcon(self.appInfo['Exit'][1]), self.appInfo['Exit'][0], self)
        self.exitAct.setStatusTip(self.appInfo['Exit'][0])
        self.exitAct.triggered.connect(self.exit_action_trigger)

        # View TD toolbar
        self.viewTDAct = QAction(QIcon(func.get_icon("")), "hide/view TD tool bar", self)
        viewTDToolBar = func.str2bool(self.settings.value("showTDToolbar", True))
        self.viewTDAct.setChecked(viewTDToolBar)
        self.viewTDAct.triggered.connect(self.show_hide_TDtoolBar)

        # View comp toolbar
        self.viewCompAct = QAction(QIcon(func.get_icon("")), "hide/view Comp tool bar", self)
        viewCompToolBar = func.str2bool(self.settings.value("showCompToolbar", True))

        # self.viewCompAct.setCheckable(True)
        self.viewCompAct.setChecked(viewCompToolBar)
        self.viewCompAct.triggered.connect(self.show_hide_ComptoolBar)

        # View art toolbar
        self.viewArtAct = QAction(QIcon(func.get_icon("")), "hide/view Art tool bar", self)
        viewArtToolBar = func.str2bool(self.settings.value("showArtToolbar", True))

        # self.viewArtAct.setCheckable(True)
        self.viewArtAct.setChecked(viewArtToolBar)
        self.viewArtAct.triggered.connect(self.show_hide_ArttoolBar)

        # View all toolbar
        self.viewAllAct = QAction(QIcon(func.get_icon("Alltoolbar")), "hide/view All tool bar", self)
        viewAllToolbar = func.str2bool(self.settings.value("showAllToolbar", True))

        # self.viewAllAct.setCheckable(True)
        self.viewAllAct.setChecked(viewAllToolbar)
        self.viewAllAct.triggered.connect(self.show_hide_AlltoolBar)

        # Clean trash file
        self.cleanAct = QAction(QIcon(self.appInfo['CleanPyc'][1]), self.appInfo['CleanPyc'][0], self)
        self.cleanAct.setStatusTip(self.appInfo['CleanPyc'][0])
        self.cleanAct.triggered.connect(partial(func.clean_unnecessary_file, '.pyc'))

        # Re-configuration
        self.reconfigAct = QAction(QIcon(self.appInfo['ReConfig'][1]), self.appInfo['ReConfig'][0], self)
        self.reconfigAct.setStatusTip(self.appInfo['ReConfig'][0])
        self.reconfigAct.triggered.connect(func.Collect_info)

        # About action
        self.aboutAct = QAction(QIcon(self.appInfo['About'][1]), self.appInfo['About'][0], self)
        self.aboutAct.setStatusTip(self.appInfo['About'][0])
        self.aboutAct.triggered.connect(partial(self.info_layout, self.mainID['About'], self.message['About'], self.appInfo['About'][1]))

        # Credit action
        self.creditAct = QAction(QIcon(self.appInfo['Credit'][1]), self.appInfo['Credit'][0], self)
        self.creditAct.setStatusTip(self.appInfo['Credit'][0])
        self.creditAct.triggered.connect(partial(self.info_layout, self.mainID['Credit'], self.message['Credit'], self.appInfo['Credit'][1]))

        # Help action
        self.helpAct = QAction(QIcon(self.appInfo['Help'][1]), self.appInfo['Help'][0], self)
        self.helpAct.setStatusTip((self.appInfo['Help'][0]))
        self.helpAct.triggered.connect(partial(webbrowser.open, self.url['Help']))

        # Seperator action
        self.separator1 = QAction(QIcon(self.appInfo['Sep'][0]), self.appInfo['Sep'][1], self)
        self.separator1.setSeparator(True)

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

    def exit_action_trigger(self):
        usql.insert_timeLog("Log out")
        logger.debug("LOG OUT")
        QApplication.instance().quit()

    def show_hide_TDtoolBar(self, param):
        self.showTDSig2.emit(param)

    def show_hide_ComptoolBar(self, param):
        self.showCompSig2.emit(param)

    def show_hide_ArttoolBar(self, param):
        self.showArtSig2.emit(param)

    def show_hide_AlltoolBar(self, param):
        self.show_hide_TDtoolBar(param)
        self.show_hide_ComptoolBar(param)
        self.show_hide_ArttoolBar(param)

    def info_layout(self, id='Note', message="", icon=func.get_icon('Logo')):
        from ui import ui_info_template
        dlg = ui_info_template.About_plt_layout(id=id, message=message, icon=icon)
        dlg.exec_()

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        # menu.addAction(self.cutAct)
        # menu.addAction(self.copyAct)
        # menu.addAction(self.pasteAct)
        menu.exec_(event.globalPos())

# -------------------------------------------------------------------------------------------------------------
""" Tab Layout """

class TabWidget(QWidget):

    dbConn = lite.connect(var.DB_PATH)
    showMainSig = pyqtSignal(bool)
    showLoginSig = pyqtSignal(bool)
    tabSizeSig = pyqtSignal(int, int)

    def __init__(self, username, package, parent=None):

        super(TabWidget, self).__init__(parent)

        self.username = username
        self.package = package
        self.appInfo = APPINFO

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

        self.layout = QVBoxLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        # Create tab layout
        # ------------------------------------------------------
        self.tabs = QTabWidget()

        self.tab1Layout()
        self.tab2Layout()
        self.tab3Layout()
        self.tab4Layout()

        self.tabs.addTab(self.tab1, 'Tool')
        self.tabs.addTab(self.tab2, 'Prj')
        self.tabs.addTab(self.tab3, 'User')
        self.tabs.addTab(self.tab4, 'Lib')

        userClass = usql.query_userClass(self.username)

        if userClass == 'Administrator Privilege':
            self.tab5 = QGroupBox()
            self.tab5Layout()
            self.tabs.addTab(self.tab5, 'DB')

        self.layout.addWidget(self.tabs)

    def tab1Layout(self):

        self.tab1 = QWidget()
        tab1layout = QGridLayout()
        self.tab1.setLayout(tab1layout)

        tab1Sec1GrpBox = QGroupBox('Dev')
        tab1Sec1Grid = QGridLayout()
        tab1Sec1GrpBox.setLayout(tab1Sec1Grid)

        tab1Sec2GrpBox = QGroupBox('cmd')
        tab1Sec2Grid = QGridLayout()
        tab1Sec2GrpBox.setLayout(tab1Sec2Grid)

        tab1Sec3GrpBox = QGroupBox('Custom')
        tab1Sec3Grid = QGridLayout()
        tab1Sec3GrpBox.setLayout(tab1Sec3Grid)

        tab1Sec4GrpBox = QGroupBox('CGI')
        tab1Sec4Grid = QGridLayout()
        tab1Sec4GrpBox.setLayout(tab1Sec4Grid)

        for key in APPINFO:
            if key == 'PyCharm':
                pycharmBtn = self.make_icon_btn2('PyCharm')
                tab1Sec1Grid.addWidget(pycharmBtn, 0, 0, 1, 1)
            if key == 'SublimeText 3':
                sublimeBtn = self.make_icon_btn2('SublimeText 3')
                tab1Sec1Grid.addWidget(sublimeBtn, 0, 1, 1, 1)
            if key == 'QtDesigner':
                qtdesignerBtn = self.make_icon_btn2('QtDesigner')
                tab1Sec1Grid.addWidget(qtdesignerBtn, 0, 2, 1, 1)

            if key == 'Git Bash':
                gitbashIconBtn = self.make_icon_btn2('Git Bash')
                tab1Sec2Grid.addWidget(gitbashIconBtn, 0, 0, 1, 1)
            if key == 'Git CMD':
                gitbashIconBtn = self.make_icon_btn2('Git Bash')
                tab1Sec2Grid.addWidget(gitbashIconBtn, 0, 1, 1, 1)

        arIconBtn = self.make_icon_btn2('Advance Renamer')
        noteReminderBtn = self.make_icon_btn1('QtNote', 'Note Reminder', self.note_reminder)
        textEditorBtn = self.make_icon_btn1('Text Editor', 'Text Editor', self.text_editor)
        dictBtn = self.make_icon_btn1('English Dictionary', 'English Dictionary', self.english_dictionary)
        screenshotBtn = self.make_icon_btn1('Screenshot', 'Screenshot', self.make_screen_shot)
        calendarBtn = self.make_icon_btn1('Calendar', 'Calendar', self.calendar)
        calculatorBtn = self.make_icon_btn1('Calculator', 'Calculator', self.calculator)
        fileFinderBtn = self.make_icon_btn1('Finder', 'Find files', self.findFiles)

        tab1Sec3Grid.addWidget(arIconBtn, 0, 0, 1, 1)
        tab1Sec3Grid.addWidget(noteReminderBtn, 0, 1, 1, 1)
        tab1Sec3Grid.addWidget(textEditorBtn, 0, 2, 1, 1)
        tab1Sec3Grid.addWidget(dictBtn, 1, 0, 1, 1)
        tab1Sec3Grid.addWidget(screenshotBtn, 1, 1, 1, 1)
        tab1Sec3Grid.addWidget(calendarBtn, 1, 2, 1, 1)
        tab1Sec3Grid.addWidget(calculatorBtn, 2, 0, 1, 1)
        tab1Sec3Grid.addWidget(fileFinderBtn, 2, 1, 1, 1)

        for key in APPINFO:
            if key == 'Mudbox 2018':
                mudbox18Btn = self.make_icon_btn2(key)
                tab1Sec4Grid.addWidget(mudbox18Btn, 2, 0, 1, 1)
            if key == 'Mudbox 2017':
                mudbox17Btn = self.make_icon_btn2(key)
                tab1Sec4Grid.addWidget(mudbox17Btn, 2, 1, 1, 1)
            if key == '3ds Max 2018':
                max18Btn = self.make_icon_btn2(key)
                tab1Sec4Grid.addWidget(max18Btn, 2, 2, 1, 1)
            if key == '3ds Max 2017':
                max17Btn = self.make_icon_btn2(key)
                tab1Sec4Grid.addWidget(max17Btn, 3, 0, 1, 1)

        tab1layout.addWidget(tab1Sec1GrpBox, 0,0,1,3)
        tab1layout.addWidget(tab1Sec2GrpBox, 1,0,2,3)
        tab1layout.addWidget(tab1Sec3GrpBox, 0,3,3,3)
        tab1layout.addWidget(tab1Sec4GrpBox, 0,6,3,2)

    def tab2Layout(self):
        # Create Layout for Tab 2.
        self.tab2 = QWidget()
        tab2layout = QHBoxLayout()
        self.tab2.setLayout(tab2layout)

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

    def tab3Layout(self):
        # Create Layout for Tab 3.
        self.tab3 = QWidget()
        tab3layout = QGridLayout()
        self.tab3.setLayout(tab3layout)

        tab3Sec1GrpBox = QGroupBox(self.username)
        tab3Sec1Grid = QGridLayout()
        tab3Sec1GrpBox.setLayout(tab3Sec1Grid)

        self.userAvatar = QLabel()
        self.userAvatar.setPixmap(QPixmap.fromImage(QImage(func.get_avatar(self.username))))
        self.userAvatar.setScaledContents(True)
        self.userAvatar.setFixedSize(100, 100)

        tab3Sec2GrpBox = QGroupBox("Account Setting")
        tab3Sec2Grid = QGridLayout()
        tab3Sec2GrpBox.setLayout(tab3Sec2Grid)

        userSettingBtn = QPushButton('Account Setting')
        userSettingBtn.clicked.connect(self.on_userSettingBtn_clicked)

        signOutBtn = QPushButton('Log Out')
        signOutBtn.clicked.connect(self.on_signOutBtn_clicked)

        tab3Sec1Grid.addWidget(self.userAvatar, 0, 0, 2, 3)
        tab3Sec2Grid.addWidget(userSettingBtn, 0, 2, 1, 5)
        tab3Sec2Grid.addWidget(signOutBtn, 1, 2, 1, 5)

        tab3layout.addWidget(tab3Sec1GrpBox)
        tab3layout.addWidget(tab3Sec2GrpBox)

    def tab4Layout(self):
        # Create Layout for Tab 4.
        self.tab4 = QWidget()
        tab4layout = QGridLayout()
        self.tab4.setLayout(tab4layout)

        tab4Section1GrpBox = QGroupBox('Library')
        tab4Section1Grid = QGridLayout()
        tab4Section1GrpBox.setLayout(tab4Section1Grid)

        tab4Section1Grid.addWidget(Clabel("Update later"), 0, 0, 1, 8)

        tab4layout.addWidget(tab4Section1GrpBox, 0, 0, 1, 8)

    def tab5Layout(self):
        # Create Layout for Tab 4
        tab5Widget = QWidget()
        tab5layout = QHBoxLayout()
        tab5Widget.setLayout(tab5layout)

        tab5Section1GrpBox = QGroupBox('Library')
        tab5Section1Grid = QGridLayout()
        tab5Section1GrpBox.setLayout(tab5Section1Grid)

        dataBrowserIconBtn = self.make_icon_btn1('Database Browser')
        tab5Section1Grid.addWidget(dataBrowserIconBtn, 0, 0, 1, 1)

        tab5layout.addWidget(tab5Section1GrpBox)
        return tab5Widget

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
        for key in APPINFO:
            if name in key:
                name = key

        icon = QIcon(APPINFO[name][1])
        iconBtn = QPushButton()
        iconBtn.setToolTip(APPINFO[name][0])
        iconBtn.setIcon(icon)
        iconBtn.setFixedSize(30, 30)
        iconBtn.setIconSize(QSize(30 - 3, 30 - 3))
        iconBtn.clicked.connect(partial(subprocess.Popen, APPINFO[name][2]))
        return iconBtn

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
        from ui import textedit
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

    def __init__(self, parent=None):
        super(Plt_application, self).__init__(parent)

        self.username, rememberLogin = usql.query_curUser()
        self.mainID = var.PLT_ID
        self.appInfo = APPINFO
        self.iconInfo = ICONINFO
        self.package = var.PLT_PKG
        self.message = var.PLT_MESS
        self.url = var.PLT_URL

        self.setWindowTitle(self.mainID['Main'])
        self.setWindowIcon(QIcon(func.get_icon('Logo')))
        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)
        self.setFixedWidth(400)

        self.trayIcon = self.sys_tray_icon_menu()
        self.trayIcon.setToolTip(__appname__)
        self.trayIcon.show()
        self.trayIcon.activated.connect(self.sys_tray_icon_activated)
        icon = QSystemTrayIcon.Information
        self.trayIcon.showMessage('Welcome', "Log in as %s" % self.username, icon, 500)

        self.mainWidget = QWidget()
        self.buildUI()
        self.setCentralWidget(self.mainWidget)

        # self.showMainUI = func.str2bool(self.settings.value("showMain", True))
        # self.show_hide_main(self.showMainUI)

        # self.layout_magrin_ratio()
        # self.layout_height_ratio()
        # self.layout_width_ratio()

        # self.restoreState(self.settings.value("layoutState", QBitArray()))

        # Log record
        # usql.insert_timeLog('Log in')

    def buildUI(self):

        sizeW, sizeH = self.get_layout_dimention()
        posX, posY, sizeW, sizeH = func.set_app_stick_to_bot_right(sizeW, sizeH)
        self.setGeometry(posX, posY, sizeW, sizeH)
        self.layout = QGridLayout()
        self.mainWidget.setLayout(self.layout)

        # Menubar build
        self.menuGrpBox = QGroupBox("Menu Layout")
        menuLayout = QHBoxLayout()
        self.menuGrpBox.setLayout(menuLayout)

        menuBar = MenuBarLayout()
        menuLayout.addWidget(menuBar)

        # ----------------------------------------------
        self.tdToolBar = self.toolBarTD()
        self.compToolBar = self.toolBarComp()
        self.artToolBar = self.toolBarArt()

        # Load Setting
        self.showTDToolBar = func.str2bool(self.settings.value("showTDToolbar", True))
        self.showCompToolBar = func.str2bool(self.settings.value("showCompToolbar", True))
        self.showArtToolBar = func.str2bool(self.settings.value("showArtToolbar", True))

        self.tdToolBar.setVisible(self.showTDToolBar)
        self.compToolBar.setVisible(self.showCompToolBar)
        self.artToolBar.setVisible(self.showArtToolBar)

        showTDSig = menuBar.showTDSig2
        showCompSig = menuBar.showCompSig2
        showArtSig = menuBar.showArtSig2
        showTDSig.connect(self.show_hide_TDtoolBar)
        showCompSig.connect(self.show_hide_ComptoolBar)
        showArtSig.connect(self.show_hide_ArttoolBar)

        # Status bar viewing message
        self.statusBar().showMessage(self.message['status'])

        # Top build
        self.topGrpBox = QGroupBox("Top Layout")
        topLayout = QHBoxLayout()
        self.topGrpBox.setLayout(topLayout)
        topLayout.addWidget(Clabel("This Layout is for drag and drop"))

        # Mid build
        self.midGrpBox = QGroupBox("plt Tool Box")
        midLayout = QHBoxLayout()
        self.midGrpBox.setLayout(midLayout)

        self.tabWidget = TabWidget(self.username, self.package)

        showMainSig = self.tabWidget.showMainSig
        showLoginSig = self.tabWidget.showLoginSig
        tabSizeSig = self.tabWidget.tabSizeSig
        showMainSig.connect(self.show_hide_main)
        showLoginSig.connect(self.send_to_login)
        tabSizeSig.connect(self.autoResize)
        midLayout.addWidget(self.tabWidget)

        # Bot build
        self.sizeGrpBox = QGroupBox("Size Setting")
        sizeGridLayout = QGridLayout()
        self.sizeGrpBox.setLayout(sizeGridLayout)

        # unitSlider = SliderWidget("UNIT")
        # margSlider = SliderWidget("MARG")
        # buffSlider = SliderWidget("BUFF")
        # scalSlider =SliderWidget("SCAL")
        #
        # unitSig = unitSlider.valueChangeSig
        # margSig = margSlider.valueChangeSig
        # buffSig = buffSlider.valueChangeSig
        # scalSig = scalSlider.valueChangeSig
        #
        # sizeGridLayout.addWidget(unitSlider, 0, 0, 1, 5)
        # sizeGridLayout.addWidget(margSlider, 1, 0, 1, 5)
        # sizeGridLayout.addWidget(buffSlider, 2, 0, 1, 5)
        # sizeGridLayout.addWidget(scalSlider, 3, 0, 1, 5)

        # Bot build
        # self.unitGrpBox = QGroupBox("Unit Setting")
        # unitGridLayout = QGridLayout()
        # self.unitGrpBox.setLayout(unitGridLayout)
        #
        # unitSetting = UnitSetting()
        # unitGridLayout.addWidget(unitSetting)
        #
        # # Add layout to main
        self.layout.addWidget(self.menuGrpBox, 1, 0, 1, 6)
        self.layout.addWidget(self.topGrpBox, 2, 0, 2, 6)
        self.layout.addWidget(self.midGrpBox, 4, 0, 4, 6)
        # self.layout.addWidget(self.sizeGrpBox, 8, 0, 4, 3)
        # self.layout.addWidget(self.unitGrpBox, 8, 3, 4, 3)

        # Restore last setting layout from user
        # stateLayout = self.settings.value("layoutState", QByteArray().toBase64())
        # try:
        #     self.restoreState(QByteArray(stateLayout))
        # except IOError or TypeError:
        #     pass

    def sys_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.showNormal()

    def sys_tray_icon_menu(self):
        trayIconMenu = QMenu(self)

        appKey, iconKey = self.get_correct_key("Snipping Tool")
        snippingAction = self.createAction(self.appInfo, appKey, iconKey)
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

    def toolBarTD(self):
        # TD Tool Bar
        toolBarTD = self.addToolBar('TD')
        TD = ['Maya', 'ZBrush', 'Mari', 'Houdini', 'Substance Painter']
        for k in TD:
            appKey, iconKey = self.get_correct_key(k)
            if not appKey == None:
                toolBarTD.addAction(self.createAction(self.appInfo, appKey, iconKey))

        # return Tool Bar
        return toolBarTD

    def toolBarComp(self):
        # VFX toolBar
        toolBarComp = self.addToolBar('VFX')
        VFX = ['Resolve', 'NukeX', 'Hiero', 'After Effect CC', 'Premiere CC']
        for k in VFX:
            appKey, iconKey = self.get_correct_key(k)
            if not appKey == None:
                toolBarComp.addAction(self.createAction(self.appInfo, appKey, iconKey))

        # Return Tool Bar
        return toolBarComp

    def toolBarArt(self):
        toolbarArt = self.addToolBar('Art')
        ART = ['Photoshop CC', 'Illustrator CC']
        for k in ART:
            appKey, iconKey = self.get_correct_key(k)
            if not appKey == None:
                toolbarArt.addAction(self.createAction(self.appInfo, appKey, iconKey))

        return toolbarArt

    def get_correct_key(self, k):
        TD = ['Maya', 'ZBrush', 'Mari', 'Houdini', 'Substance Painter']
        for app in self.appInfo:
            if k in app:
                appKey = app
            else:
                appKey = None
        for icon in self.iconInfo:
            if k in icon:
                iconKey = app
            else:
                iconKey = None
        print(appKey, iconKey)
        return appKey, iconKey

    def createAction(self, appInfo, appKey, iconKey):
        action = QAction(QIcon(appInfo[appKey]), func.get_icon(iconKey), self)
        action.setStatusTip(appInfo[appKey][0])
        action.triggered.connect (partial(subprocess.Popen, appInfo[appKey][2]))
        return action

    def createSeparatorAction(self):
        separator = QAction(QIcon(self.appInfo['Sep'][0]), self.appInfo['Sep'][1], self)
        separator.setSeparator(True)
        return separator

    def show_hide_TDtoolBar(self, param):
        self.settings.setValue("showTDToolbar", func.bool2str(param))
        self.tdToolBar.setVisible(func.str2bool(param))

    def show_hide_ComptoolBar(self, param):
        self.settings.setValue("showCompToolbar", func.bool2str(param))
        self.compToolBar.setVisible(func.str2bool(param))

    def show_hide_ArttoolBar(self, param):
        self.settings.setValue("showArtToolbar", func.bool2str(param))
        self.artToolBar.setVisible(func.str2bool(param))

    def show_hide_AlltoolBar(self, param):
        self.show_hide_TDtoolBar(param)
        self.show_hide_ComptoolBar(param)
        self.show_hide_ArttoolBar(param)

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
        usql.insert_timeLog("Log out")
        logger.debug("LOG OUT")
        QApplication.instance().quit()

    def set_app_position(self):
        pass

    def get_layout_dimention(self):
        sizeW = self.frameGeometry().width()
        sizeH = self.frameGeometry().height()
        return sizeW, sizeH

    def layout_magrin_ratio(self, margin = 5):
        self.menuGrpBox.setContentsMargins(margin, margin, margin, margin)
        self.topGrpBox.setContentsMargins(margin, margin, margin, margin)
        self.midGrpBox.setContentsMargins(margin, margin, margin, margin)
        self.sizeGrpBox.setContentsMargins(margin, margin, margin, margin)
        return True

    def layout_height_ratio(self, baseH = 60):
        self.menuGrpBox.setFixedHeight(baseH)
        self.topGrpBox.setFixedHeight(baseH*2)
        self.midGrpBox.setFixedHeight(baseH*4)
        self.sizeGrpBox.setFixedHeight(baseH * 2)
        return True

    def layout_width_ratio(self, baseW = 60):
        self.menuGrpBox.setFixedWidth(baseW)
        self.topGrpBox.setFixedWidth(baseW)
        self.midGrpBox.setFixedWidth(baseW)
        self.sizeGrpBox.setFixedWidth(baseW)
        return True

    def autoResize(self, param):
        # print(param)
        pass

    def resizeEvent(self, event):
        sizeW, sizeH = self.get_layout_dimention()
        self.settings.setValue("appW", sizeW)
        self.settings.setValue("appH", sizeH)

    def windowState(self):
        self.settings.setValue("layoutState", self.saveState().data())

    def closeEvent(self, event):
        self.settings.setValue("layoutState", QByteArray(self.saveState().data()).toBase64())
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
    # app.setStyleSheet(qdarkgraystyle.load_stylesheet_pyqt5())

    username, token, cookie = usql.query_user_session()

    if username is None or token is None or cookie is None:
        login = Plt_sign_in()
        login.show()
    else:
        r = requests.get("https://pipeline.damgteam.com/check", verify = False,
                         headers={'Authorization': 'Bearer {token}'.format(token=token)},
                         cookies={'connect.sid': cookie})

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