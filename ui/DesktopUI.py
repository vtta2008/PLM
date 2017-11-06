# -*- coding: utf-8 -*-
"""
Script Name: desktopUI.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is main file to store everything for the pipeline app

for any question or feedback, feel free to email me: dot@damgteam.com or damgteam@gmail.com
"""
# -------------------------------------------------------------------------------------------------------------
# IMPORT PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
import json, logging, os, subprocess, sys, webbrowser
from functools import partial
from tk import appFuncs as func
from tk import defaultVariable as var
from tk import getData

# -------------------------------------------------------------------------------------------------------------
# IMPORT PTQT5 ELEMENT TO MAKE UI
# -------------------------------------------------------------------------------------------------------------
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

# ------------------------------------------------------
# GET INFO DATA BEFORE START
# Update local pc info
getData.initialize()

# logger.info('Updating data')

# ------------------------------------------------------
# DEFAULT VARIABLES
# ------------------------------------------------------
CURPTH = var.MAIN_ROOT['main']
MESSAGE = var.MAIN_MESSAGE
TABID = var.MAIN_TABID
URL = var.MAIN_URL
NAMES = var.MAIN_NAMES
MAINID = var.MAIN_ID
PACKAGE = var.MAIN_PACKPAGE
TITLE = var.MAIN_ID['LogIn']
USERNAME = var.USERNAME

# UI variables preset for layout customizing
# Dimension
W = 350
H = 150
AVATAR_SIZE = 100
ICON_SIZE = 30
BUFFER = 3

# Margin
M1 = [0,5,5,5,5]

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
pthInfo = PACKAGE['appData']

infoData = NAMES['info']

filePath = os.path.join(pthInfo, infoData)

info = func.dataHandle(filePath, 'r')

# with open(os.path.join(pthInfo, infoData), 'r') as f:
#     info = json.load(f)

# Get app path
logger.info('Loading information...')
APPINFO = info['pipeline']
logger.info('Loading pipeline manager UI')

userDataPth = os.path.join(os.getenv('PROGRAMDATA'), 'Pipeline Tool/scrInfo/user.info')

userData = func.dataHandle(userDataPth, 'r')

# with open(userDataPth, 'r') as f:
#     userData = json.load(f)

prodInfoFolder = os.path.join(os.getenv('PROGRAMDATA'), 'Pipeline Tool/scrInfo/prodInfo')

prodContent = [f for f in os.listdir(prodInfoFolder) if f.endswith('.prod')]

prodLst = []

for f in prodContent:
    with open(os.path.join(prodInfoFolder, f), 'r') as f:
        info = json.load(f)
    prodLst.append(info['name'])

# ----------------------------------------------------------------------------------------------------------- #
"""                                       SUB CLASS: USER LOGIN UI                                          """
# ----------------------------------------------------------------------------------------------------------- #
class LoginUI(QDialog):

    appDataPth = os.path.join(os.getenv('PROGRAMDATA'), 'scrInfo/apps.pipeline')

    def __init__(self, parent=None):

        super(LoginUI, self).__init__()

        self.setWindowTitle(TITLE)
        self.setWindowIcon(QIcon(func.getIcon('Logo')))

        self.prevUserLogin = os.path.join(os.getenv('PROGRAMDATA'), 'Pipeline Tool/user.tempLog')

        if not os.path.exists(self.prevUserLogin):
            self.buildUI()
        else:
            with open(self.prevUserLogin, 'r') as f:
                prevUserData = json.load(f)

            userName = [f for f in prevUserData][0]

            if prevUserData[userName][6]==0:
                self.buildUI()
            else:
                self.autoLogin(userName)

        # self.setCentralWidget(self.mainFrame)

    def buildUI(self):

        x1 = X
        y1 = Y
        xh1 = XH
        xw1 = 2*XW

        x2 = x1
        y2 = xw1
        xh2 = xh1
        xw2 = GRID_TOTAL - xw1

        x3 = x1 + xh1
        y3 = y1
        xh3 = xh2
        xw3 = xw1

        x4 = x3
        y4 = xw3
        xh4 = xh3
        xw4 = GRID_TOTAL - xw3

        x5 = x3 + xh3
        y5 = y3
        xh5 = xh4
        xw5 = xw3

        x6 = x5
        y6 = xw5
        xh6 = xh5
        xw6 = XW

        x7 = x6
        y7 = xw5 + xw6
        xh7 = xh6
        xw7 = (GRID_TOTAL - (xw5 + xw6))/2

        x8 = x7
        y8 = y7 + xw7
        xh8 = xh7
        xw8 = xw7

        pos1 = [0, x1, y1, xh1, xw1]
        pos2 = [0, x2, y2, xh2, xw2]
        pos3 = [0, x3, y3, xh3, xw3]
        pos4 = [0, x4, y4, xh4, xw4]
        pos5 = [0, x5, y5, xh5, xw5]
        pos6 = [0, x6, y6, xh6, xw6]
        pos7 = [0, x7, y7, xh7, xw7]
        pos8 = [0, x8, y8, xh8, xw8]

        self.mainFrame = QGroupBox(self)
        self.mainFrame.setTitle('User Account')
        self.mainFrame.setFixedSize(W,H)

        hbox = QHBoxLayout()

        self.layout = QGridLayout()
        self.layout.setContentsMargins(M1[1],M1[2],M1[3],M1[4])

        loginText = QLabel('User Name: ')
        self.layout.addWidget(loginText, pos1[1], pos1[2], pos1[3], pos1[4])

        self.userName = QLineEdit()
        self.layout.addWidget(self.userName, pos2[1], pos2[2], pos2[3], pos2[4])

        passText = QLabel('Password: ')
        self.layout.addWidget(passText, pos3[1], pos3[2], pos3[3], pos3[4])

        self.passWord = QLineEdit()
        self.passWord.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.passWord, pos4[1],pos4[2],pos4[3],pos4[4])

        rememberCheck = QLabel('Remember Me')
        self.layout.addWidget(rememberCheck, pos5[1],pos5[2],pos5[3],pos5[4])

        self.rememberCheckBox = QCheckBox()
        self.layout.addWidget(self.rememberCheckBox, pos6[1],pos6[2],pos6[3],pos6[4])

        self.loginBtn = QPushButton('Login')
        self.loginBtn.clicked.connect(self.checkLogin)
        self.layout.addWidget(self.loginBtn, pos7[1],pos7[2],pos7[3],pos7[4])

        self.cancelBtn = QPushButton('Cancel')
        self.cancelBtn.clicked.connect(self.cancelLogin)
        self.layout.addWidget(self.cancelBtn, pos8[1],pos8[2],pos8[3],pos8[4])

        hbox.addLayout(self.layout)
        self.mainFrame.setLayout(hbox)

    def cancelLogin(self):
        sys.exit(LoginUI.exec_())

    def autoLogin(self, userName, *args):
        QMessageBox.information(self, 'Auto Login', "Welcome back %s\n"
                                "Now it's the time to make amazing thing to the world !!!" % userName)

    def checkLogin(self, *args):
        user_name = str(self.userName.text())
        pass_word = str(func.encoding(self.passWord.text()))

        if user_name == "":
            QMessageBox.information(self, 'Login Failed', 'Username can not be blank')
        elif userData[user_name] != None and pass_word == userData[user_name][1]:
            QMessageBox.information(self, 'Login Successful', "Welcome %s\n "
                                    "Now it's the time to make amazing thing to the world !!!" % user_name)
            self.close()
            func.saveCurrentUserLogin(user_name, self.rememberCheckBox.checkState())
        else:
            QMessageBox.information(self, 'Login Failed', 'Username or Password is incorrected')

# ----------------------------------------------------------------------------------------------------------- #
"""                                       SUB CLASS: TAB LAYOUT                                             """
# ----------------------------------------------------------------------------------------------------------- #
class TabWidget( QWidget ):

    def __init__(self, parent, package=PACKAGE, tabid=TABID):
        
        super( TabWidget, self ).__init__( parent )

        with open(os.path.join(os.getenv('PROGRAMDATA'), 'Pipeline Tool/user.tempLog'), 'r') as f:
            self.curUserData = json.load(f)

        self.curUser = [f for f in self.curUserData][0]

        self.buildUI(package, tabid)

    def buildUI(self, package, tabid):

        self.layout = QVBoxLayout(self)
        # Create Tabs
        self.tabs = QTabWidget()
        # self.tabs.setDocumentMode(True)
        # self.tabs.setTabPosition(QTabWidget.West)
        self.tab1 = QGroupBox(self)
        self.tab2 = QGroupBox(self)
        self.tab3 = QGroupBox(self)
        # self.tabs.resize(package['geo'][1], package['geo'][2])
        # Add Tabs
        self.tabs.addTab(self.tab1, tabid[1])
        self.tabs.addTab(self.tab2, tabid[2])
        if self.curUserData[self.curUser][2]=='Admin':
            self.tabs.addTab(self.tab3, tabid[3])
        else:
            pass
        # Create Tab 1 layout
        self.tab1Layout()
        # Create Tab 2 layout
        self.tab2Layout()
        # Create Tab 3 layout
        self.tab3Layout()
        # Add Tab to Widget
        self.layout.addWidget(self.tabs)
        # Set main layout
        self.setLayout(self.layout)

    def tab1Layout(self):

        alignL = __right__
        alignR = __left__

        x1 = X
        y1 = Y
        xh1 = 5*XH
        xw1 = 5*XW

        x2 = x1
        y2 = xw1
        xh2 = XH
        xw2 = XW

        x3 = x2
        y3 = xw1 + xw2
        xh3 = xh2
        xw3 = GRID_TOTAL - (xw1 + xw2)

        x4 = x2 + xh2
        y4 = y2
        xh4 = xh3
        xw4 = xw2

        x5 = x4
        y5 = y3
        xh5 = xh4
        xw5 = xw3

        x6 = x4 + xh4
        y6 = y4
        xh6 = xh5
        xw6 = xw4

        x7 = x6
        y7 = y5
        xh7 = xh6
        xw7 = xw5

        pos1 = [0, x1, y1, xh1, xw1]
        pos2 = [0, x2, y2, xh2, xw2]
        pos3 = [0, x3, y3, xh3, xw3]
        pos4 = [0, x4, y4, xh4, xw4]
        pos5 = [0, x5, y5, xh5, xw5]
        pos6 = [0, x6, y6, xh6, xw6]
        pos7 = [0, x7, y7, xh7, xw7]

        # Create Layout for Tab 1
        self.tab1.setTitle(self.curUser)
        # self.tab1.setFixedSize(W, H)

        hboxLayout = QHBoxLayout()

        self.tab1GridLayout = QGridLayout()

        userImg = QPixmap(func.avatar(self.curUser))
        userAvatar = QLabel()
        userAvatar.setPixmap(userImg)
        userAvatar.setScaledContents(True)
        userAvatar.setFixedSize(AVATAR_SIZE,AVATAR_SIZE)
        self.tab1GridLayout.addWidget(userAvatar, pos1[1],pos1[2],pos1[3],pos1[4])

        userNameLabel = QLabel('AKA: ')
        userNameLabel.setAlignment(alignL)
        self.tab1GridLayout.addWidget(userNameLabel, pos2[1],pos2[2],pos2[3],pos2[4])

        userNameArtist = QLabel(self.curUserData[self.curUser][4])
        userNameArtist.setAlignment(alignR)
        self.tab1GridLayout.addWidget(userNameArtist, pos3[1],pos3[2],pos3[3],pos3[4])

        titleLabel = QLabel('Group: ')
        titleLabel.setAlignment(alignL)
        self.tab1GridLayout.addWidget(titleLabel, pos4[1],pos4[2],pos4[3],pos4[4])

        classLabel = QLabel(self.curUserData[self.curUser][2])
        classLabel.setAlignment(alignR)
        self.tab1GridLayout.addWidget(classLabel, pos5[1],pos5[2],pos5[3],pos5[4])

        prodLabel = QLabel('Title: ')
        prodLabel.setAlignment(alignL)
        self.tab1GridLayout.addWidget(prodLabel, pos6[1],pos6[2],pos6[3],pos6[4])

        classGroup = QLabel(self.curUserData[self.curUser][5])
        self.tab1GridLayout.addWidget(classGroup, pos7[1],pos7[2],pos7[3],pos7[4])

        # self.tab1.layout.setMaximumSized(100,100)
        hboxLayout.addLayout(self.tab1GridLayout)

        self.tab1.setLayout(hboxLayout)

    def tab2Layout(self):
        # Create Layout for Tab 2
        self.tab2.setTitle('Extra Tool')
        # self.tab2.setFixedSize(W,H)

        hboxLayout = QHBoxLayout()

        self.tab2GridLayout = QGridLayout()

        # Content tab 2

        for key in APPINFO:
            # Illustrator
            if key == 'Illustrator CC':
                illusBtn = self.makeIconButton(key)
                self.tab2GridLayout.addWidget(illusBtn, 0,0,1,1)
            elif key == 'Illustrator CS6':
                illusBtn = self.makeIconButton(key)
                self.tab2GridLayout.addWidget(illusBtn,0,0,1,1)
            else:
                pass
            # InDesign
            if key == 'InDesign CC':
                indesignBtn = self.makeIconButton(key)
                self.tab2GridLayout.addWidget(indesignBtn, 0,1,1,1)
            elif key == 'InDesign CS6':
                indesignBtn = self.makeIconButton(key)
                self.tab2GridLayout.addWidget(indesignBtn, 0,1,1,1)
            else:
                pass
            # Mudbox
            if key == 'Mudbox 2017':
                mudboxBtn = self.makeIconButton(key)
                self.tab2GridLayout.addWidget(mudboxBtn, 0,2,1,1)
            if key == 'Mudbox 2016':
                mudboxBtn = self.makeIconButton(key)
                self.tab2GridLayout.addWidget(mudboxBtn, 0,2,1,1)
            else:
                pass
            #UV layout
            if key == 'UVLayout':
                uvLayoutBtn = self.makeIconButton(key)
                self.tab2GridLayout.addWidget(uvLayoutBtn, 0,3,1,1)

        dictBtn = QPushButton( 'English Dictionary' )
        dictBtn.clicked.connect(self.englishDict)
        self.tab2GridLayout.addWidget(dictBtn, 1,0,1,3)

        hboxLayout.addLayout(self.tab2GridLayout)

        self.tab2.setLayout(hboxLayout)

    def tab3Layout(self):
        # Create Layout for Tab 2
        # self.tab3.setTitle('Management Tool')
        # self.tab3.setFixedSize(W,H)

        hboxLayout = QHBoxLayout()

        self.tab3GridLayout = QGridLayout()

        # Content tab 3
        sqlPeopleBtn = QPushButton('Members')
        self.tab3GridLayout.addWidget(sqlPeopleBtn, 0,0,1,1)

        hboxLayout.addLayout(self.tab3GridLayout)

        self.tab3.setLayout(hboxLayout)

    def makeIconButton(self, name):

        icon = QIcon(APPINFO[name][1])
        iconBtn = QPushButton()
        iconBtn.setToolTip(APPINFO[name][0])
        iconBtn.setIcon(icon)
        iconBtn.setFixedSize(ICON_SIZE, ICON_SIZE)
        iconBtn.setIconSize(QSize(ICON_SIZE-BUFFER, ICON_SIZE-BUFFER))
        iconBtn.clicked.connect(partial(self.openApps, APPINFO[name][2]))
        return iconBtn

    def openApps(self, pth):
        subprocess.Popen(pth)

    def englishDict(self):
        from ui import englishDict
        reload(englishDict)
        engDict = englishDict.EnglishDict()
        engDict.exec_()

    def filterClassAllowance(self, func):
        if self.curUserData[self.curUser][1] == 'Admin':
            func()
        else:
            pass

# ----------------------------------------------------------------------------------------------------------- #
"""                                SUB CLASS: CUSTOM WINDOW POP UP LAYOUT                                   """
# ----------------------------------------------------------------------------------------------------------- #
class WindowDialog(QDialog):

    def __init__(self, id, message, icon):
        super(WindowDialog, self).__init__()

        self.setWindowTitle(id)

        self.setWindowIcon(QIcon(icon))

        self.buildUI(message)

    def buildUI(self, message):

        self.layout = QVBoxLayout()

        label = QLabel(message)
        self.layout.addWidget(label)

        btn = QPushButton('OK')
        btn.clicked.connect(self.close)
        btn.setMaximumWidth(100)
        self.layout.addWidget(btn)

        self.setLayout(self.layout)

# ----------------------------------------------------------------------------------------------------------- #
"""                          MAIN CLASS: DESKTOP UI APPLICATIONS: PIPELINE TOOL                             """
# ----------------------------------------------------------------------------------------------------------- #
class DesktopUI( QMainWindow ):

    def __init__(self, mainID, appInfo, package, message, names, url):

        super(DesktopUI, self).__init__()
        # Set window title
        self.setWindowTitle(mainID['Main'])
        # Set window icon
        self.setWindowIcon(QIcon(appInfo['Logo'][1]))
        # Build UI
        self.buildUI(appInfo, package, message, mainID, names, url)
        # User log in identification
        login = LoginUI()
        login.exec_()

        tempUser = os.path.join(os.getenv('PROGRAMDATA'), 'Pipeline Tool/user.tempLog')

        if not os.path.exists(tempUser):
            sys.exit()

        with open(tempUser, 'r') as f:
            self.curUserData = json.load(f)

        self.curUser = [f for f in self.curUserData][0]

        # Create Tabs
        self.tabWidget = TabWidget(self)
        # Put tabs to center of main UI
        self.setCentralWidget(self.tabWidget)
        # ShowUI
        func.proc('log in')

    def buildUI(self, appInfo, package, message, mainID, names, url):
        self.layout = self.setGeometry(package['geo'][1], package['geo'][2], package['geo'][3], package['geo'][4])

        # Status bar viewing message
        self.statusBar().showMessage(message['status'])

        #----------------------------------------------
        # Menu Tool Bar sections
        menubar = self.menuBar()

        # File menu
        fileMenu = menubar.addMenu('File')
        # Extract actions
        exitAction = self.fileMenuToolBar(appInfo, mainID, message, url)
        separator1 = self.createSeparatorAction(appInfo)
        # Put actions into file menu
        fileMenu.addAction(separator1)
        fileMenu.addAction(exitAction)

        # Tool Menu
        toolMenu = menubar.addMenu('Tool')

        # Help Menu
        helpMenu = menubar.addMenu('Help')
        # Extract actions
        aboutAction, creditAction, helpAction = self.helpMenuToolBar(appInfo, mainID, message, url)
        # Put actions into help menu
        helpMenu.addAction(aboutAction)
        helpMenu.addAction(creditAction)
        helpMenu.addAction(helpAction)

        #----------------------------------------------
        # Shelf toolbar sections
        # TD Tool Bar
        self.tdToolBar = self.toolBarTD(appInfo)
        # VFX Tool Bar
        self.compToolBar = self.toolBarComp(appInfo)
        # support ToolBar
        # self.supportApps = self.supApps( appInfo )

    def fileMenuToolBar(self, appInfo, mainid, message, url):
        # Exit action
        exitAction = QAction(QIcon(appInfo['Exit'][1]), appInfo['Exit'][0], self)
        exitAction.setStatusTip(appInfo['Exit'][0])
        exitAction.triggered.connect(qApp.quit)

        return exitAction

    def toolMenuToolBar(self, appInfo, mainid, message, url):
        pass

    def helpMenuToolBar(self, appInfo, mainid, message, url):
        # About action
        about = QAction(QIcon(appInfo['About'][1]), appInfo['About'][0], self)
        about.setStatusTip(appInfo['About'][0] )
        about.triggered.connect( partial( self.subWindow, mainid['About'], message['About'], appInfo['About'][1]))
        # Credit action
        credit = QAction(QIcon(appInfo['Credit'][1]), appInfo['Credit'][0], self)
        credit.setStatusTip(appInfo['Credit'][0])
        credit.triggered.connect( partial( self.subWindow, mainid['Credit'], message['Credit'], appInfo['Credit'][1]))
        # Help action
        helpAction = QAction( QIcon(appInfo['Help'][1]), appInfo['Help'][0], self)
        helpAction.setStatusTip( (appInfo['Help'][0]) )
        helpAction.triggered.connect( partial( self.openURL, url[ 'Help' ] ) )
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
            toolBarTD.addAction( houdiniFX )
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

    def supApps(self, appInfo):
        # support apps tool bar
        supAppsToolBar = self.addToolBar('supApps')
        # Illustrator CC
        if 'Illustrator CC' in appInfo:
            illusCC = self.createAction(appInfo, 'Illustrator CC')
            supAppsToolBar.addAction(illusCC)
        # Illustrator CS6
        elif 'Illustrator CS6' in appInfo:
            illusCS6 = self.createAction(appInfo, 'Illustrator CS6')
            supAppsToolBar.addAction(illusCS6)
        else:
            pass
        # Headus UV Layout Pro
        if 'UVLayout' in appInfo:
            uvlayout = self.createAction(appInfo, 'UVLayout')
            supAppsToolBar.addAction(uvlayout)
        else:
            pass

        return supAppsToolBar

    def filterClassAllowance(self, func):
        if self.curUserData[self.curUser][1]=='Admin':
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

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure?", QMessageBox.Yes|QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def initialize(mainID=MAINID, appInfo=APPINFO, package=PACKAGE, message=MESSAGE, names=NAMES, url=URL):

    app = QApplication(sys.argv)
    window = DesktopUI(MAINID, APPINFO, PACKAGE, MESSAGE, NAMES, URL)
    # window.setFixedWidth(W)
    window.show()
    sys.exit(app.exec_())

if __name__=='__main__':
    initialize()

# ----------------------------------------------------------------------------------------------------------- #
"""                                                END OF CODE                                              """
# ----------------------------------------------------------------------------------------------------------- #