# -*- coding: utf-8 -*-
"""

Script Name: MainMenu.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python

# Plm
from appData                        import __plmWiki__, plmInfo
from devkit.Widgets                 import GroupVBox, MenuBar
from utils                          import is_string

class MainMenuBar(GroupVBox):

    key                             = 'MainMenuBar'
    plmInfo                         = plmInfo

    def __init__(self, actionManager, parent=None):
        super(MainMenuBar, self).__init__(parent)

        self._parent                = parent
        self.actionManger           = actionManager
        self.url                    = __plmWiki__
        self.setTitle('Main Menu')
        self.menubar                = MenuBar(self)
        self.menus                  = self.menubar.menus
        self.layout.addWidget(self.menubar)
        self.buildMenu()

    def buildMenu(self):

        self.appMenu                = self.build_appMenu()
        self.goMenu                 = self.build_goMenu()
        self.editMenu               = self.build_editMenu()
        self.viewMenu               = self.build_viewMenu()
        self.officeMenu             = self.build_officceMenu()
        self.toolsMenu              = self.build_toolMenu()
        self.devMenu                = self.build_devMenu()
        self.libMenu                = self.build_libMenu()
        self.helpMenu               = self.build_helpMenu()

        for menu in [self.appMenu, self.goMenu, self.editMenu, self.viewMenu, self.officeMenu, self.toolsMenu,
                     self.devMenu, self.libMenu, self.helpMenu]:
            menu.key                = '{0}_Menu_{1}'.format(self.key, menu.title())
            menu._name              = '{0} Menu {1}'.format(self.key, menu.title())

            self.menus.add(menu.key, menu)

        self.mns                    = [mn for mn in self.menus.values()]

    def build_editMenu(self):
        menu                        = self.addMenu('&Edit')
        editActions                 = self.actionManger.editMenuActions(self.parent)
        self.add_actions(menu, editActions)
        return menu

    def build_viewMenu(self):
        menu                        = self.addMenu('&View')

        self.stylesheetMenu         = menu.addMenu('&Stylesheet')
        stylesheetActions           = self.actionManger.stylesheetMenuActions(self.parent)
        self.add_actions(self.stylesheetMenu, stylesheetActions)

        viewActions                 = self.actionManger.viewMenuActions(self.parent)
        self.add_actions(menu, viewActions)
        return menu

    def build_helpMenu(self):
        menu                        = self.addMenu("&Help")
        actions                     = self.actionManger.helpMenuActions(self.parent)
        self.add_actions(menu, actions[0:2])
        menu.addSeparator()
        self.add_actions(menu, actions[2:5])
        menu.addSeparator()
        self.add_actions(menu, actions[5:7])
        menu.addSeparator()
        self.add_actions(menu, actions[7:])
        return menu

    def build_libMenu(self):
        menu                        = self.addMenu("&Lib")
        actions                     = self.actionManger.libMenuActions(self.parent)
        self.add_actions(menu, actions)
        return menu

    def build_devMenu(self):
        menu                        = self.addMenu("&Dev")
        actions                     = self.actionManger.devMenuActions(self.parent)
        self.add_actions(menu, actions)
        return menu

    def build_toolMenu(self):
        menu                        = self.addMenu("&Tools")
        actions                     = self.actionManger.toolsMenuActions(self.parent)
        self.add_actions(menu, actions[0:7])
        menu.addSeparator()
        self.add_actions(menu, actions[7:])
        return menu

    def build_officceMenu(self):
        menu                        = self.addMenu("&Office")
        action                      = self.actionManger.officeMenuActions(self.parent)
        self.add_actions(menu, action)
        return menu

    def build_goMenu(self):
        menu                        = self.addMenu('&Go To')
        actions                     = self.actionManger.goMenuActions(self.parent)
        self.add_actions(menu, actions)
        return menu

    def build_appMenu(self):
        menu                        = self.addMenu("&App")
        actions                     = self.actionManger.appMenuActions(self.parent)
        self.add_actions(menu, actions[0:3])
        menu.addSeparator()
        self.add_actions(menu, actions[3:7])
        menu.addSeparator()
        self.add_actions(menu, actions[7:])
        return menu

    def addMenu(self, menu):
        if is_string(menu):
            return self.menubar.addMenu(menu)

    def add_actions(self, menu, actions):
        for action in actions:
            menu.addAction(action)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 11/07/2018 - 12:59 AM
# © 2017 - 2018 DAMGteam. All rights reserved