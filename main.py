# -*- coding: utf-8 -*-
"""

Script Name: desktopUI.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is main file to store everything for the pipeline app

"""

# -------------------------------------------------------------------------------------------------------------
""" Import modules """
# -------------------------------------------------------------------------------------------------------------

import logging
import os
import shutil
import qdarkgraystyle
import subprocess
import sys
import time
import webbrowser
from functools import partial
import sqlite3 as lite
import pip
import yaml

# Path value.
SCR_PATH = os.getcwd()

# PyQt5 modules
from PyQt5.QtCore import Qt, QSize, QCoreApplication, QSettings, QLocale, QRegExp
from PyQt5.QtGui import QIcon, QPixmap, QImage, QRegExpValidator
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFrame, QDialog, QWidget, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QSizePolicy, QLineEdit, QLabel, QPushButton, QMessageBox, QGroupBox,
                             QCheckBox, QTabWidget, QSystemTrayIcon, QAction, QMenu, QComboBox)

# -------------------------------------------------------------------------------------------------------------
""" PyQt5 ui element pre-define """
# -------------------------------------------------------------------------------------------------------------
__center__ = Qt.AlignCenter
__right__ = Qt.AlignRight
__left__ = Qt.AlignLeft
frameStyle = QFrame.Sunken | QFrame.Panel

# -------------------------------------------------------------------------------------------------------------
""" Create and locate local path via environment key. """
# -------------------------------------------------------------------------------------------------------------
def setup1_application_root_path():

    # Key name.
    KEY = 'PIPELINE_TOOL'
    TOOL_NAME = 'PipelineTool'

    # Set key, path into environment variable.
    os.environ[KEY] = SCR_PATH
    return KEY, TOOL_NAME

# -------------------------------------------------------------------------------------------------------------
""" Set up database path """
# -------------------------------------------------------------------------------------------------------------
def setup2_application_database_path():
    # User database will be store into here.
    appDataPath = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData')
    DATA_PATH = os.path.join(appDataPath, 'database.db')

    # Back database in case something missing
    DATA_BACKUP = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'backup', 'database.db')
    MAIN_CONFIG_PATH = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'main_config.yml')

    # If database file is missing, copy the backup one.
    if not os.path.exists(DATA_PATH):
        shutil.copy2(DATA_BACKUP, DATA_PATH)
    return MAIN_CONFIG_PATH

# -------------------------------------------------------------------------------------------------------------
""" Check extra packages """
# -------------------------------------------------------------------------------------------------------------
def setup3_extra_python_packages():
    # Extra package list.
    packages = ['pywinauto', 'winshell', 'pandas', 'opencv-python', 'pyunpack']
    # Get current installed packages.
    checkList = []

    pyPkgs = {}

    pyPkgs['__mynote__'] = 'import pip; pip.get_installed_distributions()'
    for package in pip.get_installed_distributions():
        name = package.project_name
        if name in packages:
            checkList.append(name)

    resault = [p for p in packages if p not in checkList]

    # Automatically install packages if it is not.
    if len(resault) > 0:
        for package in resault:
            subprocess.Popen("pip install %s" % package)
            time.sleep(5)

    return True

# -------------------------------------------------------------------------------------------------------------
""" Setup extra environment path for maya """
# -------------------------------------------------------------------------------------------------------------
def setup4_intergrade_for_maya():
    # Pipeline tool module paths for Maya.
    maya_tk = os.path.join(SCR_PATH, 'plt_maya')

    # Name of folders
    mayaTrack = ['utilities', 'plt_maya', 'icons', 'modules', 'plugins', 'Animation', 'MayaLib', 'Modeling', 'Rigging',
                 'Sufacing']
    pythonValue = ""
    pythonList = []
    for root, dirs, files in os.walk(maya_tk):
        for dir in dirs:
            if dir in mayaTrack:
                dirPth = os.path.join(root, dir)
                pythonList.append(dirPth)
    pythonList = list(set(pythonList))
    for pth in pythonList:
        pythonValue += pth + ';'
    os.environ['PYTHONPATH'] = pythonValue

    # Copy userSetup.py from source code to properly maya folder
    userSetup_plt_path = os.path.join(os.getcwd(), 'plt_maya', 'userSetup.py')
    userSetup_maya_path = os.path.join(os.path.expanduser('~/Documents/maya/2017/prefs/scripts'), 'userSetup.py')

    if not os.path.exists(userSetup_plt_path):
        pass
    elif not os.path.exists(userSetup_plt_path):
        pass
    else:
        shutil.copy2(userSetup_plt_path, userSetup_maya_path)

# -------------------------------------------------------------------------------------------------------------
""" Gather info from local pc to config with Pipeline tool application """
# -------------------------------------------------------------------------------------------------------------
def setup5_gather_configure_info():
    func.Generate_info()
    with open(MAIN_CONFIG_PATH, 'r') as f:
        APPINFO = yaml.load(f)
    return APPINFO

def query_user_info():
    currentUserData = ultis.query_current_user()
    curUser = currentUserData[2]
    unix = currentUserData[0]
    token = currentUserData[1]
    rememberLogin = currentUserData[3]
    status = currentUserData[-1]
    ultis.check_sys_configuration(curUser)
    return unix, token, curUser, rememberLogin, status

KEY, TOOL_NAME = setup1_application_root_path()
MAIN_CONFIG_PATH = setup2_application_database_path()

checkPackage = setup3_extra_python_packages()

# import Pipeline tool ui
from ui import ui_account_setting
from ui import ui_preference

# import Pipeline tool modules
from utilities import utils as func
from utilities import message as mess
from utilities import utils_sql as ultis
from utilities import variables as var

__appname__ = var.__appname__
__module__ = var.__module__
__version__ = var.__version__
__organization__ = var.__version__
__website__ = var.__website__
__email__ = var.__email__
__author__ = var.__author__

setup4_intergrade_for_maya()

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain logs """
# -------------------------------------------------------------------------------------------------------------

logFile = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'settings', 'main.log')

# if not os.path.exists(logFile):
#     func.dataHandle('json', 'w', logFile)

logging.basicConfig(filename=logFile,
                    format="%(asctime)-15s: %(name)-18s - %(levelname)-8s - %(module)-15s - %(funcName)-20s - %(lineno)-6d - %(message)s",
                    level=logging.DEBUG)

logger = logging.getLogger(name=__appname__)

APPINFO = setup5_gather_configure_info()
SETTING_PATH = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'settings', 'PipelineTool_settings.ini')
DB_PATH = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'database.db')

# ----------------------------------------------------------------------------------------------------------- #
""" Create New Account """
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
        self.checkBox.setStyleSheet("fontName='Times'")
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

# -------------------------------------------------------------------------------------------------------------
""" Login Layout """
# -------------------------------------------------------------------------------------------------------------
class Sign_in(QDialog):

    unix, token, curUser, rememberLogin, status = query_user_info()

    def __init__(self, parent=None):

        super(Sign_in, self).__init__(parent)

        self.setWindowTitle('Log in')
        self.setWindowIcon(QIcon(func.getIcon('Logo')))

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
        signup = Sign_up()

        # from ui import ui_sign_up
        # reload(ui_sign_up)
        # signup = ui_sign_up.main()
        # signup.exec_()

        return signup

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
            window = Main()
            window.show()

# -------------------------------------------------------------------------------------------------------------
""" Tab Layout """
# -------------------------------------------------------------------------------------------------------------
class TabWidget(QWidget):

    dbConn = lite.connect(DB_PATH)

    def __init__(self, unix, username, package, parent=None):

        super(TabWidget, self).__init__(parent)

        self.buildUI(unix, username, package)

    def buildUI(self, unix, username, package):

        # Create tab layout
        # ------------------------------------------------------
        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.tabs.resize(package['geo'][1], package['geo'][2])

        # Create and add tabs
        # ------------------------------------------------------
        # Create and add tab 1: 'Tools: Extra tools that might be useful for user & developer'
        self.tab1 = QGroupBox(self)
        self.tab1Layout()
        self.tabs.addTab(self.tab1, 'Tools')

        # Create and add tab 2: 'Proj: Project management'
        self.tab2 = QGroupBox(self)
        self.tab2Layout()
        self.tabs.addTab(self.tab2, 'Prj')

        # Create and add tab 3: 'Cal: Just a calculator'
        self.tab3 = QGroupBox(self)
        self.tab3Layout(curUser=username)
        self.tabs.addTab(self.tab3, 'User')

        # Create and add tab 4: 'User: User login profile'
        self.tab4 = QGroupBox(self)
        self.tab4Layout()
        self.tabs.addTab(self.tab4, 'Lib')

        userClass = ultis.query_user_class(unix=unix, username=username)

        if userClass == 'Administrator Privilege':
            self.tab5 = QGroupBox(self)
            self.tab5Layout()
            self.tabs.addTab(self.tab5, 'SQL')

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def tab1Layout(self):
        # Create Layout for Tab 1.
        # ------------------------------------------------------
        # Title of layout
        self.tab1.setTitle('Optional Tool')

        # Main layout
        # ------------------------------------------------------
        vboxLayout = QVBoxLayout()
        tab1VBoxLayout = QVBoxLayout()
        line1HBoxLayout = QHBoxLayout()
        line2HBoxLayout = QHBoxLayout()
        line3HBoxLayout = QHBoxLayout()

        # Content
        # ------------------------------------------------------
        line1HBoxLayout.addWidget(QLabel('Extra app: '))

        # Advance Renamer
        arIconBtn = self.makeIconButton('Advance Renamer')
        line1HBoxLayout.addWidget(arIconBtn)

        # Note
        noteReminderBtn = self.iconButtonSelfFunction('QtNote', 'Note Reminder', self.note_reminder)
        line1HBoxLayout.addWidget(noteReminderBtn)

        textEditorBtn = self.iconButtonSelfFunction('Text Editor', 'Text Editor', self.text_editor)
        line1HBoxLayout.addWidget(textEditorBtn)

        for key in APPINFO:
            # Mudbox
            if key == 'Mudbox 2018':
                mudbox18Btn = self.makeIconButton(key)
                line1HBoxLayout.addWidget(mudbox18Btn)
            if key == 'Mudbox 2017':
                mudbox17Btn = self.makeIconButton(key)
                line1HBoxLayout.addWidget(mudbox17Btn)
            if key == '3ds Max 2018':
                max18Btn = self.makeIconButton(key)
                line1HBoxLayout.addWidget(max18Btn)
            if key == '3ds Max 2017':
                max17Btn = self.makeIconButton(key)
                line1HBoxLayout.addWidget(max17Btn)

        # ------------------------------------------------------
        line2HBoxLayout.addWidget(QLabel('Enhance: '))

        # English dictionary
        dictBtn = self.iconButtonSelfFunction('English Dictionary', 'English Dictionary', self.englishDict)
        line2HBoxLayout.addWidget(dictBtn)

        # Screenshot
        screenshotBtn = self.iconButtonSelfFunction('Screenshot', 'Screenshot', self.screenShot)
        line2HBoxLayout.addWidget(screenshotBtn)

        # Calendar
        calendarBtn = self.iconButtonSelfFunction('Calendar', 'Calendar', self.calendar)
        line2HBoxLayout.addWidget(calendarBtn)

        # Calculator
        calculatorBtn = self.iconButtonSelfFunction('Calculator', 'Calculator', self.calculator)
        line2HBoxLayout.addWidget(calculatorBtn)

        # File finder
        fileFinderBtn = self.iconButtonSelfFunction('Finder', 'Find files', self.findFiles)
        line2HBoxLayout.addWidget(fileFinderBtn)

        # ------------------------------------------------------
        line3HBoxLayout.addWidget(QLabel('Dev: '))

        # PyCharm
        pycharmBtn = self.makeIconButton('PyCharm')
        line3HBoxLayout.addWidget(pycharmBtn)

        # SublimeText
        sublimeBtn = self.makeIconButton('SublimeText 3')
        line3HBoxLayout.addWidget(sublimeBtn)

        # Qt Designer
        qtdesignerBtn = self.makeIconButton('QtDesigner')
        line3HBoxLayout.addWidget(qtdesignerBtn)

        tab1VBoxLayout.addLayout(line1HBoxLayout)
        tab1VBoxLayout.addLayout(line2HBoxLayout)
        tab1VBoxLayout.addLayout(line3HBoxLayout)
        vboxLayout.addLayout(tab1VBoxLayout)
        self.tab1.setLayout(vboxLayout)

    def tab2Layout(self):

        # Create Layout for Tab 2.
        self.tab2.setTitle('Project')

        hboxLayout = QHBoxLayout()
        tab2GridLayout = QGridLayout()

        createProjectBtn = QPushButton('New Project')
        createProjectBtn.clicked.connect(self.createProject)
        tab2GridLayout.addWidget(createProjectBtn, 0, 0, 1, 2)
        currentLoginDataBtn = QPushButton('Project List')
        tab2GridLayout.addWidget(currentLoginDataBtn, 0, 2, 1, 2)
        testNewFunctionBtn = QPushButton('Project Details')
        tab2GridLayout.addWidget(testNewFunctionBtn, 0, 4, 1, 2)

        hboxLayout.addLayout(tab2GridLayout)
        self.tab2.setLayout(hboxLayout)

    def tab3Layout(self, curUser):

        # Create Layout for Tab 3.
        self.tab3.setTitle(curUser)

        hboxLayout = QHBoxLayout()
        tab3ridLayout = QGridLayout()

        userProfile = ultis.query_user_profile(curUser, 'username')
        userImg = QPixmap.fromImage(QImage(func.getAvatar(userProfile[7])))
        self.userAvatar = QLabel()
        self.userAvatar.setPixmap(userImg)
        self.userAvatar.setScaledContents(True)
        self.userAvatar.setFixedSize(100, 100)
        tab3ridLayout.addWidget(self.userAvatar, 0, 0, 3, 3)

        accountSettingBtn = QPushButton('Account Setting')
        accountSettingBtn.clicked.connect(partial(self.onAccountSettingBtnClicked, curUser))
        tab3ridLayout.addWidget(accountSettingBtn, 0, 3, 1, 3)

        logoutBtn = QPushButton('Log Out')
        logoutBtn.clicked.connect(self.onLogoutBtnClicked)
        tab3ridLayout.addWidget(logoutBtn, 1, 3, 1, 3)

        hboxLayout.addLayout(tab3ridLayout)
        self.tab3.setLayout(hboxLayout)

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

        dataBrowserIconBtn = self.makeIconButton('Database Browser')
        tab5GridLayout.addWidget(dataBrowserIconBtn)

        hboxLayout.addLayout(tab5GridLayout)
        self.tab5.setLayout(hboxLayout)

    def onAccountSettingBtnClicked(self, username):
        reload(ui_account_setting)
        window = ui_account_setting.WindowDialog(self, username)
        window.exec_()

    def userAvatarChanged(self, curUser):
        sig = ui_account_setting.WindowDialog(self, curUser).changAvatarSignal
        # print sig

    def onLogoutBtnClicked(self):
        unix, token, curUser, rememberLogin, status = query_user_info()

        user_profile = ultis.query_user_profile(curUser)
        token = user_profile[1]
        unix = user_profile[0]

        ultis.update_user_remember_login(token, 'Flase')
        ultis.update_current_user(unix, token, curUser, 'False')

    def iconButtonSelfFunction(self, iconName, tooltip, func_tool):

        icon = QIcon(func.getIcon(iconName))
        iconBtn = QPushButton()
        iconBtn.setToolTip(tooltip)
        iconBtn.setIcon(icon)
        iconBtn.setFixedSize(30, 30)
        iconBtn.setIconSize(QSize(30 - 3, 30 - 3))
        iconBtn.clicked.connect(func_tool)
        return iconBtn

    def makeIconButton(self, name):

        icon = QIcon(APPINFO[name][1])
        iconBtn = QPushButton()
        iconBtn.setToolTip(APPINFO[name][0])
        iconBtn.setIcon(icon)
        iconBtn.setFixedSize(30, 30)
        iconBtn.setIconSize(QSize(30 - 3, 30 - 3))
        iconBtn.clicked.connect(partial(self.openApps, APPINFO[name][2]))
        return iconBtn

    def openApps(self, pth):

        subprocess.Popen(pth)

    def englishDict(self):

        from ui import ui_english_dict
        reload(ui_english_dict)
        EngDict = ui_english_dict.EnglishDict()
        EngDict.exec_()

    def screenShot(self):

        from ui import ui_screenshot
        reload(ui_screenshot)
        dlg = ui_screenshot.Screenshot()
        dlg.exec_()

    def calendar(self):

        from ui import ui_calendar
        reload(ui_calendar)
        dlg = ui_calendar.Calendar()
        dlg.exec_()

    def calculator(self):

        from ui import ui_calculator
        reload(ui_calculator)
        dlg = ui_calculator.Calculator()
        dlg.exec_()

    def findFiles(self):

        from ui import ui_find_files
        reload(ui_find_files)
        dlg = ui_find_files.Findfiles()
        dlg.exec_()

    def note_reminder(self):

        from ui import ui_note_reminder
        reload(ui_note_reminder)
        window = ui_note_reminder.WindowDialog()
        window.exec_()

    def text_editor(self):

        from ui.textedit import textedit
        reload(textedit)
        window = textedit.WindowDialog()
        window.exec_()

    def createProject(self):

        from ui import ui_new_project
        reload(ui_new_project)
        window = ui_new_project.NewProject()
        window.exec_()

# -------------------------------------------------------------------------------------------------------------
""" Main """
# -------------------------------------------------------------------------------------------------------------
class Main(QMainWindow):

    unix, token, username, rememberLogin, status = query_user_info()
    mainID = var.MAIN_ID
    appInfo = APPINFO
    package = var.MAIN_PACKPAGE
    message = var.MAIN_MESSAGE
    url = var.MAIN_URL

    def __init__(self, case=None, parent=None):

        super(Main, self).__init__(parent)

        self.settings = QSettings(SETTING_PATH, QSettings.IniFormat)

        self.setWindowTitle(__appname__)
        self.setWindowIcon(QIcon(func.getIcon('Logo')))
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setToolButtonStyle(Qt.ToolButtonFollowStyle)

        self.trayIcon = self.system_tray_icon()
        self.trayIcon.setToolTip(__appname__)
        self.trayIcon.show()

        if case == 'Auto login':
            self.autoLogin(self.username)

        # Build UI
        self.buildUI()

        # Load Setting
        self.showToolBar = func.str2bool(self.settings.value("showToolbar", True))
        self.tdToolBar.setVisible(self.showToolBar)
        self.compToolBar.setVisible(self.showToolBar)

        # Tabs build
        self.tabWidget = TabWidget(self.unix, self.username, self.package)

        self.setCentralWidget(self.tabWidget)

        # Log record
        self.procedures('log in')

    def buildUI(self):

        self.layout = self.setGeometry(300, 300, 400, 350)

        # Status bar viewing message
        self.statusBar().showMessage(self.message['status'])
        # ----------------------------------------------
        """ Menu """
        menubar = self.menuBar()

        # Create FILE menu
        fileMenu = menubar.addMenu('File')

        # File menu elements
        exitAction, prefAction = self.fileMenuToolBar()
        separator1 = self.createSeparatorAction()

        # File menu content
        fileMenu.addAction(prefAction)
        fileMenu.addAction(separator1)
        fileMenu.addAction(exitAction)

        # Create TOOL menu
        toolMenu = menubar.addMenu('Tool')

        # Tool menu elements
        cleanPycAction, reconfigaction = self.toolMenuToolBar()

        # Tool menu content
        toolMenu.addAction(cleanPycAction)
        toolMenu.addAction(reconfigaction)

        # Create HELP menu
        helpMenu = menubar.addMenu('Help')

        # Help menu elements
        aboutAction, creditAction, helpAction = self.helpMenuToolBar()

        # Help menu content
        helpMenu.addAction(aboutAction)
        helpMenu.addAction(creditAction)
        helpMenu.addAction(helpAction)

        # ----------------------------------------------
        """Tool Bar"""

        self.tdToolBar = self.toolBarTD()

        self.compToolBar = self.toolBarComp()

        self.artToolBar = self.toolBarArt()

    def system_tray_icon(self):
        trayIconMenu = QMenu(self)

        testIcon = QIcon(func.getIcon('Test'))
        testAction1 = QAction(testIcon, 'Test1', self)
        testAction1.triggered.connect(partial(self.onSysTrayIconClick, 'set1'))

        testIcon = QIcon(func.getIcon('Test'))
        testAction2 = QAction(testIcon, 'Test2', self)
        testAction2.triggered.connect(partial(self.onSysTrayIconClick, 'set2'))

        trayIconMenu.addAction(testAction1)
        trayIconMenu.addAction(testAction2)

        snippingAction = self.createAction(self.appInfo, 'Snipping Tool')
        trayIconMenu.addAction(snippingAction)

        screenshoticon = QIcon(func.getIcon('Screenshot'))
        screenshotAction = QAction(screenshoticon, "Screenshot", self)
        screenshotAction.triggered.connect(self.screenshot)
        trayIconMenu.addAction(screenshotAction)

        maximizeIcon = QIcon(func.getIcon("Maximize"))
        maximizeAction = QAction(maximizeIcon, "Maximize", self)
        maximizeAction.triggered.connect(self.showMaximized)
        trayIconMenu.addSeparator()
        trayIconMenu.addAction(maximizeAction)

        minimizeIcon = QIcon(func.getIcon('Minimize'))
        minimizeAction = QAction(minimizeIcon, "Minimize", self)
        minimizeAction.triggered.connect(self.hide)
        trayIconMenu.addAction(minimizeAction)

        restoreIcon = QIcon(func.getIcon('Restore'))
        restoreAction = QAction(restoreIcon, "Restore", self)
        restoreAction.triggered.connect(self.showNormal)
        trayIconMenu.addAction(restoreAction)

        quitIcon = QIcon(func.getIcon('Close'))
        quitAction = QAction(quitIcon, "Quit", self)
        quitAction.triggered.connect(self.exit_action_trigger)
        trayIconMenu.addSeparator()
        trayIconMenu.addAction(quitAction)

        trayIcon = QSystemTrayIcon(self)
        trayIcon.setIcon(QIcon(func.getIcon('Logo')))
        trayIcon.setContextMenu(trayIconMenu)

        return trayIcon

    def fileMenuToolBar(self):
        # Preferences
        prefAction = QAction(QIcon(func.getIcon('Preferences')), 'Preferences', self)
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
        reconfigaction.triggered.connect(func.Generate_info)

        return cleanaction, reconfigaction

    def helpMenuToolBar(self):
        # About action
        about = QAction(QIcon(self.appInfo['About'][1]), self.appInfo['About'][0], self)
        about.setStatusTip(self.appInfo['About'][0])
        about.triggered.connect(partial(self.subWindow, self.mainID['About'], self.message['About'], self.appInfo['About'][1]))

        # Credit action
        credit = QAction(QIcon(self.appInfo['Credit'][1]), self.appInfo['Credit'][0], self)
        credit.setStatusTip(self.appInfo['Credit'][0])
        credit.triggered.connect(partial(self.subWindow, self.mainID['Credit'], self.message['Credit'], self.appInfo['Credit'][1]))

        # Help action
        helpAction = QAction(QIcon(self.appInfo['Help'][1]), self.appInfo['Help'][0], self)
        helpAction.setStatusTip((self.appInfo['Help'][0]))
        helpAction.triggered.connect(partial(self.openURL, self.url['Help']))

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

        # plt_mari
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

    def procedures(self, event):
        ultis.dynamic_insert_timelog(event)

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

    def subWindow(self, id='Note', message=" ", icon=func.getIcon('Logo')):
        from ui import ui_about
        reload(ui_about)
        dlg = ui_about.WindowDialog(id=id, message=message, icon=icon)
        dlg.exec_()

    def screenshot(self):
        from ui import ui_screenshot
        reload(ui_screenshot)
        dlg = ui_screenshot.Screenshot()
        dlg.exec_()

    def openURL(self, url):
        webbrowser.open(url)

    def autoLogin(self, username):
        icon = QSystemTrayIcon.Information
        self.trayIcon.showMessage('Auto Login', "Welcome back %s" % username, icon, 1000)

    def onSysTrayIconClick(self, name=None, *args):
        # from appData.db import sqlTools
        # reload(sqlTools)
        # if name == 'set1':
        #     sqlTools.create_predatabase()
        # elif name == 'set2':
        #     sqlTools.create_predatabase()
        # else:
        #     pass
        pass

    def preferences_action_triggered(self):
        dlg = ui_preference.Preferences(self)
        sig = dlg.checkboxSig
        sig.connect(self.showHideToolbar)
        dlg.exec_()

    def showHideToolbar(self, param):
        self.tdToolBar.setVisible(param)
        self.compToolBar.setVisible(param)
        self.artToolBar.setVisible(param)
        self.settings.setValue("showToolbar", func.bool2str(param))

    def exit_action_trigger(self):
        self.procedures("Log out")
        logger.debug("LOG OUT")
        QApplication.instance().quit()

    def closeEvent(self, event):
        icon = QSystemTrayIcon.Information
        self.trayIcon.showMessage('Notice', "Pipeline Tool will keep running in the system tray.", icon, 1000)
        self.hide()
        event.ignore()


def main():

    QCoreApplication.setApplicationName(__appname__)
    QCoreApplication.setApplicationVersion(__version__)
    QCoreApplication.setOrganizationName(__organization__)
    QCoreApplication.setOrganizationDomain(__website__)

    unix, token, curUser, rememberLogin, status = query_user_info()
    userdata = [unix, token, curUser, rememberLogin]

    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkgraystyle.load_stylesheet_pyqt5())

    if rememberLogin == 'False' or userdata == [] or userdata == None:

        from ui import ui_sign_in
        reload(ui_sign_in)
        login = ui_sign_in.main()
        # login = Sign_in()
        login.show()
    else:
        window = Main('Auto login')
        window.show()
        if not QSystemTrayIcon.isSystemTrayAvailable():
            QMessageBox.critical(None, "Systray could not detect any system tray on this system")
            sys.exit(1)

    QApplication.setQuitOnLastWindowClosed(False)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

# ----------------------------------------------------------------------------------------------------------- #
"""                                                END OF CODE                                              """
# ----------------------------------------------------------------------------------------------------------- #
