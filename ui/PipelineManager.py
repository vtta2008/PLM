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
from functools import partial

# PyQt5
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout)

from core.Loggers import SetLogger
# Plt
from core.Metadata import __homepage__
from core.paths import dockB, SiPoMin
from ui import TopTab, BotTab, Footer, StatusBar
from ui.AppToolbar import MainToolBar, DockToolBar
from ui.Menus import MainMenuBar, SubMenuBar
from ui.Network import ServerStatus
from ui.uikits.GroupBox import AutoSectionLayoutGrp, AutoSectionQMainGrp
from ui.uikits.UiPreset import AppIcon
from utilities.utils import get_layout_size, str2bool, bool2str

# -------------------------------------------------------------------------------------------------------------
""" Pipeline Tool main layout """

class PipelineManager(QMainWindow):

    key = 'mainUI'

    showLayout = pyqtSignal(str, str)
    executing = pyqtSignal(str)
    addLayout = pyqtSignal(object)
    openBrowser = pyqtSignal(str)
    setSetting = pyqtSignal(str, str, str)
    sysNotify = pyqtSignal(str, str, str, int)

    def __init__(self, settings, parent=None):

        super(PipelineManager, self).__init__(parent)
        self.logger = SetLogger(self)
        self.url = __homepage__
        self.setObjectName(self.key)
        self.setWindowIcon(AppIcon("Logo"))
        self.settings = settings

        self.mainWidget = QWidget()
        self.layout = QGridLayout()
        self.mainWidget.setLayout(self.layout)

        self.buildUI()
        self.setCentralWidget(self.mainWidget)
        self.applySetting()

    def buildUI(self):

        self.mainMenuBar = MainMenuBar.MainMenuBar()
        self.subMenuBar = SubMenuBar.SubMenuBar()                                                   # Sub menu
        self.toolBar = MainToolBar.MainToolBar()                                                    # Toolbar
        self.serverStatus = ServerStatus.ServerStatus()                                             # Server Status
        self.subMenuSec = AutoSectionQMainGrp("Sub Menu", self.subMenuBar)
        self.mainMenuSec = AutoSectionQMainGrp("Main Menu", self.mainMenuBar)

        self.networkStatus = AutoSectionLayoutGrp("Server Status", self.serverStatus)
        self.networkStatus.setMaximumHeight(self.subMenuBar.maximumHeight()*3)
        self.subToolBarSec = AutoSectionQMainGrp("Tool Bar", self.toolBar)

        self.topTabUI = TopTab.TopTab()                                                            # Tab layout
        self.botTabUI = BotTab.BotTab()                                                            # Bot build 1
        self.notifiSec = AutoSectionLayoutGrp("Notification", None)                                # Bot build 2

        self.subMenuBar.showLayout.connect(self.showLayout)
        self.subMenuBar.executing.connect(self.executing)
        self.subMenuBar.addLayout.connect(self.addLayout)
        self.subMenuBar.openUrl.connect(self.openBrowser)

        self.mainMenuBar.showLayout.connect(self.showLayout)
        self.mainMenuBar.executing.connect(self.executing)
        self.mainMenuBar.addLayout.connect(self.addLayout)
        self.mainMenuBar.openUrl.connect(self.openBrowser)

        self.topTabUI.executing.connect(self.executing)
        self.topTabUI.showLayout.connect(self.showLayout)
        self.topTabUI.regLayout.connect(self.addLayout)

        self.toolBar.showLayout.connect(self.showLayout)
        self.toolBar.executing.connect(self.executing)
        self.toolBar.addLayout.connect(self.addLayout)
        self.toolBar.openBrowser.connect(self.openBrowser)
        self.toolBar.setSetting.connect(self.setSetting)

        self.footer = Footer.Footer()
        self.stBar = StatusBar.StatusBar()                                                         # Status bar viewing message
        self.setStatusBar(self.stBar)

        cbs = [self.botTabUI.generalSetting.tbTDCB, self.botTabUI.generalSetting.tbCompCB,
               self.botTabUI.generalSetting.tbArtCB, self.botTabUI.generalSetting.tbTexCB,
               self.botTabUI.generalSetting.tbPostCB, self.botTabUI.generalSetting.subToolBarCB,
               self.botTabUI.generalSetting.mainToolBarCB, self.botTabUI.generalSetting.statusBarCB,
               self.botTabUI.generalSetting.subMenuCB, self.botTabUI.generalSetting.serStatusCB,
               self.botTabUI.generalSetting.notifiCB]

        sections = [self.toolBar.tdToolBar, self.toolBar.compToolBar, self.toolBar.artToolBar, self.toolBar.textureToolBar,
                    self.toolBar.postToolBar, self.subToolBarSec, self.mainMenuSec, self.stBar, self.subMenuSec,
                    self.networkStatus, self.notifiSec]

        for i in range(len(sections)):
            key = self.botTabUI.generalSetting.keys[i]
            grp = self.botTabUI.generalSetting.settingGrp

            self.settings.beginGroup(grp)
            if self.settings.value(key) is None:
                if i == 3 or i == 4:
                    val = False
                else:
                    val = True
            else:
                val = str2bool(self.settings.value(key))
            self.settings.endGroup()

            cbs[i].setChecked(val)
            sections[i].setVisible(val)
            cbs[i].stateChanged.connect(sections[i].setVisible)
            cbs[i].stateChanged.connect(partial(self.setSetting.emit, key, bool2str(val), grp))

        self.footer.showLayout.connect(self.showLayout)

        # Signal
        self.layout.addWidget(self.mainMenuSec, 0, 0, 1, 9)
        self.layout.addWidget(self.subMenuSec, 1, 0, 1, 6)
        self.layout.addWidget(self.networkStatus, 1, 6, 1, 3)
        self.layout.addWidget(self.subToolBarSec, 2, 0, 2, 9)

        self.layout.addWidget(self.topTabUI, 4, 0, 4, 9)
        self.layout.addWidget(self.botTabUI, 8, 0, 3, 6)
        self.layout.addWidget(self.notifiSec, 8, 6, 3, 3)

        self.layout.addWidget(self.footer, 11, 0, 1, 9)

        self.tdDock = DockToolBar.DockToolBar('TD')
        self.vfxDock = DockToolBar.DockToolBar('VFX')
        self.artDock = DockToolBar.DockToolBar('ART')
        self.texDock = DockToolBar.DockToolBar('TEXTURE')
        self.postDock = DockToolBar.DockToolBar('POST')

        self.docks = [self.tdDock, self.vfxDock, self.artDock, self.texDock, self.postDock]
        for dock in self.docks:
            self.addLayout.emit(dock)
            self.add_dockWidget(dock)

    def add_dockWidget(self, dock, pos=dockB):
        self.dock = dock
        self.dock.showLayout.connect(self.showLayout)
        self.dock.setSetting.connect(self.setSetting)
        self.dock.executing.connect(self.executing)
        self.dock.addLayout.connect(self.addLayout)
        self.addDockWidget(pos, self.dock)

    def resizeEvent(self, event):
        sizeW, sizeH = get_layout_size(self)
        self.setSetting.emit('width', str(sizeW), self.objectName())
        self.setSetting.emit('height', str(sizeH), self.objectName())

    def showEvent(self, event):
        # self.specs.showState.emit(True)
        self.showLayout.emit('login', 'hide')
        self.showLayout.emit('sysTray', 'show')

    def closeEvent(self, event):
        # self.specs.showState.emit(False)
        # self.sysNotify.emit('notice', "PLM hide in system tray", 'info', 500)
        self.showLayout.emit(self.key, 'hide')
        event.ignore()

    def applySetting(self):
        self.setSizePolicy(SiPoMin, SiPoMin)
        self.setContentsMargins(5,15,5,15)

# -------------------------------------------------------------------------------------------------------------
def main():
    app = QApplication(sys.argv)
    layout = PipelineManager()
    layout.show()
    app.exec_()

if __name__ == '__main__':
    main()