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
from PyQt5.QtWidgets        import (QApplication, QWidget, QGridLayout)

# PLM
from cores.Loggers          import Loggers
from appData                import __homepage__, dockB, SiPoMin
from ui                     import TopTab, BotTab, Footer, StatusBar
from ui.uikits.Widget       import Widget
from ui.uikits.GridLayout   import GridLayout
from ui.uikits.MainWindow   import MainWindow
from ui.AppToolbar          import MainToolBar, DockToolBar
from ui.Menus               import MainMenuBar, SubMenuBar
from ui.Network             import ServerStatus
from ui.uikits.GroupBox     import GroupBox
from ui.uikits.UiPreset     import AppIcon
from utils.utils            import str2bool, bool2str

# -------------------------------------------------------------------------------------------------------------
""" Pipeline Tool main layout """

class PipelineManager(MainWindow):

    key = 'MainUI'

    def __init__(self, settings, parent=None):
        super(PipelineManager, self).__init__(parent)

        self.logger = Loggers()
        self.url = __homepage__

        self.setObjectName(self.key)
        self.setWindowIcon(AppIcon("Logo"))

        self.settings       = settings

        self.mainWidget     = Widget()
        self.layout         = GridLayout()
        self.mainWidget.setLayout(self.layout)

        self.buildUI()
        self.setCentralWidget(self.mainWidget)

    def buildUI(self):

        self.mainMenuBar    = MainMenuBar.MainMenuBar()
        self.subMenuBar     = SubMenuBar.SubMenuBar()                                                   # Sub menu
        self.toolBar        = MainToolBar.MainToolBar()                                                 # Toolbar
        self.serverStatus   = ServerStatus.ServerStatus()                                               # Server Status
        self.subMenuSec     = GroupBox("Sub Menu", self.subMenuBar, "qmainLayout")
        self.mainMenuSec    = GroupBox("Main Menu", self.mainMenuBar, "qmainLayout")

        self.networkStatus  = GroupBox("Server Status", self.serverStatus, "autoGrid")
        self.networkStatus.setMaximumHeight(self.subMenuBar.maximumHeight()*3)
        self.subToolBarSec  = GroupBox("Tool Bar", self.toolBar, "qmainLayout")

        self.topTabUI       = TopTab.TopTab()                                                           # Tab layout
        self.botTabUI       = BotTab.BotTab()                                                           # Bot build 1
        self.notifiSec      = GroupBox("Notification", None, "autoGrid")                                # Bot build 2

        self.footer         = Footer.Footer()
        self.statusBar      = StatusBar.StatusBar()                                                     # Status bar viewing message

        self.setStatusBar(self.statusBar)

        for layout in [self.subMenuBar, self.mainMenuBar, self.topTabUI, self.botTabUI, self.notifiSec, self.statusBar,
                       self.footer, self.toolBar, self.serverStatus, self.subMenuSec, self.networkStatus, self.subToolBarSec, ]:

            layout.signals.showLayout.connect(self.signals.showLayout)
            layout.signals.executing.connect(self.signals.executing)
            layout.signals.regisLayout.connect(self.signals.regisLayout)
            layout.signals.openBrowser.connect(self.signals.openBrowser)
            layout.signals.setSetting.connect(self.signals.setSetting)
            layout.signals.regisLayout.emit(self)

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
            grp = self.key

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

        # Signal
        self.layout.addWidget(self.mainMenuSec, 0, 0, 1, 9)
        self.layout.addWidget(self.subMenuSec, 1, 0, 1, 6)
        self.layout.addWidget(self.networkStatus, 1, 6, 1, 3)
        self.layout.addWidget(self.subToolBarSec, 2, 0, 2, 9)

        self.layout.addWidget(self.topTabUI, 4, 0, 4, 9)
        self.layout.addWidget(self.botTabUI, 8, 0, 3, 6)
        self.layout.addWidget(self.notifiSec, 8, 6, 3, 3)

        self.layout.addWidget(self.footer, 11, 0, 1, 9)

        # self.tdDock         = DockToolBar.DockToolBar('TD')
        # self.vfxDock        = DockToolBar.DockToolBar('VFX')
        # self.artDock        = DockToolBar.DockToolBar('ART')
        # self.texDock        = DockToolBar.DockToolBar('TEXTURE')
        # self.postDock       = DockToolBar.DockToolBar('POST')
        #
        # self.docks = [self.tdDock, self.vfxDock, self.artDock, self.texDock, self.postDock]
        # for dock in self.docks:
        #     self.signals.regisLayout.emit(dock)
        #     self.add_dockWidget(dock)

    def add_dockWidget(self, dock, pos=dockB):

        self.dock = dock

        self.dock.signals.showLayout.connect(self.signals.showLayout)
        self.dock.signals.setSetting.connect(self.signals.setSetting)
        self.dock.signals.executing.connect(self.signals.executing)
        self.dock.signals.regisLayout.connect(self.signals.regisLayout)

        self.addDockWidget(pos, self.dock)


# -------------------------------------------------------------------------------------------------------------
def main():
    app = QApplication(sys.argv)
    layout = PipelineManager()
    layout.show()
    app.exec_()

if __name__ == '__main__':
    main()