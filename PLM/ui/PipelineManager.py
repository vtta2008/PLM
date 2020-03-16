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
from PLM.configs                        import __homepage__, __appname__, dockT, dockR, dockL, dockB, dockAll, SiPoMin, SiPoPre, SiPoExp, SiPoMax, SiPoIgn, FRAMELESS, CUSTOMIZE, CLOSEBTN, MINIMIZEBTN
from PLM.commons                        import DAMGDICT
from PLM.commons.Widgets                import MainWindow, Widget, GridLayout, DockWidget, Label, Button
from PLM.commons.Gui                    import LogoIcon
from .components                        import ConnectStatus, Footer, MainStatusBar, Notification, MainMenuBar, MainToolBar
from .layouts                           import TopTab, BotTab
from .models.ButtonManager              import ButtonManager
from .models.ActionManager              import ActionManager
from .models.ThreadManager              import ThreadManager

# -------------------------------------------------------------------------------------------------------------
""" Pipeline Tool main layout """


class BaseDock(DockWidget):

    key                                 = 'BaseDock'
    _name                               = 'BaseDock'

    def __init__(self, parent=None):
        super(BaseDock, self).__init__(parent)

        self.setWindowFlags(FRAMELESS)
        self.actionManager              = ActionManager(self.parent)


    def close(self):
        self.hide()

    def closeEvent(self, event):
        self.hide()
        event.ignore()


class MainMenuDock(BaseDock):

    key                                 = 'MainMenuDock'
    _name                               = 'Main Menu Dock'

    def __init__(self, parent=None):
        super(MainMenuDock, self).__init__(parent)

        self.menuBar                    = MainMenuBar(self.actionManager, self.parent)
        self.setWidget(self.menuBar)


class NetworkStatusDock(BaseDock):

    key                                 = 'NetworkStatusDock'
    _name                               = 'Connect Status Dock'

    def __init__(self, parent=None):
        super(NetworkStatusDock, self).__init__(parent)

        self.status                     = ConnectStatus(self.parent)
        self.setWidget(self.status)


class ToolBarDock(BaseDock):

    key                                 = 'ToolBarDock'
    _name                               = 'ToolBar Dock'

    def __init__(self, parent=None):
        super(ToolBarDock, self).__init__(parent)

        self.toolBar                    = MainToolBar(self.actionManager, self.parent)
        self.setWidget(self.toolBar)

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

        self.dockMenu                   = MainMenuDock(self.parent)
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

        self.addDockWidget(dockT, self.dockMenu)
        self.addDockWidget(dockT, self.dockNetwork)
        self.addDockWidget(dockT, self.dockToolBar)

        self.topTabUI                   = TopTab(self.buttonManager, self)
        self.botTabUI                   = BotTab(self)
        self.notification               = Notification(self.threadManager, self)

        self.footer                     = Footer(self.buttonManager, self.threadManager, self)
        self.statusBar                  = MainStatusBar(self)

        self.layouts = [self.notification, self.topTabUI, self.botTabUI, self.footer, self.statusBar]

        self.layout.addWidget(self.topTabUI, 0, 0, 4, 9)
        self.layout.addWidget(self.botTabUI, 4, 0, 3, 6)
        self.layout.addWidget(self.notification, 4, 6, 3, 3)

        self.layout.addWidget(self.footer, 7, 0, 1, 9)
        self.setStatusBar(self.statusBar)

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, val):
        self._count = val

# -------------------------------------------------------------------------------------------------------------