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
from PyQt5.QtCore           import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets        import QMainWindow, QApplication

from cores.Loggers          import Loggers
# PLM
from appData                import __plmWiki__, __envKey__
from appData                import CONFIG_DIR, APP_ICON_DIR, SETTING_DIR, ROOT_DIR, SiPoMin
from cores.base             import DAMG
from ui.UiSignals           import UiSignals
from ui.uikits.Action       import Action
from utils.localSQL         import TimeLog
from utils.utils            import get_layout_size

# -------------------------------------------------------------------------------------------------------------
""" Menu bar Layout """

class SubMenuBar(QMainWindow):

    key = 'subMenu'

    def __init__(self, parent=None):
        super(SubMenuBar, self).__init__(parent)
        self.logger = Loggers(__file__)
        self.signals = UiSignals(self)
        
        with open(os.path.join(os.getenv(__envKey__), 'appData/.config', 'main.cfg'), 'r') as f:
            self.appInfo = json.load(f)
        
        self.url = __plmWiki__
        self.buildMenu()
        self.setMaximumHeight(20)

    def buildMenu(self):

        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(Action({'icon': 'NewOrganisation', 'txt': 'Register new Organisation', 'trg': partial(self.signals.regisLayout.emit, 'newOrganisation', 'show')}, self))
        self.fileMenu.addAction(Action({'icon': 'YourOrganisation', 'txt': 'Your Organisation', 'trg': partial(self.signals.regisLayout.emit, 'YourOrganisation', 'show')}, self))
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(Action({'icon': 'NewTeam', 'txt': 'Create new Team', 'trg': partial(self.signals.regisLayout.emit, 'newTeam', 'show')}, self))
        self.fileMenu.addAction(Action({'icon': 'EditTeam', 'txt': 'Edit your Team', 'trg': partial(self.signals.regisLayout.emit, 'EditTeam', 'show')}, self))

        self.fileMenu.addSeparator()
        self.fileMenu.addAction(Action({'icon': 'NewProject', 'txt': 'Create new project', 'trg': partial(self.signals.regisLayout.emit, 'newProject', 'show')}, self))
        self.fileMenu.addAction(Action({'icon': 'RecentProject', 'txt': 'Open recent project', 'trg': partial(self.signals.regisLayout.emit, 'RecentProject', 'show')}, self))
        self.fileMenu.addAction(Action({'icon': 'ProjectManager', 'txt': 'Project Manager', 'trg': partial(self.signals.regisLayout.emit, 'ProjectManager', 'show')}, self))
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

        self.toolMenu.addAction(Action({'icon': "Calculator", 'txt': 'Calculator', 'trg': partial(self.signals.regisLayout.emit, 'Calculator', 'show')}, self))
        self.toolMenu.addAction(Action({'icon': "Calendar", 'txt': 'Calendar', 'trg': partial(self.signals.regisLayout.emit, 'Calendar', 'show')},self))
        self.toolMenu.addAction(Action({'icon': "EnglishDictionary", 'txt': 'EnglishDictionary', 'trg': partial(self.signals.regisLayout.emit, 'EnglishDictionary', 'show')},self))
        self.toolMenu.addAction(Action({'icon': "FindFiles", 'txt': 'FindFiles', 'trg': partial(self.signals.regisLayout.emit, 'FindFiles', 'show')}, self))
        self.toolMenu.addAction(Action({'icon': "ImageViewer", 'txt': 'ImageViewer', 'trg': partial(self.signals.regisLayout.emit, 'ImageViewer', 'show')}, self))
        self.toolMenu.addAction(Action({'icon': "NodeReminder", 'txt': 'NodeReminder', 'trg': partial(self.signals.regisLayout.emit, 'NodeReminder', 'show')}, self))
        self.toolMenu.addAction(Action({'icon': "Screenshot", 'txt': 'Screenshot', 'trg': partial(self.signals.regisLayout.emit, 'Screenshot', 'show')}, self))
        self.toolMenu.addAction(Action({'icon': "TextEditor", 'txt': 'Text Editor', 'trg': partial(self.signals.regisLayout.emit, 'TextEditor', 'show')}, self))

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

    def resizeEvent(self, event):
        sizeW, sizeH = get_layout_size(self)
        self.signals.setSetting.emit('width', str(sizeW), self.objectName())
        self.signals.setSetting.emit('height', str(sizeH), self.objectName())

    def applySetting(self):
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