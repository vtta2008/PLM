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
import appData as app
from utilities import localSQL as usql
from ui import uirc as rc
from ui import(Preferences, About, Credit)

# -------------------------------------------------------------------------------------------------------------
""" Menu bar Layout """

class SubMenuBar(QMainWindow):

    subMenuSig = pyqtSignal(str)

    def __init__(self, parent=None):

        super(SubMenuBar, self).__init__(parent)

        self.appInfo = app.APPINFO
        self.url = app.__pltWiki__
        self.settings = app.appSetting
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
        openConfigAct.triggered.connect(partial(os.startfile, app.CONFIGDIR))

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
        pref = Preferences.Preferences()
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
        usql.insert_timeLog("Log out")
        # logger.debug("LOG OUT")
        QApplication.instance().quit()

    def show_hide_subMenuBar(self, param):
        self.settings.setValue("subMenu", param)
        self.setVisible(param)

def main():
    app = QApplication(sys.argv)
    subMenu = SubMenuBar()
    subMenu.show()
    app.exec_()


if __name__=='__main__':
    main()