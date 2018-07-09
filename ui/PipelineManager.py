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
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, QDockWidget, )

# Plt
from appData import __homepage__, dockB, SiPoMin, SiPoIgn
from core.Loggers import SetLogger

from ui.uirc import AutoSectionLayoutGrp, AutoSectionQMainGrp,  AppIcon
from ui import SubMenuBar, ToolBar, TopTab, BotTab, ServerStatus, Footer, StatusBar
from core.Specs import Specs
from utilities.pUtils import get_layout_dimention

# -------------------------------------------------------------------------------------------------------------
""" Pipeline Tool main layout """

class PipelineManager(QMainWindow):

    key = 'mainUI'

    showLayout = pyqtSignal(str, str)
    executing = pyqtSignal(str)
    regLayout = pyqtSignal(str, object)
    openBrowser = pyqtSignal(str)
    setSetting = pyqtSignal(str, str, str)
    sysNotify = pyqtSignal(str, str, str, int)
    loadSetting = pyqtSignal(str, str)
    returnValue = pyqtSignal(str, str)

    def __init__(self, parent=None):

        super(PipelineManager, self).__init__(parent)
        self.specs = Specs(self.key, self)
        self.logger = SetLogger(self)
        self.url = __homepage__

        self.setWindowIcon(AppIcon("Logo"))

        self.mainWidget = QWidget()
        self.layout = QGridLayout()
        self.mainWidget.setLayout(self.layout)

        self.buildUI()
        self.setCentralWidget(self.mainWidget)

    def buildUI(self):

        self.subMenuBar = SubMenuBar.SubMenuBar()                                                        # Sub menu
        self.toolBar = ToolBar.ToolBar()                                                                 # Toolbar
        self.serverStatus = ServerStatus.ServerStatus()                                                  # Server Status
        self.subMenuSec = AutoSectionQMainGrp("Sub Menu", self.subMenuBar)
        self.networkStatus = AutoSectionLayoutGrp("Server Status", self.serverStatus)
        self.toolBarSec = AutoSectionQMainGrp("Tool Bar", self.toolBar)

        self.topTabUI = TopTab.TopTab()                                                            # Tab layout
        self.botTabUI = BotTab.BotTab()                                                            # Bot build 1
        self.notifiSec = AutoSectionLayoutGrp("Notification", None)                                # Bot build 2

        self.subMenuBar.showLayout.connect(self.showLayout)
        self.subMenuBar.executing.connect(self.executing)
        self.subMenuBar.regLayout.connect(self.regLayout)
        self.subMenuBar.openBrowser.connect(self.openBrowser)

        self.topTabUI.executing.connect(self.executing)
        self.topTabUI.showLayout.connect(self.showLayout)
        self.topTabUI.regLayout.connect(self.regLayout)

        self.toolBar.showLayout.connect(self.showLayout)
        self.toolBar.executing.connect(self.executing)
        self.toolBar.regLayout.connect(self.regLayout)
        self.toolBar.openBrowser.connect(self.openBrowser)
        self.toolBar.setSetting.connect(self.setSetting)

        self.footer = Footer.Footer()
        self.stBar = StatusBar.StatusBar()                                                         # Status bar viewing message
        self.setStatusBar(self.stBar)

        self.botTabUI.generalSetting.tbTDCB.stateChanged.connect(self.toolBar.tdToolBar.setVisible)
        self.botTabUI.generalSetting.tbCompCB.stateChanged.connect(self.toolBar.compToolBar.setVisible)
        self.botTabUI.generalSetting.tbArtCB.stateChanged.connect(self.toolBar.artToolBar.setVisible)
        self.botTabUI.generalSetting.tbMasterCB.stateChanged.connect(self.toolBarSec.setVisible)
        self.botTabUI.generalSetting.statusBarCB.stateChanged.connect(self.stBar.setVisible)
        self.botTabUI.generalSetting.subMenuCB.stateChanged.connect(self.subMenuSec.setVisible)
        self.botTabUI.generalSetting.serStatusCB.stateChanged.connect(self.networkStatus.setVisible)
        self.botTabUI.generalSetting.notifiCB.stateChanged.connect(self.notifiSec.setVisible)

        self.botTabUI.generalSetting.setSetting.connect(self.setSetting)
        self.returnValue.connect(self.botTabUI.returnValue)

        self.botTabUI.loadSetting.connect(self.loadSetting)
        self.footer.showLayout.connect(self.showLayout)

        # Signal

        self.layout.addWidget(self.subMenuSec, 0, 0, 1, 6)
        self.layout.addWidget(self.networkStatus, 0, 6, 1, 3)
        self.layout.addWidget(self.toolBarSec, 1, 0, 2, 9)

        self.layout.addWidget(self.topTabUI, 3, 0, 4, 9)
        self.layout.addWidget(self.botTabUI, 7, 0, 3, 6)
        self.layout.addWidget(self.notifiSec, 7, 6, 3, 3)

        self.layout.addWidget(self.footer, 10, 0, 1, 9)

    def add_dockWidget(self, dock):
        self.dock = dock
        self.addDockWidget(dockB, self.dock)

    def resizeEvent(self, event):
        sizeW, sizeH = get_layout_dimention(self)
        self.setSetting.emit('width', str(sizeW), self.objectName())
        self.setSetting.emit('height', str(sizeH), self.objectName())

    def showEvent(self, event):
        self.showLayout.emit('login', 'hide')
        self.showLayout.emit('sysTray', 'show')

    def closeEvent(self, event):
        self.sysNotify.emit('notice', "PLM hide in system tray", 'info', 500)
        self.hide()
        event.ignore()

# -------------------------------------------------------------------------------------------------------------
def main():
    app = QApplication(sys.argv)
    layout = PipelineManager()
    layout.show()
    app.exec_()

if __name__ == '__main__':
    main()