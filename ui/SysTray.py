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
from PyQt5.QtWidgets            import QApplication

# PLM
from appData                    import __plmSlogan__, __appname__, __envKey__, STRONG_FOCUS, STAY_ON_TOP, FRAMELESSWINDOW
from cores.SignalManager        import LayoutSignals
from ui.uikits.Icon             import LogoIcon
from ui.uikits.Menu             import Menu
from ui.uikits.Button           import Button
from ui.uikits.Widget           import Widget
from ui.uikits.BoxLayout        import VBoxLayout
from ui.uikits.GroupBox         import GroupGrid
from ui.uikits.SystemTrayIcon   import SystemTrayIcon
from utils                      import QuerryDB


# -------------------------------------------------------------------------------------------------------------

class SysTrayIconMenu(Menu):

    key = 'SysTrayIconMenu'

    def __init__(self, actionManager, parent=None):
        super(SysTrayIconMenu, self).__init__(parent)

        self.signals            = LayoutSignals(self)
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

    key = 'SystrayWheelEventObject'

    def eventFilter(self, object, event):
        if type(event) == QWheelEvent:
            if event.delta() > 0:
                print("wheel up")
            else:
                print("wheel down")
            event.accept()
            return True
        return False

class TrayMenu(Widget):

    key = 'CustomMenu'

    def __init__(self, parent=None):
        super(TrayMenu, self).__init__(parent)

        self.setFocusPolicy(STRONG_FOCUS)
        self.setWindowFlags(STAY_ON_TOP|FRAMELESSWINDOW)

        self.button = Button({'txt': 'CustomMenu', 'cl': self.button_clicked})

        self.layout = VBoxLayout()
        group, grid = GroupGrid('Custom Menu')
        grid.addWidget(self.button, 0, 0)
        self.layout.addWidget(group)

        self.setLayout(self.layout)

    def button_clicked(self):
        print('button clicked')

    def focusInEvent(self, Event):
        self.isActiveWindow()

    def focusOutEvent(self, Event):
        self.hide()

class SysTray(SystemTrayIcon):

    key = 'SysTray'
    _loggin = False

    def __init__(self, actionManager, parent=None):

        super(SysTray, self).__init__(parent)

        self.db                 = QuerryDB()
        self.actionManager      = actionManager
        self.trayMenu           = TrayMenu()

        try:
            self.username, token, cookie, remember = self.db.query_table('curUser')
        except (ValueError, IndexError):
            self.username = 'DemoUser'

        self.rightClickMenu = SysTrayIconMenu(self.actionManager)
        self.rightClickMenu.signals.executing.connect(self.signals.executing.emit)
        self.rightClickMenu.signals.showLayout.connect(self.signals.showLayout.emit)

        self.setIcon(LogoIcon('Logo'))
        self.setToolTip(__plmSlogan__)
        self.activated.connect(self.sys_tray_icon_activated)
        self.setContextMenu(self.rightClickMenu)

        self.eventObj = SystrayWheelEventObject()
        self.installEventFilter(self.eventObj)

    def sys_tray_icon_activated(self, reason):
        if reason == self.DoubleClick:
            if self._loggin:
                self.signals.emit('showLayout', 'PipelineManager', 'showRestore')
        elif reason == self.MiddleClick:
            self.customMenu()

    def customMenu(self):
        pos = self.geometry().topRight()
        x, y = pos.x() - self.trayMenu.width()/2, pos.y() - self.trayMenu.height()
        self.trayMenu.move(x, y)
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