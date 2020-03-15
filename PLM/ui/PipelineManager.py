# -*- coding: utf-8 -*-
"""
Script Name: PipelineTool.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This is main UI of PipelineTool.
"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
""" Import """

# PLM
from configs                            import __homepage__, dockB, __appname__
from PLM.commons.Widgets import MainWindow, Widget, GridLayout
from devkit.Gui                         import LogoIcon
from .Header                            import MainToolBar, MainMenuBar, ConnectStatus
from .Body                              import TopTab, BotTab, Notification
from PLM.ui.components.Footer import Footer, MainStatusBar


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
        self.setWindowIcon(LogoIcon('PLM'))

        self.actionManager              = actionManager
        self.buttonManager              = buttonManager
        self.threadManager              = threadManager

        self.mainWidget                 = Widget()
        self.layout                     = GridLayout()
        self.mainWidget.setLayout(self.layout)
        self.setCentralWidget(self.mainWidget)
        self.buildUI()

    def buildUI(self):

        self.mainMenuBar                = MainMenuBar(self.actionManager, self)
        self.mainToolBar                = MainToolBar(self.actionManager, self)
        self.connectStatus              = ConnectStatus(self)

        self.topTabUI                   = TopTab(self.buttonManager, self)
        self.botTabUI                   = BotTab(self)
        self.notification               = Notification(self.threadManager, self)

        self.footer                     = Footer(self.buttonManager, self.threadManager, self)
        self.statusBar                  = MainStatusBar(self)

        self.layouts =  [self.mainMenuBar, self.mainToolBar      , self.connectStatus    , self.notification,
                         self.topTabUI   , self.botTabUI         , self.footer           , self.statusBar, ]

        self.layout.addWidget(self.mainMenuBar, 0, 0, 1, 7)
        self.layout.addWidget(self.mainToolBar, 1, 0, 1, 9)
        self.layout.addWidget(self.connectStatus, 0, 7, 1, 2)

        self.layout.addWidget(self.topTabUI, 2, 0, 4, 9)
        self.layout.addWidget(self.botTabUI, 6, 0, 3, 6)
        self.layout.addWidget(self.notification, 6, 6, 3, 3)

        self.layout.addWidget(self.footer, 9, 0, 1, 9)
        self.setStatusBar(self.statusBar)

    def add_dockWidget(self, dock, pos=dockB):

        dock.signals.showLayout.connect(self.signals.showLayout)
        dock.signals.setSetting.connect(self.signals.setSetting)
        dock.signals.executing.connect(self.signals.executing)
        dock.signals.regisLayout.connect(self.signals.regisLayout)
        dock.signals.openBrowser.connect(self.signals.openBrowser)

        self.addDockWidget(pos, dock)

    @property
    def mode(self):
        return self.connectStatus.mode

# -------------------------------------------------------------------------------------------------------------