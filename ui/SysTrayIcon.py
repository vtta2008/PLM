#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: {}.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import os, sys, logging

from PyQt5.QtCore import QObject, pyqtSignal, QSettings
from PyQt5.QtGui import QIcon, QWheelEvent
from PyQt5.QtWidgets import QMenu, QSystemTrayIcon, QAction, QApplication

from utilities import utils as func
from utilities import sql_local as usql
from utilities import variables as var

from ui import uirc as rc
import appData as app

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logPth = os.path.join(app.LOGPTH, 'sysTrayIcon.log')
logger = logging.getLogger(__name__)
handler = logging.FileHandler(logPth)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------------------

class SysTrayIconMenu(QMenu):

    showNormalSig = pyqtSignal(bool)
    showMinimizeSig = pyqtSignal(bool)
    showMaximizeSig = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(SysTrayIconMenu, self).__init__(parent)

        self.addAction(rc.action('Shutdown', self))
        self.addSeparator()

        for key in app.CONFIG_TRAY1:
            self.addAction(rc.action(key, self))

        self.addSeparator()

        for key in app.CONFIG_TRAY2:
            self.addAction(rc.action(key, self))

        self.addSeparator()

        maximizeAction = QAction(QIcon(func.get_icon("Maximize")), "Maximize", self)
        maximizeAction.triggered.connect(lambda: self.showMainApp('maximize'))

        minimizeAction = QAction(QIcon(func.get_icon('Minimize')), "Minimize", self)
        minimizeAction.triggered.connect(lambda: self.showMainApp('minimize'))

        restoreAction = QAction(QIcon(func.get_icon('Restore')), "Restore", self)
        restoreAction.triggered.connect(lambda: self.showMainApp('normal'))

        self.addAction(maximizeAction)
        self.addAction(minimizeAction)
        self.addAction(restoreAction)

        self.addSeparator()

        quitAction = QAction(QIcon(func.get_icon('Close')), "Quit", self)
        quitAction.triggered.connect(self.exit_action_trigger)

        self.addAction(quitAction)

    def exit_action_trigger(self):
        usql.insert_timeLog("Log out")
        logger.debug("LOG OUT")
        QApplication.instance().quit()

    def showMainApp(self, mode):
        if mode == 'maximize':
            self.showMaximizeSig.emit(True)
        elif mode == 'minimize':
            self.showMinimizeSig.emit(True)
        else:
            self.showNormalSig.emit(True)

class SystrayWheelEventObject(QObject):

    def eventFilter(self, object, event):
        if type(event) == QWheelEvent:
            if event.delta() > 0:
                func.send_udp("s51153\n")
            else:
                func.send_udp("s53201\n")
            event.accept()
            return True
        return False

class SysTrayIcon(QSystemTrayIcon):

    showNormalSig = pyqtSignal(bool)
    showMinimizeSig = pyqtSignal(bool)
    showMaximizeSig = pyqtSignal(bool)

    def __init__(self, parent=None):

        super(SysTrayIcon, self).__init__(parent)

        self.username, rememberLogin = usql.query_curUser()
        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)
        self.rightClickMenu = SysTrayIconMenu()

        showNorSig = self.rightClickMenu.showNormalSig
        showMinSig = self.rightClickMenu.showMinimizeSig
        showMaxSig = self.rightClickMenu.showMaximizeSig

        showNorSig.connect(self.show_nor)
        showMinSig.connect(self.show_min)
        showMaxSig.connect(self.show_max)

        self.setIcon(QIcon(func.get_icon('Logo')))
        self.setToolTip(app.__appname__)
        self.activated.connect(self.sys_tray_icon_activated)
        self.setContextMenu(self.rightClickMenu)

        self.eventObj=SystrayWheelEventObject()
        self.installEventFilter(self.eventObj)

    def show_nor(self, param):
        param = func.str2bool(param)
        self.showNormalSig.emit(param)
        self.settings.setValue("showNormal", param)
        self.settings.setValue("showMinimize", not param)
        self.settings.setValue("showMaximize", not param)

    def show_min(self, param):
        param = func.str2bool(param)
        self.showMinimizeSig.emit(param)
        self.settings.setValue("showNormal", not param)
        self.settings.setValue("showMinimize", param)
        self.settings.setValue("showMaximize", not param)

    def show_max(self, param):
        param = func.str2bool(param)
        self.showMaximizeSig.emit(param)
        self.settings.setValue("showNormal", not param)
        self.settings.setValue("showMinimize", not param)
        self.settings.setValue("showMaximize", param)

    def sys_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_nor(True)

    def loginMess(self):
        self.showMessage('Welcome', "Log in as %s" % self.username, QSystemTrayIcon.Information, 500)

    def closeMess(self):
        self.showMessage('Notice', "Pipeline Tool will keep running in the system tray.",
                                  QSystemTrayIcon.Information, 500)

def main():
    pass

if __name__ == '__main__':
    main()