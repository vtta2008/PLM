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
import sys, os
from functools import partial

# PyQt5
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QAction, QSizePolicy, QApplication

# Plt
from utilities import localSQL as usql
from ui import uirc as rc
from ui import(Configuration, About, Credit)

from appData import APPINFO, __plmWiki__
from appData.Loggers import SetLogger
logger = SetLogger()
# -------------------------------------------------------------------------------------------------------------
""" Menu bar Layout """

class SubMenuBar(QMainWindow):

    subMenuSig = pyqtSignal(str)

    def __init__(self, parent=None):

        super(SubMenuBar, self).__init__(parent)

        self.appInfo = APPINFO
        self.url = __plmWiki__
        from core.SettingManager import Settings
        self.settings = Settings(self)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.buildMenu()

    def buildMenu(self):

        prefAct = QAction(rc.AppIcon(32, 'Preferences'), 'Preferences', self)
        prefAct.setStatusTip('Preferences')
        prefAct.triggered.connect(partial(self.subMenuSig.emit, 'Preferences'))

        aboutAct = QAction(rc.AppIcon(32, 'About'), self.appInfo['About'][0], self)
        aboutAct.setStatusTip(self.appInfo['About'][0])
        aboutAct.triggered.connect(partial(self.subMenuSig.emit, 'About'))

        creditAct = QAction(rc.AppIcon(32, 'Credit'), self.appInfo['Credit'][0], self)
        creditAct.setStatusTip(self.appInfo['Credit'][0])
        creditAct.triggered.connect(partial(self.subMenuSig.emit, 'Credit'))

        openConfigAct = QAction(rc.AppIcon(32, 'OpenConfig'), self.appInfo['OpenConfig'][0], self)
        openConfigAct.setStatusTip(self.appInfo['OpenConfig'][0])
        openConfigAct.triggered.connect(partial(self.subMenuSig.emit, 'Go to config folder'))

        exitAction = QAction(rc.AppIcon(32, 'Exit'), self.appInfo['Exit'][0], self)
        exitAction.setStatusTip(self.appInfo['Exit'][0])
        exitAction.triggered.connect(partial(self.subMenuSig.emit, 'Exit'))

        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(openConfigAct)
        self.fileMenu.addAction(prefAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(rc.ActionProcess("Exit", self))

        self.editMenu = self.menuBar().addMenu("&Edit")

        self.viewMenu = self.menuBar().addMenu("&View")

        self.toolMenu = self.menuBar().addMenu("&Tools")
        self.toolMenu.addSeparator()
        self.toolMenu.addAction(rc.ActionProcess("CleanPyc", self))
        self.toolMenu.addAction(rc.ActionProcess("ReConfig", self))

        self.windowMenu = self.menuBar().addMenu("&Window")

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(rc.ActionProcess("PLM wiki", self))
        self.helpMenu.addAction(aboutAct)
        self.helpMenu.addAction(creditAct)

    def open_preferences_layout(self):
        pref = Configuration.Configuration()
        pref.show()
        pref.exec_()

    def open_about_layout(self):
        dlg = About.About()
        dlg.show()
        dlg.exec_()

    def open_credit_layout(self):
        dlg = Credit.Credit()
        dlg.show()
        dlg.exec_()

    def on_exit_action_triggered(self):
        usql.TimeLog("Log out")
        QApplication.instance().quit()

    def show_hide_subMenuBar(self, param):
        self.settings._app.setValue("subMenu", param)
        self.setVisible(param)

def main():
    app = QApplication(sys.argv)
    subMenu = SubMenuBar()
    subMenu.show()
    app.exec_()


if __name__=='__main__':
    main()