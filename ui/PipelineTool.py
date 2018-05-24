#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: PipelineTool.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

    This is main UI of PipelineTool.

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys, logging, webbrowser
import sqlite3 as lite
from functools import partial

# PyQt5
from PyQt5.QtCore import Qt, QSize, QSettings, pyqtSignal, QByteArray, QRectF
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

from ui import (SubMenuBar, ToolBar, QuickSetting, TopTabWidget, )
from ui import uirc as rc

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logPth = os.path.join(app.LOGPTH)
handler = logging.FileHandler(logPth)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------------------
""" Pipeline Tool main layout """

class PipelineTool(QMainWindow):

    showMainSig = pyqtSignal(bool)
    showLoginSig1 = pyqtSignal(bool)
    closeMessSig = pyqtSignal(bool)

    def __init__(self, parent=None):

        super(PipelineTool, self).__init__(parent)

        self.username, rememberLogin = usql.query_curUser()

        self.url = app.__homepage__

        self.setWindowTitle(app.__appname__)
        self.setWindowIcon(QIcon(func.get_icon('Logo')))
        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

        self.mainWidget = QWidget()
        self.layout = QGridLayout()
        self.mainWidget.setLayout(self.layout)

        self.buildUI()

        self.setCentralWidget(self.mainWidget)

        # Status bar viewing message
        self.statusBar().showMessage(app.__appname__ + " " + app.VERSION)

        usql.insert_timeLog('Log in')

    def buildUI(self):
        # Sub menu
        menuLayout = SubMenuBar.SubMenuBar()
        subMenuSec = rc.AutoSectionQMainGrp("Sub Menu", menuLayout)

        # Server Status
        serverStatSec = rc.AutoSectionLayoutGrp("Server Status", None)

        # Toolbar
        toolBar = ToolBar.ToolBar()
        toolBarSec = rc.AutoSectionQMainGrp("Tool Bar", toolBar)

        # Tab layout
        self.topTabUI = TopTabWidget.TopTabWidget(self.username)

        # Bot build 1
        quickSetting = QuickSetting.QuickSetting()
        quickSettingSec = rc.AutoSectionQGridGrp("Quick Setting", quickSetting)

        # Bot build 2
        notifiSec = rc.AutoSectionLayoutGrp("Notification", None)

        # Signal definition
        showTDSig = quickSetting.checkboxTDSig
        showTDSig.connect(toolBar.show_hide_TDtoolBar)

        showCompSig = quickSetting.checkboxCompSig
        showCompSig.connect(toolBar.show_hide_ComptoolBar)

        showArtSig = quickSetting.checkboxArtSig
        showArtSig.connect(toolBar.show_hide_ArttoolBar)

        showToolBarSig = quickSetting.checkboxMasterSig
        showToolBarSig.connect(self.show_hide_toolBar)

        showMenuBarSig = quickSetting.checkboxMenuBarSig
        showMenuBarSig.connect(self.show_hide_menuBar)

        showStatSig = quickSetting.showStatusSig
        showStatSig.connect(self.show_hide_statusBar)

        serverStatusSig = quickSetting.showServerStatusSig
        serverStatusSig.connect(self.show_hide_serverStatus)

        notificatuonSig = quickSetting.showNotificationSig
        notificatuonSig.connect(self.show_hide_notification)

        quickSettingSig = quickSetting.quickSettingSig
        quickSettingSig.connect(self.show_hide_quickSetting)

        showMainSig = self.topTabUI.showMainSig
        showMainSig.connect(self.show_hide_main)

        showLoginSig = self.topTabUI.showLoginSig
        showLoginSig.connect(self.show_hide_login)

        tabSizeSig = self.topTabUI.tabSizeSig
        tabSizeSig.connect(self.autoResize)

        # scene = QGraphicsScene()
        # scene.addPixmap(QPixmap(os.path.join(os.getenv(app.__envKey__), "imgs", "DAMGteam.icon.png")))
        # self.damgteam = QGraphicsView()
        # self.damgteam.setScene(scene)
        # self.damgteam.aspectRatioMode = Qt.KeepAspectRatio
        # self.damgteam.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.damgteam = rc.ImageUI(icon='DAMGteam', size=[20, 20])

        self.layout.addWidget(subMenuSec, 0, 0, 1, 6)
        self.layout.addWidget(serverStatSec, 0, 6, 1, 3)
        self.layout.addWidget(toolBarSec, 1, 0, 2, 9)

        self.layout.addWidget(self.topTabUI, 3, 0, 4, 9)
        self.layout.addWidget(quickSettingSec, 7, 0, 3, 6)
        self.layout.addWidget(notifiSec, 7, 6, 3, 3)

        self.layout.addWidget(self.damgteam, 10, 8, 2, 2)
        self.layout.addWidget(rc.Label(txt=app.COPYRIGHT, alg=app.center), 11, 0, 1, 8)

        self.applySetting()

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

    def show_hide_quickSetting(self, param):
        self.show_hide_statusBar(param)
        self.show_hide_toolBar(param)
        self.show_hide_menuBar(param)
        self.show_hide_serverStatus(param)
        self.show_hide_notification(param)
        self.settings.setValue("showMasterQuickSetting", param)
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

    def autoResize(self, param):
        print(param)

    def applySetting(self):
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.mainWidget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.layout.setSpacing(1)

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