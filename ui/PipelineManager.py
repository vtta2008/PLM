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
from functools              import partial

# PyQt5
from PyQt5.QtCore           import pyqtSignal
from PyQt5.QtWidgets        import (QApplication, QMainWindow, QWidget, QGridLayout)

# PLM
from cores.Loggers          import Loggers
from cores.base             import DAMG
from ui.UiSignals           import UiSignals
from appData                import __homepage__, dockB, SiPoMin
from ui                     import TopTab, BotTab, Footer, StatusBar
from ui.uikits.MainWindow   import MainWindow
from ui.AppToolbar          import MainToolBar, DockToolBar
from ui.Menus               import MainMenuBar, SubMenuBar
from ui.Network             import ServerStatus
from ui.uikits.GroupBox     import AutoSectionLayoutGrp, AutoSectionQMainGrp
from ui.uikits.UiPreset     import AppIcon
from utils.utils            import get_layout_size, str2bool, bool2str

# -------------------------------------------------------------------------------------------------------------
""" Pipeline Tool main layout """

class PipelineManager(MainWindow):

    key = 'mainUI'

    def __init__(self, settings, parent=None):
        super(PipelineManager, self).__init__(parent)

        self.logger = Loggers()
        self.url = __homepage__

        self.setObjectName(self.key)
        self.setWindowIcon(AppIcon("Logo"))

        self.settings       = settings

        self.mainWidget     = QWidget()
        self.layout         = QGridLayout()
        self.mainWidget.setLayout(self.layout)

        self.buildUI()
        self.setCentralWidget(self.mainWidget)
        self.applySetting()

    def buildUI(self):

        self.mainMenuBar    = MainMenuBar.MainMenuBar()
        self.subMenuBar     = SubMenuBar.SubMenuBar()                                                   # Sub menu
        self.toolBar        = MainToolBar.MainToolBar()                                                 # Toolbar
        self.serverStatus   = ServerStatus.ServerStatus()                                               # Server Status
        self.subMenuSec     = AutoSectionQMainGrp("Sub Menu", self.subMenuBar)
        self.mainMenuSec    = AutoSectionQMainGrp("Main Menu", self.mainMenuBar)

        self.networkStatus  = AutoSectionLayoutGrp("Server Status", self.serverStatus)
        self.networkStatus.setMaximumHeight(self.subMenuBar.maximumHeight()*3)
        self.subToolBarSec  = AutoSectionQMainGrp("Tool Bar", self.toolBar)

        self.topTabUI       = TopTab.TopTab()                                                           # Tab layout
        self.botTabUI       = BotTab.BotTab()                                                           # Bot build 1
        self.notifiSec      = AutoSectionLayoutGrp("Notification", None)                                # Bot build 2

        self.footer         = Footer.Footer()
        self.statusBar      = StatusBar.StatusBar()                                                     # Status bar viewing message
        self.setStatusBar(self.statusBar)

        self.subMenuBar.signals.showLayout.connect(self.signals.showLayout)
        self.subMenuBar.signals.executing.connect(self.signals.executing)
        self.subMenuBar.signals.regisLayout.connect(self.signals.regisLayout)
        self.subMenuBar.signals.openBrowser.connect(self.signals.openBrowser)

        self.mainMenuBar.signals.showLayout.connect(self.signals.showLayout)
        self.mainMenuBar.signals.executing.connect(self.signals.executing)
        self.mainMenuBar.signals.regisLayout.connect(self.signals.regisLayout)
        self.mainMenuBar.signals.openBrowser.connect(self.signals.openBrowser)

        self.topTabUI.signals.executing.connect(self.signals.executing)
        self.topTabUI.signals.showLayout.connect(self.signals.showLayout)
        self.topTabUI.signals.regisLayout.connect(self.signals.regisLayout)

        self.toolBar.signals.showLayout.connect(self.signals.showLayout)
        self.toolBar.signals.executing.connect(self.signals.executing)
        self.toolBar.signals.regisLayout.connect(self.signals.regisLayout)
        self.toolBar.signals.openBrowser.connect(self.signals.openBrowser)
        self.toolBar.signals.setSetting.connect(self.signals.setSetting)


        cbs = [self.botTabUI.generalSetting.tbTDCB, self.botTabUI.generalSetting.tbCompCB,
               self.botTabUI.generalSetting.tbArtCB, self.botTabUI.generalSetting.tbTexCB,
               self.botTabUI.generalSetting.tbPostCB, self.botTabUI.generalSetting.subToolBarCB,
               self.botTabUI.generalSetting.mainToolBarCB, self.botTabUI.generalSetting.statusBarCB,
               self.botTabUI.generalSetting.subMenuCB, self.botTabUI.generalSetting.serStatusCB,
               self.botTabUI.generalSetting.notifiCB]

        sections = [self.toolBar.tdToolBar, self.toolBar.compToolBar, self.toolBar.artToolBar, self.toolBar.textureToolBar,
                    self.toolBar.postToolBar, self.subToolBarSec, self.mainMenuSec, self.statusBar, self.subMenuSec,
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
            cbs[i].stateChanged.connect(partial(self.signals.setSetting.emit, key, bool2str(val), grp))

        self.footer.signals.showLayout.connect(self.signals.showLayout)

        # Signal
        self.layout.addWidget(self.mainMenuSec, 0, 0, 1, 9)
        self.layout.addWidget(self.subMenuSec, 1, 0, 1, 6)
        self.layout.addWidget(self.networkStatus, 1, 6, 1, 3)
        self.layout.addWidget(self.subToolBarSec, 2, 0, 2, 9)

        self.layout.addWidget(self.topTabUI, 4, 0, 4, 9)
        self.layout.addWidget(self.botTabUI, 8, 0, 3, 6)
        self.layout.addWidget(self.notifiSec, 8, 6, 3, 3)

        self.layout.addWidget(self.footer, 11, 0, 1, 9)

        self.tdDock         = DockToolBar.DockToolBar('TD')
        self.vfxDock        = DockToolBar.DockToolBar('VFX')
        self.artDock        = DockToolBar.DockToolBar('ART')
        self.texDock        = DockToolBar.DockToolBar('TEXTURE')
        self.postDock       = DockToolBar.DockToolBar('POST')

        self.docks = [self.tdDock, self.vfxDock, self.artDock, self.texDock, self.postDock]
        for dock in self.docks:
            self.signals.regisLayout.emit(dock)
            self.add_dockWidget(dock)

    def add_dockWidget(self, dock, pos=dockB):

        self.dock = dock

        self.dock.signals.showLayout.connect(self.signals.showLayout)
        self.dock.signals.setSetting.connect(self.signals.setSetting)
        self.dock.signals.executing.connect(self.signals.executing)
        self.dock.signals.regisLayout.connect(self.signals.regisLayout)

        self.addDockWidget(pos, self.dock)

    def hideEvent(self, event):
        pass

    def showEvent(self, event):
        # self.specs.showState.emit(True)
        self.signals.showLayout.emit('login', 'hide')
        self.signals.showLayout.emit('sysTray', 'show')

    def closeEvent(self, event):

        # self.specs.showState.emit(False)
        # self.sysNotify.emit('notice', "PLM hide in system tray", 'info', 500)

        self.signals.showLayout.emit(self.key, 'hide')
        event.ignore()

    def applySetting(self):
        self.setSizePolicy(SiPoMin, SiPoMin)
        self.setContentsMargins(5,5,5,5)

# -------------------------------------------------------------------------------------------------------------
def main():
    app = QApplication(sys.argv)
    layout = PipelineManager()
    layout.show()
    app.exec_()

if __name__ == '__main__':
    main()