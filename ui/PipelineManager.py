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
from functools                          import partial

# PyQt5
from PyQt5.QtWidgets                    import QApplication

# PLM
print(1)
from appData                            import __homepage__, dockB, __appname__
print(2)
from ui.uikits.MainWindow               import MainWindow
print(3)
from ui.uikits.GroupBox                 import GroupBox
print(4)
from ui.uikits.Widget                   import Widget
print(5)
from ui.uikits.GridLayout               import GridLayout
print(6)
from ui.uikits.Icon                     import LogoIcon
print(7)
from ui.Menus                           import MainMenuBar                      # Header
from ui.Network.ConnectStatus           import ConnectStatus
from ui.AppToolbar.MainToolBar          import MainToolBar
print(8)
from ui.TopTab                          import TopTab                           # Body
from ui.BotTab                          import BotTab
from ui.Footer                          import Footer                           # Footer
from ui.StatusBar                       import StatusBar
print(9)
from utils                              import str2bool, bool2str

# -------------------------------------------------------------------------------------------------------------
""" Pipeline Tool main layout """

class PipelineManager(MainWindow):

    key = 'PipelineManager'
    _name = __appname__

    def __init__(self, settings, parent=None):
        super(PipelineManager, self).__init__(parent)

        self.url = __homepage__

        self.setObjectName(self._name)
        self.setWindowIcon(LogoIcon("Logo"))

        self.settings       = settings

        self.mainWidget     = Widget()
        self.layout         = GridLayout()
        self.mainWidget.setLayout(self.layout)

        self.buildUI()
        self.setCentralWidget(self.mainWidget)

    def buildUI(self):

        self.mainMenuBar    = MainMenuBar.MainMenuBar()
        self.toolBar        = MainToolBar()                                                 # Toolbar
        self.serverStatus   = ConnectStatus()                                                # Server Status

        self.mainMenuSec    = GroupBox("Main Menu", self.mainMenuBar, "qmainLayout")
        self.mainMenuSec.key = "MainMenuSection"
        self.networkStatus  = GroupBox("Server Status", self.serverStatus, "autoGrid")

        self.networkStatus.key = "NetworkStatus"
        self.subToolBarSec  = GroupBox("Tool Bar", self.toolBar, "qmainLayout")
        self.subToolBarSec.key = "SubtoolBarSec"

        self.topTabUI       = TopTab()                                                           # Tab layout
        self.botTabUI       = BotTab()                                                           # Bot build 1
        self.notifiSec      = GroupBox("Notification", None, "autoGrid")                                # Bot build 2
        self.notifiSec.key = "Notification"

        self.footer         = Footer()
        self.statusBar      = StatusBar()                                                     # Status bar viewing message

        self.setStatusBar(self.statusBar)

        self.mainUI_layouts =  [
                                self.mainMenuBar, self.toolBar, self.serverStatus, self.mainMenuSec,
                                self.networkStatus, self.subToolBarSec, self.topTabUI, self.botTabUI, self.notifiSec,
                                self.statusBar, self.footer,
                                ]

        for layout in self.mainUI_layouts:
            layout.signals.showLayout.connect(self.signals.showLayout)
            layout.signals.executing.connect(self.signals.executing)
            layout.signals.regisLayout.connect(self.signals.regisLayout)
            layout.signals.openBrowser.connect(self.signals.openBrowser)
            layout.signals.setSetting.connect(self.signals.setSetting)

        cbs = [
               self.botTabUI.generalSetting.tbTDCB, self.botTabUI.generalSetting.tbCompCB,
               self.botTabUI.generalSetting.tbArtCB, self.botTabUI.generalSetting.tbTexCB,
               self.botTabUI.generalSetting.tbPostCB, self.botTabUI.generalSetting.mainToolBarCB,
               self.botTabUI.generalSetting.statusBarCB, self.botTabUI.generalSetting.connectStatuCB,
               self.botTabUI.generalSetting.notifiCB,
                ]

        sections = [
                    self.toolBar.tdToolBar, self.toolBar.compToolBar, self.toolBar.artToolBar, self.toolBar.textureToolBar,
                    self.toolBar.postToolBar, self.mainMenuSec, self.statusBar, self.networkStatus, self.notifiSec
                    ]

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
        self.layout.addWidget(self.mainMenuSec, 0, 0, 1, 6)
        self.layout.addWidget(self.networkStatus, 0, 6, 1, 3)
        self.layout.addWidget(self.subToolBarSec, 1, 0, 1, 9)

        self.layout.addWidget(self.topTabUI, 2, 0, 4, 9)
        self.layout.addWidget(self.botTabUI, 6, 0, 3, 6)
        self.layout.addWidget(self.notifiSec, 6, 6, 3, 3)

        self.layout.addWidget(self.footer, 9, 0, 1, 9)

    def add_dockWidget(self, dock, pos=dockB):

        dock.signals.showLayout.connect(self.signals.showLayout)
        dock.signals.setSetting.connect(self.signals.setSetting)
        dock.signals.executing.connect(self.signals.executing)
        dock.signals.regisLayout.connect(self.signals.regisLayout)
        dock.signals.openBrowser.connect(self.signals.openBrowser)

        self.addDockWidget(pos, dock)

    def showEvent(self, event):
        self.signals.showLayout.emit('PipelineManager', 'show')

        for layout in self.mainUI_layouts:
            layout.signals.showLayout.emit(layout.key, 'show')

        self.signals.showLayout.emit('SysTray', 'show')
        self.signals.showLayout.emit('SignIn', 'hide')
        self.signals.showLayout.emit('SignUp', 'hide')
        self.signals.showLayout.emit('ForgotPassword', 'hide')

    def hideEvent(self, event):
        self.signals.showLayout.emit('PipelineManager', 'hide')
        self.setValue('showLayout', 'hide')

# -------------------------------------------------------------------------------------------------------------
def main():
    app = QApplication(sys.argv)
    layout = PipelineManager()
    layout.show()
    app.exec_()

if __name__ == '__main__':
    main()