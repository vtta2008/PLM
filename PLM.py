# -*- coding: utf-8 -*-
"""

Script Name: PLM.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is master file of Pipeline Manager

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

from __buildtins__ import *
from __buildtins__ import __envKey__
# -------------------------------------------------------------------------------------------------------------
""" import """

# Python
import os, sys, requests, ctypes

# PyQt5
from PyQt5.QtCore                   import pyqtSlot, QCoreApplication
from PyQt5.QtWidgets                import QApplication
from PyQt5.QtGui                    import QCursor, QGuiApplication

# Plm
from appData                        import (__localServer__, PLMAPPID, __organization__,
                                            __appname__, __version__, __website__, SETTING_FILEPTH,
                                            ST_FORMAT, SYSTRAY_UNAVAI)

from cores.StyleSheets              import StyleSheets
from cores.ThreadManager            import ThreadManager
from utils                          import str2bool, clean_file_ext, QuerryDB
from cores.Loggers                  import Loggers
from cores.Settings                 import Settings
from ui.ActionManager               import ActionManager
from ui.ButtonManager               import ButtonManager
from ui.uikits.Icon                 import LogoIcon
from ui.Web.Browser                 import Browser
from ui.LayoutManager               import LayoutManager
from ui.EventManager                import EventManager

# -------------------------------------------------------------------------------------------------------------
""" Operation """

class PLM(QApplication):

    key                             = 'PLM'
    configManager                   = configManager

    ignoreIDs                       = []

    toBuildLayouts = ['ProjectManager', 'ConfigProject', 'EditProject', 'NewOrganisation', 'EditOrganisation',
                      'ConfigOrganisation', 'OrganisationManager', 'NewTeam', 'EditTeam', 'ConfigTeam', 'TeamManager',
                      'Alpha', 'HDRI', 'Texture', 'Feedback', 'ContactUs']

    toBuildCommand = []

    def __init__(self):
        super(PLM, self).__init__(sys.argv)

        # Run all neccessary configuration to start PLM

        self.logger                 = Loggers(self.__class__.__name__)
        self.settings               = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self._login                 = False

        self.appInfo                = self.configManager.appInfo                                    # Configuration data

        # Multithreading.
        self.thread_manager         = ThreadManager()
        self.database               = QuerryDB()                                                    # Database tool
        self.browser                = Browser()

        self.set_styleSheet('dark')                                                                  # Layout style
        self.setWindowIcon(LogoIcon("Logo"))                                                         # Set up task bar icon
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(PLMAPPID)                      # Change taskbar icon

        QCoreApplication.setOrganizationName(__organization__)
        QCoreApplication.setApplicationName(__appname__)
        QCoreApplication.setOrganizationDomain(__website__)
        QCoreApplication.setApplicationVersion(__version__)

        self.eventManager           = EventManager()
        self.buttonManager          = ButtonManager()
        self.actionManager          = ActionManager()
        self.layoutManager          = LayoutManager(self.settings, self.actionManager, self.buttonManager, self)
        self.layoutManager.regisLayout(self.browser)
        self.layoutManager.buildLayouts()

        self.ignoreIDs              = self.layoutManager.ignoreIDs

        self.sysTray = self.layoutManager.sysTray
        self.sysTray.installEventFilter(self.eventManager.wheelEvent)
        self.mainUI = self.layoutManager.mainUI

        for layout in self.layoutManager.layouts():
            if not layout.key in self.ignoreIDs:
                layout.signals.connect('showLayout', self.showLayout)
                layout.signals.connect('executing', self.executing)
                layout.signals.connect('openBrowser', self.openBrowser)
                layout.signals.connect('setSetting', self.setSetting)
                layout.signals.connect('sysNotify', self.sysNotify)

                if layout.key == 'SignIn':
                    layout.signals.connect('loginChanged', self.loginChanged)

        try:
            self.username, token, cookie, remember = self.database.query_table('curUser')
        except (ValueError, IndexError):
            self.logger.info("Error occur, can not query data")
            self.showLayout('SignIn', "show")
        else:
            if not str2bool(remember):
                self.showLayout('SignIn', "show")
            else:
                r = requests.get(__localServer__, verify = False, headers = {'Authorization': 'Bearer {0}'.format(token)}, cookies = {'connect.sid': cookie})
                if r.status_code == 200:
                    if not self.layoutManager.sysTray.isSystemTrayAvailable():
                        self.logger.report(SYSTRAY_UNAVAI)
                        self.exitEvent()
                    else:
                        self.loginChanged(True)
                        self.sysTray.log_in()
                        self.showLayout(self.mainUI.key, "show")
                else:
                    self.showLayout('SignIn', "show")

        self.setQuitOnLastWindowClosed(False)
        sys.exit(self.exec_())

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, newVal):
        self._login = newVal

    @pyqtSlot(str, name='openBrowser')
    def openBrowser(self, url):
        # self.logger.report("receive signal open browser: {0}".format(url))
        self.browser.setUrl(url)
        self.browser.update()
        self.browser.show()

    @pyqtSlot(str, str, str, name='setSetting')
    def setSetting(self, key=None, value=None, grp=None):
        # self.logger.report("receive setting: configKey: {0}, to value: {1}, in group {2}".format(key, value, grp))
        self.settings.initSetValue(key, value, grp)

    @pyqtSlot(str, name="executing")
    def executing(self, cmd):
        if cmd in self.layoutManager.keys():
            self.signals.showLayout.emit(cmd, 'show')
        elif os.path.isdir(cmd):
            os.startfile(cmd)
        elif cmd in self.configManager.appInfo.keys():
            os.system(self.appInfo[cmd])
        elif cmd == 'Debug':
            from ui.Debugger import Debugger
            debugger = Debugger()
            return debugger
        elif cmd == 'open_cmd':
            os.system('start /wait cmd')
        elif cmd == 'CleanPyc':
            clean_file_ext('.pyc')
        elif cmd == 'ReConfig':
            self.configManager = ConfigManager(__envKey__, ROOT)
        elif cmd == 'Exit':
            self.exitEvent()
        else:
            if not cmd in self.toBuildCommand:
                self.logger.report("This command is not regiested yet: {0}".format(cmd))
                self.toBuildCommand.append(cmd)
            else:
                self.logger.info("This command will be built later.".format(cmd))

    @pyqtSlot(str, str, name="showLayout")
    def showLayout(self, layoutID, mode):
        print('get signal: {0} {1}'.format(layoutID, mode))

        if layoutID == 'SignOut' and mode == 'show':
            self.signOutEvent()
        elif layoutID == 'SwitchAccount' and mode == 'show':
            self.switchAccountEvent()
        elif layoutID == 'SignUp' and mode == 'show':
            self.newAccountEvent()
        elif layoutID in self.layoutManager.keys():
            if not layoutID in self.ignoreIDs:
                if mode == "hide":
                    self.layoutManager[layoutID].hide()
                    self.layoutManager[layoutID].setValue('state', 'hide')
                elif mode == "show":
                    self.layoutManager[layoutID].show()
                    self.layoutManager[layoutID].setValue('state', 'show')
                elif mode == 'showRestore':
                    self.layoutManager[layoutID].showNormal()
                    self.layoutManager[layoutID].setValue('state', 'showNormal')
                elif mode == 'showMin':
                    self.layoutManager[layoutID].showMinimize()
                    self.layoutManager[layoutID].setValue('state', 'showMinimize')
                elif mode == 'showMax':
                    self.layoutManager[layoutID].showMaximized()
                    self.layoutManager[layoutID].setValue('state', 'showMaximized')
                elif mode == 'quit' or mode == 'exit':
                    self.exitEvent()
                else:
                    self.logger.report("LayouKeyError: {0}".format(layoutID) )
        else:
            if not layoutID in self.toBuildLayouts:
                self.logger.report("Layout: '{0}' is not registerred yet.".format(layoutID))
                self.toBuildLayouts.append(layoutID)
                return

    @pyqtSlot(str, str, str, int, name='sysNotify')
    def sysNotify(self, title, mess, iconType, timeDelay):
        # self.logger.report('Receive signal sysNotify: {0} {1} {2} {3}'.format(title, mess, iconType, timeDelay))
        return self.layoutManager.sysTray.sysNotify(title, mess, iconType, timeDelay)

    def set_styleSheet(self, style):

        stylesheet = dict(dark      =StyleSheets('dark').changeStylesheet,
                          bright    =StyleSheets('bright').changeStylesheet, )

        self.setStyleSheet(stylesheet[style])
        self.settings.initSetValue('styleSheet', 'dark')

    @pyqtSlot(bool, name='loginChanged')
    def loginChanged(self, val):
        self._login = val
        self.sysTray.loginChanged(self._login)
        self.sysTray.rightClickMenu.loginChanged(self._login)
        self.layoutManager.signin.loginChanged(self._login)
        return self._login

    def signOutEvent(self):
        self.loginChanged(False)
        self.layoutManager.signOutEvent()

    def newAccountEvent(self):
        self.layoutManager.newAcountEvent()
        self.loginChanged(False)

    def switchAccountEvent(self):
        self.layoutManager.switchAccountEvent()
        self.loginChanged(False)

    def exitEvent(self):
        # print(self.toBuildLayouts, self.toBuildCommand)
        self.exit()

if __name__ == '__main__':
    PLM()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 2:26 AM
# © 2017 - 2018 DAMGteam. All rights reserved