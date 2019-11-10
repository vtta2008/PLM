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
from PyQt5.QtCore               import pyqtSlot
from PyQt5.QtWidgets            import QApplication

# PLM
from appData                    import __plmSlogan__, __appname__, STRONG_FOCUS, STAY_ON_TOP, FRAMELESSWINDOW
from ui.uikits.Icon             import LogoIcon
from ui.Menus.SysTrayIconMenu   import SysTrayIconMenu
from ui.uikits.Button           import Button
from ui.uikits.Widget           import Widget
from ui.uikits.BoxLayout        import VBoxLayout
from ui.uikits.GroupBox         import GroupGrid
from ui.uikits.SystemTrayIcon   import SystemTrayIcon
from utils                      import QuerryDB


# -------------------------------------------------------------------------------------------------------------

class TrayMenu(Widget):

    key = 'CustomMenu'

    def __init__(self, parent=None):
        super(TrayMenu, self).__init__(parent)

        self.setFocusPolicy(STRONG_FOCUS)
        self.setWindowFlags(STAY_ON_TOP|FRAMELESSWINDOW)

        self.layout = VBoxLayout()

        pos = self.geometry().topRight()
        x, y = pos.x() - self.width() / 2, pos.y() - self.height()
        self.move(x, y)

        self.setMouseTracking(True)

        self.buildUI()

        self.setLayout(self.layout)

    def buildUI(self):
        self.button = Button({'txt': 'CustomMenu', 'cl': self.button_clicked})
        group, grid = GroupGrid('Custom Menu')
        grid.addWidget(self.button, 0, 0)
        self.layout.addWidget(group)

    def button_clicked(self):
        print('button clicked')

    def mouseMoveEvent(self, Event):
        self.settings.initSetValue('posX', Event.x(), 'MouseCusor')
        self.settings.initSetValue('posY', Event.y(), 'MouseCusor')
        print(Event.x(), Event.y())

    def focusInEvent(self, Event):
        self.isActiveWindow()

    def focusOutEvent(self, Event):
        self.hide()

class SysTray(SystemTrayIcon):

    key = 'SysTray'
    _login = False

    def __init__(self, actionManager, eventManager, parent=None):

        super(SysTray, self).__init__(parent)

        self.db                 = QuerryDB()
        self.actionManager      = actionManager
        self.eventManager       = eventManager
        self.trayMenu           = TrayMenu(self)
        self.signals.emit('regisLayout', self.trayMenu)

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
            # print('login: {}'.format(self._login))
            if self._login:
                self.signals.emit('showLayout', 'PipelineManager', 'showRestore')
        elif reason == self.MiddleClick:
            self.customMenu()

    def customMenu(self):
        self.trayMenu.show()
        self.trayMenu.setFocus()

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
        return self._login

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