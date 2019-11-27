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
from toolkits.Widgets.MainWindow import MainWindow
from toolkits.Widgets.GroupBoxBase import GroupBox
from toolkits.Widgets.Widget import Widget
from toolkits.Widgets.GridLayout import GridLayout
from toolkits.Widgets.Icon import LogoIcon
from ui.Header.Menus.MainMenuBar        import MainMenuBar
from ui.Header.Network.ConnectStatus    import ConnectStatus
from ui.Header.Toolbars.MainToolBar   import MainToolBar
from ui.Body.TopTab                     import TopTab                           # Body
from ui.Body.BotTab                     import BotTab
from ui.Body.Notification               import Notification
from ui.Footer.Footer                   import Footer                           # Footer
from ui.Footer.MainStatusBar            import MainStatusBar

# -------------------------------------------------------------------------------------------------------------
""" Pipeline Tool main layout """

class PipelineManager(MainWindow):

    key = 'PipelineManager'
    _name = __appname__

    def __init__(self, actionManager, buttonManager, threadManager, parent=None):
        super(PipelineManager, self).__init__(parent)

        self.url = __homepage__
        self.setObjectName(self._name)
        self.setWindowTitle(__appname__)
        self.setWindowIcon(LogoIcon("Logo"))

        self.actionManager  = actionManager
        self.buttonManager  = buttonManager
        self.threadManager  = threadManager

        self.mainWidget     = Widget()
        self.layout         = GridLayout()
        self.mainWidget.setLayout(self.layout)

        self.buildUI()
        self.setCentralWidget(self.mainWidget)

    def buildUI(self):

        self.mainMenuBar            = MainMenuBar(self.actionManager, self)
        self.mainToolBar            = MainToolBar(self.actionManager, self)
        self.connectStatus          = ConnectStatus(self)
        self.notification           = Notification(self.threadManager, self)

        self.mainMenuSec            = GroupBox("Main Menu"      , self.mainMenuBar      , "qmainLayout" , self)
        self.connectStatusSec       = GroupBox("Connect Status" , self.connectStatus    , "autoGrid"    , self)
        self.mainToolBarSec         = GroupBox("Tool Bar"       , self.mainToolBar      , "qmainLayout" , self)
        self.notifiSec              = GroupBox("Notification"   , self.notification     , "autoGrid"    , self)

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
        self.footer                 = Footer(self.buttonManager, self.threadManager, self)
        self.statusBar              = MainStatusBar(self)

        self.layouts =  [self.mainMenuBar, self.mainToolBar      , self.connectStatus    , self.notification,
                         self.mainMenuSec, self.mainToolBarSec   , self.connectStatusSec , self.notifiSec,
                         self.topTabUI   , self.botTabUI         , self.footer           , self.statusBar, ]

        # self.allowSettingLayouts = [self.mainMenuBar, self.mainToolBar, self.connectStatus, self.notification, ]
                                    # self.topTabUI, self.botTabUI, self.footer, self.statusBar, ]

        # for layout in self.allowSettingLayouts:
        #     layout.settings._settingEnable = True

        # for layout in self.layouts:
        #     print(layout.key)
        #     layout.signals.connect('executing', self.signals.executing)
        #     layout.signals.connect('regisLayout', self.signals.regisLayout)
        #     layout.signals.connect('openBrowser', self.signals.openBrowser)
        #     layout.signals.connect('setSetting', self.signals.setSetting)
        #     layout.signals.connect('showLayout', self.signals.showLayout)
        #     layout.settings._settingEnable = True

        # Header
        # Header Menu
        self.layout.addWidget(self.mainMenuSec, 0, 0, 1, 7)
        self.layout.addWidget(self.connectStatusSec, 0, 7, 1, 2)

        # Header ToolBar
        self.layout.addWidget(self.mainToolBarSec, 1, 0, 1, 9)

        # Body
        # Body top
        self.layout.addWidget(self.topTabUI, 2, 0, 4, 9)

        # Body bot
        self.layout.addWidget(self.botTabUI, 6, 0, 3, 6)
        self.layout.addWidget(self.notifiSec, 6, 6, 3, 3)

        # Footer
        # Footer layout
        self.layout.addWidget(self.footer, 9, 0, 1, 9)
        # Footer status bar
        self.setStatusBar(self.statusBar)

    def add_dockWidget(self, dock, pos=dockB):

        dock.signals.showLayout.connect(self.signals.showLayout)
        dock.signals.setSetting.connect(self.signals.setSetting)
        dock.signals.executing.connect(self.signals.executing)
        dock.signals.regisLayout.connect(self.signals.regisLayout)
        dock.signals.openBrowser.connect(self.signals.openBrowser)

        self.addDockWidget(pos, dock)

    # def resizeEvent(self, event):
    #
    #     w = self.width()
    #     h = self.height()
    #     p = 15
    #
    #     hd = 2
    #     tt = 6
    #     bt = 3
    #     ft = 2
    #
    #     self.mainMenuSec.resize(w*3/5, h/p)
    #     self.connectStatusSec.resize(w*2/5, h/p)
    #     self.mainToolBarSec.resize(w-2, h/p)
    #
    #     self.topTabUI.resize(w-2, h*tt/p)
    #     self.botTabUI.resize(w*2/3, h*bt/p)
    #     self.notifiSec.resize(w/3, h*bt/p)
    #
    #     self.footer.resize(w-2, h/p)
    #     self.statusBar.resize(w-2, h/p)

    def showEvent(self, event):
        for layout in [self.mainMenuSec, self.mainMenuSec, self.connectStatusSec, self.notifiSec]:
            if layout.isHidden():
                self.signals.emit('showLayout', layout.key, 'show')

    def keyPressEvent(self, event):
        print('aa: {0}'.format(event.key()))

        if event.key() == Qt.CTRL + Qt.Key_Backspace:
            print(event.key())

    @property
    def mode(self):
        return self.connectStatus.mode

# -------------------------------------------------------------------------------------------------------------