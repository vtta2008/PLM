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
from utilities import utils as func
from ui import (SubMenuBar, ToolBar, TopTab, BotTab, ServerStatus, StatusBar)
from ui import uirc as rc

# -------------------------------------------------------------------------------------------------------------
""" Pipeline Tool main layout """

class PipelineManager(QMainWindow):

    showPlt = pyqtSignal(bool)
    close_event = pyqtSignal(bool)
    timelogSig = pyqtSignal(str)
    updateAvatar = pyqtSignal(bool)
    loadLayout = pyqtSignal(str)
    execute = pyqtSignal(str)

    def __init__(self, parent=None):

        super(PipelineManager, self).__init__(parent)

        self.url = app.__homepage__
        self.setWindowTitle(app.__appname__)
        self.setWindowIcon(rc.AppIcon("Logo"))
        self.settings = app.appSetting

        self.mainWidget = QWidget()
        self.layout = QGridLayout()
        self.mainWidget.setLayout(self.layout)
        self.buildUI()
        self.setCentralWidget(self.mainWidget)

        dock1 = rc.DockWidget("Note 1")
        dock2 = rc.DockWidget("Note 2")
        self.addDockWidget(app.dockB, dock1)
        self.addDockWidget(app.dockB, dock2)

        # Status bar viewing message
        self.statusBar = StatusBar.StatusBar()
        self.setStatusBar(self.statusBar)

    def buildUI(self):

        subMenuBar = SubMenuBar.SubMenuBar()                                                # Sub menu
        toolBar = ToolBar.ToolBar()                                                         # Toolbar
        serverStatus = ServerStatus.ServerStatus()                                          # Server Status
        self.subMenuSec = rc.AutoSectionQMainGrp("Sub Menu", subMenuBar)
        self.networkStatus = rc.AutoSectionLayoutGrp("Server Status", serverStatus)
        self.toolBarSec = rc.AutoSectionQMainGrp("Tool Bar", toolBar)
        self.topTabUI = TopTab.TopTab()                                                     # Tab layout
        self.updateAvatar.connect(self.topTabUI.updateAvatar)
        self.botTabUI = BotTab.BotTab()                                                     # Bot build 1
        self.notifiSec = rc.AutoSectionLayoutGrp("Notification", None)                      # Bot build 2

        # Signal
        self.botTabUI.tbTD.connect(toolBar.show_td)
        self.botTabUI.tbComp.connect(toolBar.show_comp)
        self.botTabUI.tbArt.connect(toolBar.show_art)
        self.botTabUI.tbMaster.connect(self.toolBarSec.setVisible)

        self.botTabUI.subMenu.connect(self.show_subMenu)
        self.botTabUI.statusBar.connect(self.show_statusBar)
        self.botTabUI.serStatus.connect(self.show_serStatus)
        self.botTabUI.notifi.connect(self.show_notifi)

        self.topTabUI.showPlt.connect(self.showPlt.emit)
        self.topTabUI.loadLayout.connect(self.loadLayout.emit)
        self.topTabUI.execute.connect(self.execute.emit)

        self.layout.addWidget(self.subMenuSec, 0, 0, 1, 6)
        self.layout.addWidget(self.networkStatus, 0, 6, 1, 3)
        self.layout.addWidget(self.toolBarSec, 1, 0, 2, 9)

        self.layout.addWidget(self.topTabUI, 3, 0, 4, 9)
        self.layout.addWidget(self.botTabUI, 7, 0, 3, 6)
        self.layout.addWidget(self.notifiSec, 7, 6, 3, 3)

        self.applySetting()

    def show_tbMaster(self, param):
        self.settings.setValue("tbMaster", param)
        self.toolBarSec.setVisible(param)

    def show_statusBar(self, param):
        self.settings.setValue("statusBar", param)
        if param:
            self.statusBar().show()
        else:
            self.statusBar().hide()

    def show_serStatus(self, param):
        self.settings.setValue("serStatus", param)
        self.networkStatus.setVisible(param)

    def show_notifi(self, param):
        self.settings.setValue("notifi", param)
        self.notifiSec.setVisible(func.str2bool(param))

    def show_subMenu(self, param):
        self.settings.setValue("subMenu", param)
        self.subMenuSec.setVisible(func.str2bool(param))

    def get_layout_dimention(self):
        sizeW = self.frameGeometry().width()
        sizeH = self.frameGeometry().height()
        return sizeW, sizeH

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
        self.networkStatus.setSizePolicy(app.SiPoMin, app.SiPoMin)
        self.toolBarSec.setSizePolicy(app.SiPoMin, app.SiPoMin)
        self.subMenuSec.setSizePolicy(app.SiPoMin, app.SiPoMin)
        self.mainWidget.setSizePolicy(app.SiPoMin, app.SiPoMin)
        self.notifiSec.setSizePolicy(app.SiPoMin, app.SiPoMin)
        self.setSizePolicy(app.SiPoIgn, app.SiPoIgn)

        self.networkStatus.setMaximumSize(150, 75)
        self.toolBarSec.setFixedHeight(75)
        self.subMenuSec.setFixedHeight(75)
        self.layout.setSpacing(1)

        keys = ["subMenu", "tbMaster", "statusBar", "serStatus", "notifi"]
        funcs = [self.show_subMenu, self.show_tbMaster, self.show_statusBar, self.show_serStatus, self.show_notifi]

        for key in keys:
            value = func.str2bool(self.settings.value(key, True))
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