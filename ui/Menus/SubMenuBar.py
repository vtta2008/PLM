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
import json
import os
import sys
from functools import partial

# PyQt5
from PyQt5.QtCore           import pyqtSlot
from PyQt5.QtWidgets        import QApplication

from cores.Loggers          import Loggers
# PLM
from appData                import __plmWiki__, __envKey__
from appData                import CONFIG_DIR, APP_ICON_DIR, SETTING_DIR, ROOT_DIR, SiPoMin
from ui.uikits.MainWindow   import MainWindow
from ui.uikits.Action       import Action
from utils.localSQL         import TimeLog

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

        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(Action({'icon': 'NewOrganisation', 'txt': 'Register new Organisation', 'trg': partial(self.signals.showLayout.emit, 'newOrganisation', 'show')}, self))
        self.fileMenu.addAction(Action({'icon': 'YourOrganisation', 'txt': 'Your Organisation', 'trg': partial(self.signals.showLayout.emit, 'YourOrganisation', 'show')}, self))
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(Action({'icon': 'NewTeam', 'txt': 'Create new Team', 'trg': partial(self.signals.showLayout.emit, 'newTeam', 'show')}, self))
        self.fileMenu.addAction(Action({'icon': 'EditTeam', 'txt': 'Edit your Team', 'trg': partial(self.signals.showLayout.emit, 'EditTeam', 'show')}, self))

        self.fileMenu.addSeparator()
        self.fileMenu.addAction(Action({'icon': 'NewProject', 'txt': 'Create new project', 'trg': partial(self.signals.showLayout.emit, 'newProject', 'show')}, self))
        self.fileMenu.addAction(Action({'icon': 'RecentProject', 'txt': 'Open recent project', 'trg': partial(self.signals.showLayout.emit, 'RecentProject', 'show')}, self))
        self.fileMenu.addAction(Action({'icon': 'ProjectManager', 'txt': 'Project Manager', 'trg': partial(self.signals.showLayout.emit, 'ProjectManager', 'show')}, self))
        self.fileMenu.addSeparator()

        self.gotoMenu = self.menuBar().addMenu('Go to')
        self.gotoMenu.addAction(Action({'icon': 'ConfigFolder', 'txt': 'Config folder', 'trg':partial(self.signals.executing.emit, CONFIG_DIR)}, self))
        self.gotoMenu.addAction(Action({'icon': 'IconFolder', 'txt': 'Icon folder', 'trg': partial(self.signals.executing.emit, APP_ICON_DIR)}, self))
        self.gotoMenu.addAction(Action({'icon': 'SettingFolder', 'txt': 'Setting folder', 'trg': partial(self.signals.executing.emit, SETTING_DIR)}, self))
        self.gotoMenu.addAction(Action({'icon': 'AppFolder', 'txt': 'Application folder', 'trg': partial(self.signals.executing.emit, ROOT_DIR)}, self))

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addMenu('Copy')
        self.editMenu.addMenu('Copy')
        self.editMenu.addMenu('Cut')
        self.editMenu.addMenu('Paste')

        self.viewMenu = self.menuBar().addMenu("&View")

        self.toolMenu = self.menuBar().addMenu("&Tools")

        self.toolMenu.addAction(Action({'icon': "Calculator", 'txt': 'Calculator', 'trg': partial(self.signals.showLayout.emit, 'Calculator', 'show')}, self))
        self.toolMenu.addAction(Action({'icon': "Calendar", 'txt': 'Calendar', 'trg': partial(self.signals.showLayout.emit, 'Calendar', 'show')},self))
        self.toolMenu.addAction(Action({'icon': "EnglishDictionary", 'txt': 'EnglishDictionary', 'trg': partial(self.signals.showLayout.emit, 'EnglishDictionary', 'show')},self))
        self.toolMenu.addAction(Action({'icon': "FindFiles", 'txt': 'FindFiles', 'trg': partial(self.signals.showLayout.emit, 'FindFiles', 'show')}, self))
        self.toolMenu.addAction(Action({'icon': "ImageViewer", 'txt': 'ImageViewer', 'trg': partial(self.signals.showLayout.emit, 'ImageViewer', 'show')}, self))
        self.toolMenu.addAction(Action({'icon': "NodeReminder", 'txt': 'NodeReminder', 'trg': partial(self.signals.showLayout.emit, 'NodeReminder', 'show')}, self))
        self.toolMenu.addAction(Action({'icon': "Screenshot", 'txt': 'Screenshot', 'trg': partial(self.signals.showLayout.emit, 'Screenshot', 'show')}, self))
        self.toolMenu.addAction(Action({'icon': "TextEditor", 'txt': 'Text Editor', 'trg': partial(self.signals.showLayout.emit, 'TextEditor', 'show')}, self))

        self.toolMenu.addSeparator()

        self.toolMenu.addAction(Action({'icon': "CleanPyc", 'txt': 'Remove .pyc files', 'trg':partial(self.signals.executing.emit, 'Remove pyc')}, self))
        self.toolMenu.addAction(Action({'icon': "Reconfig", 'txt': 'Re-configure', 'trg':partial(self.signals.executing.emit, 'Re-config local')}, self))
        self.toolMenu.addAction(Action({'icon': "Debug", 'txt': 'Run PLM Debugger', 'trg': self.run_debugger}, self))

        self.windowMenu = self.menuBar().addMenu("&Window")

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

    def run_debugger(self):
        from ui.Debugger import Debugger
        debugger = Debugger()
        debugger.show()
        return debugger

def main():
    app = QApplication(sys.argv)
    subMenu = SubMenuBar()
    subMenu.show()
    app.exec_()


if __name__=='__main__':
    main()