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
import os, sys, json
from damg                       import DAMG

# PyQt5
from PyQt5.QtCore               import pyqtSlot
from PyQt5.QtGui                import QWheelEvent
from PyQt5.QtWidgets            import QMenu, QSystemTrayIcon, QApplication

# PLM
from appData                    import __plmSlogan__, __appname__, __envKey__
from cores.SignalManager        import LayoutSignals
from ui.uikits.Icon             import LogoIcon
from ui.uikits.SystemTrayIcon   import SystemTrayIcon
from utils                      import QuerryDB


# -------------------------------------------------------------------------------------------------------------

class SysTrayIconMenu(QMenu):

    key = 'SysTrayIconMenu'

    def __init__(self, settings, actionManager, parent=None):
        super(SysTrayIconMenu, self).__init__(parent)

        self.signals            = LayoutSignals(self)
        self.settings           = settings
        self.actionManager      = actionManager

        with open(os.path.join(os.getenv(__envKey__), 'appData/.config', 'main.cfg'), 'r') as f:
            self.appInfo = json.load(f)

        actions                 = self.actionManager.sysTrayMenuActions(self)

        self.addActions(actions[3:5])
        self.addSeparator()
        self.addActions(actions[0:3])
        self.addSeparator()
        self.addAction(actions[-1])

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
    _loggin = False

    def __init__(self, settings, actionManager, parent=None):

        super(SysTray, self).__init__(parent)

        self.db                 = QuerryDB()
        self.settings           = settings
        self.actionManager      = actionManager

        try:
            self.username, token, cookie, remember = self.db.query_table('curUser')
        except (ValueError, IndexError):
            self.username = 'DemoUser'

        self.rightClickMenu = SysTrayIconMenu(self.settings, self.actionManager)
        self.rightClickMenu.signals.executing.connect(self.signals.executing.emit)
        self.rightClickMenu.signals.showLayout.connect(self.signals.showLayout.emit)

        self.setIcon(LogoIcon('Logo'))
        self.setToolTip(__plmSlogan__)
        self.activated.connect(self.sys_tray_icon_activated)
        self.setContextMenu(self.rightClickMenu)

        self.eventObj = SystrayWheelEventObject()
        self.installEventFilter(self.eventObj)

    def sys_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.signals.showLayout.emit('PipelineManager', 'showRestore')

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

    @property
    def login(self):
        return self._loggin

    @login.setter
    def login(self, newVal):
        self._loggin = newVal

def main():
    sysApp = QApplication(sys.argv)
    sysTray = SysTray()
    sysTray.show()
    sysApp.exec_()

if __name__ == '__main__':
    main()