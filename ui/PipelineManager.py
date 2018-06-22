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
import sys

# PyQt5
from PyQt5.QtCore import pyqtSignal, QByteArray
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, QDockWidget, )

# Plt
import appData as app
from appData import __homepage__, __appname__, dockB, SiPoMin, SiPoIgn
from utilities.utils import str2bool

from ui.uirc import AutoSectionLayoutGrp, AutoSectionQMainGrp,  AppIcon

from ui.SubMenuBar import SubMenuBar
from ui.ToolBar import ToolBar
from ui.TopTab import TopTab
from ui.BotTab import BotTab
from ui.ServerStatus import ServerStatus
from ui.Footer import Footer
from ui.StatusBar import StatusBar

logger = app.logger
# -------------------------------------------------------------------------------------------------------------
""" Pipeline Tool main layout """

class PipelineManager(QMainWindow):

    showPlt = pyqtSignal(bool)
    showLogin = pyqtSignal(bool)
    close_event = pyqtSignal(bool)
    timelogSig = pyqtSignal(str)
    updateAvatar = pyqtSignal(bool)
    execute = pyqtSignal(str)

    def __init__(self, parent=None):

        super(PipelineManager, self).__init__(parent)

        self.url = __homepage__
        self.setWindowTitle(__appname__)
        self.setWindowIcon(AppIcon("Logo"))

        # from core.Settings import Settings
        self.settings = app.appSetting

        self.mainWidget = QWidget()
        self.layout = QGridLayout()
        self.mainWidget.setLayout(self.layout)

        self.buildUI()
        self.setCentralWidget(self.mainWidget)

    def buildUI(self):

        subMenuBar = SubMenuBar()                                                           # Sub menu
        toolBar = ToolBar()                                                                 # Toolbar
        serverStatus = ServerStatus()                                                       # Server Status
        self.subMenuSec = AutoSectionQMainGrp("Sub Menu", subMenuBar)
        self.networkStatus = AutoSectionLayoutGrp("Server Status", serverStatus)
        self.toolBarSec = AutoSectionQMainGrp("Tool Bar", toolBar)

        self.topTabUI = TopTab()                                                            # Tab layout

        self.botTabUI = BotTab()                                                            # Bot build 1
        self.notifiSec = AutoSectionLayoutGrp("Notification", None)                         # Bot build 2

        self.footer = Footer()
        self.stBar = StatusBar()                                                            # Status bar viewing message

        self.setStatusBar(self.stBar)

        # Signal
        subMenuBar.subMenuSig.connect(self.execute.emit)

        self.botTabUI.tbTD.connect(toolBar.show_td)
        self.botTabUI.tbComp.connect(toolBar.show_comp)
        self.botTabUI.tbArt.connect(toolBar.show_art)
        self.botTabUI.tbMaster.connect(self.toolBarSec.setVisible)

        self.botTabUI.subMenu.connect(self.show_subMenu)
        # self.botTabUI.statusBar.connect(self.stBar.show_statusBar)
        self.botTabUI.serStatus.connect(self.show_serStatus)
        self.botTabUI.notifi.connect(self.show_notifi)

        self.topTabUI.showPlt.connect(self.showPlt.emit)
        self.topTabUI.execute.connect(self.execute.emit)
        self.topTabUI.showLogin.connect(self.showLogin.emit)

        self.stBar.statusBarSig.connect(self.execute.emit)

        self.updateAvatar.connect(self.topTabUI.updateAvatar)

        self.layout.addWidget(self.subMenuSec, 0, 0, 1, 6)
        self.layout.addWidget(self.networkStatus, 0, 6, 1, 3)
        self.layout.addWidget(self.toolBarSec, 1, 0, 2, 9)

        self.layout.addWidget(self.topTabUI, 3, 0, 4, 9)
        self.layout.addWidget(self.botTabUI, 7, 0, 3, 6)
        self.layout.addWidget(self.notifiSec, 7, 6, 3, 3)

        self.layout.addWidget(self.footer, 10, 0, 1, 9)

        self.applySetting()

    def show_tbMaster(self, param):
        self.settings.setValue("tbMaster", param)
        self.toolBarSec.setVisible(param)

    def show_serStatus(self, param):
        self.settings.setValue("serStatus", param)
        self.networkStatus.setVisible(param)

    def show_notifi(self, param):
        self.settings.setValue("notifi", param)
        self.notifiSec.setVisible(str2bool(param))

    def show_subMenu(self, param):
        self.settings.setValue("subMenu", param)
        self.subMenuSec.setVisible(str2bool(param))

    def show_statusBar(self, param):
        self.settings.setValue("statusBar", param)
        if str2bool(param):
            self.show()
        else:
            self.hide()

    def get_layout_dimention(self):
        sizeW = self.frameGeometry().width()
        sizeH = self.frameGeometry().height()
        return sizeW, sizeH

    def add_dockWidget(self, dock):
        self.dock = dock
        self.addDockWidget(dockB, self.dock)

    def resizeEvent(self, event):
        sizeW, sizeH = self.get_layout_dimention()
        self.settings.setValue("appW", sizeW)
        self.settings.setValue("appH", sizeH)

    def windowState(self):
        self.settings.setValue("layoutState", self.saveState().data())

    def closeEvent(self, event):
        self.settings.setValue("layoutState", QByteArray(self.saveState().data()).toBase64())
        self.close_event.emit(True)
        self.hide()
        event.ignore()

    def applySetting(self):
        self.networkStatus.setSizePolicy(SiPoMin, SiPoMin)
        self.toolBarSec.setSizePolicy(SiPoMin, SiPoMin)
        self.subMenuSec.setSizePolicy(SiPoMin, SiPoMin)
        self.mainWidget.setSizePolicy(SiPoMin, SiPoMin)
        self.notifiSec.setSizePolicy(SiPoMin, SiPoMin)
        self.setSizePolicy(SiPoIgn, SiPoIgn)

        self.networkStatus.setMaximumSize(150, 75)
        self.toolBarSec.setFixedHeight(75)
        self.subMenuSec.setFixedHeight(75)
        self.layout.setSpacing(1)

        keys = ["subMenu", "tbMaster", "statusBar", "serStatus", "notifi"]
        funcs = [self.show_subMenu, self.show_tbMaster, self.show_statusBar, self.show_serStatus, self.show_notifi]

        for key in keys:
            value = str2bool(self.settings.value(key, True))
            funcs[keys.index(key)](value)

    def exit_action_trigger(self):
        self.timelogSig.emit("log out")
        QApplication.instance().quit()

# -------------------------------------------------------------------------------------------------------------
def main():
    app = QApplication(sys.argv)
    layout = PipelineManager()
    layout.show()
    app.exec_()

if __name__ == '__main__':
    main()