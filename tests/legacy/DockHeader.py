# -*- coding: utf-8 -*-
"""

Script Name: DockHeader.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """



from PLM.cores                          import ThreadManager
from PLM.ui.base                        import BaseDock
from PLM.ui.models                      import ActionManager, ButtonManager
from PLM.ui.components.MainMenuBar import MainMenuBar
from PLM.ui.components.MainToolBar import MainToolBar
from PLM.ui.components.ConnectStatus import ConnectStatus
from PLM.ui.components.BotTab import BotTab
from PLM.ui.components.MidTab import MidTab
from tests.legacy.Notification import Notification



class MidTabDock(BaseDock):

    key                                 = 'MidTabDock'
    _name                               = 'MidTabDock'

    def __init__(self, parent=None):
        super(MidTabDock, self).__init__(parent)

        self.buttonManager              = ButtonManager(self.parent)
        self.tabs                       = MidTab(self.buttonManager, self)
        self.setWidget(self.tabs)


class MenubarDock(BaseDock):

    key                                 = 'MainMenuDock'
    _name                               = 'Main Menu Dock'

    def __init__(self, parent=None):
        super(MenubarDock, self).__init__(parent)

        self.actionManager              = ActionManager(self.parent)
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
        self.actionManager              = ActionManager(self.parent)
        self.toolBar                    = MainToolBar(self.actionManager, self.parent)
        self.setWidget(self.toolBar)


class BotTabDock(BaseDock):

    key                                 = 'BotTabDock'
    _name                               = 'Bot Tab Dock'

    def __init__(self, parent=None):
        super(BotTabDock, self).__init__(parent)

        self.tabs                     = BotTab(self)
        self.setWidget(self.tabs)


class NotificationDock(BaseDock):

    key                                 = 'NotificationDock'
    _name                               = 'Notification Dock'

    def __init__(self, parent=None):
        super(NotificationDock, self).__init__(parent)

        self.threadManager              = ThreadManager()
        self.notify                     = Notification(self.threadManager, self.parent)
        self.setWidget(self.notify)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/17/2020 - 3:32 AM
# © 2017 - 2019 DAMGteam. All rights reserved