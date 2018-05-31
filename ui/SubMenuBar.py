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
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, QSizePolicy, QApplication

# Plt
import appData as app
from utilities import utils as func
from utilities import localdb as usql
from ui import uirc as rc
from ui import(Preferences, AboutPlt, Credit)

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logger = app.set_log()

# -------------------------------------------------------------------------------------------------------------
""" Menu bar Layout """

class SubMenuBar(QMainWindow):

    def __init__(self, parent=None):

        super(SubMenuBar, self).__init__(parent)

        self.appInfo = func.preset_load_appInfo()
        self.url = app.__pltWiki__
        self.settings = app.APPSETTING
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.buildMenu()

    def buildMenu(self):

        prefAct = QAction(QIcon(func.get_icon('Preferences')), 'Preferences', self)
        prefAct.setStatusTip('Preferences')
        prefAct.triggered.connect(self.open_preferences_layout)

        aboutAct = QAction(QIcon(self.appInfo['AboutPlt'][1]), self.appInfo['AboutPlt'][0], self)
        aboutAct.setStatusTip(self.appInfo['AboutPlt'][0])
        aboutAct.triggered.connect(self.open_about_layout)

        creditAct = QAction(QIcon(self.appInfo['Credit'][1]), self.appInfo['Credit'][0], self)
        creditAct.setStatusTip(self.appInfo['Credit'][0])
        creditAct.triggered.connect(self.open_credit_layout)

        openConfigAct = QAction(QIcon(self.appInfo['OpenConfig'][1]), self.appInfo['OpenConfig'][0], self)
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
        self.helpMenu.addAction(rc.ActionProcess("Plt wiki", self))
        self.helpMenu.addAction(aboutAct)
        self.helpMenu.addAction(creditAct)

    def open_preferences_layout(self):
        pref = Preferences.Preferences()
        pref.show()
        pref.exec_()

    def open_about_layout(self):
        dlg = AboutPlt.AboutPlt()
        dlg.show()
        dlg.exec_()

    def open_credit_layout(self):
        dlg = Credit.Credit()
        dlg.show()
        dlg.exec_()

    def on_exit_action_triggered(self):
        usql.insert_timeLog("Log out")
        logger.debug("LOG OUT")
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