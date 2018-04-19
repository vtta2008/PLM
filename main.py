# -*- coding: utf-8 -*-
"""
Script Name: desktopUI.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is main file to store everything for the pipeline app

"""

__appname__ = "Pipeline Tool"
__module__ = "main"
__version__ = "0.13"
__organization__ = "DAMG team"
__website__ = "www.damgteam.com"
__email__ = "dot@damgteam.com"
__author__ = "Trinh Do, a.k.a: Jimmy"


# -------------------------------------------------------------------------------------------------------------
""" Import Python modules """

import logging
import os
import shutil
import sqlite3 as lite
import subprocess
import sys
import time
import webbrowser
from functools import partial

import pip
import yaml

# PyQt5 modules
from PyQt5.QtCore import Qt, QSize, QCoreApplication, QSettings
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFrame, QDialog, QWidget, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QSizePolicy, QLineEdit, QLabel, QPushButton, QMessageBox, QGroupBox,
                             QCheckBox, QTabWidget, QSystemTrayIcon, QAction, QMenu)

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
    global SCR_PATH
    # Key name.
    KEY = 'PIPELINE_TOOL'
    TOOL_NAME = 'PipelineTool'
    # Path value.
    SCR_PATH = os.getcwd()
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
    mayaTrack = ['util', 'plt_maya', 'icons', 'modules', 'plugins', 'Animation', 'MayaLib', 'Modeling', 'Rigging',
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


# setup(
#     name='PipelineTool',
#     version='13',
#     packages=['', 'util', 'ui', 'appData', 'plt_mari', 'plt_maya', 'plt_maya.modules', 'plt_maya.modules.Modeling',
#               'plt_maya.modules.Sufacing', 'plt_maya.plugins', 'plt_maya.userLibrary',
#               'plt_maya.userLibrary.controllerLibrary', 'plt_nuke', 'plt_zbrush', 'houdini_plt'],
#     url='https://github.com/vtta2008/PipelineTool',
#     license='internal share',
#     author='Trinh Do (aka. Jimmy)',
#     author_email='dot@damgteam.com',
#     description='soft package manager in custom pipeline'
# )

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

# Pipeline tool ui
from ui import ui_account_setting
from ui import ui_preference

# Pipeline tool modules
from util import utilities as func
from util import message as mes
from util import util_sql as ultis
from util import variables as var

setup4_intergrade_for_maya()

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain logs """
# -------------------------------------------------------------------------------------------------------------
logFile = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'settings', 'main.log')

if not os.path.exists(logFile):
    func.dataHandle('json', 'w', logFile)

logging.basicConfig(filename=logFile,
                    format="%(asctime)-15s: %(name)-18s - %(levelname)-8s - %(module)-15s - %(funcName)-20s - %(lineno)-6d - %(message)s",
                    level=logging.DEBUG)
logger = logging.getLogger(name=__appname__)

APPINFO = setup5_gather_configure_info()
SETTING_PATH = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'settings', 'PipelineTool_settings.ini')
DB_PATH = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'database.db')

""" Create New Account """
# ----------------------------------------------------------------------------------------------------------- #
class Create_account(QDialog):

    TITLEBLANK = 'If title is blank, it will be considered as a "Tester"'

    def __init__(self, parent=None):

        super(Create_account, self).__init__(parent)

        self.setWindowTitle("Create New Account")
        self.setWindowIcon(QIcon(func.getIcon('Logo')))
        self.layout = QGridLayout()
        self.firstnameField = QLineEdit()
        self.lastnameField = QLineEdit()
        self.regisTitle = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.passwordRetype = QLineEdit()
        self.passwordRetype.setEchoMode(QLineEdit.Password)
        self.buildUI()

    def buildUI(self):

        self.layout.addWidget(self.clabel('Register!'), 0, 0, 1, 4)
        self.layout.addWidget(self.clabel('Title(modeler, artist, etc.)'), 1, 0, 1, 1)
        self.layout.addWidget(self.clabel('First Name'), 2, 0, 1, 1)
        self.layout.addWidget(self.clabel('Last Name'), 3, 0, 1, 1)
        self.layout.addWidget(self.clabel(self.TITLEBLANK), 4, 0, 1, 4)
        self.layout.addWidget(self.clabel('Password'), 5, 0, 1, 1)
        self.layout.addWidget(self.clabel('Re-type password'), 6, 0, 1, 1)
        self.layout.addWidget(self.regisTitle, 1, 1, 1, 3)
        self.layout.addWidget(self.firstnameField, 2, 1, 1, 3)
        self.layout.addWidget(self.lastnameField, 3, 1, 1, 3)
        self.layout.addWidget(self.password, 5, 1, 1, 3)
        self.layout.addWidget(self.passwordRetype, 6, 1, 1, 3)
        self.layout.addWidget(self.clabel(''), 7, 0, 1, 4)
        okBtn = QPushButton('Ok')
        okBtn.clicked.connect(self.onOKclicked)
        cancelBtn = QPushButton('Cancel')
        cancelBtn.clicked.connect(self.close)
        self.layout.addWidget(okBtn, 8, 0, 1, 2)
        self.layout.addWidget(cancelBtn, 8, 2, 1, 2)
        self.setLayout(self.layout)

    def clabel(self, text):
        label = QLabel(text)
        label.setAlignment(__center__)
        label.setMinimumWidth(50)
        return label

    def onOKclicked(self):
        FIRSTNAME = "Firstname cannot be blank"
        LASTNAME = "Lastname cannot be blank"

        # Get title info
        title = self.regisTitle.text()
        if title is None or title == '':
            title = 'Tester'
        else:
            title = str(title)

        # Get first name and last name
        lastname = str(self.lastnameField.text())
        firstname = str(self.firstnameField.text())

        # Check first name and last name available
        if firstname == "" or firstname is None:
            QMessageBox.critical(self, "Error", FIRSTNAME, QMessageBox.Retry)
            return False
        elif lastname == "":
            QMessageBox.critical(self, "Error", LASTNAME, QMessageBox.Retry)
            return False
        else:
            pass

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
            login = Login()
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
class Login(QDialog):

    def __init__(self, parent=None):

        super(Login, self).__init__(parent)

        self.setWindowTitle('Log in')
        self.setWindowIcon(QIcon(func.getIcon('Logo')))
        
        self.buildUI()

    def buildUI(self):

        unix, token, curUser, rememberLogin, status = query_user_info()

        self.mainFrame = QGroupBox(self)
        self.mainFrame.setTitle('User Account')
        self.mainFrame.setFixedSize(350, 250)
        hboxLogin = QHBoxLayout()
        self.layout = QGridLayout()
        self.layout.setContentsMargins(5, 5, 5, 5)
        loginText = QLabel('User Name: ')
        loginText.setAlignment(__center__)
        self.layout.addWidget(loginText, 0, 0, 1, 2)
        self.userName = QLineEdit(curUser)
        self.layout.addWidget(self.userName, 0, 2, 1, 7)
        passText = QLabel('Password: ')
        passText.setAlignment(__center__)
        self.layout.addWidget(passText, 1, 0, 1, 2)
        self.passWord = QLineEdit()
        self.passWord.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.passWord, 1, 2, 1, 7)
        rememberCheck = QLabel('Remember Me')
        rememberCheck.setAlignment(__center__)
        self.layout.addWidget(rememberCheck, 2, 0, 1, 2)
        self.rememberCheckBox = QCheckBox()
        self.layout.addWidget(self.rememberCheckBox, 2, 2, 1, 1)
        self.loginBtn = QPushButton('Login')
        self.loginBtn.clicked.connect(self.onLoginBtnClicked)
        self.layout.addWidget(self.loginBtn, 2, 3, 1, 3)
        self.cancelBtn = QPushButton('Cancel')
        self.cancelBtn.clicked.connect(self.onCancelBtnClicked)
        self.layout.addWidget(self.cancelBtn, 2, 6, 1, 3)
        noteLabel = QLabel(mes.LOGIN_NOTE)
        self.layout.addWidget(noteLabel, 3, 0, 1, 3)
        createAccountBtn = QPushButton('Create Account')
        createAccountBtn.clicked.connect(self.onCreateAccountClicked)
        self.layout.addWidget(createAccountBtn, 3,3,1,6)

        hboxLogin.addLayout(self.layout)
        self.mainFrame.setLayout(hboxLogin)

    def onCreateAccountClicked(self):
        createAcc = Create_account()
        createAcc.exec_()

    def onCancelBtnClicked(self):
        self.close()

    def onLoginBtnClicked(self, *args):
        username = str(self.userName.text())

        if username == "" or username is None:
            QMessageBox.critical(self, 'Login Failed', 'Username can not be blank')
            return
        
        pass_word = self.passWord.text()
        
        if pass_word == "" or pass_word is None:
            QMessageBox.critical(self, 'Login Failed', 'No password')
            return
            
        password = str(func.encoding(pass_word))
        
        checkUserExists = ultis.check_data_exists(username)
        
        if not checkUserExists:
            QMessageBox.critical(self, 'Login Failed', "Username not exists")
            return

        checkUserStatus = ultis.query_user_status(username)

        if checkUserStatus == 'disabled':
            QMessageBox.critical(self, 'Login Failed', "This username is not activated")
            return

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
        # self.tabs.setDocumentMode(False)
        # self.tabs.setTabPosition(QTabWidget.West)
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
        # self.tab1.setFixedSize(W,H)

        # Main layout
        # ------------------------------------------------------
        vboxLayout = QVBoxLayout()
        tab1VBoxLayout = QVBoxLayout()
        line1GroupBox = QGroupBox()
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

        # line1GroupBox.setLayout(line1HBoxLayout)

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
        tab2GridLayout.addWidget(createProjectBtn, 0,0,1,2)
        currentLoginDataBtn = QPushButton('Project List')
        tab2GridLayout.addWidget(currentLoginDataBtn, 0,2,1,2)
        testNewFunctionBtn = QPushButton('Project Details')
        tab2GridLayout.addWidget(testNewFunctionBtn, 0,4,1,2)

        hboxLayout.addLayout(tab2GridLayout)
        self.tab2.setLayout(hboxLayout)

    def tab3Layout(self, curUser):

        # Create Layout for Tab 3.
        self.tab3.setTitle(curUser)
        # self.tab1.setFixedSize(W, H)

        hboxLayout = QHBoxLayout()
        tab3ridLayout = QGridLayout()

        userProfile = ultis.query_user_profile(curUser, 'username')
        userImg = QPixmap.fromImage(QImage(func.getAvatar(userProfile[7])))
        self.userAvatar = QLabel()
        self.userAvatar.setPixmap(userImg)
        self.userAvatar.setScaledContents(True)
        self.userAvatar.setFixedSize(100, 100)
        tab3ridLayout.addWidget(self.userAvatar, 0,0,3,3)

        accountSettingBtn = QPushButton('Account Setting')
        accountSettingBtn.clicked.connect(partial(self.onAccountSettingBtnClicked, curUser))
        tab3ridLayout.addWidget(accountSettingBtn, 0,3,1,3)

        logoutBtn = QPushButton('Log Out')
        logoutBtn.clicked.connect(self.onLogoutBtnClicked)
        tab3ridLayout.addWidget(logoutBtn, 1,3,1,3)

        hboxLayout.addLayout(tab3ridLayout)
        self.tab3.setLayout(hboxLayout)

    def tab4Layout(self):
        # Create Layout for Tab 4.
        self.tab4.setTitle('Library')
        # self.tab4.setFixedSize(W, H)

        hboxLayout = QHBoxLayout()
        tab4ridLayout = QGridLayout()

        tab4ridLayout.addWidget(QLabel('Update later'), 0,0)

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

    def __init__(self, case=None, parent=None):
        unix, token, username, rememberLogin, status = query_user_info()
        super(Main, self).__init__(parent)

        mainID = var.MAIN_ID
        appInfo = APPINFO
        package = var.MAIN_PACKPAGE
        message = var.MAIN_MESSAGE
        url = var.MAIN_URL

        self.settings = QSettings(SETTING_PATH, QSettings.IniFormat)

        self.setWindowTitle(mainID['Main'])
        self.setWindowIcon(QIcon(func.getIcon('Logo')))
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setToolButtonStyle(Qt.ToolButtonFollowStyle)

        self.trayIcon = self.system_tray_icon(appInfo)
        self.trayIcon.setToolTip(__appname__)
        self.trayIcon.show()

        if case == 'Auto login':
            self.autoLogin(username)

        # Build UI
        self.buildUI(appInfo, message, mainID, url)

        # Load Setting
        self.showToolBar = func.str2bool(self.settings.value("showToolbar", True))
        self.tdToolBar.setVisible(self.showToolBar)
        self.compToolBar.setVisible(self.showToolBar)

        # Tabs build
        self.tabWidget = TabWidget(unix, username, package)
        self.setCentralWidget(self.tabWidget)

        # Log record
        self.procedures('log in')

    def buildUI(self, appInfo, message, mainID, url):

        self.layout = self.setGeometry(300, 300, 400, 350)

        # Status bar viewing message
        self.statusBar().showMessage(message['status'])
        # ----------------------------------------------
        # Menu Tool Bar sections
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        exitAction, prefAction = self.fileMenuToolBar(appInfo)
        separator1 = self.createSeparatorAction(appInfo)
        fileMenu.addAction(prefAction)
        fileMenu.addAction(separator1)
        fileMenu.addAction(exitAction)
        # ----------------------------------------------
        toolMenu = menubar.addMenu('Tool')
        cleanPycAction, reconfigaction = self.toolMenuToolBar(appInfo)
        toolMenu.addAction(cleanPycAction)
        toolMenu.addAction(reconfigaction)
        # ----------------------------------------------
        helpMenu = menubar.addMenu('Help')
        aboutAction, creditAction, helpAction = self.helpMenuToolBar(appInfo, mainID, message, url)
        helpMenu.addAction(aboutAction)
        helpMenu.addAction(creditAction)
        helpMenu.addAction(helpAction)
        # ----------------------------------------------
        self.tdToolBar = self.toolBarTD(appInfo)
        self.compToolBar = self.toolBarComp(appInfo)
        self.artToolBar = self.toolBarArt(appInfo)
        # ----------------------------------------------

    def system_tray_icon(self, appInfo):
        trayIconMenu = QMenu(self)

        testIcon = QIcon(func.getIcon('Test'))
        testAction1 = QAction(testIcon, 'Test1', self)
        testAction1.triggered.connect(partial(self.onSysTrayIconClick, 'set1'))

        testIcon = QIcon(func.getIcon('Test'))
        testAction2 = QAction(testIcon, 'Test2', self)
        testAction2.triggered.connect(partial(self.onSysTrayIconClick, 'set2'))

        trayIconMenu.addAction(testAction1)
        trayIconMenu.addAction(testAction2)

        snippingAction = self.createAction(appInfo, 'Snipping Tool')
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

    def fileMenuToolBar(self, appInfo):
        # Preferences
        prefAction = QAction(QIcon(func.getIcon('Preferences')), 'Preferences', self)
        prefAction.setStatusTip('Preferences')
        prefAction.triggered.connect(self.preferences_action_triggered)

        # Exit action
        exitAction = QAction(QIcon(appInfo['Exit'][1]), appInfo['Exit'][0], self)
        exitAction.setStatusTip(appInfo['Exit'][0])
        exitAction.triggered.connect(self.exit_action_trigger)
        return exitAction, prefAction

    def toolMenuToolBar(self, appInfo):
        cleanaction = QAction(QIcon(appInfo['CleanPyc'][1]), appInfo['CleanPyc'][0], self)
        cleanaction.setStatusTip(appInfo['CleanPyc'][0])
        cleanaction.triggered.connect(partial(func.clean_unnecessary_file, '.pyc'))

        reconfigaction = QAction(QIcon(appInfo['ReConfig'][1]), appInfo['ReConfig'][0], self)
        reconfigaction.setStatusTip(appInfo['ReConfig'][0])
        reconfigaction.triggered.connect(func.Generate_info)

        return cleanaction, reconfigaction

    def helpMenuToolBar(self, appInfo, mainid, message, url):
        # About action
        about = QAction(QIcon(appInfo['About'][1]), appInfo['About'][0], self)
        about.setStatusTip(appInfo['About'][0])
        about.triggered.connect(partial(self.subWindow, mainid['About'], message['About'], appInfo['About'][1]))
        # Credit action
        credit = QAction(QIcon(appInfo['Credit'][1]), appInfo['Credit'][0], self)
        credit.setStatusTip(appInfo['Credit'][0])
        credit.triggered.connect(partial(self.subWindow, mainid['Credit'], message['Credit'], appInfo['Credit'][1]))
        # Help action
        helpAction = QAction(QIcon(appInfo['Help'][1]), appInfo['Help'][0], self)
        helpAction.setStatusTip((appInfo['Help'][0]))
        helpAction.triggered.connect(partial(self.openURL, url['Help']))
        return about, credit, helpAction

    def toolBarTD(self, appInfo):
        # TD Tool Bar
        toolBarTD = self.addToolBar('TD')
        # Maya_tk 2017
        if 'Maya 2018' in appInfo:
            maya2017 = self.createAction(appInfo, 'Maya 2017')
            toolBarTD.addAction(maya2017)
        # Maya_tk 2017
        if 'Maya 2017' in appInfo:
            maya2017 = self.createAction(appInfo, 'Maya 2017')
            toolBarTD.addAction(maya2017)

        # ZBrush 4R8
        if 'ZBrush 4R8' in appInfo:
            zbrush4R8 = self.createAction(appInfo, 'ZBrush 4R8')
            toolBarTD.addAction(zbrush4R8)
        # ZBrush 4R7
        if 'ZBrush 4R7' in appInfo:
            zbrush4R7 = self.createAction(appInfo, 'ZBrush 4R7')
            toolBarTD.addAction(zbrush4R7)

        # Houdini FX
        if 'Houdini FX' in appInfo:
            houdiniFX = self.createAction(appInfo, 'Houdini FX')
            toolBarTD.addAction(houdiniFX)

        # plt_mari
        if 'Mari' in appInfo:
            mari = self.createAction(appInfo, 'Mari')
            toolBarTD.addAction(mari)

        # return Tool Bar
        return toolBarTD

    def toolBarComp(self, appInfo):
        # VFX toolBar
        toolBarComp = self.addToolBar('VFX')

        # Davinci
        if 'Resolve' in appInfo:
            davinci = self.createAction(appInfo, 'Resolve')
            toolBarComp.addAction(davinci)

        # NukeX
        if 'NukeX' in appInfo:
            nukeX = self.createAction(appInfo, 'NukeX')
            toolBarComp.addAction(nukeX)

        # Hiero
        if 'Hiero' in appInfo:
            hiero = self.createAction(appInfo, 'Hiero')
            toolBarComp.addAction(hiero)

        # After Effect CC
        if 'After Effects CC' in appInfo:
            aeCC = self.createAction(appInfo, 'After Effects CC')
            toolBarComp.addAction(aeCC)

        # After Effect CS6
        if 'After Effects CS6' in appInfo:
            aeCS6 = self.createAction(appInfo, 'After Effects CS6')
            toolBarComp.addAction(aeCS6)

        # Premiere CC
        if 'Premiere Pro CC' in appInfo:
            prCC = self.createAction(appInfo, 'Premiere Pro CC')
            toolBarComp.addAction(prCC)

        # Premiere CS6
        if 'Premiere Pro CS6' in appInfo:
            prCS6 = self.createAction(appInfo, 'Premiere Pro CS6')
            toolBarComp.addAction(prCS6)

        # Return Tool Bar
        return toolBarComp

    def toolBarArt(self, appInfo):
        toolbarArt = self.addToolBar('Art')

        if 'Photoshop CC' in appInfo:
            ptsCS6 = self.createAction(appInfo, 'Photoshop CC')
            toolbarArt.addAction(ptsCS6)

        # Photoshop CS6
        if 'Photoshop CS6' in appInfo:
            ptsCC = self.createAction(appInfo, 'Photoshop CS6')
            toolbarArt.addAction(ptsCC)

        # Illustrator CC
        if 'Illustrator CC' in appInfo:
            illusCC = self.createAction(appInfo, 'Illustrator CC')
            toolbarArt.addAction(illusCC)

        # Illustrator CS6
        if 'Illustrator CS6' in appInfo:
            illusCS6 = self.createActioin(appInfo, 'Illustrator CS6')
            toolbarArt.addAction(illusCS6)

        return toolbarArt

    def procedures(self, event):
        ultis.dynamic_insert_timelog(event)

    def createAction(self, appInfo, key):
        action = QAction(QIcon(appInfo[key][1]), appInfo[key][0], self)
        action.setStatusTip(appInfo[key][0])
        action.triggered.connect(partial(self.openApplication, appInfo[key][2]))
        return action

    def createSeparatorAction(self, appInfo):
        separator = QAction(QIcon(appInfo['Sep'][0]), appInfo['Sep'][1], self)
        separator.setSeparator(True)
        return separator

    def openApplication(self, path):
        subprocess.Popen(path)

    def subWindow(self, id='Note', message=" ", icon = func.getIcon('Logo')):
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
        # assert type(param) is bool
        self.tdToolBar.setVisible(param)
        self.compToolBar.setVisible(param)
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

    if rememberLogin == 'False' or userdata == [] or userdata == None:
        login = Login()
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
