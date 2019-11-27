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

# PyQt5
from PyQt5.QtCore                       import Qt

# PLM

from appData                            import __homepage__, dockB, __appname__
from toolkits.Widgets                   import MainWindow, GroupBox, Widget, GridLayout, LogoIcon
from .Header                            import MainToolBar, MainMenuBar, ConnectStatus
from .Body                              import TopTab, BotTab, Notification
from .Footer                            import Footer, MainStatusBar

# -------------------------------------------------------------------------------------------------------------
""" Pipeline Tool main layout """

class PipelineManager(MainWindow):

    key                                 = 'PipelineManager'
    _name                               = __appname__

    def __init__(self, actionManager, buttonManager, threadManager, parent=None):
        super(PipelineManager, self).__init__(parent)

        self.url                        = __homepage__
        self.setObjectName(self._name)
        self.setWindowTitle(__appname__)
        self.setWindowIcon(LogoIcon("Logo"))

        self.actionManager              = actionManager
        self.buttonManager              = buttonManager
        self.threadManager              = threadManager

        self.mainWidget                 = Widget()
        self.layout                     = GridLayout()
        self.mainWidget.setLayout(self.layout)
        self.buildUI()
        self.setCentralWidget(self.mainWidget)

    def buildUI(self):

        self.mainMenuBar                = MainMenuBar(self.actionManager, self)
        self.mainToolBar                = MainToolBar(self.actionManager, self)
        self.connectStatus              = ConnectStatus(self)
        self.notification               = Notification(self.threadManager, self)

        self.mainMenuSec                = GroupBox("Main Menu"      , self.mainMenuBar      , "qmainLayout" , self)
        self.connectStatusSec           = GroupBox("Connect Status" , self.connectStatus    , "autoGrid"    , self)
        self.mainToolBarSec             = GroupBox("Tool Bar"       , self.mainToolBar      , "qmainLayout" , self)
        self.notifiSec                  = GroupBox("Notification"   , self.notification     , "autoGrid"    , self)

        self.mainMenuSec.key            = "MainMenuSection"
        self.mainToolBarSec.key         = "MainToolBarSection"
        self.connectStatusSec.key       = "ConnectStatusSection"
        self.notifiSec.key              = "NotificationSection"

        self.topTabUI                   = TopTab(self.buttonManager, self)
        self.botTabUI                   = BotTab(self)
        self.footer                     = Footer(self.buttonManager, self.threadManager, self)
        self.statusBar                  = MainStatusBar(self)

        self.layouts =  [self.mainMenuBar, self.mainToolBar      , self.connectStatus    , self.notification,
                         self.mainMenuSec, self.mainToolBarSec   , self.connectStatusSec , self.notifiSec,
                         self.topTabUI   , self.botTabUI         , self.footer           , self.statusBar, ]

        self.layout.addWidget(self.mainMenuSec, 0, 0, 1, 7)
        self.layout.addWidget(self.connectStatusSec, 0, 7, 1, 2)
        self.layout.addWidget(self.mainToolBarSec, 1, 0, 1, 9)

        self.layout.addWidget(self.topTabUI, 2, 0, 4, 9)
        self.layout.addWidget(self.botTabUI, 6, 0, 3, 6)
        self.layout.addWidget(self.notifiSec, 6, 6, 3, 3)

        self.layout.addWidget(self.footer, 9, 0, 1, 9)
        self.setStatusBar(self.statusBar)

    def add_dockWidget(self, dock, pos=dockB):

        dock.signals.showLayout.connect(self.signals.showLayout)
        dock.signals.setSetting.connect(self.signals.setSetting)
        dock.signals.executing.connect(self.signals.executing)
        dock.signals.regisLayout.connect(self.signals.regisLayout)
        dock.signals.openBrowser.connect(self.signals.openBrowser)

        self.addDockWidget(pos, dock)

    def showEvent(self, event):
        for layout in [self.mainMenuSec, self.mainMenuSec, self.connectStatusSec, self.notifiSec]:
            if layout.isHidden():
                self.signals.emit('showLayout', layout.key, 'show')

    @property
    def mode(self):
        return self.connectStatus.mode

# -------------------------------------------------------------------------------------------------------------