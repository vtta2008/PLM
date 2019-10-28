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
import json
import os
import sys
from functools import partial

# PyQt5
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtWidgets import QMenu, QSystemTrayIcon, QApplication

from cores.Loggers import Loggers
# PLM
from appData import __plmSlogan__, __appname__, __envKey__, CONFIG_SYSTRAY
from ui.SignalManager import SignalManager
from ui import Action, LogoIcon, SystemTrayIcon
from cores.base import DAMG
from utils.localSQL import QuerryDB


# -------------------------------------------------------------------------------------------------------------

class SysTrayIconMenu(QMenu):

    key = 'SysTrayIconMenu'

    def __init__(self, parent=None):
        super(SysTrayIconMenu, self).__init__(parent)

        self.signals = SignalManager(self)

        with open(os.path.join(os.getenv(__envKey__), 'appData/.config', 'main.cfg'), 'r') as f:
            self.appInfo = json.load(f)

        self.addSeparator()
        for k in CONFIG_SYSTRAY:
            if k == 'Screenshot':
                self.addAction(Action({'icon':k, 'txt': k, 'trg': partial(self.signals.showLayout.emit, self.appInfo[k][2], 'show')}, self))
            elif k == 'Snipping Tool':
                self.addAction(Action({'icon': k, 'txt': k, 'trg': partial(self.signals.executing.emit, self.appInfo[k][2])}, self))

        self.addSeparator()

        self.addAction(Action({'icon':'Maximize','txt':'Maximize','trg':partial(self.signals.showLayout.emit, 'PipelineManager', 'showMax')}, self))
        self.addAction(Action({'icon':'Minimize','txt':"Minimize",'trg':partial(self.signals.showLayout.emit, 'PipelineManager', 'showMin')}, self))
        self.addAction(Action({'icon':'Restore','txt':"Restore", 'trg':partial(self.signals.showLayout.emit, 'PipelineManager', 'showNor')}, self))

        self.addSeparator()
        self.addAction(Action({'icon':'Close','txt':"Quit", 'trg':partial(self.signals.showLayout.emit, 'app', 'quit')}, self))

class SystrayWheelEventObject(DAMG):

    def eventFilter(self, object, event):
        if type(event) == QWheelEvent:
            if event.delta() > 0:
                print("wheel up")
            else:
                print("wheel down")
            event.accept()
            return True
        return False

class SysTray(SystemTrayIcon):

    key = 'SysTray'

    def __init__(self, parent=None):

        super(SysTray, self).__init__(parent)

        self.db = QuerryDB()

        try:
            self.username, token, cookie, remember = self.db.query_table('curUser')
        except (ValueError, IndexError):
            self.username = 'DemoUser'

        self.rightClickMenu = SysTrayIconMenu()
        self.rightClickMenu.signals.executing.connect(self.signals.executing.emit)
        self.rightClickMenu.signals.showLayout.connect(self.signals.showLayout.emit)

        self.setIcon(LogoIcon('Logo'))
        self.setToolTip(__plmSlogan__)
        self.activated.connect(self.sys_tray_icon_activated)
        self.setContextMenu(self.rightClickMenu)

        self.eventObj=SystrayWheelEventObject()
        self.installEventFilter(self.eventObj)

    def sys_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.signals.showLayout.emit('PipelineManager', 'showNor')

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
    sysTray = SysTray()
    sysTray.show()
    sysApp.exec_()

if __name__ == '__main__':
    main()