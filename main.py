# -*- coding: utf-8 -*-
"""
Script Name: desktopUI.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is main file to store everything for the pipeline app

"""

# -------------------------------------------------------------------------------------------------------------
# IMPORT PYTHON MODULES
import logging
import math
import os
import shutil
import subprocess
import sys
import webbrowser
from functools import partial

import pip
import yaml
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# ------------------------------------------------------
# IMPORT PTQT5 ELEMENT TO MAKE UI
from PyQt5.QtWidgets import *

from util import message as mes
from util import util_sql as ulti
# ------------------------------------------------------
# IMPORT FROM PIPELINE TOOLS APP
from util import utilities as func
from util import variables as var

# -------------------------------------------------------------------------------------------------------------
logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

# ------------------------------------------------------
# DEFAULT VARIABLES
CURUSERDATA = ulti.query_current_user()
CURUSER = CURUSERDATA[2]
USERCLASS = ulti.query_user_class(CURUSERDATA[0], CURUSERDATA[1])

# Alignment attribute from PyQt5
__center__ = Qt.AlignCenter
__right__ = Qt.AlignRight
__left__ = Qt.AlignLeft
frameStyle = QFrame.Sunken | QFrame.Panel



KEY = 'PIPELINE_TOOL'
TOOL_NAME = 'PipelineTool'
SCR_PATH = os.getcwd()

# Check environment key to get the path to source code
os.environ[KEY] = SCR_PATH
# Name of required packages which should be installed along with Anaconda
packages = ['pywinauto', 'winshell', 'pandas', 'opencv-python', 'pyunpack']

checkList = []

pyPkgs = {}

pyPkgs['__mynote__'] = 'import pip; pip.get_installed_distributions()'

for package in pip.get_installed_distributions():
    name = package.project_name
    if name in packages:
        checkList.append(name)

resault = [p for p in packages if p not in checkList]

if len(resault) > 0:
    for package in resault:
        subprocess.Popen("pip install %s" % packages)

# from util import appFuncs as func

DATA_PATH = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData/database.db')
DATA_BACKUP= os.path.join(os.getenv('PIPELINE_TOOL'), 'appData/backup/database.db')
MAIN_CONFIG_PATH = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData/main_config.yml')
appDataPath = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData')

if not os.path.exists(DATA_PATH):
    shutil.copy2(DATA_BACKUP, DATA_PATH)

maya_tk = os.path.join(SCR_PATH, 'plt_maya')
pythonValue = ""
pythonList = []

mayaBlock = ['util', 'plt_maya', 'icons', 'modules', 'plugins', 'Animation', 'MayaLib', 'Modeling', 'Rigging', 'Sufacing']

for root, dirs, files in os.walk(maya_tk):
    for dir in dirs:
        if dir in mayaBlock:
            dirPth = os.path.join(root, dir)
            pythonList.append(dirPth)

pythonList = list(set(pythonList))

for pth in pythonList:
    pythonValue += pth + ';'

os.environ['PYTHONPATH'] = pythonValue

# Copy userSetup.py from source code to properly maya folder
userSetup_plt_path = os.path.join(os.getcwd(), 'plt_maya/userSetup.py')
userSetup_maya_path = os.path.join(os.path.expanduser('~/Documents/maya/2017/prefs/scripts'), 'userSetup.py')
shutil.copy2(userSetup_plt_path, userSetup_maya_path)

func.Generate_info()

with open(MAIN_CONFIG_PATH, 'r') as f:
    APPINFO = yaml.load(f)

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


"""  Customising QToolButton """
# ----------------------------------------------------------------------------------------------------------- #
class Button(QToolButton):

    def __init__(self, text, parent=None):
        super(Button, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 5)
        size.setWidth(max(size.width(), size.height()))
        return size


"""  Create New Account """
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
        title = self.regisTitle.text()
        if title is None or title == '':
            title = 'Tester'
        else:
            title = str(title)
        FIRSTNAME = "Firstname cannot be blank"
        LASTNAME = "Lastname cannot be blank"
        firstname = str(self.firstnameField.text())
        if firstname == "" or firstname is None:
            QMessageBox.critical(self, "Error", FIRSTNAME, QMessageBox.Retry)
            return False
        else:
            pass
        lastname = str(self.lastnameField.text())
        if lastname == "":
            QMessageBox.critical(self, "Error", LASTNAME, QMessageBox.Retry)
            return False
        else:
            pass

        username = '%s.%s' % (lastname, firstname)
        check = ulti.check_data_exists(username)
        if check:
            USEREXISTS = 'Username %s exists, try again or you already have an account?' % username
            QMessageBox.critical(self, "Username Exists", USEREXISTS, QMessageBox.Retry)
        else:
            pass

        password = str(self.password.text())
        passretype = str(self.passwordRetype.text())
        check = self.checkMatchPassWord(firstname, lastname, title, password, passretype)
        SUCCESS = "Your account has been created: %s" % username
        if not check:
            pass
        else:
            ulti.CreateNewUser(firstname, lastname, title, password)
            QMessageBox.information(self, "Your username", SUCCESS, QMessageBox.Retry)
            self.hide()
            login = Login()
            login.show()

    def checkMatchPassWord(self, firstname, lastname, title, password, passretype):
        NOTMATCH = "Password doesn't match"
        if not password == passretype:
            QMessageBox.critical(self, "Password not matches", NOTMATCH, QMessageBox.Retry)
            return False
        else:
            return True


"""  Login Layout         """
# ----------------------------------------------------------------------------------------------------------- #
class Login(QDialog):

    def __init__(self, parent=None):

        super(Login, self).__init__(parent)

        self.setWindowTitle('Log in')
        self.setWindowIcon(QIcon(func.getIcon('Logo')))
        
        self.buildUI()

    def buildUI(self):

        self.mainFrame = QGroupBox(self)
        self.mainFrame.setTitle('User Account')
        self.mainFrame.setFixedSize(350, 250)
        hboxLogin = QHBoxLayout()
        self.layout = QGridLayout()
        self.layout.setContentsMargins(5, 5, 5, 5)
        loginText = QLabel('User Name: ')
        loginText.setAlignment(__center__)
        self.layout.addWidget(loginText, 0, 0, 1, 2)
        self.userName = QLineEdit(CURUSER)
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
        
        pass_word = self.passWord.text()
        
        if pass_word == "" or pass_word is None:
            QMessageBox.critical(self, 'Login Failed', 'No password')
            
        password = str(func.encoding(pass_word))
        
        checkU = ulti.check_data_exists(username)
        
        if not checkU:
            QMessageBox.critical(self, 'Login Failed', "Username not exists")
        
        check = ulti.check_password_match(username, password)

        if not check:
            QMessageBox.critical(self, 'Login Failed', "Password not match")
        else:
            QMessageBox.information(self, 'Login Successful', "Welcome %s" % username)
            checkState = self.rememberCheckBox.checkState()
            if checkState:
                check = 'True'
            else:
                check = 'False'

            user = ulti.query_current_user()

            token = user[1]
            setting = user[3]
            if setting == check:
                pass
            else:
                ulti.update_user_remember_login(token, setting)
                ulti.dynamic_update_current_user(user[0], user[1], username, user[3])

            self.hide()
            window = Main()
            window.show()


"""   Tab Layout          """
# ----------------------------------------------------------------------------------------------------------- #
class TabWidget(QWidget):

    def __init__(self, package):

        super(TabWidget, self).__init__()
        self.buildUI(package)

    def buildUI(self, package):
        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        # self.tabs.setDocumentMode(False)
        # self.tabs.setTabPosition(QTabWidget.West)
        self.tabs.resize(package['geo'][1], package['geo'][2])

        self.tab1 = QGroupBox(self)
        self.tab2 = QGroupBox(self)
        self.tab3 = QGroupBox(self)
        self.tab4 = QGroupBox(self)
        self.tab5 = QGroupBox(self)

        # Add Tabs
        self.tabs.addTab(self.tab1, 'Tools')
        self.tabs.addTab(self.tab2, 'Prj')
        self.tabs.addTab(self.tab3, 'Cal')
        self.tabs.addTab(self.tab4, 'User')
        self.tabs.addTab(self.tab5, 'SQL')

        # Create Tab 1 layout
        self.tab1Layout()
        self.tab2Layout()
        self.tab3Layout()
        self.tab4Layout()
        self.tab5Layout()

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def tab1Layout(self):
        # Create Layout for Tab 2
        self.tab1.setTitle('Extra Tool')
        # self.tab1.setFixedSize(W,H)
        vboxLayout = QVBoxLayout()
        tab1HBoxLayout1 = QHBoxLayout()
        tab1HBoxLayout2 = QHBoxLayout()

        # Content tab 2
        arIconBtn = self.makeIconButton('Advance Renamer')
        tab1HBoxLayout1.addWidget(arIconBtn)
        pycharmBtn = self.makeIconButton('PyCharm 2017')
        tab1HBoxLayout1.addWidget(pycharmBtn)
        sublimeBtn = self.makeIconButton('SublimeText 3')
        tab1HBoxLayout1.addWidget(sublimeBtn)
        qtdesignerBtn = self.makeIconButton('QtDesigner')
        tab1HBoxLayout1.addWidget(qtdesignerBtn)
        for key in APPINFO:
            # Mudbox
            if key == 'Mudbox 2018':
                mudbox18Btn = self.makeIconButton(key)
                tab1HBoxLayout1.addWidget(mudbox18Btn)
            if key == 'Mudbox 2017':
                mudbox17Btn = self.makeIconButton(key)
                tab1HBoxLayout1.addWidget(mudbox17Btn)
            if key == '3ds Max 2018':
                max18Btn = self.makeIconButton(key)
                tab1HBoxLayout1.addWidget(max18Btn)
            if key == '3ds Max 2017':
                max17Btn = self.makeIconButton(key)
                tab1HBoxLayout1.addWidget(max17Btn)
        dictBtn = QPushButton('English Dictionary')
        dictBtn.clicked.connect(self.englishDict)
        tab1HBoxLayout2.addWidget(dictBtn)

        vboxLayout.addLayout(tab1HBoxLayout1)
        vboxLayout.addLayout(tab1HBoxLayout2)
        self.tab1.setLayout(vboxLayout)

    def tab2Layout(self):
        # Create Layout for Tab 4
        self.tab2.setTitle('database')

        hboxLayout = QHBoxLayout()
        tab2GridLayout = QGridLayout()

        allUserProfileBtn = QPushButton('New Project')
        tab2GridLayout.addWidget(allUserProfileBtn, 0, 0, 1, 2)
        currentLoginDataBtn = QPushButton('Login')
        tab2GridLayout.addWidget(currentLoginDataBtn, 0, 2, 1, 2)
        testNewFunctionBtn = QPushButton('Profile')
        tab2GridLayout.addWidget(testNewFunctionBtn, 0, 4, 1, 2)

        hboxLayout.addLayout(tab2GridLayout)
        self.tab2.setLayout(hboxLayout)

    def tab3Layout(self):
        self.tab3.setTitle('Calculator')
        self.tab3.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        NumDigitButtons = 10

        hboxLayout = QHBoxLayout()
        tab3GridLayout = QGridLayout()
        tab3GridLayout.setContentsMargins(1,1,1,1)
        hboxLayout.addLayout(tab3GridLayout)

        self.pendingAdditiveOperator = ''
        self.pendingMultiplicativeOperator = ''
        self.sumInMemory = 0.0
        self.sumSoFar = 0.0
        self.factorSoFar = 0.0
        self.waitingForOperand = True
        self.display = QLineEdit('0')
        self.display.setReadOnly(False)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(1)
        font = self.display.font()
        font.setPointSize(font.pointSize())
        self.display.setFont(font)
        self.digitButtons = []

        for i in range(NumDigitButtons):
            self.digitButtons.append(self.createButton(str(i), self.digitClicked))

        self.pointButton = self.createButton(".", self.pointClicked)
        self.changeSignButton = self.createButton(u"\N{PLUS-MINUS SIGN}", self.changeSignClicked)
        self.backspaceButton = self.createButton("Backspace", self.backspaceClicked)
        self.clearButton = self.createButton("Clear", self.clear)
        self.clearAllButton = self.createButton("Clear All", self.clearAll)
        self.clearMemoryButton = self.createButton("MC", self.clearMemory)
        self.readMemoryButton = self.createButton("MR", self.readMemory)
        self.setMemoryButton = self.createButton("MS", self.setMemory)
        self.addToMemoryButton = self.createButton("M+", self.addToMemory)
        self.divisionButton = self.createButton(u"\N{DIVISION SIGN}", self.multipleactiveClicked)
        self.timesButton = self.createButton(u"\N{MULTIPLICATION SIGN}", self.multipleactiveClicked)
        self.minusButton = self.createButton("-", self.additiveOperatorClicked)
        self.plusButton = self.createButton("+", self.additiveOperatorClicked)
        self.squareRootButton = self.createButton("Sqrt", self.unaryOperatorClicked)
        self.powerButton = self.createButton(u"x\N{SUPERSCRIPT TWO}", self.unaryOperatorClicked)
        self.reciprocalButton = self.createButton("1/x", self.unaryOperatorClicked)
        self.equalButton = self.createButton("=", self.equalClicked)

        tab3GridLayout.setSizeConstraint(QLayout.SetFixedSize)
        tab3GridLayout.addWidget(self.display,0,0,1,6)
        tab3GridLayout.addWidget(self.backspaceButton,1,0,1,2)
        tab3GridLayout.addWidget(self.clearButton,1,2,1,2)
        tab3GridLayout.addWidget(self.clearAllButton,1,4,1,2)
        tab3GridLayout.addWidget(self.clearMemoryButton,2,0)
        tab3GridLayout.addWidget(self.readMemoryButton,3,0)
        tab3GridLayout.addWidget(self.setMemoryButton,4,0)
        tab3GridLayout.addWidget(self.addToMemoryButton,5,0)
        for i in range(1, NumDigitButtons):
            row = ((9 - i) / 3) + 2
            column = ((i - 1) % 3) + 1
            tab3GridLayout.addWidget(self.digitButtons[i], row, column)
        tab3GridLayout.addWidget(self.digitButtons[0], 5, 1)
        tab3GridLayout.addWidget(self.pointButton, 5, 2)
        tab3GridLayout.addWidget(self.changeSignButton, 5, 3)
        tab3GridLayout.addWidget(self.divisionButton, 2, 4)
        tab3GridLayout.addWidget(self.timesButton, 3, 4)
        tab3GridLayout.addWidget(self.minusButton, 4, 4)
        tab3GridLayout.addWidget(self.plusButton, 5, 4)
        tab3GridLayout.addWidget(self.squareRootButton, 2, 5)
        tab3GridLayout.addWidget(self.powerButton, 3, 5)
        tab3GridLayout.addWidget(self.reciprocalButton, 4, 5)
        tab3GridLayout.addWidget(self.equalButton, 5, 5)

        self.tab3.setLayout(hboxLayout)

    def tab4Layout(self):
        # Create Layout for Tab 1
        self.tab4.setTitle(CURUSER)
        # self.tab1.setFixedSize(W, H)

        hboxLayout = QHBoxLayout()
        tab4ridLayout = QGridLayout()

        userProfile = ulti.query_user_profile(CURUSER, 'username')
        userImg = QPixmap(func.getAvatar(userProfile[7]))
        self.userAvatar = QLabel()
        self.userAvatar.setPixmap(userImg)
        self.userAvatar.setScaledContents(True)
        self.userAvatar.setFixedSize(100, 100)
        tab4ridLayout.addWidget(self.userAvatar, 0, 0, 3, 3)

        changeAvatarBtn = QPushButton('Change Avatar')
        changeAvatarBtn.clicked.connect(self.onChangeAvatarBtnClicked)
        tab4ridLayout.addWidget(changeAvatarBtn, 0,3,1,3)

        settingBtn = QPushButton('Change Password')
        tab4ridLayout.addWidget(settingBtn, 1, 3, 1, 3)

        settingBtn = QPushButton('Log Out')
        tab4ridLayout.addWidget(settingBtn, 2, 3, 1, 3)

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

    def onChangeAvatarBtnClicked(self, ext='jpg'):
        basePth = '%s.avatar.%s' % (CURUSER, ext)
        oldImgPth = os.path.join(os.getenv('PIPELINE_TOOL'), 'imgs/%s.avatar.jpg') % CURUSER
        _bkDir = os.path.join(os.getenv('PIPELINE_TOOL'), 'imgs/backup')
        _bkPth = os.path.join(_bkDir, basePth)
        initialPath = QDir.currentPath() + "/untitled." + ext
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Choose your image file", initialPath,
                                                  "Img Files (*.jpg, *.png)", options=options)
        if fileName:
            if initialPath == oldImgPth:
                pass
            else:
                if not os.path.exists(_bkDir):
                    os.mkdir(_bkDir)
                shutil.copy2(oldImgPth, _bkPth)
                os.remove(oldImgPth)
                shutil.copy2(initialPath, oldImgPth)
                self.userAvatar.setPixmap(QPixmap(oldImgPth))

    def makeIconButton(self, name):
        icon = QIcon(APPINFO[name][1])
        iconBtn = QPushButton()
        iconBtn.setToolTip(APPINFO[name][0])
        iconBtn.setIcon(icon)
        iconBtn.setFixedSize(30, 30)
        iconBtn.setIconSize(QSize(30 - 3, 30 - 3))
        iconBtn.clicked.connect(partial(self.openApps, APPINFO[name][2]))
        return iconBtn

    def createButton(self, text, member):
        button = Button(text)
        button.clicked.connect(member)
        return button

    def openApps(self, pth):
        subprocess.Popen(pth)

    def englishDict(self):
        from ui import english_dictionary
        reload(english_dictionary)
        EngDict = english_dictionary.EnglishDict()
        EngDict.exec_()

    def filteringUI(self):
        # Not Welcome To use this tab
        if USERCLASS == 'FatherOfThisApp':
            self.tab5.setDisabled(True)

    def digitClicked(self):
        clickedButton = self.sender()
        digitValue = int(clickedButton.text())

        if self.display.text() == '0' and digitValue == 0.0:
            return

        if self.waitingForOperand:
            self.display.clear()
            self.waitingForOperand = False

        self.display.setText(self.display.text() + str(digitValue))

    def unaryOperatorClicked(self):
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand = float(self.display.text())

        if clickedOperator == "Sqrt":
            if operand < 0.0:
                self.abortOperation()
                return

            result = math.sqrt(operand)
        elif clickedOperator == u"x\N{SUPERSCRIPT TWO}":
            result = math.pow(operand, 2.0)
        elif clickedOperator == "1/x":
            if operand == 0.0:
                self.abortOperation()
                return

            result = 1.0 / operand

        self.display.setText(str(result))
        self.waitingForOperand = True

    def additiveOperatorClicked(self):
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand = float(self.display.text())

        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return

            self.display.setText(str(self.factorSoFar))
            operand = self.factorSoFar
            self.factorSoFar = 0.0
            self.pendingMultiplicativeOperator = ''

        if self.pendingAdditiveOperator:
            if not self.calculate(operand, self.pendingAdditiveOperator):
                self.abortOperation()
                return

            self.display.setText(str(self.sumSoFar))
        else:
            self.sumSoFar = operand

        self.pendingAdditiveOperator = clickedOperator
        self.waitingForOperand = True

    def multipleactiveClicked(self):
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand = float(self.display.text())

        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return

            self.display.setText(str(self.factorSoFar))
        else:
            self.factorSoFar = operand

        self.pendingMultiplicativeOperator = clickedOperator
        self.waitingForOperand = True

    def equalClicked(self):
        operand = float(self.display.text())

        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return

            operand = self.factorSoFar
            self.factorSoFar = 0.0
            self.pendingMultiplicativeOperator = ''

        if self.pendingAdditiveOperator:
            if not self.calculate(operand, self.pendingAdditiveOperator):
                self.abortOperation()
                return

            self.pendingAdditiveOperator = ''
        else:
            self.sumSoFar = operand

        self.display.setText(str(self.sumSoFar))
        self.sumSoFar = 0.0
        self.waitingForOperand = True

    def pointClicked(self):
        if self.waitingForOperand:
            self.display.setText('0')

        if "." not in self.display.text():
            self.display.setText(self.display.text() + ".")

        self.waitingForOperand = False

    def changeSignClicked(self):
        text = self.display.text()
        value = float(text)

        if value > 0.0:
            text = "-" + text
        elif value < 0.0:
            text = text[1:]

        self.display.setText(text)

    def backspaceClicked(self):
        if self.waitingForOperand:
            return

        text = self.display.text()[:-1]
        if not text:
            text = '0'
            self.waitingForOperand = True

        self.display.setText(text)

    def clear(self):
        if self.waitingForOperand:
            return

        self.display.setText('0')
        self.waitingForOperand = True

    def clearAll(self):
        self.sumSoFar = 0.0
        self.factorSoFar = 0.0
        self.pendingAdditiveOperator = ''
        self.pendingMultiplicativeOperator = ''
        self.display.setText('0')
        self.waitingForOperand = True

    def clearMemory(self):
        self.sumInMemory = 0.0

    def readMemory(self):
        self.display.setText(str(self.sumInMemory))
        self.waitingForOperand = True

    def setMemory(self):
        self.equalClicked()
        self.sumInMemory = float(self.display.text())

    def addToMemory(self):
        self.equalClicked()
        self.sumInMemory += float(self.display.text())

    def abortOperation(self):
        self.clearAll()
        self.display.setText("####")

    def calculate(self, rightOperand, pendingOperator):
        if pendingOperator == "+":
            self.sumSoFar += rightOperand
        elif pendingOperator == "-":
            self.sumSoFar -= rightOperand
        elif pendingOperator == u"\N{MULTIPLICATION SIGN}":
            self.factorSoFar *= rightOperand
        elif pendingOperator == u"\N{DIVISION SIGN}":
            if rightOperand == 0.0:
                return False

            self.factorSoFar /= rightOperand

        return True


"""   Main                """
# ----------------------------------------------------------------------------------------------------------- #
class Main(QMainWindow):

    def __init__(self, case=None, parent = None):

        super(Main, self).__init__(parent)

        mainID = var.MAIN_ID
        appInfo = APPINFO
        package = var.MAIN_PACKPAGE
        message = var.MAIN_MESSAGE
        url = var.MAIN_URL

        self.setWindowTitle(mainID['Main'])
        self.setWindowIcon(QIcon(func.getIcon('Logo')))
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setToolButtonStyle(Qt.ToolButtonFollowStyle)

        if case == 'Auto login':
            self.autoLogin(str(CURUSER))

        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, 'PipelineTool', 'PipelineTool')

        # Build UI
        self.buildUI(appInfo, message, mainID, url)
        self.tabWidget = TabWidget(package)
        self.setCentralWidget(self.tabWidget)
        # ShowUI
        self.procedures('log in')

    def buildUI(self, appInfo, message, mainID, url):

        self.layout = self.setGeometry(300, 300, 400, 350)

        # Status bar viewing message
        self.statusBar().showMessage(message['status'])
        # ----------------------------------------------
        # Menu Tool Bar sections
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        exitAction = self.fileMenuToolBar(appInfo)
        separator1 = self.createSeparatorAction(appInfo)
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
        # self.artToolBar = self.toolBarArt(appInfo)
        # ----------------------------------------------
        self.tray_Icon = self.system_tray_icon(appInfo)
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

        minimizeIcon = QIcon(func.getIcon('Minimize'))
        minimizeAction = QAction(minimizeIcon, "Mi&nimize", self)
        minimizeAction.triggered.connect(self.hide)
        trayIconMenu.addAction(minimizeAction)

        restoreIcon = QIcon(func.getIcon('Restore'))
        restoreAction = QAction(restoreIcon, "&Restore", self)
        restoreAction.triggered.connect(self.showNormal)
        trayIconMenu.addAction(restoreAction)

        quitIcon = QIcon(func.getIcon('Close'))
        quitAction = QAction(quitIcon, "&Quit", self)
        quitAction.triggered.connect(QApplication.instance().quit)
        trayIconMenu.addSeparator()
        trayIconMenu.addAction(quitAction)

        trayIcon = QSystemTrayIcon(self)
        trayIcon.setIcon(QIcon(func.getIcon('Logo')))
        trayIcon.setContextMenu(trayIconMenu)
        trayIcon.show()

        return trayIcon

    def fileMenuToolBar(self, appInfo):
        # Exit action
        exitAction = QAction(QIcon(appInfo['Exit'][1]), appInfo['Exit'][0], self)
        exitAction.setStatusTip(appInfo['Exit'][0])
        exitAction.triggered.connect(qApp.quit)
        return exitAction

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
        # Photoshop CC
        if 'Photoshop CC' in appInfo:
            ptsCS6 = self.createAction(appInfo, 'Photoshop CC')
            toolBarComp.addAction(ptsCS6)
        # Photoshop CS6
        if 'Photoshop CS6' in appInfo:
            ptsCC = self.createAction(appInfo, 'Photoshop CS6')
            toolBarComp.addAction(ptsCC)
        # Illustrator CC
        if 'Illustrator CC' in appInfo:
            illusCC = self.createAction(appInfo, 'Illustrator CC')
            toolBarComp.addAction(illusCC)
        # Illustrator CS6
        if 'Illustrator CS6' in appInfo:
            illusCS6 = self.createActioin(appInfo, 'Illustrator CS6')
            toolBarComp.addAction(illusCS6)
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
        ulti.dynamic_insert_timelog(event)

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
        from ui import about
        reload(about)
        dlg = about.WindowDialog(id=id, message=message, icon=icon)
        dlg.exec_()

    def screenshot(self):
        from ui import screen_shot
        reload(screen_shot)
        dlg = screen_shot.Screenshot()
        dlg.exec_()

    def openURL(self, url):
        webbrowser.open(url)

    def autoLogin(self, username):
        QMessageBox.information(self, 'Auto Login', "Welcome back %s" % username)

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

def main():

    QCoreApplication.setApplicationName("PipelineTool")
    QCoreApplication.setApplicationVersion("0.13")
    QCoreApplication.setOrganizationName("DAMG_TEAM")
    QCoreApplication.setOrganizationDomain("damgteam.com")

    app = QApplication(sys.argv)
    if CURUSERDATA[3] == 'False' or CURUSERDATA == [] or CURUSERDATA == None:
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
