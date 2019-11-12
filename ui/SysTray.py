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
from PyQt5.QtCore                       import pyqtSlot
from PyQt5.QtWidgets                    import QApplication

# PLM
from appData                            import __plmSlogan__, __appname__
from ui.uikits.Icon                     import LogoIcon
from ui.Header.Menus.SysTrayIconMenu    import SysTrayIconMenu
from ui.uikits.SystemTrayIcon           import SystemTrayIcon
from utils                              import QuerryDB


# -------------------------------------------------------------------------------------------------------------
class SysTray(SystemTrayIcon):

    key = 'SysTray'
    _login = False

    def __init__(self, settings, actionManager, eventManager, parent=None):

        super(SysTray, self).__init__(parent)

        self.db                 = QuerryDB()
        self.settings           = settings
        self.actionManager      = actionManager
        self.eventManager       = eventManager

        try:
            self.username, token, cookie, remember = self.db.query_table('curUser')
        except (ValueError, IndexError):
            self.username = 'DemoUser'

        self.rightClickMenu = SysTrayIconMenu(self.actionManager, self)
        self.rightClickMenu.signals.executing.connect(self.signals.executing.emit)
        self.rightClickMenu.signals.showLayout.connect(self.signals.showLayout.emit)

        self.setIcon(LogoIcon('Logo'))
        self.setToolTip(__plmSlogan__)
        self.activated.connect(self.sys_tray_icon_activated)
        self.setContextMenu(self.rightClickMenu)
        self.installEventFilter(self.eventManager.wheelEvent)

    def sys_tray_icon_activated(self, reason):
        if reason == self.DoubleClick:
            if self._login:
                self.signals.emit('showLayout', 'PipelineManager', 'showRestore')

    def log_in(self):
        self.showMessage('Welcome', "Log in as {0}".format(self.username), self.Information, 500)

    def log_out(self):
        self.showMessage('Log out', "{0} Loged out".format(self.username), self.Information, 500)

    def close_event(self):
        self.showMessage('Notice', "{0} will keep running in the system tray.".format(__appname__), self.Information, 500)

    @pyqtSlot(str, str, str, int)
    def sysNotify(self, title, mess, iconType, timeDelay):
        if iconType == 'info':
            icon = self.Information
        elif iconType == 'crit':
            icon = self.Critical
        else:
            icon = self.Context

        self.showMessage(title, mess, icon, timeDelay)

    def loginChanged(self, login):
        self._login = login
        self.rightClickMenu.loginChanged(self._login)

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, newVal):
        self._login = newVal

def main():
    sysApp = QApplication(sys.argv)
    sysTray = SysTray()
    sysTray.show()
    sysApp.exec_()

if __name__ == '__main__':
    main()