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
import sys, os, json
from functools import partial

# PyQt5
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtWidgets import QMenu, QSystemTrayIcon, QApplication


# Plt
from appData import __plmSlogan__, __appname__, __envKey__
from ui.uikits.UiPreset import AppIcon
from ui.uikits.Action import Action
from utilities.localSQL import QuerryDB
from core.Loggers import SetLogger
from core.Specs import Specs
from core.keys import CONFIG_SYSTRAY

# -------------------------------------------------------------------------------------------------------------

class SysTrayIconMenu(QMenu):

    key = 'sysTray'
    showLayout = pyqtSignal(str, str)
    executing = pyqtSignal(str)

    def __init__(self, parent=None):
        super(SysTrayIconMenu, self).__init__(parent)

        with open(os.path.join(os.getenv(__envKey__), 'cfg', 'main.cfg'), 'r') as f:
            self.appInfo = json.load(f)

        self.addSeparator()
        for k in CONFIG_SYSTRAY:
            if k == 'Screenshot':
                self.addAction(Action({'icon':k, 'txt': k, 'trg': partial(self.showLayout.emit, self.appInfo[k][2], 'show')}, self))
            elif k == 'Snipping Tool':
                self.addAction(Action({'icon': k, 'txt': k, 'trg': partial(self.executing.emit, self.appInfo[k][2])}, self))

        self.addSeparator()

        self.addAction(Action({'icon':'Maximize','txt':'Maximize','trg':partial(self.showLayout.emit, 'mainUI', 'showMax')}, self))
        self.addAction(Action({'icon':'Minimize','txt':"Minimize",'trg':partial(self.showLayout.emit, 'mainUI', 'showMin')}, self))
        self.addAction(Action({'icon':'Restore','txt':"Restore", 'trg':partial(self.showLayout.emit, 'mainUI', 'showNor')}, self))

        self.addSeparator()
        self.addAction(Action({'icon':'Close','txt':"Quit", 'trg':partial(self.showLayout.emit, 'app', 'quit')}, self))

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

    key = 'sysTray'
    showLayout = pyqtSignal(str, str)
    executing = pyqtSignal(str)

    def __init__(self, parent=None):

        super(SysTrayIcon, self).__init__(parent)
        self.specs = Specs(self.key, self)
        self.logger = SetLogger(self)
        self.db = QuerryDB()

        try:
            self.username, token, cookie, remember = self.db.query_table('curUser')
        except IndexError:
            self.username = 'DemoUser'

        self.rightClickMenu = SysTrayIconMenu()
        self.rightClickMenu.executing.connect(self.executing.emit)
        self.rightClickMenu.showLayout.connect(self.showLayout.emit)

        self.setIcon(AppIcon('Logo'))
        self.setToolTip(__plmSlogan__)
        self.activated.connect(self.sys_tray_icon_activated)
        self.setContextMenu(self.rightClickMenu)

        self.eventObj=SystrayWheelEventObject()
        self.installEventFilter(self.eventObj)

    def sys_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.showLayout.emit('mainUI', 'showNor')

    def log_in(self):
        self.showMessage('Welcome', "Log in as {0}".format(self.username), QSystemTrayIcon.Information, 500)

    def log_out(self):
        self.showMessage('Log out', "{0} Loged out".format(self.username), QSystemTrayIcon.Information, 500)

    def close_event(self):
        self.showMessage('Notice', "{0} will keep running in the system tray.".format(__appname__), QSystemTrayIcon.Information, 500)

    @pyqtSlot(str, str, str, int)
    def sysNotify(self, title, mess, iconType, timeDelay):
        if iconType == 'info':
            icon = self.Information
        elif iconType == 'crit':
            icon = self.Critical
        else:
            icon = self.Context

        self.showMessage(title, mess, icon, timeDelay)

def main():
    sysApp = QApplication(sys.argv)
    sysTray = SysTrayIcon()
    sysTray.show()
    sysApp.exec_()

if __name__ == '__main__':
    main()