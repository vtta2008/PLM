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
import json, logging, os, subprocess, sys, webbrowser, yaml
from functools import partial
from tk import message as mes
# ------------------------------------------------------
# IMPORT PTQT5 ELEMENT TO MAKE UI
# ------------------------------------------------------
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# ------------------------------------------------------
# IMPORT FROM PIPELINE TOOLS APP
# ------------------------------------------------------
from tk import appFuncs as func
from tk import defaultVariable as var
from tk import getData

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

# Get icon path
# pthInfo = PACKAGE['appData']
# infoData = NAMES['info']

getData.initialize()

filePath = os.path.join(os.getenv('PIPELINE_TOOL'), 'sql_tk\db\main.config.yml')

with open(filePath, 'r') as f:
    APPINFO = yaml.load(f)

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
        # self.tabs.setDocumentMode(True)
        # self.tabs.setTabPosition(QTabWidget.West)
        self.tab1 = QGroupBox(self)
        self.tab2 = QGroupBox(self)
        self.tab3 = QGroupBox(self)
        self.tab4 = QGroupBox(self)
        # self.tabs.resize(package['geo'][1], package['geo'][2])
        # Add Tabs
        self.tabs.addTab(self.tab1, 'User')
        self.tabs.addTab(self.tab2, 'Tools')
        self.tabs.addTab(self.tab3, 'Projects')
        if self.curUser['group'] == 'Admin':
            self.tabs.addTab(self.tab4, 'Admin')
        else:
            pass

        # Create Tab 1 layout
        self.tab1Layout()

        # Create Tab 2 layout
        self.tab2Layout()

        # Create Tab 3 layout
        self.tab3Layout()

        # Create Tab 4 layout
        self.tab4Layout()

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

        updateLibraryBtn = QPushButton('Update Library')
        updateLibraryBtn.clicked.connect(self.updateLibrary)
        tab2HBoxLayout2.addWidget(updateLibraryBtn)

        vboxLayout.addLayout(tab2HBoxLayout1)
        vboxLayout.addLayout(tab2HBoxLayout2)

        self.tab2.setLayout(vboxLayout)

    def tab3Layout(self):
        self.tab3.setTitle('Project Tool')

        hboxLayout = QHBoxLayout()
        self.tab3GridLayout = QGridLayout()
        self.tab3GridLayout.addWidget(QLabel('Will design this tab later on'), 0,0)

        hboxLayout.addLayout(self.tab3GridLayout)
        self.tab3.setLayout(hboxLayout)

    def tab4Layout(self):
        # Create Layout for Tab 4
        self.tab4.setTitle('SQL Tool')

        hboxLayout = QHBoxLayout()

        self.tab4GridLayout = QGridLayout()

        dataBrowserIconBtn = self.makeIconButton('Database Browser')
        self.tab4GridLayout.addWidget(dataBrowserIconBtn, 0, 0, 1, 1)

        allUserProfileBtn = QPushButton('User')
        self.tab4GridLayout.addWidget(allUserProfileBtn, 0, 1, 1, 2)
        allUserProfileBtn.clicked.connect(partial(self.connectSQL, 'accountCf'))

        currentLoginDataBtn = QPushButton('Login')
        self.tab4GridLayout.addWidget(currentLoginDataBtn, 0, 3, 1, 2)
        currentLoginDataBtn.clicked.connect(partial(self.connectSQL, 'LoginCf'))

        testNewFunctionBtn = QPushButton('Profile')
        testNewFunctionBtn.clicked.connect(partial(self.connectSQL, 'SettingCf'))
        self.tab4GridLayout.addWidget(testNewFunctionBtn, 0,5,1,2)

        hboxLayout.addLayout(self.tab4GridLayout)

        self.tab4.setLayout(hboxLayout)

    def makeIconButton(self, name):
        icon = QIcon(APPINFO[name][1])
        iconBtn = QPushButton()
        iconBtn.setToolTip(APPINFO[name][0])
        iconBtn.setIcon(icon)
        iconBtn.setFixedSize(ICON_SIZE, ICON_SIZE)
        iconBtn.setIconSize(QSize(ICON_SIZE - BUFFER, ICON_SIZE - BUFFER))
        iconBtn.clicked.connect(partial(self.openApps, APPINFO[name][2]))
        return iconBtn

    def openApps(self, pth):
        subprocess.Popen(pth)

    def englishDict(self):
        from ui import EnglishDict
        reload(EnglishDict)
        EngDict = EnglishDict.EnglishDict()
        EngDict.exec_()

    def connectSQL(self, tableName, *args):
        from ui import SqlTable
        reload(SqlTable)
        SqlTable = SqlTable.SqlTable(tableName)
        SqlTable.exec_()

    def testNewFunction(self):
        from tk import testFunction
        reload(testFunction)
        testFunction.testFunction()

    def updateLibrary(self):
        from lib_tk import LibHandle
        reload(LibHandle)
        LibHandle.initialize()

    def filterClassAllowance(self, func):
        if self.curUserData[self.curUser][1] == 'Admin':
            func()
        else:
            pass

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
        self.artToolBar = self.toolBarArt(appInfo)

        # Systray Icon
        self.tray_Icon = self.system_tray_icon(appInfo)

    def system_tray_icon(self, appInfo):
        trayIconMenu = QMenu(self)

        testIcon = QIcon(func.getIcon('Test'))
        testAction1 = QAction(testIcon, 'Test1', self)
        testAction1.triggered.connect(partial(self.testActionDef, 'set1'))

        testIcon = QIcon(func.getIcon('Test'))
        testAction2 = QAction(testIcon, 'Test2', self)
        testAction2.triggered.connect(partial(self.testActionDef, 'set2'))

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
            pass
        # After Effect CS6
        elif 'After Effects CS6' in appInfo:
            aeCS6 = self.createAction(appInfo, 'After Effects CS6')
            toolBarComp.addAction(aeCS6)
        # Premiere CC
        if 'Premiere Pro CC' in appInfo:
            prCC = self.createAction(appInfo, 'Premiere Pro CC')
            toolBarComp.addAction(prCC)
            pass
        elif 'Premiere Pro CS6' in appInfo:
            prCS6 = self.createAction(appInfo, 'Premiere Pro CS6')
            toolBarComp.addAction(prCS6)
        # Return Tool Bar
        return toolBarComp

    def toolBarArt(self, appInfo):
        toolbarArt = self.addToolBar('Art')

        # Photoshop CC
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
        screenshot.initialize()

    def autoLogin(self, username):
        QMessageBox.information(self, 'Auto Login', "Welcome back %s" % username)

    def testActionDef(self, name=None, *args):
        from sql_tk import sqlTools
        reload(sqlTools)
        if name == 'set1':
            sqlTools.create_predatabase()
        elif name == 'set2':
            sqlTools.create_predatabase()
        else:
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
