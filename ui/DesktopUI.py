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
        self.tab1GridLayout.addWidget(userAvatar,0,0,5,5)

        userNameLabel = QLabel('AKA: ')
        userNameLabel.setAlignment(__right__)
        self.tab1GridLayout.addWidget(userNameLabel, 0,5,1,2)

        userNameArtist = QLabel(self.curUser['aka'])
        userNameArtist.setAlignment(__left__)
        self.tab1GridLayout.addWidget(userNameArtist, 0,7,1,2)

        titleLabel = QLabel('Group: ')
        titleLabel.setAlignment(__right__)
        self.tab1GridLayout.addWidget(titleLabel, 1,5,1,2)

        classLabel = QLabel(self.curUser['group'])
        classLabel.setAlignment(__left__)
        self.tab1GridLayout.addWidget(classLabel,1,7,1,2)

        prodLabel = QLabel('Title: ')
        prodLabel.setAlignment(__right__)
        self.tab1GridLayout.addWidget(prodLabel, 2,5,1,2)

        classGroup = QLabel(self.curUser['title'])
        classGroup.setAlignment(__left__)
        self.tab1GridLayout.addWidget(classGroup, 2,7,1,2)

        settingBtn = QPushButton('Your Account')
        self.tab1GridLayout.addWidget(settingBtn, 4,5,1,2)

        settingBtn = QPushButton('Setting')
        self.tab1GridLayout.addWidget(settingBtn, 4,7,1,2)

        # self.check_box = QCheckBox('Minimize to Tray')
        # self.check_box.setCheckState(True)
        # self.tab1GridLayout.addWidget(self.check_box, 5,5,1,2)
        # self.tab1GridLayout.addItem(QSpacerItem(0,1,QSizePolicy.Expanding, QSizePolicy.Expanding),2,0)

        # self.tray_icon = QSystemTrayIcon(self)
        # self.tray_icon.setIcon(QIcon(func.getIcon('Logo')))
        # show_action = QAction('Show', self)
        # quit_action = QAction('Exit', self)
        # hide_action = QAction("Hide", self)
        # show_action.triggered.connect(self.show)
        # hide_action.triggered.connect(self.hide)
        # quit_action.triggered.connect(qApp.quit)
        # tray_menu = QMenu()
        # tray_menu.addAction(show_action)
        # tray_menu.addAction(hide_action)
        # tray_menu.addAction(quit_action)
        # self.tray_icon.setContextMenu(tray_menu)
        # self.tray_icon.show()

        settingBtn = QPushButton('Log Out')
        self.tab1GridLayout.addWidget(settingBtn, 5,7,1,2)

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

        for key in APPINFO:
            # Illustrator
            if key == 'Illustrator CC':
                illusBtn = self.makeIconButton(key)
                tab2HBoxLayout1.addWidget(illusBtn)
            elif key == 'Illustrator CS6':
                illusBtn = self.makeIconButton(key)
                tab2HBoxLayout1.addWidget(illusBtn)
            # Mudbox
            if key == 'Mudbox 2017':
                mudboxBtn = self.makeIconButton(key)
                tab2HBoxLayout1.addWidget(mudboxBtn)
            if key == 'Mudbox 2016':
                mudboxBtn = self.makeIconButton(key)
                tab2HBoxLayout1.addWidget(mudboxBtn)

        icon = QIcon(os.path.join(os.getenv('PIPELINE_TOOL'), 'icons/AdvanceRenamer.icon.png'))
        pth = os.path.join(os.getenv('PIPELINE_TOOL'), 'apps/batchRenamer/ARen.exe')
        iconBtn = QPushButton()
        iconBtn.setToolTip('Advance Renamer 3.8')
        iconBtn.setIcon(icon)
        iconBtn.setFixedSize(ICON_SIZE, ICON_SIZE)
        iconBtn.setIconSize(QSize(ICON_SIZE - BUFFER, ICON_SIZE - BUFFER))
        iconBtn.clicked.connect(partial(self.openApps, pth))
        tab2HBoxLayout1.addWidget(iconBtn)

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
        self.tab4.setTitle('Admin Tool')

        hboxLayout = QHBoxLayout()

        self.tab4GridLayout = QGridLayout()

        # Content tab 3
        icon = QIcon(os.path.join(os.getenv('PIPELINE_TOOL'), 'icons/SqliteTool.icon.png'))
        pth = os.path.join(os.getenv('PIPELINE_TOOL'), 'apps/__admin__/SQLiteDatabaseBrowserPortable.exe')
        iconBtn = QPushButton()
        iconBtn.setToolTip('Database Tool(Admin)')
        iconBtn.setIcon(icon)
        iconBtn.setFixedSize(ICON_SIZE, ICON_SIZE)
        iconBtn.setIconSize(QSize(ICON_SIZE - BUFFER, ICON_SIZE - BUFFER))
        iconBtn.clicked.connect(partial(self.openApps, pth))
        self.tab4GridLayout.addWidget(iconBtn, 0, 0, 1, 1)

        allUserProfileBtn = QPushButton('User Profile')
        self.tab4GridLayout.addWidget(allUserProfileBtn, 1, 0, 1, 2)
        allUserProfileBtn.clicked.connect(partial(self.userDatabase, 'user_profile'))

        currentLoginDataBtn = QPushButton('Current Profile')
        self.tab4GridLayout.addWidget(currentLoginDataBtn, 2, 0, 1, 2)
        currentLoginDataBtn.clicked.connect(self.currentUserLogin)

        testNewFunctionBtn = QPushButton('Test New Function')
        testNewFunctionBtn.clicked.connect(self.testNewFunction)
        self.tab4GridLayout.addWidget(testNewFunctionBtn, 1,2,1,2)

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

    def userDatabase(self, tableName, *args):
        from ui import SqlTable
        reload(SqlTable)
        SqlTable = SqlTable.SqlTable(tableName)
        SqlTable.exec_()

    def currentUserLogin(self, *args):
        from ui import SqlTable
        reload(SqlTable)
        SqlTable = SqlTable.SqlTable('current_login')
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

    def closeEvent(self, event):

        if self.check_box.isChecked():
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "Tray Program",
                "Application was minimized to Tray",
                QSystemTrayIcon.Information,
                2000
                )

class LeftClickMenu(QMenu):
    def __init__(self, parent=None):
        QMenu.__init__(self, "File", parent)

        icon = QIcon(func.getIcon('New'))
        self.addAction(QAction(icon, "&New", self))

        icon = QIcon(func.getIcon('Open'))
        self.addAction(QAction(icon, "&Open", self))

        icon = QIcon(func.getIcon('Save'))
        self.addAction(QAction(icon, "&Save", self))

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        QSystemTrayIcon.__init__(self, parent)
        self.setIcon(QIcon(func.getIcon('Logo')))

        self.left_menu = LeftClickMenu()
        self.setContextMenu(self.left_menu)

        self.activated.connect(self.click_trap)

    def click_trap(self, value):
        if value == self.Trigger:  # left click!
            self.left_menu.exec_(QCursor.pos())

    def welcome(self):
        self.showMessage("Hello", "I should be aware of both buttons")

    def show(self):
        QSystemTrayIcon.show(self)
        QTimer.singleShot(100, self.welcome)


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
        # VFX Tool Bar
        self.compToolBar = self.toolBarComp(appInfo)
        # support ToolBar
        # self.supportApps = self.supApps( appInfo )

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
        if 'Maya 2017' in appInfo:
            maya2017 = self.createAction(appInfo, 'Maya 2017')
            toolBarTD.addAction(maya2017)
        # Maya_tk 2016
        elif 'Maya 2016' in appInfo:
            maya2016 = self.createAction(appInfo, 'Maya 2016')
            toolBarTD.addAction(maya2016)
        else:
            pass

        # 3ds Max 2017
        if '3ds Max 2017' in appInfo:
            max2017 = self.createAction(appInfo, '3ds Max 2017')
            toolBarTD.addAction(max2017)

        # ZBrush 4R8
        if 'ZBrush 4R8' in appInfo:
            zbrush4R8 = self.createAction(appInfo, 'ZBrush 4R8')
            toolBarTD.addAction(zbrush4R8)
        # ZBrush 4R7
        elif 'ZBrush 4R7' in appInfo:
            zbrush4R7 = self.createAction(appInfo, 'ZBrush 4R7')
            toolBarTD.addAction(zbrush4R7)
        else:
            pass

        # Houdini FX
        if 'Houdini FX' in appInfo:
            houdiniFX = self.createAction(appInfo, 'Houdini FX')
            toolBarTD.addAction(houdiniFX)
        else:
            pass
        # Mari_tk
        if 'Mari' in appInfo:
            mari = self.createAction(appInfo, 'Mari')
            toolBarTD.addAction(mari)
        else:
            pass

        # Photoshop CC
        if 'Photoshop CC' in appInfo:
            ptsCS6 = self.createAction(appInfo, 'Photoshop CC')
            toolBarTD.addAction(ptsCS6)
        # Photoshop CS6
        elif 'Photoshop CS6' in appInfo:
            ptsCC = self.createAction(appInfo, 'Photoshop CS6')
            toolBarTD.addAction(ptsCC)
        else:
            pass

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
        dlg = WindowDialog(id, message, icon)
        dlg.exec_()

    def openURL(self, url):
        webbrowser.open(url)

    def autoLogin(self, username):
        QMessageBox.information(self, 'Auto Login', "Welcome back %s" % username)

    def closeEvent(self, event):
        reply = QMessageBox.Information(self, 'Confirm', 'It will minimize to tray', QMessageBox.Ok, QMessageBox.No)

        if reply is QMessageBox.Ok:
            event.ignore()
            self.hide()
            self.tray_icon.showMessage("Minimized to tray", QSystemTrayIcon.Information, 2000)

def initialize():
    app = QApplication(sys.argv)
    tray = SystemTrayIcon()
    tray.show()

    prevUserLogin1 = func.checkTempUserLogin()
    print prevUserLogin1
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

    sys.exit(app.exec_())

if __name__ == '__main__':
    initialize()

# ----------------------------------------------------------------------------------------------------------- #
"""                                                END OF CODE                                              """
# ----------------------------------------------------------------------------------------------------------- #
