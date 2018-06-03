#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: {}.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys

# PyQt5
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtWidgets import QMenu, QSystemTrayIcon, QAction, QApplication

# Plt
import appData as app
from ui import uirc as rc
from utilities import utils as func
from utilities import localSQL as usql

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logger = app.set_log()

# -------------------------------------------------------------------------------------------------------------

class SysTrayIconMenu(QMenu):

    showNor = pyqtSignal(bool)
    showMin = pyqtSignal(bool)
    showMax = pyqtSignal(bool)

    def __init__(self, parent=None):

        super(SysTrayIconMenu, self).__init__(parent)

        self.addSeparator()

        for key in app.CONFIG_SYSTRAY:
            self.addAction(rc.ActionProcess(key, self))

        self.addSeparator()

        maxAction = QAction(rc.IconPth(32, "Maximize"), "Maximize", self)
        maxAction.triggered.connect(self.showMax.emit)

        minAction = QAction(rc.IconPth(32, 'Minimize'), "Minimize", self)
        minAction.triggered.connect(self.showMin.emit)

        norAction = QAction(rc.IconPth(32, 'Restore'), "Restore", self)
        norAction.triggered.connect(self.showNor.emit)

        self.addAction(maxAction)
        self.addAction(minAction)
        self.addAction(norAction)

        self.addSeparator()

        quitAction = QAction(rc.IconPth(32, 'Close'), "Quit", self)
        quitAction.triggered.connect(self.exit_action_trigger)

        self.addAction(quitAction)

    def exit_action_trigger(self):
        usql.insert_timeLog("Log out")
        QApplication.instance().quit()

class SystrayWheelEventObject(QObject):

    def eventFilter(self, object, event):
        if type(event) == QWheelEvent:
            if event.delta() > 0:
                print("wheel up")
            else:
                print("wheel down")
            event.accept()
            return True
        return False

class SysTrayIcon(QSystemTrayIcon):

    showNor = pyqtSignal(bool)
    showMin = pyqtSignal(bool)
    showMax = pyqtSignal(bool)

    def __init__(self, parent=None):

        super(SysTrayIcon, self).__init__(parent)

        self.query = usql.QuerryDB

        try:
            self.username, token, cookie, remember = self.query.query_table("curUser")
        except IndexError:
            self.username = 'DemoUser'

        self.settings = app.APPSETTING
        self.rightClickMenu = SysTrayIconMenu()

        self.rightClickMenu.showNor.connect(self.showNor.emit)
        self.rightClickMenu.showMin.connect(self.showMin.emit)
        self.rightClickMenu.showMax.connect(self.showMax.emit)

        self.setIcon(rc.AppIcon('Logo'))
        self.setToolTip(app.__appname__)
        self.activated.connect(self.sys_tray_icon_activated)
        self.setContextMenu(self.rightClickMenu)

        self.eventObj=SystrayWheelEventObject()
        self.installEventFilter(self.eventObj)

    def sys_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.showNor.emit(True)

    def log_in(self):
        self.showMessage('Welcome', "Log in as {0}".format(self.username),
                         QSystemTrayIcon.Information, 500)

    def log_out(self):
        self.showMessage('Welcome', "Log out",
                         QSystemTrayIcon.Information, 500)

    def close_event(self):
        self.showMessage('Notice', "{0} will keep running in the system tray.".format(app.__appname__),
                         QSystemTrayIcon.Information, 500)

def main():
    sysApp = QApplication(sys.argv)
    sysTray = SysTrayIcon()
    sysTray.show()
    sysApp.exec_()

if __name__ == '__main__':
    main()