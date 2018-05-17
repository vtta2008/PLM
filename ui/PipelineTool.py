#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: {}.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Check data flowing """
print("Import from modules: {file}".format(file=__name__))
print("Directory: {path}".format(path=__file__.split(__name__)[0]))
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys, logging, subprocess, webbrowser, requests
import sqlite3 as lite
from functools import partial

# PyQt5
from PyQt5.QtCore import Qt, QSize, QCoreApplication, QSettings, pyqtSignal, QByteArray
from PyQt5.QtGui import QIcon, QPixmap, QImage, QIntValidator, QFont
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFrame, QDialog, QWidget, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QLineEdit, QLabel, QPushButton, QMessageBox, QGroupBox,
                             QCheckBox, QTabWidget, QSystemTrayIcon, QAction, QMenu, QFileDialog, QComboBox,
                             QDockWidget, QSlider, QSizePolicy, QStackedWidget, QStackedLayout)

# -------------------------------------------------------------------------------------------------------------
""" Plt tools """
import appData as app
from ui import uirc as rc

from utilities import utils as func
from utilities import sql_local as usql
from utilities import variables as var

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logPth = os.path.join(app.LOGPTH, 'plt.log')
logger = logging.getLogger(__name__)
handler = logging.FileHandler(logPth)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

from ui import (UserSetting, Preferences, SignIn)
from ui import uirc as rc

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
""" Menu bar Layout """

class MenuBarLayout(QMainWindow):

    showTDSig2 = pyqtSignal(bool)
    showCompSig2 = pyqtSignal(bool)
    showArtSig2 = pyqtSignal(bool)

    def __init__(self, parent=None):

        super(MenuBarLayout, self).__init__(parent)

        self.appInfo = APPINFO
        self.mainID = var.PLT_ID
        self.message = var.PLT_MESS
        self.url = var.PLT_URL

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

        self.layout = QGridLayout()
        self.buildUI()

        self.setLayout(self.layout)

    def buildUI(self):

        self.createAction()

        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.prefAct)
        self.fileMenu.addAction(self.separator1)
        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = self.menuBar().addMenu("&View")
        self.viewMenu.addAction(self.viewTDAct)
        self.viewMenu.addAction(self.viewCompAct)
        self.viewMenu.addAction(self.viewArtAct)
        self.viewMenu.addAction(self.viewAllAct)

        self.toolMenu = self.menuBar().addMenu("&Tools")
        self.toolMenu.addAction(self.cleanAct)
        self.toolMenu.addAction(self.reconfigAct)

        self.aboutMenu = self.menuBar().addMenu("&About")
        self.aboutMenu.addAction(self.aboutAct)

        self.creditMenu = self.menuBar().addMenu("&Credit")
        self.creditMenu.addAction(self.creditAct)

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.helpAct)

    def createAction(self):
        # Preferences
        self.prefAct = QAction(QIcon(func.get_icon('Preferences')), 'Preferences', self)
        self.prefAct.setStatusTip('Preferences')
        self.prefAct.triggered.connect(self.preferences_action_triggered)

        # Exit
        self.exitAct = QAction(QIcon(self.appInfo['Exit'][1]), self.appInfo['Exit'][0], self)
        self.exitAct.setStatusTip(self.appInfo['Exit'][0])
        self.exitAct.triggered.connect(self.exit_action_trigger)

        # View TD toolbar
        self.viewTDAct = QAction(QIcon(func.get_icon("")), "hide/view TD tool bar", self)
        viewTDToolBar = func.str2bool(self.settings.value("showTDToolbar", True))
        self.viewTDAct.setChecked(viewTDToolBar)
        self.viewTDAct.triggered.connect(self.show_hide_TDtoolBar)

        # View comp toolbar
        self.viewCompAct = QAction(QIcon(func.get_icon("")), "hide/view Comp tool bar", self)
        viewCompToolBar = func.str2bool(self.settings.value("showCompToolbar", True))

        # self.viewCompAct.setCheckable(True)
        self.viewCompAct.setChecked(viewCompToolBar)
        self.viewCompAct.triggered.connect(self.show_hide_ComptoolBar)

        # View art toolbar
        self.viewArtAct = QAction(QIcon(func.get_icon("")), "hide/view Art tool bar", self)
        viewArtToolBar = func.str2bool(self.settings.value("showArtToolbar", True))

        # self.viewArtAct.setCheckable(True)
        self.viewArtAct.setChecked(viewArtToolBar)
        self.viewArtAct.triggered.connect(self.show_hide_ArttoolBar)

        # View all toolbar
        self.viewAllAct = QAction(QIcon(func.get_icon("Alltoolbar")), "hide/view All tool bar", self)
        viewAllToolbar = func.str2bool(self.settings.value("showAllToolbar", True))

        # self.viewAllAct.setCheckable(True)
        self.viewAllAct.setChecked(viewAllToolbar)
        self.viewAllAct.triggered.connect(self.show_hide_AlltoolBar)

        # Clean trash file
        self.cleanAct = QAction(QIcon(self.appInfo['CleanPyc'][1]), self.appInfo['CleanPyc'][0], self)
        self.cleanAct.setStatusTip(self.appInfo['CleanPyc'][0])
        self.cleanAct.triggered.connect(partial(func.clean_unnecessary_file, '.pyc'))

        # Re-configuration
        self.reconfigAct = QAction(QIcon(self.appInfo['ReConfig'][1]), self.appInfo['ReConfig'][0], self)
        self.reconfigAct.setStatusTip(self.appInfo['ReConfig'][0])
        self.reconfigAct.triggered.connect(func.Collect_info)

        # About action
        with open(os.path.join(os.getenv(app.__envKey__), 'README.rst'), 'r') as f:
            readme = f.read()
        self.aboutAct = QAction(QIcon(self.appInfo['About'][1]), self.appInfo['About'][0], self)
        self.aboutAct.setStatusTip(self.appInfo['About'][0])
        self.aboutAct.triggered.connect(partial(self.info_layout, self.mainID['About'], readme, self.appInfo['About'][1]))

        # Credit action
        self.creditAct = QAction(QIcon(self.appInfo['Credit'][1]), self.appInfo['Credit'][0], self)
        self.creditAct.setStatusTip(self.appInfo['Credit'][0])
        self.creditAct.triggered.connect(partial(self.info_layout, self.mainID['Credit'], self.message['Credit'], self.appInfo['Credit'][1]))

        # Help action
        self.helpAct = QAction(QIcon(self.appInfo['Help'][1]), self.appInfo['Help'][0], self)
        self.helpAct.setStatusTip((self.appInfo['Help'][0]))
        self.helpAct.triggered.connect(partial(webbrowser.open, self.url['Help']))

        # Seperator action
        self.separator1 = QAction(QIcon(self.appInfo['Sep'][0]), self.appInfo['Sep'][1], self)
        self.separator1.setSeparator(True)

    def preferences_action_triggered(self):
        dlg = Preferences.Preference()
        dlg.show()
        sigTD = dlg.checkboxTDSig
        sigComp = dlg.checkboxCompSig
        sigArt = dlg.checkboxArtSig
        sigTD.connect(self.show_hide_TDtoolBar)
        sigComp.connect(self.show_hide_ComptoolBar)
        sigArt.connect(self.show_hide_ArttoolBar)
        dlg.exec_()

    def exit_action_trigger(self):
        usql.insert_timeLog("Log out")
        logger.debug("LOG OUT")
        QApplication.instance().quit()

    def show_hide_TDtoolBar(self, param):
        self.showTDSig2.emit(param)

    def show_hide_ComptoolBar(self, param):
        self.showCompSig2.emit(param)

    def show_hide_ArttoolBar(self, param):
        self.showArtSig2.emit(param)

    def show_hide_AlltoolBar(self, param):
        self.show_hide_TDtoolBar(param)
        self.show_hide_ComptoolBar(param)
        self.show_hide_ArttoolBar(param)

    def info_layout(self, id='Note', message="", icon=func.get_icon('Logo')):
        from ui import AboutPlt
        dlg = AboutPlt.AboutPlt(id=id, message=message, icon=icon)
        dlg.exec_()

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

        if userClass == 'Administrator Privilege':
            self.tab5 = QGroupBox()
            self.tab5Layout()
            self.tabs.addTab(self.tab5, 'DB')

        self.layout.addWidget(self.tabs)

    def tab1Layout(self):

        self.tab1 = QWidget()
        tab1layout = QGridLayout()
        self.tab1.setLayout(tab1layout)

        tab1Sec1GrpBox = QGroupBox('Dev')
        tab1Sec1Grid = QGridLayout()
        tab1Sec1GrpBox.setLayout(tab1Sec1Grid)

        tab1Sec2GrpBox = QGroupBox('cmd')
        tab1Sec2Grid = QGridLayout()
        tab1Sec2GrpBox.setLayout(tab1Sec2Grid)

        tab1Sec3GrpBox = QGroupBox('Custom')
        tab1Sec3Grid = QGridLayout()
        tab1Sec3GrpBox.setLayout(tab1Sec3Grid)

        tab1Sec4GrpBox = QGroupBox('CGI')
        tab1Sec4Grid = QGridLayout()
        tab1Sec4GrpBox.setLayout(tab1Sec4Grid)

        devBtns = [rc.iconBtn(key) for key in app.CONFIG_DEV if key in self.appInfo] or []
        cmdBtns = [rc.iconBtn(key) for key in app.CONFIG_CMD if key in self.appInfo] or []
        pyBtns = [rc.iconBtn(key) for key in app.CONFIG_TAB1 if key in self.appInfo] or []

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
                    tab1Sec2Grid.addWidget(cmdBtns[i], 0, 0, 1, 1)
                if i == 1:
                    tab1Sec2Grid.addWidget(cmdBtns[i], 0, 1, 1, 1)
                if i == 2:
                    tab1Sec2Grid.addWidget(cmdBtns[i], 1, 0, 1, 1)
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

        tab1layout.addWidget(tab1Sec1GrpBox, 0,0,1,3)
        tab1layout.addWidget(tab1Sec2GrpBox, 1,0,2,3)
        tab1layout.addWidget(tab1Sec3GrpBox, 0,3,3,3)
        tab1layout.addWidget(tab1Sec4GrpBox, 0,6,3,2)

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

        self.userAvatar = QLabel()
        self.userAvatar.setPixmap(QPixmap.fromImage(QImage(func.get_avatar(self.username))))
        self.userAvatar.setScaledContents(True)
        self.userAvatar.setFixedSize(100, 100)

        tab3Sec2GrpBox = QGroupBox("Account Setting")
        tab3Sec2Grid = QGridLayout()
        tab3Sec2GrpBox.setLayout(tab3Sec2Grid)

        userSettingBtn = QPushButton('Account Setting')
        userSettingBtn.clicked.connect(self.on_userSettingBtn_clicked)

        signOutBtn = QPushButton('Log Out')
        signOutBtn.clicked.connect(self.on_signOutBtn_clicked)

        tab3Sec1Grid.addWidget(self.userAvatar, 0, 0, 2, 3)
        tab3Sec2Grid.addWidget(userSettingBtn, 0, 2, 1, 5)
        tab3Sec2Grid.addWidget(signOutBtn, 1, 2, 1, 5)

        tab3layout.addWidget(tab3Sec1GrpBox)
        tab3layout.addWidget(tab3Sec2GrpBox)

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
        self.showMainSig.emit(False)
        self.showLoginSig.emit(True)

# -------------------------------------------------------------------------------------------------------------
""" Pipeline Tool main layout """

class PipelineTool(QMainWindow):

    showLoginSig2 = pyqtSignal(bool)

    def __init__(self, parent=None):

        super(PipelineTool, self).__init__(parent)

        self.username, rememberLogin = usql.query_curUser()
        self.mainID = var.PLT_ID
        self.appInfo = APPINFO
        self.iconInfo = ICONINFO
        self.package = var.PLT_PKG
        self.message = var.PLT_MESS
        self.url = var.PLT_URL

        self.setWindowTitle(self.mainID['Main'])
        self.setWindowIcon(QIcon(func.get_icon('Logo')))
        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

        self.mainWidget = QWidget()
        self.buildUI()
        self.setCentralWidget(self.mainWidget)

        # self.showMainUI = func.str2bool(self.settings.value("showMain", True))
        # self.show_hide_main(self.showMainUI)

        # self.layout_magrin_ratio()
        # self.layout_height_ratio()
        # self.layout_width_ratio()

        # self.restoreState(self.settings.value("layoutState", QBitArray()))

        usql.insert_timeLog('Log in')

    def buildUI(self):

        sizeW, sizeH = self.get_layout_dimention()
        posX, posY, sizeW, sizeH = func.set_app_stick_to_bot_right(sizeW, sizeH)
        self.setGeometry(posX, posY, sizeW, sizeH)
        self.layout = QGridLayout()
        self.mainWidget.setLayout(self.layout)

        # Menubar build
        self.menuGrpBox = QGroupBox("Menu Layout")
        self.menuGrpBox.setFixedHeight(HFIX)
        menuLayout = QHBoxLayout()
        self.menuGrpBox.setLayout(menuLayout)

        menuBar = MenuBarLayout()
        menuLayout.addWidget(menuBar)

        # ----------------------------------------------
        self.tdToolBar = self.make_toolBar("TD", app.CONFIG_TDS)
        self.compToolBar = self.make_toolBar("VFX", app.CONFIG_VFX)
        self.artToolBar = self.make_toolBar("ART", app.CONFIG_ART)

        # Load Setting
        self.showTDToolBar = func.str2bool(self.settings.value("showTDToolbar", True))
        self.showCompToolBar = func.str2bool(self.settings.value("showCompToolbar", True))
        self.showArtToolBar = func.str2bool(self.settings.value("showArtToolbar", True))

        self.tdToolBar.setVisible(self.showTDToolBar)
        self.compToolBar.setVisible(self.showCompToolBar)
        self.artToolBar.setVisible(self.showArtToolBar)

        showTDSig = menuBar.showTDSig2
        showCompSig = menuBar.showCompSig2
        showArtSig = menuBar.showArtSig2
        showTDSig.connect(self.show_hide_TDtoolBar)
        showCompSig.connect(self.show_hide_ComptoolBar)
        showArtSig.connect(self.show_hide_ArttoolBar)

        # Status bar viewing message
        self.statusBar().showMessage(self.message['status'])

        # Top build
        self.topGrpBox = QGroupBox("Top Layout")
        topLayout = QHBoxLayout()

        self.topGrpBox.setLayout(topLayout)
        self.topGrpBox.setFixedHeight(HFIX)
        topLayout.addWidget(rc.Clabel("This Layout is for drag and drop"))

        # Mid build
        self.midGrpBox = QGroupBox("plt Tool Box")
        midLayout = QHBoxLayout()
        self.midGrpBox.setLayout(midLayout)

        self.tabWidget = TabWidget(self.username, self.package)

        showMainSig = self.tabWidget.showMainSig
        showLoginSig = self.tabWidget.showLoginSig
        tabSizeSig = self.tabWidget.tabSizeSig
        showMainSig.connect(self.show_hide_main)
        showLoginSig.connect(self.send_to_login)
        tabSizeSig.connect(self.autoResize)
        midLayout.addWidget(self.tabWidget)

        # Bot build
        self.sizeGrpBox = QGroupBox("Size Setting")
        sizeGridLayout = QGridLayout()
        self.sizeGrpBox.setLayout(sizeGridLayout)

        # unitSlider = SliderWidget("UNIT")
        # margSlider = SliderWidget("MARG")
        # buffSlider = SliderWidget("BUFF")
        # scalSlider =SliderWidget("SCAL")
        #
        # unitSig = unitSlider.valueChangeSig
        # margSig = margSlider.valueChangeSig
        # buffSig = buffSlider.valueChangeSig
        # scalSig = scalSlider.valueChangeSig
        #
        # sizeGridLayout.addWidget(unitSlider, 0, 0, 1, 5)
        # sizeGridLayout.addWidget(margSlider, 1, 0, 1, 5)
        # sizeGridLayout.addWidget(buffSlider, 2, 0, 1, 5)
        # sizeGridLayout.addWidget(scalSlider, 3, 0, 1, 5)

        # Bot build
        # self.unitGrpBox = QGroupBox("Unit Setting")
        # unitGridLayout = QGridLayout()
        # self.unitGrpBox.setLayout(unitGridLayout)
        #
        # unitSetting = UnitSetting()
        # unitGridLayout.addWidget(unitSetting)
        #
        # # Add layout to main

        self.layout.addWidget(self.menuGrpBox, 1, 0, 1, 6)
        self.layout.addWidget(self.topGrpBox, 2, 0, 2, 6)
        self.layout.addWidget(self.midGrpBox, 4, 0, 4, 6)
        # self.layout.addWidget(self.sizeGrpBox, 8, 0, 4, 3)
        # self.layout.addWidget(self.unitGrpBox, 8, 3, 4, 3)

        # Restore last setting layout from user
        # stateLayout = self.settings.value("layoutState", QByteArray().toBase64())
        # try:
        #     self.restoreState(QByteArray(stateLayout))
        # except IOError or TypeError:
        #     pass

    def make_toolBar(self, name="", apps=[]):
        toolBar = self.addToolBar(name)
        for key in apps:
            if key in self.appInfo.keys():
                toolBar.addAction(rc.action(key, self))
        return toolBar

    def createSeparatorAction(self):
        separator = QAction(QIcon(self.appInfo['Sep'][0]), self.appInfo['Sep'][1], self)
        separator.setSeparator(True)
        return separator

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

    def show_hide_main(self, param):
        param = func.str2bool(param)
        if not param:
            self.trayIcon.hide()
            self.close()
        else:
            self.trayIcon.show()
            self.show()

    def send_to_login(self, param):
        self.settings.setValue("showLogin", param)
        self.showLoginSig2.emit(param)

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
        self.menuGrpBox.setContentsMargins(margin, margin, margin, margin)
        self.topGrpBox.setContentsMargins(margin, margin, margin, margin)
        self.midGrpBox.setContentsMargins(margin, margin, margin, margin)
        self.sizeGrpBox.setContentsMargins(margin, margin, margin, margin)
        return True

    def layout_height_ratio(self, baseH = 60):
        self.menuGrpBox.setFixedHeight(baseH)
        self.topGrpBox.setFixedHeight(baseH*2)
        self.midGrpBox.setFixedHeight(baseH*4)
        self.sizeGrpBox.setFixedHeight(baseH * 2)
        return True

    def layout_width_ratio(self, baseW = 60):
        self.menuGrpBox.setFixedWidth(baseW)
        self.topGrpBox.setFixedWidth(baseW)
        self.midGrpBox.setFixedWidth(baseW)
        self.sizeGrpBox.setFixedWidth(baseW)
        return True

    def autoResize(self, param):
        # print(param)
        pass

    def resizeEvent(self, event):
        sizeW, sizeH = self.get_layout_dimention()
        self.settings.setValue("appW", sizeW)
        self.settings.setValue("appH", sizeH)

    def windowState(self):
        self.settings.setValue("layoutState", self.saveState().data())

    def closeEvent(self, event):
        self.settings.setValue("layoutState", QByteArray(self.saveState().data()).toBase64())
        # icon = QSystemTrayIcon.Information
        # self.trayIcon.showMessage('Notice', "Pipeline Tool will keep running in the system tray.", icon, 1000)
        self.hide()
        event.ignore()

    def showEvent(self, event):
        pass

# -------------------------------------------------------------------------------------------------------------

def main():
    app = QApplication(sys.argv)
    layout = PipelineTool()
    layout.show()
    app.exec_()

if __name__ == '__main__':
    main()