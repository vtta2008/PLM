# -*- coding: utf-8 -*-
"""

Script Name: plt.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This script is master file of Pipeline Tool

"""

__appname__ = "Pipeline Tool"
__module__ = "main"
__version__ = "0.13"
__organization__ = "DAMG team"
__website__ = "www.damgteam.com"
__email__ = "dot@damgteam.com"
__author__ = "Trinh Do, a.k.a: Jimmy"

# -------------------------------------------------------------------------------------------------------------
""" Import modules """

# Python
import logging
import os
import subprocess
import sys
import webbrowser
import sqlite3 as lite
from functools import partial

# PyQt5
from PyQt5.QtCore import Qt, QSize, QCoreApplication, QSettings, QRegExp, QLocale
from PyQt5.QtGui import QIcon, QPixmap, QImage, QRegExpValidator
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFrame, QDialog, QWidget, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QSizePolicy, QLineEdit, QLabel, QPushButton, QMessageBox, QGroupBox,
                             QCheckBox, QTabWidget, QSystemTrayIcon, QAction, QMenu, QComboBox)

# Run Preset
import plt_presets as pltp

KEY, TOOL_NAME = pltp.preset1_plt_root_path()
checkPackage = pltp.preset3_install_extra_python_package()
pltp.preset4_maya_intergrate()

# UI
from ui import ui_account_setting
from ui import ui_preference

# Plt tools
from utilities import utils as func
from utilities import utils_sql as usql
from utilities import message as mess
from utilities import variables as var

# -------------------------------------------------------------------------------------------------------------
""" Declare variables """
# -------------------------------------------------------------------------------------------------------------
# PyQt5 ui elements
__center__ = Qt.AlignCenter
__right__ = Qt.AlignRight
__left__ = Qt.AlignLeft
frameStyle = QFrame.Sunken | QFrame.Panel

# Get apps info configuration
APPINFO = pltp.preset5_gather_configure_info()
SETTING_PATH = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'settings', 'PipelineTool_settings.ini')
DB_PATH = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'database.db')

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain logs """
# -------------------------------------------------------------------------------------------------------------
logPth = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'settings', 'plt.log')

logger = logging.getLogger('plt')
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
""" Create New Account """
# ----------------------------------------------------------------------------------------------------------- #
class Plt_sign_up(QDialog):

    def __init__(self, parent=None):

        super(Plt_sign_up, self).__init__(parent)

        self.setWindowTitle("Sign Up")
        self.setWindowIcon(QIcon(func.getIcon('Logo')))
        self.setContentsMargins(0,0,0,0)
        self.setFixedSize(400, 800)

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.layout.addWidget(clabel("All fields are required."), 0,0,1,6)

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

        account_grid.addWidget(clabel('User Name'), 0, 0, 1, 2)
        account_grid.addWidget(clabel('Password'), 1, 0, 1, 2)
        account_grid.addWidget(clabel('Re-type'), 2, 0, 1, 2)

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

        profile_grid.addWidget(clabel('First Name'), 0, 0, 1, 2)
        profile_grid.addWidget(clabel('Last Name'), 1, 0, 1, 2)
        profile_grid.addWidget(clabel('Your Title'), 2, 0, 1, 2)

        self.titleField = QLineEdit()
        self.firstnameField = QLineEdit()
        self.lastnameField = QLineEdit()

        profile_grid.addWidget(self.firstnameField, 0, 3, 1, 4)
        profile_grid.addWidget(self.lastnameField, 1, 3, 1, 4)
        profile_grid.addWidget(self.titleField, 2, 3, 1, 4)

        return profile_groupBox

    def contact_section(self):

        contact_groupBox = QGroupBox()
        contact_groupBox.setTitle("Contact")
        contact_grid = QGridLayout()
        contact_groupBox.setLayout(contact_grid)

        contact_grid.addWidget(clabel("Line 1"), 0, 0, 1, 2)
        contact_grid.addWidget(clabel("Line 2"), 1, 0, 1, 2)
        contact_grid.addWidget(clabel("Postal"), 2, 0, 1, 2)
        contact_grid.addWidget(clabel("City"), 3, 0, 1, 2)
        contact_grid.addWidget(clabel("Country"), 4, 0, 1, 2)

        self.addressLine1 = QLineEdit()
        self.addressLine2 = QLineEdit()
        self.postalCode = QLineEdit()
        self.cityLst = QLineEdit()
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

        self.checkBox = QCheckBox(mess.USER_CHECK)
        btn_grid.addWidget(self.checkBox, 0, 0, 1, 1)

        okBtn = QPushButton('Create Account')
        okBtn.clicked.connect(self.on_create_btn_clicked)
        btn_grid.addWidget(okBtn, 1, 0, 1, 1)

        cancelBtn = QPushButton('Cancel')
        cancelBtn.clicked.connect(self.close)
        btn_grid.addWidget(cancelBtn, 1, 1, 1, 1)

        return btn_groupBox

    def on_create_btn_clicked(self):

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
            QMessageBox.critical(self, "Error", mess.FIRSTNAME_BLANK, QMessageBox.Retry)
            return False
        elif lastname == "":
            QMessageBox.critical(self, "Error", mess.LASTNAME_BLANK, QMessageBox.Retry)
            return False
        else:
            pass

        username = '%s.%s' % (lastname, firstname)

        # Check username already exists
        check = usql.check_data_exists(username)
        if check:
            USEREXISTS = 'Username %s exists, try again or you already have an account?' % username
            QMessageBox.critical(self, "Username Exists", USEREXISTS, QMessageBox.Retry)
        else:
            pass

        # Get password and retype password then check them
        password = str(self.password.text())
        passretype = str(self.passwordRetype.text())
        check = self.check_password_matching(password, passretype)

        SUCCESS = "Your account has been created: %s" % username
        if not check:
            pass
        else:
            usql.CreateNewUser(firstname, lastname, title, password)
            QMessageBox.information(self, "Your username", SUCCESS, QMessageBox.Retry)
            self.hide()
            login = Sign_in_layout()
            login.show()

    def check_password_matching(self, password, passretype):

        if not password == passretype:
            QMessageBox.critical(self, "Warning", mess.PASSWORD_UNMATCH, QMessageBox.Retry)
            return False
        else:
            return True


# -------------------------------------------------------------------------------------------------------------
""" Login Layout """
# -------------------------------------------------------------------------------------------------------------
class Sign_in_layout(QDialog):

    def __init__(self, parent=None):

        super(Sign_in_layout, self).__init__(parent)

        # Sign in layout preset
        self.setWindowTitle('Sign in')
        self.setWindowIcon(QIcon(func.getIcon('Logo')))
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedSize(360, 240)

        # Main layout
        self.layout = QGridLayout()

        # Layout content
        self.buildUI()

        # Load layout content
        self.setLayout(self.layout)

    def buildUI(self):

        unix, token, curUser, rememberLogin, status = pltp.preset6_query_user_info()

        login_groupBox = QGroupBox()
        login_groupBox.setTitle('Sign in')
        login_grid = QGridLayout()
        login_groupBox.setLayout(login_grid)

        self.usernameField = QLineEdit(curUser)
        self.passwordField = QLineEdit()
        self.rememberCheckBox = QCheckBox('Remember me.')
        self.passwordField.setEchoMode(QLineEdit.Password)

        login_btn = QPushButton('Login')
        cancel_btn = QPushButton('Cancel')
        sign_up_btn = QPushButton('Sign up')

        login_btn.clicked.connect(self.on_sign_in_btn_clicked)
        cancel_btn.clicked.connect(self.close)
        sign_up_btn.clicked.connect(self.on_sign_up_btn_clicked)

        login_grid.addWidget(clabel('Username'), 1, 0, 1, 2)
        login_grid.addWidget(clabel('Password'), 2, 0, 1, 2)
        login_grid.addWidget(self.usernameField, 1, 2, 1, 4)
        login_grid.addWidget(self.passwordField, 2, 2, 1, 4)

        login_grid.addWidget(self.rememberCheckBox, 3, 3, 1, 2)

        login_grid.addWidget(login_btn, 4, 0, 1, 3)
        login_grid.addWidget(cancel_btn, 4, 3, 1, 3)

        login_grid.addWidget(clabel(mess.SIGN_UP), 5, 0, 1, 3)
        login_grid.addWidget(sign_up_btn, 5, 3, 1, 3)

        self.layout.addWidget(login_groupBox, 0, 0, 1, 1)

    def on_sign_up_btn_clicked(self):
        self.hide()
        print 1
        signup = Plt_sign_up()
        print 2
        signup.show()
        print 3
        signup.exec_()
        print 4

    def on_sign_in_btn_clicked(self):
        username = str(self.userName.text())

        if username == "" or username is None:
            QMessageBox.critical(self, 'Login Failed', mess.USERNAME_BLANK)
            return

        pass_word = self.passWord.text()

        if pass_word == "" or pass_word is None:
            QMessageBox.critical(self, 'Login Failed', mess.PASSWORD_BLANK)
            return

        password = str(func.encoding(pass_word))

        checkUserExists = usql.check_data_exists(username)
        checkUserStatus = usql.query_user_status(username)

        if not checkUserExists:
            QMessageBox.critical(self, 'Login Failed', mess.USER_NOT_EXSIST)
        elif checkUserStatus == 'disabled':
            QMessageBox.critical(self, 'Login Failed', "This username is not activated")

        checkPasswordMatch = usql.check_password_match(username, password)

        if not checkPasswordMatch:
            QMessageBox.critical(self, 'Login Failed', "Password not match")
        else:
            QMessageBox.information(self, 'Login Successful', "Welcome %s" % username)
            checkSettingState = self.rememberCheckBox.checkState()
            if checkSettingState:
                setting = 'True'
            else:
                setting = 'False'

            user_profile = usql.query_user_profile(username)
            token = user_profile[1]
            unix = user_profile[0]

            usql.update_user_remember_login(token, setting)
            usql.update_current_user(unix, token, username, setting)

            self.hide()
            window = Main_layout()
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

        userClass = usql.query_user_class(unix=unix, username=username)

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
        line1HBoxLayout = QHBoxLayout()
        line2HBoxLayout = QHBoxLayout()
        line3HBoxLayout = QHBoxLayout()

        # Content
        # ------------------------------------------------------
        line1HBoxLayout.addWidget(QLabel('Extra app: '))

        # Advance Renamer
        arIconBtn = self.make_icon_btn2('Advance Renamer')
        line1HBoxLayout.addWidget(arIconBtn)

        # Note
        noteReminderBtn = self.make_icon_btn1('QtNote', 'Note Reminder', self.note_reminder)
        line1HBoxLayout.addWidget(noteReminderBtn)

        textEditorBtn = self.make_icon_btn1('Text Editor', 'Text Editor', self.text_editor)
        line1HBoxLayout.addWidget(textEditorBtn)

        for key in APPINFO:
            # Mudbox 2018
            if key == 'Mudbox 2018':
                mudbox18Btn = self.make_icon_btn2(key)
                line1HBoxLayout.addWidget(mudbox18Btn)
            # Mudbox 2017
            if key == 'Mudbox 2017':
                mudbox17Btn = self.make_icon_btn2(key)
                line1HBoxLayout.addWidget(mudbox17Btn)
            # 3ds Max 2018
            if key == '3ds Max 2018':
                max18Btn = self.make_icon_btn2(key)
                line1HBoxLayout.addWidget(max18Btn)
            # 3ds Max 2017
            if key == '3ds Max 2017':
                max17Btn = self.make_icon_btn2(key)
                line1HBoxLayout.addWidget(max17Btn)

        # ------------------------------------------------------
        line2HBoxLayout.addWidget(QLabel('Enhance: '))

        # English dictionary
        dictBtn = self.make_icon_btn1('English Dictionary', 'English Dictionary', self.english_dictionary)
        line2HBoxLayout.addWidget(dictBtn)

        # Screenshot
        screenshotBtn = self.make_icon_btn1('Screenshot', 'Screenshot', self.make_screen_shot)
        line2HBoxLayout.addWidget(screenshotBtn)

        # Calendar
        calendarBtn = self.make_icon_btn1('Calendar', 'Calendar', self.calendar)
        line2HBoxLayout.addWidget(calendarBtn)

        # Calculator
        calculatorBtn = self.make_icon_btn1('Calculator', 'Calculator', self.calculator)
        line2HBoxLayout.addWidget(calculatorBtn)

        # File finder
        fileFinderBtn = self.make_icon_btn1('Finder', 'Find files', self.findFiles)
        line2HBoxLayout.addWidget(fileFinderBtn)

        # ------------------------------------------------------
        line3HBoxLayout.addWidget(QLabel('Dev: '))

        # PyCharm
        pycharmBtn = self.make_icon_btn2('PyCharm')
        line3HBoxLayout.addWidget(pycharmBtn)

        # SublimeText
        sublimeBtn = self.make_icon_btn2('SublimeText 3')
        line3HBoxLayout.addWidget(sublimeBtn)

        # Qt Designer
        qtdesignerBtn = self.make_icon_btn2('QtDesigner')
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
        createProjectBtn.clicked.connect(self.create_new_project)
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
        # self.tab1.setFixedSize(W, H)

        hboxLayout = QHBoxLayout()
        tab3ridLayout = QGridLayout()

        userProfile = usql.query_user_profile(curUser, 'username')
        userImg = QPixmap.fromImage(QImage(func.getAvatar(userProfile[7])))
        self.userAvatar = QLabel()
        self.userAvatar.setPixmap(userImg)
        self.userAvatar.setScaledContents(True)
        self.userAvatar.setFixedSize(100, 100)
        tab3ridLayout.addWidget(self.userAvatar, 0, 0, 3, 3)

        accountSettingBtn = QPushButton('Account Setting')
        accountSettingBtn.clicked.connect(partial(self.on_account_setting_btn_clicked, curUser))
        tab3ridLayout.addWidget(accountSettingBtn, 0, 3, 1, 3)

        logoutBtn = QPushButton('Log Out')
        logoutBtn.clicked.connect(self.on_log_out_btn_clicked)
        tab3ridLayout.addWidget(logoutBtn, 1, 3, 1, 3)

        hboxLayout.addLayout(tab3ridLayout)
        self.tab3.setLayout(hboxLayout)

    def tab4Layout(self):
        # Create Layout for Tab 4.
        self.tab4.setTitle('Library')
        # self.tab4.setFixedSize(W, H)

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

    def on_account_setting_btn_clicked(self, username):
        reload(ui_account_setting)
        window = ui_account_setting.WindowDialog(self, username)
        window.exec_()

    def user_avatar_changed(self, curUser):
        sig = ui_account_setting.WindowDialog(self, curUser).changAvatarSignal
        # print sig

    def on_log_out_btn_clicked(self):
        unix, token, curUser, rememberLogin, status = pltp.preset6_query_user_info()

        user_profile = usql.query_user_profile(curUser)
        token = user_profile[1]
        unix = user_profile[0]

        usql.update_user_remember_login(token, 'Flase')
        usql.update_current_user(unix, token, curUser, 'False')

    def make_icon_btn1(self, iconName, tooltip, func_tool):
        icon = QIcon(func.getIcon(iconName))
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
        reload(ui_english_dict)
        EngDict = ui_english_dict.EnglishDict()
        EngDict.exec_()

    def make_screen_shot(self):
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

    def create_new_project(self):
        from ui import ui_new_project
        reload(ui_new_project)
        window = ui_new_project.NewProject()
        window.exec_()

# -------------------------------------------------------------------------------------------------------------
""" Pipeline Tool main layout """
# -------------------------------------------------------------------------------------------------------------
class Main_layout(QMainWindow):

    def __init__(self, case=None, parent=None):
        unix, token, username, rememberLogin, status = pltp.preset6_query_user_info()
        super(Main_layout, self).__init__(parent)

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
        usql.dynamic_insert_timelog(event)

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

    unix, token, curUser, rememberLogin, status = pltp.preset6_query_user_info()
    userdata = [unix, token, curUser, rememberLogin]

    app = QApplication(sys.argv)

    if rememberLogin == 'False' or userdata == [] or userdata == None:
        login = Sign_in_layout()
        login.show()
    else:
        window = Main_layout('Auto login')
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