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

# PyQt5
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QSettings
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QInputDialog, QLineEdit

# Plm
from appData import APPINFO, __plmWiki__
from core.Loggers import SetLogger
from core.Specs import Specs
from utilities.pUtils import get_layout_dimention
from ui.lib.LayoutPreset import Action
from ui.Settings.SettingUI import SettingUI

class MainMenuBar(QMainWindow):

    key = 'mainMenu'
    setSetting = pyqtSignal(str, str, str)

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
        self.appMenu.addMenu("New freelancer project")
        self.appMenu.addMenu("New studio project")

        self.settingMenu = self.mainMenu.addMenu('Settings')
        self.settingMenu.addAction(Action({'txt':"&PLM Settings", 'trg': self.openSetting}, self))

        self.config = self.mainMenu.addMenu("&Config")
        self.config.addMenu("Configurations")
        self.config.addMenu("Preference")

        self.mainMenu.addMenu("&Pipeline")

        self.mainMenu.addMenu("&Lib")

        self.mainMenu.addMenu("&Docs")

        self.feedback = self.mainMenu.addMenu("&Feedback")

        self.feedback.addMenu("Use feedback tool")
        self.feedback.addMenu("Contact us")

    @pyqtSlot(bool)
    def show_layout(self, param):
        self.setVisible(param)

    def openSetting(self):
        from ui.Settings.AppSetting import AppSetting
        self.appSetting = AppSetting()
        self.appSetting.show()

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