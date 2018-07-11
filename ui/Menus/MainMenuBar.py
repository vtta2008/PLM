# -*- coding: utf-8 -*-
"""

Script Name: MainMenu.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys
from functools import partial

# PyQt5
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication

# Plm
from appData import APPINFO, __plmWiki__
from core.Loggers import SetLogger
from core.Specs import Specs
from utilities.pUtils import get_layout_dimention
from ui.lib.LayoutPreset import Action
from ui.Settings.SettingUI import SettingUI

class MainMenuBar(QMainWindow):

    key = 'mainMenu'
    showLayout = pyqtSignal(str, str)
    executing = pyqtSignal(str)
    proceduring = pyqtSignal(str)
    addLayout = pyqtSignal(object)
    setSetting = pyqtSignal(str, str, str)
    openUrl = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MainMenuBar, self).__init__(parent)
        self.specs = Specs(self.key, self)
        self.logger = SetLogger(self)
        self.appInfo = APPINFO
        self.url = __plmWiki__
        self.buildMenu()
        self.setMaximumHeight(20)

    def buildMenu(self):
        self.mainMenu = self.menuBar()

        self.appMenu = self.mainMenu.addMenu("&App")
        self.appMenu.addMenu("New Organisation")
        self.appMenu.addMenu("New group/team")
        self.appMenu.addSeparator()
        self.appMenu.addMenu("New project")

        self.settingMenu = self.mainMenu.addMenu('Settings')
        self.settingMenu.addAction(Action({'txt':"&PLM Settings", 'trg': self.openSetting}, self))

        self.config = self.mainMenu.addMenu("&Config")
        self.config.addAction(Action({'icon': 'Configurations', 'txt': 'Config', 'trg': partial(self.showLayout.emit, 'config', 'show')}, self))
        self.config.addAction(Action({'icon': 'Preferences', 'txt': 'Preferences', 'trg': partial(self.showLayout.emit, 'preferences', 'show')}, self))

        self.mainMenu.addMenu("&Pipeline")

        self.mainMenu.addMenu("&Lib")

        self.docs = self.mainMenu.addMenu("&Docs")
        self.docs.addMenu('About')
        self.docs.addMenu('Code of conduct')
        self.docs.addMenu('Contributing')
        self.docs.addMenu('Copyright')
        self.docs.addMenu('Credit')
        self.docs.addMenu('Link')
        self.docs.addMenu('Reference')
        self.docs.addMenu('Version')

        self.feedback = self.mainMenu.addMenu("&Feedback")

        self.feedback.addMenu("User feedbac ticket")
        self.feedback.addMenu("Contact us")

    @pyqtSlot(bool)
    def show_layout(self, param):
        self.setVisible(param)

    def openSetting(self):
        self.appSetting = SettingUI()
        self.appSetting.show()

    def openConfig(self):
        from ui.Menus.config.Configuration import ServerConfig
        self.config = ServerConfig()
        self.config.show()

    def resizeEvent(self, event):
        sizeW, sizeH = get_layout_dimention(self)
        self.setSetting.emit('width', str(sizeW), self.objectName())
        self.setSetting.emit('height', str(sizeH), self.objectName())

def main():
    app = QApplication(sys.argv)
    subMenu = MainMenuBar()
    subMenu.show()
    app.exec_()

if __name__ == '__main__':
    main()
# -------------------------------------------------------------------------------------------------------------
# Created by panda on 11/07/2018 - 12:59 AM
# © 2017 - 2018 DAMGteam. All rights reserved