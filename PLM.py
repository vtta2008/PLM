# -*- coding: utf-8 -*-
"""

Script Name: PLM.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is master file of Pipeline Manager

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

from __buildtins__                      import *
from __buildtins__                      import __envKey__
# -------------------------------------------------------------------------------------------------------------
""" import """

# Python
import os, sys, requests, ctypes

# PyQt5
from PyQt5.QtCore                       import pyqtSlot

# Plm
from appData                            import (__localServer__, PLMAPPID, __organization__, StateNormal, StateMax,
                                                StateMin, __appname__, __version__, __website__, SETTING_FILEPTH,
                                                ST_FORMAT, SYSTRAY_UNAVAI, KEY_TAB, KEY_PRESS)

from ui.ThreadManager                   import ThreadManager
from utils                              import str2bool, clean_file_ext, LocalDatabase
from cores.Loggers                      import Loggers
from cores.Settings                     import Settings
from cores.Registry                     import RegistryLayout
from ui.ActionManager                   import ActionManager
from ui.ButtonManager                   import ButtonManager
from ui.uikits.Icon                     import LogoIcon
from ui.Web.Browser                     import Browser
from ui.LayoutManager                   import LayoutManager
from ui.EventManager                    import EventManager

# -------------------------------------------------------------------------------------------------------------
""" Operation """

class PLM(Application):

    key                                 = 'PLM'
    dataConfig                          = configManager
    count                               = 0

    showLayout_old  = []
    executing_old   = []
    setSetting_old  = []
    openBrowser_old = []

    def __init__(self):
        super(PLM, self).__init__(sys.argv)

        # Run all neccessary configuration to start PLM

        self.logger                     = Loggers(self.__class__.__name__)
        self.settings                   = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.settings._settingEnable    = True

        self.appInfo                    = self.dataConfig.appInfo                                    # Configuration data

        # Multithreading.
        self.threadManager              = ThreadManager()
        self.database                   = LocalDatabase()                                            # Database tool
        self.browser                    = Browser()

        self.database.create_table('test_table', {'test_column': 'varchar'})

        self.set_styleSheet('dark')                                                                  # Layout name
        self.setWindowIcon(LogoIcon("Logo"))                                                         # Set up task bar icon
        self.appID = self.applicationPid()
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(PLMAPPID)                      # Change taskbar icon

        self.setOrganizationName(__organization__)
        self.setApplicationName(__appname__)
        self.setOrganizationDomain(__website__)
        self.setApplicationVersion(__version__)
        self.setApplicationDisplayName(__appname__)
        self.setCursorFlashTime(1000)
        self.setQuitOnLastWindowClosed(False)

        self.eventManager               = EventManager()
        self.buttonManager              = ButtonManager()
        self.actionManager              = ActionManager()
        self.registryLayout             = RegistryLayout()
        self.layoutManager              = LayoutManager(self.settings, self.registryLayout, self.actionManager,
                                                        self.buttonManager, self.eventManager, self.threadManager, self)
        self.layoutManager.registLayout(self.browser)
        self.layoutManager.buildLayouts()
        self.layoutManager.globalSetting()

        self.signIn                     = self.layoutManager.signin
        self.signUp                     = self.layoutManager.signup
        self.commandLayout              = self.layoutManager.hiddenLayout
        self.forgotPassword             = self.layoutManager.forgotPW
        self.sysTray                    = self.layoutManager.sysTray
        self.mainUI                     = self.layoutManager.mainUI

        for layout in [self.signIn, self.signUp, self.forgotPassword, self.sysTray, self.mainUI]:
            layout.signals.connect('loginChanged', self.loginChanged)

        for layout in self.layoutManager.layouts():
            if not layout.key in self.ignoreIDs:
                layout.signals.connect('showLayout', self.showLayout)
                layout.signals.connect('executing', self.executing)
                layout.signals.connect('openBrowser', self.openBrowser)
                layout.signals.connect('setSetting', self.setSetting)
                layout.signals.connect('sysNotify', self.sysNotify)
                # print(layout.key)
                layout.settings._settingEnable = True

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
                    if not self.sysTray.isSystemTrayAvailable():
                        self.logger.report(SYSTRAY_UNAVAI)
                        self.exitEvent()
                    else:
                        self.loginChanged(True)
                        self.sysTray.log_in()
                        self.showLayout(self.mainUI.key, "show")
                else:
                    self.showLayout('SignIn', "show")

        sys.exit(self.exec_())

    @pyqtSlot(str, name='openBrowser')
    def openBrowser(self, url):
        if self._trackRecieveSignal:
            self.logger.report("receive signal open browser: {0}".format(url))

        self.openBrowser_old, repeat = self.checkSignalRepeat(self.openBrowser_old, [url])
        if not repeat:
            self.browser.setUrl(url)
            self.browser.update()
            self.browser.show()
        else:
            if self._trackBlockSignal:
                self.logger.report('{1}: block signal openBrowser: {0}'.format(url, self.key))

    @pyqtSlot(str, str, str, name='setSetting')
    def setSetting(self, key=None, value=None, grp=None):
        if self._trackRecieveSignal:
            self.logger.report("receive signal setSetting: {0}, {1}, {2}".format(key, value, grp))

        self.setSetting_old, repeat = self.checkSignalRepeat(self.setSetting_old, [key, value, grp])
        if not repeat:
            self.settings.initSetValue(key, value, grp)
        else:
            if self._trackBlockSignal:
                self.logger.report('{3}: block signal setSetting: {0}, {1}, {2}'.format(key, value, grp, self.key))
            return

    @pyqtSlot(str, name="executing")
    def executing(self, cmd):
        if self._trackRecieveSignal:
            self.logger.report("receive signal executing: {0}".format(cmd))

        self.executing_old, repeat = self.checkSignalRepeat(self.executing_old, [cmd])

        if repeat:
            limit = 10
            if self.threadManager.counter.printCounter:
                self.threadManager.setPrintCounter(False)

            if self.threadManager.counter._countLimited != limit:
                self.threadManager.setCountLimited(limit)

            if not self.threadManager.isCounting():
                self.threadManager.startCounting()

            if self._trackBlockSignal:
                print('block signal executing: {0}'.format(cmd))

            return self.countDownReset(limit)
        else:
            if cmd in self.registryLayout.keys():
                return self.signals.emit('showLayout', cmd, 'show')
            elif os.path.isdir(cmd):
                return os.startfile(cmd)
            elif cmd in self.dataConfig.appInfo.keys():
                return os.system(self.appInfo[cmd])
            elif cmd == 'Debug':
                return self.mainUI.botTabUI.botTab2.test()
            elif cmd == 'open_cmd':
                return os.system('start /wait cmd')
            elif cmd == 'CleanPyc':
                return clean_file_ext('.pyc')
            elif cmd == 'ReConfig':
                self.dataConfig = ConfigManager(__envKey__, ROOT)
                return self.dataConfig
            elif cmd == 'Exit':
                return self.exitEvent()
            else:
                if not cmd in self.toBuildCommand:
                    if self._trackCommand:
                        self.logger.report("This command is not regiested yet: {0}".format(cmd))
                    return self.toBuildCommand.append(cmd)
                else:
                    if self._trackCommand:
                        self.logger.info("This command will be built later.".format(cmd))
                    return

    def countDownReset(self, limit):
        self.count += 1
        if self.count == limit:
            self.executing_old = []

        return self.executing_old

    @pyqtSlot(str, str, name="showLayout")
    def showLayout(self, layoutID, mode):

        self.showLayout_old, repeat = self.checkSignalRepeat(self.showLayout_old, [layoutID, mode])

        if layoutID in self.registryLayout.keys():
            layout = self.registryLayout[layoutID]
            if layout.windowState() & StateNormal:
                state = 'showNormal'
            elif layout.windowState() & StateMax:
                state = 'showMaximized'
            elif layout.windowState() & StateMin:
                state = 'showMinimized'
            else:
                state = layout.getValue('showLayout')

            if not repeat:
                if mode == state:
                    if self._trackBlockSignal:
                        self.logger.report('{2}: block signal showLayout from {0}: {1}'.format(layoutID, mode, self.key))
                    repeat = True
                else:
                    if mode == 'show':
                        if state in ['show', 'showNormal', 'showRestore']:
                            if self._trackBlockSignal:
                                self.logger.report('{2}: block signal showLayout from {0}: {1}'.format(layoutID, mode, self.key))
                            repeat = True
                    elif mode == 'hide':
                        if state in ['hide', 'showMinimized']:
                            if self._trackBlockSignal:
                                self.logger.report('{2}: block signal showLayout from {0}: {1}'.format(layoutID, mode, self.key))
                            repeat = True
            else:
                repeat = True

        if not repeat:
            if self._trackRecieveSignal:
                self.logger.report('recieve signal showLayout from {0}: {1}'.format(layoutID, mode))
            pass
        else:
            if self._trackBlockSignal:
                self.logger.report('{2}: block signal showLayout from {0}: {1}'.format(layoutID, mode, self.key))
            return

        if mode in ['SignIn', 'SignOut', 'SignUp', 'SwitchAccount']:
            if layoutID == mode:
                if mode == 'SignIn':
                    return self.signInEvent()
                elif mode == 'SignOut':
                    return self.signOutEvent()
                elif mode == 'SignUp':
                    return self.signUpEvent()
                else:
                    return self.switchAccountEvent()

        if layoutID in self.registryLayout.keys():
            if layoutID in self.ignoreIDs:
                if not layoutID in self.toBuildUis:
                    self.logger.report("Layout: '{0}' is not registerred yet.".format(layoutID))
                    self.toBuildUis.append(layoutID)
                    self.todoList.update()
            else:
                layout = self.registryLayout[layoutID]

                if mode == "hide":
                    if not layout.isHidden():
                        layout.hide()
                        self.setSetting('showLayout', 'hide', layout.key)
                        self.mainUI.signals.states[layout.key] = mode
                elif mode == "show":
                    if layout.isHidden():
                        layout.show()
                        self.setSetting('showLayout', 'show', layout.key)
                        self.mainUI.signals.states[layout.key] = mode
                elif mode == 'showRestore' or mode == 'showNormal':
                    if not layout.windowState() & StateNormal:
                        layout.showNormal()
                        self.setSetting('showLayout', 'show', layout.key)
                        self.mainUI.signals.states[layout.key] = mode
                elif mode == 'showMinimized' or mode == 'showMin':
                    if not layout.isMinimized():
                        layout.showMinimized()
                        self.setSetting('showLayout', 'showMinimized', layout.key)
                        self.mainUI.signals.states[layout.key] = mode
                elif mode == 'showMaximized' or mode == 'showMax':
                    if not layout.isMaximized():
                        layout.showMaximized()
                        self.setSetting('showLayout', 'showMaximized', layout.key)
                        self.mainUI.signals.states[layout.key] = mode
                elif mode == 'switch':
                    if layout.isHidden():
                        layout.show()
                        self.setSetting('showLayout', 'show', layout.key)
                        self.mainUI.signals.states[layout.key] = mode
                    else:
                        layout.hide()
                        self.setSetting('showLayout', 'hide', layout.key)
                        self.mainUI.signals.states[layout.key] = mode
                elif mode == 'quit' or mode == 'exit':
                    self.exitEvent()
                else:
                    self.logger.report('LayoutModeError: {0} does not have mode: {1}'.format(layoutID, mode))
        else:
            if not layoutID in self.toBuildUis:
                self.logger.report("Layout key does not exists: {0}".format(layoutID))
                self.toBuildUis.append(layoutID)
                self.todoList.update()

    @pyqtSlot(str, str, str, int, name='sysNotify')
    def sysNotify(self, title, mess, iconType, timeDelay):
        if self._trackRecieveSignal:
            self.logger.report('Receive signal sysNotify: {0} {1} {2} {3}'.format(title, mess, iconType, timeDelay))
        return self.layoutManager.sysTray.sysNotify(title, mess, iconType, timeDelay)

    @pyqtSlot(bool, name='loginChanged')
    def loginChanged(self, val):
        self._login = val

        if not self._login:
            self.mainUI.hide()
            self.setSetting('showLayout', 'hide', self.mainUI.key)
            self.mainUI.signals.states[self.mainUI.key] = 'hide'
        else:
            self.mainUI.show()
            self.setSetting('showLayout', 'show', self.mainUI.key)
            self.mainUI.signals.states[self.mainUI.key] = 'show'
            for layout in [self.signIn, self.signUp, self.forgotPassword]:
                if not layout.isHidden():
                    layout.hide()
                    self.setSetting('showLayout', 'hide', layout.key)
                    self.mainUI.signals.states[layout.key] = 'hide'

        self.sysTray.loginChanged(self._login)
        self.signIn.loginChanged(self._login)
        self.signUp.loginChanged(self._login)

        return self._login

    @pyqtSlot(str, name='setStylesheet')
    def set_styleSheet(self, style):
        from cores.StyleSheet import StyleSheet
        self._styleSheet = StyleSheet(style).stylesheet
        self.setStyleSheet(self._styleSheet)
        self.setSetting('styleSheet', style, self.key)

    def signInEvent(self):
        self.switchAccountEvent()

    def signOutEvent(self):
        self.loginChanged(False)
        self.signIn.show()
        self.signUp.hide()
        self.forgotPassword.hide()

    def signUpEvent(self):
        self.loginChanged(False)
        self.signIn.hide()
        self.signUp.show()
        self.forgotPassword.hide()

    def switchAccountEvent(self):
        self.signOutEvent()

if __name__ == '__main__':
    PLM()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 2:26 AM
# © 2017 - 2018 DAMGteam. All rights reserved