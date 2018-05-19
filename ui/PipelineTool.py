#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: {}.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys, logging, webbrowser
import sqlite3 as lite
from functools import partial

# PyQt5
from PyQt5.QtCore import Qt, QSize, QSettings, pyqtSignal, QByteArray
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFrame, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QGridLayout, QLabel, QPushButton, QGroupBox, QTabWidget, QAction, QMenu,
                             QSizePolicy, QDockWidget, QGraphicsView, QGraphicsScene)

# -------------------------------------------------------------------------------------------------------------
""" Plt tools """
import appData as app
from ui import uirc as rc

from utilities import utils as func
from utilities import sql_local as usql
from utilities import variables as var

from ui import (UserSetting, Preferences, AboutPlt, Credit, QuickSetting)
from ui import uirc as rc

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logPth = os.path.join(app.LOGPTH, 'plt.log')
logger = logging.getLogger(__name__)
handler = logging.FileHandler(logPth)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

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
HFIX = 80
ICON_SIZE = 30
ICON_BUFFRATE = 10
ICON_BUFFREGION = -1
ICON_BUFF = ICON_BUFFREGION*(ICON_SIZE*ICON_BUFFRATE/100)
ICON_SET_SIZE = QSize(ICON_SIZE+ICON_BUFF, ICON_SIZE+ICON_BUFF)

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
PYUIINFO = func.preset_load_pyuiInfor()
ICONINFO = func.preset_load_iconInfo()

# -------------------------------------------------------------------------------------------------------------
""" ToolBar """

class ToolBarLayout(QMainWindow):

    def __init__(self, parent=None):

        super(ToolBarLayout, self).__init__(parent)

        self.appInfo = APPINFO
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

        self.tdToolBar = self.make_toolBar("TD", app.CONFIG_TDS)
        self.compToolBar = self.make_toolBar("VFX", app.CONFIG_VFX)
        self.artToolBar = self.make_toolBar("ART", app.CONFIG_ART)

        self.showTDToolBar = func.str2bool(self.settings.value("showTDToolbar", True))
        self.showCompToolBar = func.str2bool(self.settings.value("showCompToolbar", True))
        self.showArtToolBar = func.str2bool(self.settings.value("showArtToolbar", True))

        self.tdToolBar.setVisible(self.showTDToolBar)
        self.compToolBar.setVisible(self.showCompToolBar)
        self.artToolBar.setVisible(self.showArtToolBar)

    def make_toolBar(self, name="", apps=[]):
        toolBar = self.addToolBar(name)
        for key in apps:
            if key in self.appInfo:
                toolBar.addAction(rc.action(key, self))
        return toolBar

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

# -------------------------------------------------------------------------------------------------------------
""" Menu bar Layout """

class MenuBarLayout(QMainWindow):

    def __init__(self, parent=None):

        super(MenuBarLayout, self).__init__(parent)

        self.appInfo = APPINFO
        self.url = app.__pltWiki__
        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.buildMenu()

    def buildMenu(self):

        prefAct = QAction(QIcon(func.get_icon('Preferences')), 'Preferences', self)
        prefAct.setStatusTip('Preferences')
        prefAct.triggered.connect(self.open_preferences_layout)

        aboutAct = QAction(QIcon(self.appInfo['About'][1]), self.appInfo['About'][0], self)
        aboutAct.setStatusTip(self.appInfo['About'][0])
        aboutAct.triggered.connect(self.open_about_layout)

        creditAct = QAction(QIcon(self.appInfo['Credit'][1]), self.appInfo['Credit'][0], self)
        creditAct.setStatusTip(self.appInfo['Credit'][0])
        creditAct.triggered.connect(self.open_credit_layout)

        helpAct = QAction(QIcon(self.appInfo['Help'][1]), self.appInfo['Help'][0], self)
        helpAct.setStatusTip((self.appInfo['Help'][0]))
        helpAct.triggered.connect(partial(webbrowser.open, self.url))

        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(prefAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(rc.action('Exit', self))

        self.editMenu = self.menuBar().addMenu("&Edit")

        self.viewMenu = self.menuBar().addMenu("&View")

        self.toolMenu = self.menuBar().addMenu("&Tools")
        self.toolMenu.addAction(rc.action("CleanPyc", self))
        self.toolMenu.addAction(rc.action("ReConfig", self))

        self.windowMenu = self.menuBar().addMenu("&Window")

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(helpAct)
        self.helpMenu.addAction(aboutAct)
        self.helpMenu.addAction(creditAct)

    def open_preferences_layout(self):
        pref = Preferences.Preferences()
        pref.show()
        pref.exec_()

    def open_about_layout(self):
        dlg = AboutPlt.AboutPlt()
        dlg.show()
        dlg.exec_()

    def open_credit_layout(self):
        dlg = Credit.Credit()
        dlg.show()
        dlg.exec_()

    def on_exit_action_triggered(self):
        usql.insert_timeLog("Log out")
        logger.debug("LOG OUT")
        QApplication.instance().quit()

    def toogleMenu(self, state):
        self.viewStatusSig.emit(state)
        self.settings.setValue("statusBar", state)

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
        self.iconInfo = ICONINFO
        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

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

        if userClass == "Administrator Privilege":
            self.tab5 = QGroupBox()
            self.tab5Layout()
            self.tabs.addTab(self.tab5, 'DB')

        self.layout.addWidget(self.tabs)

    def tab1Layout(self):

        self.tab1 = QWidget()
        tab1layout = QGridLayout()
        self.tab1.setLayout(tab1layout)

        tab1Sec1GrpBox = QGroupBox("Dev")
        tab1Sec1Grid = QGridLayout()
        tab1Sec1GrpBox.setLayout(tab1Sec1Grid)

        tab1Sec2GrpBox = QGroupBox("CMD")
        tab1Sec2Grid = QGridLayout()
        tab1Sec2GrpBox.setLayout(tab1Sec2Grid)

        tab1Sec3GrpBox = QGroupBox("Tools")
        tab1Sec3Grid = QGridLayout()
        tab1Sec3GrpBox.setLayout(tab1Sec3Grid)

        tab1Sec4GrpBox = QGroupBox("Office")
        tab1Sec4Grid = QGridLayout()
        tab1Sec4GrpBox.setLayout(tab1Sec4Grid)

        tab1Sec5GrpBox = QGroupBox("CGI")
        tab1Sec5Grid = QGridLayout()
        tab1Sec5GrpBox.setLayout(tab1Sec5Grid)

        devBtns = [rc.iconBtn(key) for key in app.CONFIG_DEV if key in self.appInfo] or []
        cmdBtns = [rc.iconBtn(key) for key in app.CONFIG_CMD if key in self.appInfo] or []
        pyBtns = [rc.iconBtn(key) for key in app.CONFIG_TAB1 if key in self.appInfo] or []

        self.cmdLineEdit = QLineEdit()
        cmdBtn = QPushButton("CMD")

        self.findPyEdit = QLineEdit()
        findPyBtn = QPushButton("Find")

        if not len(devBtns) == 0:
            for i in range(len(devBtns)):
                if i == 0:
                    tab1Sec1Grid.addWidget(devBtns[i], 0, 0, 1, 1)
                if i == 1:
                    tab1Sec1Grid.addWidget(devBtns[i], 0, 1, 1, 1)
                if i == 2:
                    tab1Sec1Grid.addWidget(devBtns[i], 0, 2, 1, 1)
                i += 1

        if not len(cmdBtns) == 0:
            for i in range(len(cmdBtns)):
                if i == 0:
                    tab1Sec1Grid.addWidget(cmdBtns[i], 1, 0, 1, 1)
                if i == 1:
                    tab1Sec1Grid.addWidget(cmdBtns[i], 1, 1, 1, 1)
                if i == 2:
                    tab1Sec1Grid.addWidget(cmdBtns[i], 1, 2, 1, 1)
                i += 1

        if not len(pyBtns) == 0:
            for i in range(len(pyBtns)):
                if i == 0:
                    tab1Sec3Grid.addWidget(pyBtns[i], 0, 0, 1, 1)
                elif i == 1:
                    tab1Sec3Grid.addWidget(pyBtns[i], 0, 1, 1, 1)
                elif i == 2:
                    tab1Sec3Grid.addWidget(pyBtns[i], 0, 2, 1, 1)
                elif i == 3:
                    tab1Sec3Grid.addWidget(pyBtns[i], 1, 0, 1, 1)
                elif i == 4:
                    tab1Sec3Grid.addWidget(pyBtns[i], 1, 1, 1, 1)
                elif i == 5:
                    tab1Sec3Grid.addWidget(pyBtns[i], 1, 2, 1, 1)
                elif i == 6:
                    tab1Sec3Grid.addWidget(pyBtns[i], 2, 0, 1, 1)
                elif i == 7:
                    tab1Sec3Grid.addWidget(pyBtns[i], 2, 1, 1, 1)
                elif i == 8:
                    tab1Sec3Grid.addWidget(pyBtns[i], 2, 2, 1, 1)
                i += 1

        tab1Sec2Grid.addWidget(self.cmdLineEdit, 0, 0, 1, 3)
        tab1Sec2Grid.addWidget(cmdBtn, 1, 0, 1, 3)

        tab1Sec3Grid.addWidget(self.findPyEdit, 3, 0, 1, 3)
        tab1Sec3Grid.addWidget(findPyBtn, 4, 0, 1, 3)

        tab1Sec4Grid.addWidget(rc.iconBtn("Wordpad"), 0, 0, 1, 1)

        for key in self.appInfo:
            if key == 'Mudbox 2018':
                mudbox18Btn = rc.iconBtn(key)
                tab1Sec4Grid.addWidget(mudbox18Btn, 2, 0, 1, 1)
            if key == 'Mudbox 2017':
                mudbox17Btn = rc.iconBtn(key)
                tab1Sec4Grid.addWidget(mudbox17Btn, 2, 1, 1, 1)
            if key == '3ds Max 2018':
                max18Btn = rc.iconBtn(key)
                tab1Sec4Grid.addWidget(max18Btn, 2, 2, 1, 1)
            if key == '3ds Max 2017':
                max17Btn = rc.iconBtn(key)
                tab1Sec4Grid.addWidget(max17Btn, 3, 0, 1, 1)

        tab1layout.addWidget(tab1Sec1GrpBox, 0, 0, 2, 3)
        tab1layout.addWidget(tab1Sec2GrpBox, 2, 0, 2, 3)

        tab1layout.addWidget(tab1Sec3GrpBox, 0, 3, 4, 3)

        tab1layout.addWidget(tab1Sec4GrpBox, 0, 6, 2, 2)
        tab1layout.addWidget(tab1Sec5GrpBox, 2, 6, 2, 2)

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

        tab3Sec2GrpBox = QGroupBox("Account Setting")
        tab3Sec2Grid = QGridLayout()
        tab3Sec2GrpBox.setLayout(tab3Sec2Grid)

        tab3Sec3GrpBox = QGroupBox("Messenger")
        tab3Sec3Grid = QGridLayout()
        tab3Sec3GrpBox.setLayout(tab3Sec3Grid)

        self.userAvatar = QLabel()
        self.userAvatar.setPixmap(QPixmap.fromImage(QImage(func.get_avatar(self.username))))
        self.userAvatar.setScaledContents(True)
        self.userAvatar.setFixedSize(100, 100)

        userSettingBtn = QPushButton('Account Setting')
        userSettingBtn.clicked.connect(self.on_userSettingBtn_clicked)

        signOutBtn = QPushButton('Log Out')
        signOutBtn.clicked.connect(self.on_signOutBtn_clicked)

        tab3Sec1Grid.addWidget(self.userAvatar, 0, 0, 1, 1)
        tab3Sec2Grid.addWidget(userSettingBtn, 0, 0, 1, 1)
        tab3Sec2Grid.addWidget(signOutBtn, 1, 0, 1, 1)

        tab3layout.addWidget(tab3Sec1GrpBox, 0, 0, 2, 2)
        tab3layout.addWidget(tab3Sec2GrpBox, 2, 0, 2, 2)
        tab3layout.addWidget(tab3Sec3GrpBox, 0, 2, 5, 6)

    def tab4Layout(self):
        # Create Layout for Tab 4.
        self.tab4 = QWidget()
        tab4layout = QGridLayout()
        self.tab4.setLayout(tab4layout)

        tab4Section1GrpBox = QGroupBox('Library')
        tab4Section1Grid = QGridLayout()
        tab4Section1GrpBox.setLayout(tab4Section1Grid)

        tab4Section1Grid.addWidget(rc.Clabel("Update later"), 0, 0, 1, 8)

        tab4layout.addWidget(tab4Section1GrpBox, 0, 0, 1, 8)

    def tab5Layout(self):
        # Create Layout for Tab 4
        tab5Widget = QWidget()
        tab5layout = QHBoxLayout()
        tab5Widget.setLayout(tab5layout)

        tab5Section1GrpBox = QGroupBox('Library')
        tab5Section1Grid = QGridLayout()
        tab5Section1GrpBox.setLayout(tab5Section1Grid)

        dataBrowserIconBtn = rc.iconBtn1('Database Browser')
        tab5Section1Grid.addWidget(dataBrowserIconBtn, 0, 0, 1, 1)

        tab5layout.addWidget(tab5Section1GrpBox)
        return tab5Widget

    def update_avatar(self, param):
        self.userAvatar.setPixmap(QPixmap.fromImage(QImage(param)))
        self.userAvatar.update()

    def english_dictionary(self):
        from ui import EnglishDictionary
        EngDict = EnglishDictionary.EnglishDictionary()
        EngDict.exec_()

    def make_screen_shot(self):
        from ui import Screenshot
        dlg = Screenshot.Screenshot()
        dlg.exec_()

    def calendar(self):
        from ui import Calendar
        dlg = Calendar.Calendar()
        dlg.exec_()

    def calculator(self):
        from ui import Calculator
        dlg = Calculator.Calculator()
        dlg.exec_()

    def findFiles(self):
        from ui import FindFiles
        dlg = FindFiles.FindFiles()
        dlg.exec_()

    def note_reminder(self):
        from ui import NoteReminder
        window = NoteReminder.NoteReminder()
        window.exec_()

    def text_editor(self):
        from ui import TextEditor
        window = TextEditor.WindowDialog()
        window.exec_()

    def on_newProjBtbn_clicked(self):
        from ui import NewProject
        window = NewProject.NewProject()
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
        user_setting_layout = UserSetting.Account_setting()
        user_setting_layout.show()
        sig = user_setting_layout.changeAvatarSignal
        sig.connect(self.update_avatar)
        user_setting_layout.exec_()

    def on_signOutBtn_clicked(self):
        self.settings.setValue("showMain", False)
        self.settings.setValue("showLogin", True)
        self.showMainSig.emit(False)
        self.showLoginSig.emit(True)

# -------------------------------------------------------------------------------------------------------------
""" Pipeline Tool main layout """

class PipelineTool(QMainWindow):

    showMainSig = pyqtSignal(bool)
    showLoginSig1 = pyqtSignal(bool)
    closeMessSig = pyqtSignal(bool)

    def __init__(self, parent=None):

        super(PipelineTool, self).__init__(parent)

        self.username, rememberLogin = usql.query_curUser()
        self.appInfo = APPINFO
        self.iconInfo = ICONINFO
        self.package = var.PLT_PKG
        self.url = app.__homepage__

        self.setWindowTitle(app.__appname__)
        self.setWindowIcon(QIcon(func.get_icon('Logo')))
        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.mainWidget = QWidget()
        self.buildUI()
        self.setCentralWidget(self.mainWidget)

        # Status bar viewing message
        self.statusBar().showMessage(app.__appname__ + " " + app.VERSION)

        usql.insert_timeLog('Log in')

    def buildUI(self):
        self.layout = QGridLayout()
        self.layout.setSpacing(1)
        self.mainWidget.setLayout(self.layout)

        # Menubar build
        self.subMenuGrpBox = QGroupBox("Menu")
        menuLayout = QHBoxLayout()
        self.subMenuGrpBox.setLayout(menuLayout)

        self.serverStatusGrpBox = QGroupBox("Server Status")
        infoLayout = QGridLayout()
        self.serverStatusGrpBox.setLayout(infoLayout)

        # Toolbar build
        self.toolBarGrpBox = QGroupBox("ToolBar")
        topLayout = QHBoxLayout()
        self.toolBarGrpBox.setLayout(topLayout)

        # Tab layout build
        self.tabLayoutGrpBox = QGroupBox("Plt Tool Box")
        midLayout = QHBoxLayout()
        self.tabLayoutGrpBox.setLayout(midLayout)

        # Bot build 1
        self.quickSettingGrpBox = QGroupBox("Quick Setting")
        quickSetting = QuickSetting.QuickSetting()
        self.quickSettingGrpBox.setLayout(quickSetting)

        # Bot build 2
        self.notificationGrpBox = QGroupBox("Notification")
        botGridLayout2 = QGridLayout()
        self.notificationGrpBox.setLayout(botGridLayout2)

        menuBar = MenuBarLayout()
        toolBar = ToolBarLayout()
        tabWidget = TabWidget(self.username, self.package)

        topLayout.addWidget(toolBar)
        menuLayout.addWidget(menuBar)
        midLayout.addWidget(tabWidget)

        showTDSig = quickSetting.checkboxTDSig
        showCompSig = quickSetting.checkboxCompSig
        showArtSig = quickSetting.checkboxArtSig
        showToolBarSig = quickSetting.checkboxMasterSig
        showMenuBarSig = quickSetting.checkboxMenuBarSig
        showStatSig = quickSetting.showStatusSig
        serverStatusSig = quickSetting.showServerStatusSig
        notificatuonSig = quickSetting.showNotificationSig
        masterSettingSig = quickSetting.showAllSettingSig
        showMainSig = tabWidget.showMainSig
        showLoginSig = tabWidget.showLoginSig
        tabSizeSig = tabWidget.tabSizeSig

        showTDSig.connect(toolBar.show_hide_TDtoolBar)
        showCompSig.connect(toolBar.show_hide_ComptoolBar)
        showArtSig.connect(toolBar.show_hide_ArttoolBar)
        showToolBarSig.connect(self.show_hide_toolBar)
        showMenuBarSig.connect(self.show_hide_menuBar)
        showStatSig.connect(self.show_hide_statusBar)
        serverStatusSig.connect(self.show_hide_serverStatus)
        notificatuonSig.connect(self.show_hide_notification)
        masterSettingSig.connect(self.show_hide_masterQuickSetting)
        showMainSig.connect(self.show_hide_main)
        showLoginSig.connect(self.show_hide_login)
        tabSizeSig.connect(self.autoResize)

        scene = QGraphicsScene()
        self.damgteamLogo = QGraphicsView()
        self.damgteamLogo.aspectRatioMode = Qt.KeepAspectRatio
        self.damgteamLogo.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        scene.addPixmap(QPixmap(os.path.join(os.getenv(app.__envKey__), "imgs", "DAMGteam.icon.png")))
        self.damgteamLogo.setScene(scene)

        self.layout.addWidget(self.subMenuGrpBox, 0, 0, 1, 6)
        self.layout.addWidget(self.serverStatusGrpBox, 0, 6, 1, 3)
        self.layout.addWidget(self.toolBarGrpBox, 1, 0, 2, 9)

        self.layout.addWidget(self.tabLayoutGrpBox, 3, 0, 4, 9)
        self.layout.addWidget(self.quickSettingGrpBox, 7, 0, 3, 6)
        self.layout.addWidget(self.notificationGrpBox, 7, 6, 3, 3)

        self.layout.addWidget(self.damgteamLogo, 10, 8, 2, 2)
        self.layout.addWidget(rc.Clabel(txt=app.COPYRIGHT, alg=Qt.AlignRight), 11, 0, 1, 8)

    def show_hide_main(self, param):
        param = func.str2bool(param)
        self.showMainSig.emit(param)

    def show_hide_login(self, param):
        self.settings.setValue("showLogin", param)
        self.showLoginSig1.emit(param)

    def show_hide_statusBar(self, param):
        self.settings.setValue("showStatusBar", param)
        if param:
            self.statusBar().show()
        else:
            self.statusBar().hide()

    def show_hide_toolBar(self, param):
        self.settings.setValue("showToolBar", param)
        self.toolBarGrpBox.setVisible(param)

    def show_hide_menuBar(self, param):
        self.settings.setValue("showMenuBar", param)
        self.subMenuGrpBox.setVisible(param)

    def show_hide_serverStatus(self, param):
        self.settings.setValue("showServerStatus", param)
        self.serverStatusGrpBox.setVisible(param)

    def show_hide_notification(self, param):
        self.settings.setValue("showNotification", param)
        self.notificationGrpBox.setVisible(param)

    def show_hide_masterQuickSetting(self, param):
        self.settings.setValue("showMasterQuickSetting", param)
        self.subMenuGrpBox.setVisible(param)
        self.serverStatusGrpBox.setVisible(param)
        self.toolBarGrpBox.setVisible(param)
        self.notificationGrpBox.setVisible(param)
        self.quickSettingGrpBox.setVisible(param)

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
        self.subMenuGrpBox.setContentsMargins(margin, margin, margin, margin)
        self.toolBarGrpBox.setContentsMargins(margin, margin, margin, margin)
        self.tabLayoutGrpBox.setContentsMargins(margin, margin, margin, margin)
        self.botGrpBox.setContentsMargins(margin, margin, margin, margin)
        return True

    def layout_height_ratio(self, baseH = 60):
        self.subMenuGrpBox.setFixedHeight(baseH)
        self.toolBarGrpBox.setFixedHeight(baseH * 2)
        self.tabLayoutGrpBox.setFixedHeight(baseH * 4)
        self.botGrpBox.setFixedHeight(baseH * 2)
        return True

    def layout_width_ratio(self, baseW = 60):
        self.subMenuGrpBox.setFixedWidth(baseW)
        self.toolBarGrpBox.setFixedWidth(baseW)
        self.tabLayoutGrpBox.setFixedWidth(baseW)
        self.botGrpBox.setFixedWidth(baseW)
        return True

    def autoResize(self, param):
        print(param)

    def resizeEvent(self, event):
        sizeW, sizeH = self.get_layout_dimention()
        self.settings.setValue("appW", sizeW)
        self.settings.setValue("appH", sizeH)

    def windowState(self):
        self.settings.setValue("layoutState", self.saveState().data())

    def closeEvent(self, event):
        self.settings.setValue("layoutState", QByteArray(self.saveState().data()).toBase64())
        self.closeMessSig.emit(True)
        self.hide()
        event.ignore()

# -------------------------------------------------------------------------------------------------------------
def main():
    app = QApplication(sys.argv)
    layout = PipelineTool()
    layout.show()
    app.exec_()

if __name__ == '__main__':
    main()