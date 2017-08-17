"""
Script Name: desktopUI.py
Author: Do Trinh/Jimmy - 3D artist, leader DAMG team.

Description:
    This script is main file to store everything for the pipeline app

Reference:
        Managing shortcuts - winshell 0.6.4a documentation. (n.d.). Retrieved from:
        http://winshell.readthedocs.io/en/lartest/cookbook/shortcuts.html

        GitHub - mottosso/Qt.py: Minimal Python 2 & 3 shim around all Qt bindings - PySide,
        PySide2, PyQt4 and PyQt5. (n.d.). Retrieved from https://github.com/mottosso/Qt.py

for any question or feedback, feel free to email me: dot@damgteam.com or damgteam@gmail.com
"""
# -------------------------------------------------------------------------------------------------------------
# IMPORT PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
import os, sys, subprocess, json, webbrowser, logging
from functools import partial
from tk import getData, proc
from tk import defaultVariable as var

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

# ------------------------------------------------------
# GET INFO DATA BEFORE START
# Update local pc info
def updateInfo():
    getData.initialize()

updateInfo()
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

# Get icon path
pthInfo = PACKAGE['appData']

infoData = NAMES['info']
with open(os.path.join(pthInfo, infoData), 'r') as f:
    info = json.load(f)

# Get app path
logger.info('Loading information...')
APPINFO = info['pipeline']
logger.info('Loading pipeline manager UI')

userDataPth = os.path.join(os.getenv(NAMES['key']), os.path.join('scrInfo', 'user.info'))
with open(userDataPth, 'r') as f:
    userData = json.load(f)

prodInfoFolder = os.path.join(os.getenv(NAMES['key']), os.path.join(NAMES['appdata'][1], 'prodInfo'))

prodContent = [f for f in os.listdir(prodInfoFolder) if f.endswith('.prod')]

prodLst = []

for f in prodContent:
    with open(os.path.join(prodInfoFolder, f), 'r') as f:
        info = json.load(f)
    prodLst.append(info['name'])

# -------------------------------------------------------------------------------------------------------------
# IMPORT PTQT5 ELEMENT TO MAKE UI
# -------------------------------------------------------------------------------------------------------------
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def getIcon(name):
    iconName = name + '.icon.png'
    rootPth = os.getcwd().split('ui')[0]
    iconPth = os.path.join(os.path.join(rootPth, 'icons'), iconName)
    return iconPth

def avatar(userName):
    img = userName + '.avatar.jpg'
    imgPth = os.path.join(os.getcwd(), 'imgs')
    avatarPth = os.path.join(imgPth, img)
    return avatarPth

def getCurrentUserLogin(userName):
    curUser = {}
    curUser[userName] = userData[userName]
    currentUserLoginPth = os.path.join(os.getenv('PIPELINE_TOOL'), 'user.tempLog')
    with open(currentUserLoginPth, 'w') as f:
        json.dump(curUser, f, indent=4)
# ----------------------------------------------------------------------------------------------------------- #
"""                                       SUB CLASS: USER LOGIN UI                                          """
# ----------------------------------------------------------------------------------------------------------- #
class LoginUI(QDialog):

    def __init__(self):

        super(LoginUI, self).__init__()

        self.setWindowTitle(TITLE)

        self.setWindowIcon(QIcon(getIcon('Logo')))

        self.buildUI()

        # self.setCentralWidget(self.mainFrame)

    def buildUI(self):

        self.mainFrame = QGroupBox(self)
        self.mainFrame.setTitle('User Account')
        self.mainFrame.setFixedSize(300,125)

        hbox = QHBoxLayout()

        self.layout = QGridLayout()
        self.layout.setContentsMargins(5,5,5,5)

        loginText = QLabel('User Name: ')
        self.layout.addWidget(loginText, 0,0,1,2)

        self.userName = QLineEdit()
        self.layout.addWidget(self.userName, 0,2,1,7)

        passText = QLabel('Password: ')
        self.layout.addWidget(passText, 1,0,1,2)

        self.passWord = QLineEdit()
        self.passWord.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.passWord, 1,2,1,7)

        rememberCheck = QLabel('Remember Me')
        self.layout.addWidget(rememberCheck, 2,0,1,2)

        self.rememberCheckBox = QCheckBox()
        self.layout.addWidget(self.rememberCheckBox, 2,2,1,1)

        self.loginBtn = QPushButton('Login')
        self.loginBtn.clicked.connect(self.checkLogin)
        self.layout.addWidget(self.loginBtn, 2,3,1,3)

        self.cancelBtn = QPushButton('Cancel')
        self.cancelBtn.clicked.connect(qApp.quit)
        self.layout.addWidget(self.cancelBtn, 2,6,1,3)

        hbox.addLayout(self.layout)
        self.mainFrame.setLayout(hbox)

    def checkLogin(self):
        user_name = str(self.userName.text())
        pass_word = str(proc.endconding(self.passWord.text()))

        if user_name == "":
            QMessageBox.information(self, 'Login Failed', 'Username can not be blank')
        elif userData[user_name] != None and pass_word == userData[user_name][0]:
            QMessageBox.information(self, 'Login Successful', 'Username and Password are corrected')
            self.close()
            getCurrentUserLogin(user_name)
        else:
            QMessageBox.information(self, 'Login Failed', 'Username or Password is incorrected')

# ----------------------------------------------------------------------------------------------------------- #
"""                                       SUB CLASS: TAB LAYOUT                                             """
# ----------------------------------------------------------------------------------------------------------- #
class TabWidget( QWidget ):

    def __init__(self, parent, package=PACKAGE, tabid=TABID):
        super( TabWidget, self ).__init__( parent )

        self.buildUI(package, tabid)

    def buildUI(self, package, tabid):

        self.layout = QVBoxLayout(self)
        # Create Tabs
        self.tabs = QTabWidget()
        # self.tabs.setDocumentMode(True)
        # self.tabs.setTabPosition(QTabWidget.West)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        # self.tabs.resize(package['geo'][1], package['geo'][2])
        # Add Tabs
        self.tabs.addTab(self.tab1, tabid[1])
        self.tabs.addTab(self.tab2, tabid[2])
        self.tabs.addTab(self.tab3, tabid[3])
        # Create Tab 1 layout
        self.tab1Layout()
        # Create Tab 2 layout
        self.tab2Layout()
        # Create Tab 3 layout
        self.tab3Layout()
        # Add Tab to Widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def tab1Layout(self):
        with open(os.path.join(os.getenv('PIPELINE_TOOL'), 'user.tempLog'), 'r') as f:
            curUserData = json.load(f)

        curUser = [f for f in curUserData][0]

        # Create Layout for Tab 1

        self.tab1.layout = QGridLayout(self)

        userImg = QPixmap(avatar(curUser))
        userImg.scaled(QSize(100,100))
        userAvatar = QLabel()
        userAvatar.setPixmap(userImg)
        userAvatar.setFixedSize(100,100)
        self.tab1.layout.addWidget(userAvatar)


        userNameLabel = QLabel(curUser)
        userNameLabel.setAlignment(Qt.AlignCenter)
        self.tab1.layout.addWidget(userNameLabel, 0,3,1,6)

        prodLabel = QLabel('Production: ')
        self.tab1.layout.addWidget(prodLabel, 1,3,1,2)

        self.productionList = QComboBox()
        for prod in prodLst:
            self.productionList.addItem(prod)
        self.tab1.layout.addWidget(self.productionList, 1,5,1,4)

        titleLabel = QLabel('Class: ')
        self.tab1.layout.addWidget(titleLabel, 2,3,1,3)

        classLabel = QLabel(curUserData[curUser][1])
        self.tab1.layout.addWidget(classLabel, 2,6,1,3)

        self.tab1.setLayout(self.tab1.layout)

    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        self.drawText(QPaintEvent, painter)
        painter.end()

    def tab2Layout(self):
        # Create Layout for Tab 2
        self.tab2.layout = QVBoxLayout( self )
        self.tab2.setLayout(self.tab2.layout)
        # Content tab 2
        tab2btn1 = QPushButton( 'Just For Test 2' )
        self.tab2.layout.addWidget( tab2btn1 )

    def tab3Layout(self):
        # Create Layout for Tab 2
        self.tab3.layout = QVBoxLayout(self)
        self.tab3.setLayout(self.tab3.layout)
        # Content tab 3
        tab3btn1 = QPushButton('Just For Test 3')
        self.tab3.layout.addWidget(tab3btn1)

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

        super( DesktopUI, self ).__init__()
        # Set window title
        self.setWindowTitle(mainID['Main'])
        # Set window icon
        self.setWindowIcon(QIcon(appInfo['Logo'][1]))
        # Build UI
        self.buildUI(appInfo, package, message, mainID, names, url)
        # User log in identification
        login = LoginUI()
        login.exec_()
        # Create Tabs
        self.tabWidget = TabWidget(self)
        # Put tabs to center of main UI
        self.setCentralWidget(self.tabWidget)
        # ShowUI
        proc.proc('log in')

    def buildUI(self, appInfo, package, message, mainID, names, url):
        self.layout = self.setGeometry(package['geo'][1], package['geo'][2], package['geo'][3], package['geo'][4])
        # Status bar viewing message
        self.statusBar().showMessage(message['status'])
        # Menu Tool Bar
        exitAction, aboutAction, creditAction, helpAction = self.addMenuToolBar(appInfo, mainID, message, url)
        # File menu
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        separator1 = self.createSeparatorAction(appInfo)
        fileMenu.addAction(separator1)
        fileMenu.addAction(exitAction)
        # Tool Menu
        toolMenu = menubar.addMenu('Tool')
        # Help Menu
        helpMenu = menubar.addMenu('Help')
        helpMenu.addAction(aboutAction)
        helpMenu.addAction(creditAction)
        helpMenu.addAction(helpAction)
        # TD Tool Bar
        self.tdToolBar = self.toolBarTD(appInfo)
        # VFX Tool Bar
        self.compToolBar = self.toolBarComp(appInfo)
        # support ToolBar
        # self.supportApps = self.supApps( appInfo )

    def addMenuToolBar(self, appInfo, mainid, message, url):
        # Exit action
        exitAction = QAction(QIcon(appInfo['Exit'][1]), appInfo['Exit'][0], self)
        exitAction.setStatusTip( appInfo['Exit'][0])
        exitAction.triggered.connect(qApp.quit)
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
        return exitAction, about, credit, helpAction

    def toolBarTD(self, appInfo):
        # TD Tool Bar
        toolBarTD = self.addToolBar('TD')
        # Maya 2017
        if 'Maya 2017' in appInfo:
            maya2017 = self.createAction(appInfo, 'Maya 2017')
            toolBarTD.addAction(maya2017)
            pass
        # Maya 2016
        elif 'Maya 2016' in appInfo:
            maya2016 = self.createAction(appInfo, 'Maya 2016')
            toolBarTD.addAction(maya2016)
        # ZBrush 4R8
        if 'ZBrush 4R8' in appInfo:
            zbrush4R8 = self.createAction(appInfo, 'ZBrush 4R8')
            toolBarTD.addAction(zbrush4R8)
            pass
        # ZBrush 4R7
        elif 'ZBrush 4R7' in appInfo:
            zbrush4R7 = self.createAction(appInfo, 'ZBrush 4R7')
            toolBarTD.addAction(zbrush4R7)
        # Houdini FX
        if 'Houdini FX' in appInfo:
            houdiniFX = self.createAction(appInfo, 'Houdini FX')
            toolBarTD.addAction( houdiniFX )
        # Mari
        if 'Mari' in appInfo:
            mari = self.createAction(appInfo, 'Mari')
            toolBarTD.addAction(mari)
        # Photoshop CS6
        if 'Photoshop CS6' in appInfo:
            ptsCS6 = self.createAction(appInfo, 'Photoshop CS6')
            toolBarTD.addAction(ptsCS6)
        # Photoshop CC
        if 'Photoshop CC' in appInfo:
            ptsCC = self.createAction(appInfo, 'Photoshop CC')
            toolBarTD.addAction(ptsCC)
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
            pass
        # Illustrator CS6
        elif 'Illustrator CS6' in appInfo:
            illusCS6 = self.createAction(appInfo, 'Illustrator CS6')
            supAppsToolBar.addAction(illusCS6)
        # Headus UV Layout Pro
        if 'UVLayout' in appInfo:
            uvlayout = self.createAction(appInfo, 'UVLayout')
            supAppsToolBar.addAction(uvlayout)


        return supAppsToolBar

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
    window.show()
    sys.exit(app.exec_())

if __name__=='__main__':
    initialize()

# ----------------------------------------------------------------------------------------------------------- #
"""                                                END OF CODE                                              """
# ----------------------------------------------------------------------------------------------------------- #