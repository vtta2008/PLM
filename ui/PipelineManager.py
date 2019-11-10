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
from PyQt5.QtWidgets                    import QApplication

# PLM

from appData                            import __homepage__, dockB, __appname__
from ui.uikits.MainWindow               import MainWindow
from ui.uikits.GroupBox                 import GroupBox
from ui.uikits.Widget                   import Widget
from ui.uikits.GridLayout               import GridLayout
from ui.uikits.Icon                     import LogoIcon
from ui.Menus.MainMenuBar               import MainMenuBar
from ui.Network.ConnectStatus           import ConnectStatus
from ui.AppToolbar.MainToolBar          import MainToolBar
from ui.Tabs.TopTab                     import TopTab                           # Body
from ui.Tabs.BotTab                     import BotTab
from ui.Footer.Footer                   import Footer                           # Footer
from ui.Footer.MainStatusBar            import MainStatusBar

# -------------------------------------------------------------------------------------------------------------
""" Pipeline Tool main layout """

class PipelineManager(MainWindow):

    key = 'PipelineManager'
    _name = __appname__

    def __init__(self, settings, actionManager, buttonManager, parent=None):
        super(PipelineManager, self).__init__(parent)

        self.url = __homepage__
        self.setObjectName(self._name)
        self.setWindowTitle(__appname__)
        self.setWindowIcon(LogoIcon("Logo"))
        self.settings       = settings
        self.actionManager  = actionManager
        self.buttonManager  = buttonManager

        self.mainWidget     = Widget()
        self.layout         = GridLayout()
        self.mainWidget.setLayout(self.layout)

        self.buildUI()
        self.setCentralWidget(self.mainWidget)

    def buildUI(self):

        self.mainMenuBar            = MainMenuBar(self.actionManager, self)
        self.mainToolBar            = MainToolBar(self.actionManager, self)
        self.connectStatus          = ConnectStatus(self)
        self.notification           = GridLayout(self)

        self.mainMenuSec            = GroupBox("Main Menu"      , self.mainMenuBar      , "qmainLayout")
        self.connectStatusSec       = GroupBox("Connect Status" , self.connectStatus    , "autoGrid")
        self.mainToolBarSec         = GroupBox("Tool Bar"       , self.mainToolBar      , "qmainLayout")
        self.notifiSec              = GroupBox("Notification"   , self.notification     , "autoGrid")

        self.mainMenuSec.key        = "MainMenuSectionSection"
        self.mainToolBarSec.key     = "MainToolBarSectionSection"
        self.connectStatusSec.key   = "ConnectStatusSection"
        self.notifiSec.key          = "NotificationSection"

        self.mainMenuSec.setParent(self)
        self.mainToolBarSec.setParent(self)
        self.connectStatusSec.setParent(self)
        self.notifiSec.setParent(self)

        self.topTabUI               = TopTab(self.buttonManager, self)
        self.botTabUI               = BotTab(self)
        self.footer                 = Footer(self.buttonManager, self)
        self.statusBar              = MainStatusBar(self)
        self.setStatusBar(self.statusBar)

        self.mainUI_layouts =  [self.mainMenuBar, self.mainToolBar      , self.connectStatus    , self.notification,
                                self.mainMenuSec, self.mainToolBarSec   , self.connectStatusSec , self.notifiSec,
                                self.topTabUI   , self.botTabUI         , self.footer           , self.statusBar, ]

        # for layout in self.mainUI_layouts:
        #     layout.signals.executing.connect(self.signals.executing)
        #     layout.signals.regisLayout.connect(self.signals.regisLayout)
        #     layout.signals.openBrowser.connect(self.signals.openBrowser)
        #     layout.signals.setSetting.connect(self.signals.setSetting)

        # Header

        # Header Menu
        self.layout.addWidget(self.mainMenuSec, 0, 0, 1, 6)
        self.layout.addWidget(self.connectStatusSec, 0, 6, 1, 3)

        # Header ToolBar
        self.layout.addWidget(self.mainToolBarSec, 1, 0, 1, 9)

        # Body
        # Body top
        self.layout.addWidget(self.topTabUI, 2, 0, 4, 9)

        # Body bot
        self.layout.addWidget(self.botTabUI, 6, 0, 3, 6)
        self.layout.addWidget(self.notifiSec, 6, 6, 3, 3)

        # Footer
        self.layout.addWidget(self.footer, 9, 0, 1, 9)

    def add_dockWidget(self, dock, pos=dockB):

        dock.signals.showLayout.connect(self.signals.showLayout)
        dock.signals.setSetting.connect(self.signals.setSetting)
        dock.signals.executing.connect(self.signals.executing)
        dock.signals.regisLayout.connect(self.signals.regisLayout)
        dock.signals.openBrowser.connect(self.signals.openBrowser)

        self.addDockWidget(pos, dock)

    def showEvent(self, event):
        self.notifiSec.show()
        self.connectStatusSec.show()
        self.mainToolBarSec.show()
        self.mainMenuSec.show()

# -------------------------------------------------------------------------------------------------------------
def main():
    app = QApplication(sys.argv)
    layout = PipelineManager()
    layout.show()
    app.exec_()

if __name__ == '__main__':
    main()