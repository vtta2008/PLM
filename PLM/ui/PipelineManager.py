# -*- coding: utf-8 -*-
"""
Script Name: PipelineTool.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This is main UI of PipelineTool.
"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PLM
from PLM.configs                        import __homepage__, __appname__, dockT, dockB
from PLM.api.damg                       import DAMGDICT
from PLM.api.Widgets                    import MainWindow, Widget, GridLayout
from PLM.api.Gui                        import LogoIcon
from .components                        import (Footer, MainStatusBar, MenubarDock, ToolBarDock, NetworkStatusDock,
                                                BotTabDock, NotificationDock, MidTabDock)
from .models.ButtonManager              import ButtonManager
from .models.ActionManager              import ActionManager
from PLM.cores.ThreadManager            import ThreadManager

# -------------------------------------------------------------------------------------------------------------
""" Pipeline Tool main layout """

class PipelineManager(MainWindow):

    key                                 = 'PipelineManager'
    _name                               = __appname__
    toolBars                            = DAMGDICT()
    menus                               = DAMGDICT()
    _count                              = 0

    def __init__(self, parent=None):
        super(PipelineManager, self).__init__(parent)

        self.url                        = __homepage__
        self.setObjectName(self._name)
        self.setWindowTitle(__appname__)
        self.setWindowIcon(LogoIcon('PLM'))

        self.actionManager              = ActionManager(self.parent)
        self.buttonManager              = ButtonManager(self.parent)
        self.threadManager              = ThreadManager(self.parent)

        self.mainWidget                 = Widget()
        self.layout                     = GridLayout()
        self.mainWidget.setLayout(self.layout)
        self.setCentralWidget(self.mainWidget)

        self.buildUI()

    def buildUI(self):

        self.dockMenu                   = MenubarDock(self.parent)
        self.dockNetwork                = NetworkStatusDock(self.parent)
        self.dockToolBar                = ToolBarDock(self.parent)
        self.menus                      = self.dockMenu.menuBar.menus
        self.toolBars                   = self.dockToolBar.toolBar.toolBars
        self.mns                        = self.dockMenu.menuBar.mns
        self.tbs                        = self.dockToolBar.toolBar.tbs
        self.updating                   = self.dockNetwork.status.updating
        self.server                     = self.dockNetwork.status.server
        self.mode                       = self.dockNetwork.status.mode
        self.connectServer              = self.dockNetwork.status.connectServer
        self.connectInternet            = self.dockNetwork.status.connectInternet
        self.topDockArea                = MainWindow(self.parent)

        self.addDockWidget(dockT, self.dockMenu)
        self.addDockWidget(dockT, self.dockNetwork)
        self.topDockArea.addDockWidget(dockT, self.dockToolBar)

        self.midTabDock                 = MidTabDock(self.parent)
        self.midDockArea                = MainWindow(self.parent)
        self.midDockArea.addDockWidget(dockT, self.midTabDock)

        self.botTabDock                 = BotTabDock(self.parent)
        self.notificationDock           = NotificationDock(self.parent)
        self.botDockArea                = MainWindow(self.parent)
        self.botDockArea.addDockWidget(dockB, self.botTabDock)
        self.botDockArea.addDockWidget(dockB, self.notificationDock)

        self.footer                     = Footer(self.buttonManager, self.threadManager, self)
        self.statusBar                  = MainStatusBar(self)
        self.setStatusBar(self.statusBar)
        self.layouts                    = [self.footer, self.statusBar]

        self.layout.addWidget(self.topDockArea, 0, 0, 2, 9)
        self.layout.addWidget(self.midDockArea, 2, 0, 4, 9)
        self.layout.addWidget(self.botDockArea, 6, 0, 3, 9)

        self.layout.addWidget(self.footer, 9, 0, 1, 9)


    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, val):
        self._count = val



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/07/2018 - 11:31 AM
# © 2017 - 2018 DAMGTEAM. All rights reserved