# -*- coding: utf-8 -*-
"""

Script Name: MainMenu.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys

# PyQt5
from PyQt5.QtWidgets                import QApplication

# Plm
from appData                        import (__plmWiki__, mainConfig)
from ui.uikits.MenuBar              import MenuBar
from utils                          import data_handler

class MainMenuBar(MenuBar):

    key                     = 'MainMenuBar'
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

        for menu in [self.appMenu, self.goMenu, self.officeMenu, self.toolMenu, self.devMenu, self.libMenu,
                     self.helpMenu, self.organisationMenu, self.teamMenu, self.projectMenu]:
            parent = menu.parentWidget()
            menu.key = '{0}_{1}'.format(parent.key, menu.title())
            menu._name = menu.key
            self.menus.add(menu.title(), menu)

    def build_helpMenu(self):
        menu = self.addMenu("&Help")
        actions = self.actionManger.helpMenuActions(self.parent)
        self.add_actions(menu, actions[0:2])
        menu.addSeparator()
        self.add_actions(menu, actions[2:5])
        menu.addSeparator()
        self.add_actions(menu, actions[5:7])
        menu.addSeparator()
        self.add_actions(menu, actions[7:])
        return menu

    def build_livMenu(self):
        menu = self.addMenu("&Lib")
        actions = self.actionManger.libMenuActions(self.parent)
        self.add_actions(menu, actions)
        return menu

    def build_devMenu(self):
        menu = self.addMenu("&Dev")
        actions = self.actionManger.devMenuActions(self.parent)
        self.add_actions(menu, actions)
        return menu

    def build_toolMenu(self):
        menu = self.addMenu("&Tools")
        actions = self.actionManger.toolsMenuActions(self.parent)
        self.add_actions(menu, actions[0:7])
        menu.addSeparator()
        self.add_actions(menu, actions[7:])
        return menu

    def build_officceMenu(self):
        menu = self.addMenu("&Office")
        action = self.actionManger.officeMenuActions(self.parent)
        self.add_actions(menu, action)
        return menu

    def build_goMenu(self):
        menu = self.addMenu('&Go')
        actions = self.actionManger.goMenuActions(self.parent)
        self.add_actions(menu, actions)
        return menu

    def build_appMenu(self):
        menu = self.addMenu("&App")
        actions = self.actionManger.appMenuActions(self.parent)
        self.add_actions(menu, actions[0:3])

        menu.addSeparator()
        self.organisationMenu = menu.addMenu("&Organisation")
        orgActions = self.actionManger.orgMenuActions(self.parent)
        self.add_actions(self.organisationMenu, orgActions)

        self.teamMenu = menu.addMenu('&Team')
        teamActions = self.actionManger.teamMenuActions(self.parent)
        self.add_actions(self.teamMenu, teamActions)

        self.projectMenu = menu.addMenu('&Project')
        prjActions = self.actionManger.projectMenuActions(self.parent)
        self.add_actions(self.projectMenu, prjActions)

        menu.addSeparator()
        self.add_actions(menu, actions[3:])
        return menu

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