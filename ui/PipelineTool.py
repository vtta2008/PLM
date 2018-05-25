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
import os, sys, logging

# PyQt5
from PyQt5.QtCore import QSettings, pyqtSignal, QByteArray
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, QSizePolicy, QDockWidget)

# -------------------------------------------------------------------------------------------------------------
""" Plt tools """
import appData as app

from utilities import utils as func
from utilities import sql_local as usql
from utilities import variables as var

from ui import (SubMenuBar, ToolBar, TopTab, BotTab, ServerStatus)
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

    quickSettingSig = pyqtSignal(bool)
    showMainSig = pyqtSignal(bool)
    showLoginSig = pyqtSignal(bool)
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
        subMenuBar = SubMenuBar.SubMenuBar()
        self.subMenuSec = rc.AutoSectionQMainGrp("Sub Menu", subMenuBar)

        # Server Status
        serverStatus = ServerStatus.ServerStatus()
        self.networkStatus = rc.AutoSectionLayoutGrp("Server Status", serverStatus)

        # Toolbar
        toolBar = ToolBar.ToolBar()
        self.toolBarSec = rc.AutoSectionQMainGrp("Tool Bar", toolBar)

        # Tab layout
        self.topTabUI = TopTab.TopTab(self.username)

        # Bot build 1
        self.botTabUI = BotTab.BotTab()

        # Bot build 2
        self.notifiSec = rc.AutoSectionLayoutGrp("Notification", None)

        # Signal definition

        self.botTabUI.tdToolBarSig.connect(toolBar.show_hide_TDtoolBar)
        self.botTabUI.compToolBarSig.connect(toolBar.show_hide_ComptoolBar)
        self.botTabUI.artToolBarSig.connect(toolBar.show_hide_ArttoolBar)
        self.botTabUI.toolBarSig.connect(toolBar.show_hide_AlltoolBar)
        self.botTabUI.subMenuSig.connect(subMenuBar.show_hide_subMenuBar)
        self.botTabUI.statusBarSig.connect(self.show_hide_statusBar)
        self.botTabUI.serverStatSig.connect(self.show_hide_serverStatus)
        self.botTabUI.notifiSig.connect(self.show_hide_notification)

        self.topTabUI.showMainSig.connect(self.showMainSig.emit)
        self.topTabUI.showLoginSig.connect(self.showLoginSig.emit)

        self.damgteam = rc.ImageUI('DAMG', [20, 20])

        self.layout.addWidget(self.subMenuSec, 0, 0, 1, 6)
        self.layout.addWidget(self.networkStatus, 0, 6, 1, 3)
        self.layout.addWidget(self.toolBarSec, 1, 0, 2, 9)

        self.layout.addWidget(self.topTabUI, 3, 0, 4, 9)
        self.layout.addWidget(self.botTabUI, 7, 0, 3, 6)
        self.layout.addWidget(self.notifiSec, 7, 6, 3, 3)

        self.layout.addWidget(rc.Label(txt=" "), 10, 0, 1, 9)
        self.layout.addWidget(rc.Label(txt=app.COPYRIGHT, alg=app.right), 11, 0, 1, 8)
        self.layout.addWidget(self.damgteam, 11, 8, 1, 1)

        self.applySetting()

    def show_hide_statusBar(self, param):
        self.settings.setValue("showStatusBar", param)
        if param:
            self.statusBar().show()
        else:
            self.statusBar().hide()

    def show_hide_serverStatus(self, param):
        self.settings.setValue("serverStatus", param)
        self.networkStatus.setVisible(param)

    def show_hide_notification(self, param):
        self.settings.setValue("notification", param)
        self.notifiSec.setVisible(param)

    def show_hide_quickSetting(self, param):
        self.show_hide_statusBar(param)
        self.show_hide_serverStatus(param)
        self.show_hide_notification(param)
        self.quickSettingSig.emit(param)

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

    def applySetting(self):
        self.setSizePolicy(app.SiPoMin, app.SiPoMin)

        self.networkStatus.setSizePolicy(app.SiPoMin, app.SiPoMin)

        self.networkStatus.setMaximumSize(150, 75)

        self.toolBarSec.setSizePolicy(app.SiPoMin, app.SiPoMin)
        self.toolBarSec.setFixedHeight(75)

        self.subMenuSec.setSizePolicy(app.SiPoMin, app.SiPoMin)
        self.subMenuSec.setFixedHeight(75)

        self.mainWidget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.notifiSec.setSizePolicy(app.SiPoMin, app.SiPoMin)

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