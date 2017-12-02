# -*- coding: utf-8 -*-
"""
Script Name: desktopUI.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is main file to store everything for the pipeline app

"""

# -------------------------------------------------------------------------------------------------------------
# IMPORT PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
import json
import logging
import math
import os
import subprocess
import sys
import webbrowser
import yaml
from functools import partial

from PyQt5.QtCore import *
from PyQt5.QtGui import *
# ------------------------------------------------------
# IMPORT PTQT5 ELEMENT TO MAKE UI
# ------------------------------------------------------
from PyQt5.QtWidgets import *

# ------------------------------------------------------
# IMPORT FROM PIPELINE TOOLS APP
# ------------------------------------------------------
from tk import appFuncs as func
from tk import defaultVariable as var
from tk import getData
from tk import message as mes

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

# ------------------------------------------------------
# GET INFO DATA BEFORE START
# Update local pc info
# getData.initialize()

# logger.info('Updating data')

# ------------------------------------------------------
# DEFAULT VARIABLES
# ------------------------------------------------------
# UI variables preset for layout customizing
# Dimension
W = 350
H = 260
AVATAR_SIZE = 100
ICON_SIZE = 30
BUFFER = 3

# Margin
M1 = [0, 5, 5, 5, 5]

# Base unit of position to be using in QGridlayout
X = 0
Y = 0
XW = 1
XH = 1
GRID_TOTAL = 9

# Alignment attribute from PyQt5
__center__ = Qt.AlignCenter
__right__ = Qt.AlignRight
__left__ = Qt.AlignLeft
frameStyle = QFrame.Sunken | QFrame.Panel
# Get icon path
# pthInfo = PACKAGE['appData']
# infoData = NAMES['info']

getData.initialize()

filePath = os.path.join(os.getenv('PIPELINE_TOOL'), 'sql_tk\db\main.config.yml')

with open(filePath, 'r') as f:
    APPINFO = yaml.load(f)

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

# ----------------------------------------------------------------------------------------------------------- #
"""                                       SUB CLASS: REGISTER UI                                            """
# ----------------------------------------------------------------------------------------------------------- #
class NewAccount(QDialog):
    TITLEBLANK = 'If title is blank, it will be considered as a "Tester"'

    def __init__(self, parent=None):
        super(NewAccount, self).__init__(parent)
        self.setWindowTitle("Create New Account")
        self.setWindowIcon(QIcon(func.getIcon('Logo')))
        self.layout = QGridLayout()
        # self.layout.setColumnStretch(1, 1)
        # self.layout.setColumnMinimumWidth(1, 250)
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
        okBtn.clicked.connect(self.setOKclciked)
        cancelBtn = QPushButton('Cancel')
        cancelBtn.clicked.connect(sys.exit())
        self.layout.addWidget(okBtn, 8, 0, 1, 2)
        self.layout.addWidget(cancelBtn, 8, 2, 1, 2)
        self.setLayout(self.layout)

    def clabel(self, text):
        label = QLabel(text)
        label.setAlignment(__center__)
        label.setMinimumWidth(50)
        return label

    def setOKclciked(self):
        title = self.regisTitle.text()
        firstname = self.firstnameField.text()
        lastname = self.lastnameField.text()
        password = self.password.text()
        passretype = self.passwordRetype.text()
        check = self.checkMatchPassWord(firstname, lastname, title, password, passretype)
        if not check:
            pass
        else:
            SUCCESS = "%s.%s" % (lastname, firstname)
            self.processNewAcountData(lastname, firstname, title, password)
            QMessageBox.information(self, "Error", SUCCESS, QMessageBox.Retry)
            self.hide()
            login = LoginUI()
            login.show()

    def checkMatchPassWord(self, firstname, lastname, title, password, passretype):
        NOTMATCH = "Password doesn't match"
        FIRSTNAME = "Firstname cannot be blank"
        LASTNAME = "Lastname cannot be blank"
        if title == "":
            title = 'Tester'
        if firstname == "":
            QMessageBox.critical(self, "Error", FIRSTNAME, QMessageBox.Retry)
            return False
        else:
            pass
        if lastname == "":
            QMessageBox.critical(self, "Error", LASTNAME, QMessageBox.Retry)
            return False
        else:
            pass
        if not password == passretype:
            QMessageBox.critical(self, "Password not matches", NOTMATCH, QMessageBox.Retry)
            return False
        else:
            return True

    def processNewAcountData(self, lastname, firstname, title, password):
        from sql_tk.db import ultilitis_user
        reload(ultilitis_user)
        ultilitis_user.CreateNewUser(lastname, firstname, title, password)

# ----------------------------------------------------------------------------------------------------------- #
"""                                       SUB CLASS: USER LOGIN UI                                          """
# ----------------------------------------------------------------------------------------------------------- #
class LoginUI(QDialog):
    appDataPth = os.path.join(os.getenv('PIPELINE_TOOL'), 'sql_tk/db/main.config')

    def __init__(self, parent=None):

        super(LoginUI, self).__init__()

        self.setWindowTitle('Log in')
        self.setWindowIcon(QIcon(func.getIcon('Logo')))
        self.prevUserLogin = os.path.join(os.getenv('PIPELINE_TOOL'), 'sql_tk/db/user.config')
        self.buildUI()

    def buildUI(self):

        self.mainFrame = QGroupBox(self)
        self.mainFrame.setTitle('User Account')
        self.mainFrame.setFixedSize(W, H)
        hboxLogin = QHBoxLayout()
        self.layout = QGridLayout()
        self.layout.setContentsMargins(5, 5, 5, 5)
        loginText = QLabel('User Name: ')
        loginText.setAlignment(__center__)
        self.layout.addWidget(loginText, 0, 0, 1, 2)
        self.userName = QLineEdit()
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
        self.loginBtn.clicked.connect(self.Login_btn)
        self.layout.addWidget(self.loginBtn, 2, 3, 1, 3)
        self.cancelBtn = QPushButton('Cancel')
        self.cancelBtn.clicked.connect(self.Cancel_btn)
        self.layout.addWidget(self.cancelBtn, 2, 6, 1, 3)
        noteLabel = QLabel(mes.LOGIN_NOTE)
        self.layout.addWidget(noteLabel, 3, 0, 1, 9)
        hboxLogin.addLayout(self.layout)
        self.mainFrame.setLayout(hboxLogin)

    def Cancel_btn(self):
        self.close()

    def Login_btn(self, *args):
        user_name = str(self.userName.text())
        pass_word = str(func.encoding(self.passWord.text()))

        if user_name == "":
            QMessageBox.information(self, 'Login Failed', 'Username can not be blank')
        elif pass_word == "":
            QMessageBox.information(self, 'Login Failed', 'No password')
        else:
            self.AttemptLogin(user_name, pass_word)

    def AttemptLogin(self, username, password):
        userData = func.checkUserLogin(username)
        userLogin = {}
        if userData == {}:
            QMessageBox.information(self, 'Login Failed', "Username not exists")
            return
        else:
            if not password == userData[username][7]:
                QMessageBox.information(self, 'Login Failed', "Wrong password")
                return
            else:
                QMessageBox.information(self, 'Login Successful', "Welcome %s" % username)
                userLogin['remember login'] = self.rememberCheckBox.checkState()
                userLogin['username'] = username
                userLogin['group'] = userData[username][8]
                userLogin['avatar'] = userData[username][9]
                userLogin['aka'] = userData[username][6]
                userLogin['title'] = userData[username][5]
                userLogin['fullname'] = userData[username][4]
                func.saveCurrentUserLogin(userLogin)
                self.hide()
                window = DesktopUI()
                window.show()

# ----------------------------------------------------------------------------------------------------------- #
"""                                       SUB CLASS: TAB LAYOUT                                             """
# ----------------------------------------------------------------------------------------------------------- #
class TabWidget(QWidget):

    def __init__(self, parent, package, tabid):

        super(TabWidget, self).__init__(parent)

        with open(os.path.join(os.getenv('PIPELINE_TOOL'), 'sql_tk/db/user.config'), 'r') as f:
            self.curUser = json.load(f)

        self.buildUI(tabid)

    def buildUI(self, tabid):

        self.layout = QVBoxLayout(self)
        # Create Tabs
        self.tabs = QTabWidget()
        self.tabs.setTabIcon(1, QIcon(func.getIcon('Calculator')))
        # self.tabs.setDocumentMode(False)
        # self.tabs.setTabPosition(QTabWidget.West)
        self.tab1 = QGroupBox(self)
        self.tab2 = QGroupBox(self)
        self.tab3 = QGroupBox(self)
        self.tab4 = QGroupBox(self)
        # self.tab5 = QGroupBox(self)
        # self.tabs.resize(package['geo'][1], package['geo'][2])
        # Add Tabs
        self.tabs.addTab(self.tab2, 'Tools')
        # self.tabs.addTab(self.tab3, 'SQL')
        if self.curUser['group'] == 'Admin':
            self.tabs.addTab(self.tab3, 'SQL')
        else:
            pass
        self.tabs.addTab(self.tab4, 'Cal')
        self.tabs.addTab(self.tab1, 'User')
        # self.tabs.addTab(self.tab5, 'Calendar')
        # Create Tab 1 layout
        self.tab1Layout()
        # Create Tab 2 layout
        self.tab2Layout()
        # Create Tab 3 layout
        self.tab3Layout()
        # Create Tab 4 layout
        self.tab4Layout()
        # Create Tab 4 layout
        # self.tab5Layout()
        # Add Tab to Widget
        self.layout.addWidget(self.tabs)

        # Set main layout
        self.setLayout(self.layout)

    def tab1Layout(self):

        # Create Layout for Tab 1
        self.tab1.setTitle(self.curUser['username'])
        # self.tab1.setFixedSize(W, H)

        hboxLayout = QHBoxLayout()

        self.tab1GridLayout = QGridLayout()

        userImg = QPixmap(func.avatar(self.curUser['avatar']))
        userAvatar = QLabel()
        userAvatar.setPixmap(userImg)
        userAvatar.setScaledContents(True)
        userAvatar.setFixedSize(AVATAR_SIZE, AVATAR_SIZE)
        self.tab1GridLayout.addWidget(userAvatar,0,0,3,3)

        settingBtn = QPushButton('Change Avatar')
        self.tab1GridLayout.addWidget(settingBtn, 0,3,1,3)

        settingBtn = QPushButton('Change Password')
        self.tab1GridLayout.addWidget(settingBtn, 1,3,1,3)

        settingBtn = QPushButton('Log Out')
        self.tab1GridLayout.addWidget(settingBtn, 2,3,1,3)

        # userNameLabel = QLabel('AKA: ')
        # userNameLabel.setAlignment(__right__)
        # self.tab1GridLayout.addWidget(userNameLabel, 0,3,1,2)

        # userNameArtist = QLabel(self.curUser['aka'])
        # userNameArtist.setAlignment(__left__)
        # self.tab1GridLayout.addWidget(userNameArtist, 0,5,1,2)

        # titleLabel = QLabel('Group: ')
        # titleLabel.setAlignment(__right__)
        # self.tab1GridLayout.addWidget(titleLabel, 1,3,1,2)

        # classLabel = QLabel(self.curUser['group'])
        # classLabel.setAlignment(__left__)
        # self.tab1GridLayout.addWidget(classLabel,1,5,1,2)

        # prodLabel = QLabel('Title: ')
        # prodLabel.setAlignment(__right__)
        # self.tab1GridLayout.addWidget(prodLabel, 2,3,1,2)
        #
        # classGroup = QLabel(self.curUser['title'])
        # classGroup.setAlignment(__left__)
        # self.tab1GridLayout.addWidget(classGroup, 2,5,1,2)

        # self.tab1.layout.setMaximumSized(100,100)
        hboxLayout.addLayout(self.tab1GridLayout)

        self.tab1.setLayout(hboxLayout)

    def tab2Layout(self):
        # Create Layout for Tab 2
        self.tab2.setTitle('Extra Tool')
        # self.tab2.setFixedSize(W,H)

        vboxLayout = QVBoxLayout()

        tab2HBoxLayout1 = QHBoxLayout()
        tab2HBoxLayout2 = QHBoxLayout()

        # Content tab 2
        dataBrowserIconBtn = self.makeIconButton('Database Browser')
        tab2HBoxLayout1.addWidget(dataBrowserIconBtn)

        arIconBtn = self.makeIconButton('Advance Renamer')
        tab2HBoxLayout1.addWidget(arIconBtn)

        pycharmBtn = self.makeIconButton('PyCharm 2017')
        tab2HBoxLayout1.addWidget(pycharmBtn)

        sublimeBtn = self.makeIconButton('SublimeText 3')
        tab2HBoxLayout1.addWidget(sublimeBtn)

        qtdesignerBtn = self.makeIconButton('QtDesigner')
        tab2HBoxLayout1.addWidget(qtdesignerBtn)

        for key in APPINFO:

            # Mudbox
            if key == 'Mudbox 2017':
                mudbox17Btn = self.makeIconButton(key)
                tab2HBoxLayout1.addWidget(mudbox17Btn)

            if key == '3ds Max 2017':
                max17Btn = self.makeIconButton(key)
                tab2HBoxLayout1.addWidget(max17Btn)

        dictBtn = QPushButton('English Dictionary')
        dictBtn.clicked.connect(self.englishDict)
        tab2HBoxLayout2.addWidget(dictBtn)

        # calculatorBtn = QPushButton('Calculator')
        # calculatorBtn.clicked.connect(self.calculator)
        # tab2HBoxLayout2.addWidget(calculatorBtn)

        vboxLayout.addLayout(tab2HBoxLayout1)
        vboxLayout.addLayout(tab2HBoxLayout2)

        self.tab2.setLayout(vboxLayout)

    def tab3Layout(self):
        # Create Layout for Tab 4
        self.tab3.setTitle('database')

        hboxLayout = QHBoxLayout()

        self.tab3GridLayout = QGridLayout()
        self.tab3GridLayout.addWidget(QLabel('Develope it later'))


        # allUserProfileBtn = QPushButton('User')
        # self.tab3GridLayout.addWidget(allUserProfileBtn, 0, 1, 1, 2)
        # allUserProfileBtn.clicked.connect(partial(self.connectSQL, 'accountCf'))
        #
        # currentLoginDataBtn = QPushButton('Login')
        # self.tab3GridLayout.addWidget(currentLoginDataBtn, 0, 3, 1, 2)
        # currentLoginDataBtn.clicked.connect(partial(self.connectSQL, 'loginCf'))
        #
        # testNewFunctionBtn = QPushButton('Profile')
        # testNewFunctionBtn.clicked.connect(partial(self.connectSQL, 'settingCf'))
        # self.tab3GridLayout.addWidget(testNewFunctionBtn, 0,5,1,2)

        hboxLayout.addLayout(self.tab3GridLayout)

        self.tab3.setLayout(hboxLayout)

    def tab4Layout(self):
        self.tab4.setTitle('Calculator')

        NumDigitButtons = 10

        hboxLayout = QHBoxLayout()
        self.tab4GridLayout = QGridLayout()
        self.tab4GridLayout.setContentsMargins(1,1,1,1)
        hboxLayout.addLayout(self.tab4GridLayout)

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
        self.tab4GridLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.tab4GridLayout.addWidget(self.display,0,0,1,6)
        self.tab4GridLayout.addWidget(self.backspaceButton,1,0,1,2)
        self.tab4GridLayout.addWidget(self.clearButton,1,2,1,2)
        self.tab4GridLayout.addWidget(self.clearAllButton,1,4,1,2)
        self.tab4GridLayout.addWidget(self.clearMemoryButton,2,0)
        self.tab4GridLayout.addWidget(self.readMemoryButton,3,0)
        self.tab4GridLayout.addWidget(self.setMemoryButton,4,0)
        self.tab4GridLayout.addWidget(self.addToMemoryButton,5,0)
        for i in range(1, NumDigitButtons):
            row = ((9 - i) / 3) + 2
            column = ((i - 1) % 3) + 1
            self.tab4GridLayout.addWidget(self.digitButtons[i], row, column)
        self.tab4GridLayout.addWidget(self.digitButtons[0], 5, 1)
        self.tab4GridLayout.addWidget(self.pointButton, 5, 2)
        self.tab4GridLayout.addWidget(self.changeSignButton, 5, 3)
        self.tab4GridLayout.addWidget(self.divisionButton, 2, 4)
        self.tab4GridLayout.addWidget(self.timesButton, 3, 4)
        self.tab4GridLayout.addWidget(self.minusButton, 4, 4)
        self.tab4GridLayout.addWidget(self.plusButton, 5, 4)
        self.tab4GridLayout.addWidget(self.squareRootButton, 2, 5)
        self.tab4GridLayout.addWidget(self.powerButton, 3, 5)
        self.tab4GridLayout.addWidget(self.reciprocalButton, 4, 5)
        self.tab4GridLayout.addWidget(self.equalButton, 5, 5)

        self.tab4.setLayout(hboxLayout)

    def tab5Layout(self):
        # Create Layout for Tab 4
        self.tab5.setTitle('Calendar')

        hboxLayout = QHBoxLayout()

        self.tab5GridLayout = QGridLayout()
        self.tab5GridLayout.addWidget(QLabel('Develope it later'))

        hboxLayout.addLayout(self.tab5GridLayout)

        self.tab5.setLayout(hboxLayout)

    def makeIconButton(self, name):
        icon = QIcon(APPINFO[name][1])
        iconBtn = QPushButton()
        iconBtn.setToolTip(APPINFO[name][0])
        iconBtn.setIcon(icon)
        iconBtn.setFixedSize(ICON_SIZE, ICON_SIZE)
        iconBtn.setIconSize(QSize(ICON_SIZE - BUFFER, ICON_SIZE - BUFFER))
        iconBtn.clicked.connect(partial(self.openApps, APPINFO[name][2]))
        return iconBtn

    def createButton(self, text, member):
        button = Button(text)
        button.clicked.connect(member)
        return button

    def openApps(self, pth):
        subprocess.Popen(pth)

    def englishDict(self):
        from ui import EnglishDict
        reload(EnglishDict)
        EngDict = EnglishDict.EnglishDict()
        EngDict.exec_()

    def connectSQL(self, tableName, *args):
        pass

    def filterClassAllowance(self, func):
        if self.curUserData[self.curUser][1] == 'Admin':
            func()
        else:
            pass

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

# ----------------------------------------------------------------------------------------------------------- #
"""                          MAIN CLASS: DESKTOP UI APPLICATIONS: PIPELINE TOOL                             """
# ----------------------------------------------------------------------------------------------------------- #
class DesktopUI(QMainWindow):

    def __init__(self, case=None, parent = None):

        super(DesktopUI, self).__init__(parent)
        mainID = var.MAIN_ID
        appInfo = APPINFO
        package = var.MAIN_PACKPAGE
        message = var.MAIN_MESSAGE
        names = var.MAIN_NAMES
        url = var.MAIN_URL
        # Set window title
        self.setWindowTitle(mainID['Main'])
        # Set window icon
        self.setWindowIcon(QIcon(func.getIcon('Logo')))
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setToolButtonStyle(Qt.ToolButtonFollowStyle)
        tempUser = os.path.join(os.getenv('PIPELINE_TOOL'), 'sql_tk/db/user.config')

        if not os.path.exists(tempUser):
            sys.exit()

        with open(tempUser, 'r') as f:
            self.curUserData = json.load(f)

        if case == 'Auto login':
            self.autoLogin(str(self.curUserData['username']))

        self.curUser = [f for f in self.curUserData][0]
        # Build UI
        self.buildUI(appInfo, package, message, mainID, names, url)
        # Create Tabs
        self.tabWidget = TabWidget(self, package, var.MAIN_TABID)
        # Put tabs to center of main UI
        self.setCentralWidget(self.tabWidget)
        # ShowUI
        func.proc('log in')

    def buildUI(self, appInfo, package, message, mainID, names, url):
        self.layout = self.setGeometry(300, 300, 400, 350)

        # Status bar viewing message
        self.statusBar().showMessage(message['status'])

        # ----------------------------------------------
        # Menu Tool Bar sections
        menubar = self.menuBar()

        # File menu
        fileMenu = menubar.addMenu('File')
        # Extract actions
        exitAction = self.fileMenuToolBar(appInfo)
        separator1 = self.createSeparatorAction(appInfo)
        # Put actions into file menu
        fileMenu.addAction(separator1)
        fileMenu.addAction(exitAction)

        # Tool Menu
        toolMenu = menubar.addMenu('Tool')
        cleanPycAction, reconfigaction = self.toolMenuToolBar(appInfo)
        # Put actions into the file menu
        toolMenu.addAction(cleanPycAction)
        toolMenu.addAction(reconfigaction)

        # Help Menu
        helpMenu = menubar.addMenu('Help')
        # Extract actions
        aboutAction, creditAction, helpAction = self.helpMenuToolBar(appInfo, mainID, message, url)
        # Put actions into help menu
        helpMenu.addAction(aboutAction)
        helpMenu.addAction(creditAction)
        helpMenu.addAction(helpAction)
        # ----------------------------------------------
        # Shelf toolbar sections
        # TD Tool Bar
        self.tdToolBar = self.toolBarTD(appInfo)
        # comping Tool Bar
        self.compToolBar = self.toolBarComp(appInfo)
        # Art Tool Bar
        # self.artToolBar = self.toolBarArt(appInfo)
        # ----------------------------------------------
        # Systray Icon
        self.tray_Icon = self.system_tray_icon(appInfo)

    def system_tray_icon(self, appInfo):
        trayIconMenu = QMenu(self)

        testIcon = QIcon(func.getIcon('Test'))
        testAction1 = QAction(testIcon, 'Test1', self)
        testAction1.triggered.connect(partial(self.actionConf, 'set1'))

        testIcon = QIcon(func.getIcon('Test'))
        testAction2 = QAction(testIcon, 'Test2', self)
        testAction2.triggered.connect(partial(self.actionConf, 'set2'))

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
        reconfigaction.triggered.connect(partial(getData.initialize, 'rc'))

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

        # Mari_tk
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

    def filterClassAllowance(self, func):
        if self.curUserData[self.curUser][1] == 'Admin':
            func()
        else:
            pass

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

    def subWindow(self, id, message, icon):
        from ui import WindowDialog
        reload(WindowDialog)
        dlg = WindowDialog.WindowDialog(id=id, message=message, icon=icon)
        dlg.exec_()

    def openURL(self, url):
        webbrowser.open(url)

    def screenshot(self):
        from tk import screenshot
        reload(screenshot)
        screenshot.exe_()

    def autoLogin(self, username):
        QMessageBox.information(self, 'Auto Login', "Welcome back %s" % username)

    def actionConf(self, name=None, *args):
        # from sql_tk.db import sqlTools
        # reload(sqlTools)
        # if name == 'set1':
        #     sqlTools.create_predatabase()
        # elif name == 'set2':
        #     sqlTools.create_predatabase()
        # else:
        #     pass
        pass

def initialize():
    app = QApplication(sys.argv)

    # prevUserLogin1 = func.checkTempUserLogin()
    # print prevUserLogin1
    prevUserLogin = os.path.join(os.getenv('PIPELINE_TOOL'), 'sql_tk/db/user.config')
    if not os.path.exists(prevUserLogin):
        login = LoginUI()
        login.show()
    else:
        with open(prevUserLogin, 'r') as f:
            userLogin = json.load(f)

        if userLogin['remember login'] == 0:
            login = LoginUI()
            login.show()
        else:
            window = DesktopUI('Auto login')
            window.show()
            if not QSystemTrayIcon.isSystemTrayAvailable():
                QMessageBox.critical(None, "Systray could not detect any system tray on this system" )

                sys.exit(1)
            QApplication.setQuitOnLastWindowClosed(False)


    sys.exit(app.exec_())

if __name__ == '__main__':
    initialize()

# ----------------------------------------------------------------------------------------------------------- #
"""                                                END OF CODE                                              """
# ----------------------------------------------------------------------------------------------------------- #
