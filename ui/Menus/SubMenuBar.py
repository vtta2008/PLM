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
import sys, os, json
from functools import partial

# PyQt5
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication

# Plt
from utilities.localSQL import TimeLog
from ui.uikits.Action import Action
from utilities.utils import get_layout_size

from appData import __plmWiki__, __envKey__, CONFIG_DIR, APP_ICON_DIR, SETTING_DIR, ROOT_DIR, SiPoMin
from core.Loggers import SetLogger

# -------------------------------------------------------------------------------------------------------------
""" Menu bar Layout """

class SubMenuBar(QMainWindow):

    key = 'subMenu'
    showLayout = pyqtSignal(str, str)
    executing = pyqtSignal(str)
    addLayout = pyqtSignal(object)
    setSetting = pyqtSignal(str, str, str)
    openUrl = pyqtSignal(str)

    def __init__(self, parent=None):
        super(SubMenuBar, self).__init__(parent)
        self.logger = SetLogger(self)
        with open(os.path.join(os.getenv(__envKey__), 'cfg', 'main.cfg'), 'r') as f:
            self.appInfo = json.load(f)
        self.url = __plmWiki__
        self.buildMenu()
        self.setMaximumHeight(20)

    def buildMenu(self):

        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addMenu("New Organisation")
        self.fileMenu.addMenu("New group/team")
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(Action({'icon': 'NewProject', 'txt': 'Create new project', 'trg': partial(self.showLayout.emit, 'newProj', 'show')}, self))
        self.fileMenu.addSeparator()

        self.gotoMenu = self.menuBar().addMenu('Go to')
        self.gotoMenu.addAction(Action({'icon': 'ConfigFolder', 'txt': 'Config folder', 'trg':partial(self.executing.emit, CONFIG_DIR)}, self))
        self.gotoMenu.addAction(Action({'icon': 'IconFolder', 'txt': 'Icon folder', 'trg': partial(self.executing.emit, APP_ICON_DIR)}, self))
        self.gotoMenu.addAction(Action({'icon': 'SettingFolder', 'txt': 'Setting folder', 'trg': partial(self.executing.emit, SETTING_DIR)}, self))
        self.gotoMenu.addAction(Action({'icon': 'AppFolder', 'txt': 'Application folder', 'trg': partial(self.executing.emit, ROOT_DIR)}, self))

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addMenu('Copy')
        self.editMenu.addMenu('Copy')
        self.editMenu.addMenu('Cut')
        self.editMenu.addMenu('Paste')

        self.viewMenu = self.menuBar().addMenu("&View")

        self.toolMenu = self.menuBar().addMenu("&Tools")

        self.toolMenu.addSeparator()

        self.toolMenu.addAction(Action({'icon': "CleanPyc", 'txt': 'Remove .pyc files', 'trg':partial(self.executing.emit, 'Remove pyc')}, self))
        self.toolMenu.addAction(Action({'icon': "ReConfig", 'txt': 'Re-configure', 'trg':partial(self.executing.emit, 'Re-config local')}, self))
        self.windowMenu = self.menuBar().addMenu("&Window")

    def on_exit_action_triggered(self):
        TimeLog("Log out")
        QApplication.instance().quit()

    @pyqtSlot(bool)
    def show_hide_subMenuBar(self, param):
        self.setVisible(param)

    def resizeEvent(self, event):
        sizeW, sizeH = get_layout_size(self)
        self.setSetting.emit('width', str(sizeW), self.objectName())
        self.setSetting.emit('height', str(sizeH), self.objectName())

    def applySetting(self):
        self.setSizePolicy(SiPoMin, SiPoMin)
        self.setContentsMargins(5, 5, 5, 5)

def main():
    app = QApplication(sys.argv)
    subMenu = SubMenuBar()
    subMenu.show()
    app.exec_()


if __name__=='__main__':
    main()