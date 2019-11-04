# -*- coding: utf-8 -*-
"""

Script Name: MainMenu.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys, os
from functools                      import partial
from damg import DAMGLIST

# PyQt5
from PyQt5.QtCore                   import pyqtSlot
from PyQt5.QtWidgets                import QApplication

# Plm
from appData                        import (__plmWiki__, mainConfig)

from ui.uikits.MenuBar              import MenuBar
from utils                          import data_handler

class MainMenuBar(MenuBar):

    key                     = 'TestMainMenuBar'
    mainMenus               = ['&App', '&Go', '&Office', '&Tools', '&Dev', '&Lib', '&Help']
    appMenus                = ['&Organisation', '&Team', '&Project']
    menus                   = DAMGLIST()

    appInfo = data_handler(filePath=mainConfig)

    def __init__(self, actionManager, parent=None):
        super(MainMenuBar, self).__init__(parent)

        self._parent = parent
        self.actionManger = actionManager
        self.url = __plmWiki__
        self.buildMenu()

    def buildMenu(self):

        self.appMenu = self.build_appMenu()
        self.goMenu = self.build_goMenu()
        self.officeMenu = self.build_officceMenu()
        self.toolMenu = self.build_toolMenu()
        self.devMenu = self.build_devMenu()
        self.libMenu = self.build_livMenu()
        self.helpMenu = self.build_helpMenu()

        for menu in [self.appMenu, self.goMenu, self.officeMenu, self.toolMenu, self.devMenu, self.libMenu, self.helpMenu]:
            self.menus.append(menu)

    def build_helpMenu(self):
        helpMenu = self.addMenu("&Help")
        helpActions = self.actionManger.helpMenuActions(self)
        self.add_actions(helpMenu, helpActions[0:2])
        helpMenu.addSeparator()
        self.add_actions(helpMenu, helpActions[2:5])
        helpMenu.addSeparator()
        self.add_actions(helpMenu, helpActions[5:7])
        helpMenu.addSeparator()
        self.add_actions(helpMenu, helpActions[7:])
        return helpMenu

    def build_livMenu(self):
        libMenu = self.addMenu("&Lib")
        libActions = self.actionManger.libMenuActions(self)
        self.add_actions(libMenu, libActions)
        return libMenu

    def build_devMenu(self):
        devMenu = self.addMenu("&Dev")
        devActions = self.actionManger.devMenuActions(self)
        self.add_actions(devMenu, devActions)
        return devMenu

    def build_toolMenu(self):
        toolMenu = self.addMenu("&Tools")
        toolActions = self.actionManger.toolsMenuActions(self)
        self.add_actions(toolMenu, toolActions[0:-3])
        toolMenu.addSeparator()
        self.add_actions(toolMenu, toolActions[-3:0])
        return toolMenu

    def build_officceMenu(self):
        officeMenu = self.addMenu("&Office")
        officeActions = self.actionManger.officeMenuActions(self)
        self.add_actions(officeMenu, officeActions)
        return officeMenu

    def build_goMenu(self):
        gotoMenu = self.addMenu('&Go')
        goActions = self.actionManger.goMenuActions(self)
        self.add_actions(gotoMenu, goActions)
        return gotoMenu

    def build_appMenu(self):
        appMenu = self.addMenu("&App")
        appActions = self.actionManger.appMenuActions(self)
        self.add_actions(appMenu, appActions[0:3])

        appMenu.addSeparator()
        self.organisationMenu = appMenu.addMenu("&Organisation")
        orgActions = self.actionManger.orgMenuActions(self)
        self.add_actions(self.organisationMenu, orgActions)

        self.teamMenu = appMenu.addMenu('&Team')
        teamActions = self.actionManger.teamMenuActions(self)
        self.add_actions(self.teamMenu, teamActions)

        self.projectMenu = appMenu.addMenu('&Project')
        prjActions = self.actionManger.projectMenuActions(self)
        self.add_actions(self.projectMenu, prjActions)

        appMenu.addSeparator()
        self.add_actions(appMenu, appActions[3:])
        return appMenu

    def add_actions(self, menu, actions):
        for action in actions:
            menu.addAction(action)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    from ui.uikits.GroupBox import GroupBox
    subMenu = MainMenuBar()
    layout = GroupBox("Main Menu", subMenu, "qmainLayout")
    layout.show()
    app.exec_()
# -------------------------------------------------------------------------------------------------------------
# Created by panda on 11/07/2018 - 12:59 AM
# © 2017 - 2018 DAMGteam. All rights reserved