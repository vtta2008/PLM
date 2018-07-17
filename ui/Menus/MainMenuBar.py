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
        self.appMenu.addAction(Action({'icon': 'Exit', 'txt': self.appInfo['Exit'][0], 'trg': partial(self.showLayout.emit, 'app', 'exit')}, self))

        self.settingMenu = self.mainMenu.addMenu('Settings')
        self.settingMenu.addAction(Action({'icon': 'Settings', 'txt':"&Settings", 'trg': partial(self.showLayout.emit, 'settingUI', 'show')}, self))
        self.settingMenu.addAction(Action({'icon': 'Configurations', 'txt': '&Config', 'trg': partial(self.showLayout.emit, 'config', 'show')}, self))
        self.settingMenu.addAction(Action({'icon': 'Preferences', 'txt': '&Preferences', 'trg': partial(self.showLayout.emit, 'preferences', 'show')}, self))

        self.mainMenu.addMenu("&Pipeline")

        self.mainMenu.addMenu("&Lib")

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(Action({'icon': 'PLM wiki', 'txt': self.appInfo['PLM wiki'][0], 'trg': partial(self.openUrl.emit, 'vnexpress.net')}, self))
        self.helpMenu.addAction(Action({'icon': 'About', 'txt': self.appInfo['About'][0], 'trg':partial(self.showLayout.emit, 'about', 'show')}, self))
        self.helpMenu.addAction(Action({'icon': 'Credit', 'txt': self.appInfo['Credit'][0], 'trg':partial(self.showLayout.emit, 'credit', 'show')}, self))

        self.helpMenu.addSeparator()

        self.helpMenu.addAction(Action({'icon': 'CodeConduct', 'txt': self.appInfo['CodeConduct'][0], 'trg': partial(self.showLayout.emit, 'codeConduct', 'show')}, self))
        self.helpMenu.addAction(Action({'icon': 'Contributing', 'txt': self.appInfo['Contributing'][0], 'trg': partial(self.showLayout.emit, 'contributing', 'show')}, self))
        self.helpMenu.addAction(Action({'icon': 'Reference', 'txt': self.appInfo['Reference'][0], 'trg': partial(self.showLayout.emit, 'reference', 'show')}, self))

        self.helpMenu.addSeparator()

        self.helpMenu.addAction(Action({'txt': 'Licence', 'trg': partial(self.showLayout.emit, 'licenceMIT', 'show')}, self))
        self.helpMenu.addAction(Action({'txt': 'Version', 'trg': partial(self.showLayout.emit, 'version', 'show')}, self))


        self.feedback = self.mainMenu.addMenu("&Feedback")
        self.feedback.addMenu("Feedback ticket")
        self.feedback.addMenu("Contact us")

    @pyqtSlot(bool)
    def show_layout(self, param):
        self.specs.showState.emit(True)
        self.setVisible(param)

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