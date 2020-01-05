#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: {}.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PyQt5
from PyQt5.QtCore                       import pyqtSlot

# PLM
from appData                            import __plmSlogan__, __appname__
from devkit.Widgets                     import SystemTrayIcon
from devkit.Gui                         import LogoIcon
from ui.Header.SysTrayIconMenu          import SysTrayIconMenu
from utils                              import LocalDatabase


# -------------------------------------------------------------------------------------------------------------
class SysTray(SystemTrayIcon):

    key                                 = 'SysTray'
    _login                              = False

    def __init__(self, actionManager, eventManager, parent=None):
        super(SysTray, self).__init__(parent)

        self.db                         = LocalDatabase()
        self.actionManager              = actionManager
        self.eventManager               = eventManager

        try:
            self.username               = self.db.query_table('curUser')[0]
        except (ValueError, IndexError):
            self.username = 'DemoUser'

        self.rightClickMenu             = SysTrayIconMenu(self.actionManager, self)
        self.rightClickMenu.signals.connect('command', self.parent.command)

        self.setIcon(LogoIcon('Logo'))
        self.setToolTip(__plmSlogan__)
        self.activated.connect(self.sys_tray_icon_activated)
        self.setContextMenu(self.rightClickMenu)
        self.installEventFilter(self.eventManager.wheelEvent)

        self.show()

    def sys_tray_icon_activated(self, reason):
        if reason == self.DoubleClick:
            if self._login:
                self.parent.command('Restore')

    def log_in(self):
        self.showMessage('Welcome', "Log in as {0}".format(self.username), self.Information, 500)

    def log_out(self):
        self.showMessage('Log out', "{0} Loged out".format(self.username), self.Information, 500)

    def close_event(self):
        self.showMessage('Notice', "{0} will keep running in the system tray.".format(__appname__), self.Information, 500)

    def loginChanged(self, login):
        self._login = login
        self.rightClickMenu.loginChanged(self._login)

    def sysNotify(self, title, mess, iconType='info', timeDelay=500):
        if iconType == 'info':
            icon = self.Information
        elif iconType == 'crit':
            icon = self.Critical
        else:
            icon = self.Context

        self.showMessage(title, mess, icon, timeDelay)

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, newVal):
        self._login = newVal

    def hide(self):
        return self.show()

    def close(self):
        return self.show()

    def setVisible(self, bool):
        if not self.isVisible():
            return self.setVisible(True)