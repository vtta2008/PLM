#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: {[$]}.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import json, os, sys
from functools import partial

# PyQt5
from PyQt5.QtCore           import pyqtSlot
from PyQt5.QtWidgets        import QApplication

# PLM
from appData                import (__plmWiki__, __envKey__, CONFIG_DIR, APP_ICON_DIR, SETTING_DIR, ROOT_DIR, SiPoMin,
                                    CONFIG_OFFICE, CONFIG_DEV, CONFIG_TOOLS)
from ui.uikits.Action       import Action
from ui.uikits.MainWindow   import MainWindow
from utils                  import TimeLog

# -------------------------------------------------------------------------------------------------------------
""" Menu bar Layout """

class SubMenuBar(MainWindow):

    key = 'SubMenuBar'

    with open(os.path.join(os.getenv(__envKey__), 'appData/.config', 'main.cfg'), 'r') as f:
        appInfo = json.load(f)

    def __init__(self, parent=None):
        super(SubMenuBar, self).__init__(parent)

        self.parent = parent
        self.url = __plmWiki__
        self.buildMenu()

        # self.applySetting()

    def buildMenu(self):

        self.mainMenu = self.menuBar()

        self.organisationMenu = self.mainMenu.addMenu("&Organisation")
        self.organisationMenu.addAction(Action({'icon': 'NewOrganisation', 'txt': 'New', 'trg': partial(self.signals.showLayout.emit, 'NewOrganisation', 'show')}, self))
        self.organisationMenu.addAction(Action({'icon': 'EditOrganisation', 'txt': 'Edit', 'trg': partial(self.signals.showLayout.emit, 'EditOrganisation', 'show')}, self))
        self.organisationMenu.addAction(Action({'icon': 'SetTeam', 'txt': 'Set', 'trg': partial(self.signals.showLayout.emit, 'SetTeam', 'show')}, self))
        self.organisationMenu.addAction(Action({'icon': 'OrganisationManager', 'txt': 'Organisation Manager', 'trg': partial(self.signals.showLayout, 'OrganisationManager', 'show')}, self))

        self.teamMenu = self.mainMenu.addMenu('&Team')
        self.teamMenu.addAction(Action({'icon': 'NewTeam', 'txt': 'New', 'trg': partial(self.signals.showLayout.emit, 'NewTeam', 'show')}, self))
        self.teamMenu.addAction(Action({'icon': 'EditTeam', 'txt': 'Edit', 'trg': partial(self.signals.showLayout.emit, 'EditTeam', 'show')}, self))
        self.teamMenu.addAction(Action({'icon': 'SetTeam', 'txt': 'Set', 'trg': partial(self.signals.showLayout.emit, 'SetTeam', 'show')}, self))
        self.teamMenu.addAction(Action({'icon': 'TeamManager', 'txt': 'Team Manager', 'trg': partial(self.signals.showLayout, 'TeamManager', 'show')}, self))

        self.projectMenu = self.mainMenu.addMenu('&Project')
        self.projectMenu.addAction(Action({'icon': 'NewProject', 'txt': 'New', 'trg': partial(self.signals.showLayout.emit, 'NewProject', 'show')}, self))
        self.projectMenu.addAction(Action({'icon': 'EditProject', 'txt': 'Edit', 'trg': partial(self.signals.showLayout.emit, 'EditProject', 'show')}, self))
        self.projectMenu.addAction(Action({'icon': 'SetProject', 'txt': 'Set', 'trg': partial(self.signals.showLayout.emit, 'SetProject', 'show')}, self))
        self.projectMenu.addAction(Action({'icon': 'ProjectManager', 'txt': 'Project Manager', 'trg': partial(self.signals.showLayout.emit, 'ProjectManager', 'show')}, self))


        self.gotoMenu = self.menuBar().addMenu('Go to')
        self.gotoMenu.addAction(Action({'icon': 'ConfigFolder', 'txt': 'Config folder', 'trg':partial(self.signals.executing.emit, CONFIG_DIR)}, self))
        self.gotoMenu.addAction(Action({'icon': 'IconFolder', 'txt': 'Icon folder', 'trg': partial(self.signals.executing.emit, APP_ICON_DIR)}, self))
        self.gotoMenu.addAction(Action({'icon': 'SettingFolder', 'txt': 'Setting folder', 'trg': partial(self.signals.executing.emit, SETTING_DIR)}, self))
        self.gotoMenu.addAction(Action({'icon': 'AppFolder', 'txt': 'Application folder', 'trg': partial(self.signals.executing.emit, ROOT_DIR)}, self))

        self.officeMenu = self.menuBar().addMenu("&Office")

        officeKeys = ['TextEditor', 'NoteReminder']

        for key in officeKeys:
            if key in self.appInfo:
                self.officeMenu.addAction(Action({'icon': key,
                                                  'txt': key,
                                                  'trg': partial(self.signals.showLayout.emit, key, 'show')}, self))
        for key in CONFIG_OFFICE:
            if key in self.appInfo:
                self.officeMenu.addAction(Action({'icon': key,
                                                  'txt': key,
                                                  'trg': partial(self.signals.executing.emit, key)}, self))

        self.toolMenu = self.menuBar().addMenu("&Tools")

        for key in CONFIG_TOOLS:
            if key in self.appInfo:
                self.toolMenu.addAction(Action({'icon': key,
                                                'txt': key,
                                                'trg': partial(self.signals.showLayout.emit, key, 'show')}, self))

        self.toolMenu.addSeparator()

        self.toolMenu.addAction(Action({'icon': "CleanPyc", 'txt': 'Remove .pyc files', 'trg':partial(self.signals.executing.emit, 'CleanPyc')}, self))
        self.toolMenu.addAction(Action({'icon': "ReConfig", 'txt': 'Re-configure', 'trg':partial(self.signals.executing.emit, 'ReConfig')}, self))
        self.toolMenu.addAction(Action({'icon': "Debug", 'txt': 'Run PLM Debugger', 'trg': partial(self.signals.executing.emit, 'Debug')}, self))

        self.devMenu = self.menuBar().addMenu("&Dev")

        for key in CONFIG_DEV:
            if key in self.appInfo:
                if key in self.appInfo:
                    print(self.appInfo[key])
                    self.devMenu.addAction(Action({'icon': key,
                                                   'txt': key,
                                                   'trg': partial(self.signals.executing.emit, self.appInfo[key][2])}, self))

    def on_exit_action_triggered(self):
        TimeLog("Log out")
        QApplication.instance().quit()

    @pyqtSlot(bool)
    def show_hide_subMenuBar(self, param):
        self.setVisible(param)

    def applySetting(self):
        self.setMaximumHeight(20)
        self.setSizePolicy(SiPoMin, SiPoMin)
        self.setContentsMargins(5, 5, 5, 5)

def main():
    app = QApplication(sys.argv)
    subMenu = SubMenuBar()
    subMenu.show()
    app.exec_()


if __name__=='__main__':
    main()