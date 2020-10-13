# -*- coding: utf-8 -*-
"""

Script Name: AppBase.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
__globalServer__        = "https://server.damgteam.com"
__globalServerCheck__   = "https://server.damgteam.com/check"
__globalServerAutho__   = "https://server.damgteam.com/auth"

__localPort__           = "20987"
__localHost__           = "http://localhost:"
__localServer__         = "{0}{1}".format(__localHost__, __localPort__)
__localServerCheck__    = "{0}/check".format(__localServer__)
__localServerAutho__    = "{0}/auth".format(__localServer__)

# Python
import os, sys, requests

# PLM

from PLM                                import __version__, __appName__, __organization__, __organizationDomain__, APP_LOG

from PLM.configs                        import configPropText, ConfigPipeline
p = configPropText()
from bin.loggers                        import DamgLogger
from PLM.cores                          import sqlUtils, StyleSheet, ThreadManager
from bin.Widgets                        import Application, MessageBox
from bin.Gui                            import LogoIcon
from bin.settings                       import AppSettings
from bin.models                         import SignalManager
from PLM.utils                          import clean_file_ext
from PLM.ui.tools                       import Browser


class AppModel(Application):

    key                                 = 'AppBase'

    _login                              = False
    _styleSheetData                     = None

    _server                             = None
    _verify                             = False

    threadManager                       = None
    eventManager                        = None
    layoutManager                       = None

    plmInfo                             = ConfigPipeline()
    layouts                             = None

    token                               = None
    cookie                              = None

    browser                             = None
    mainUI                              = None
    sysTray                             = None
    shortcutCMD                         = None
    signIn                              = None
    signUp                              = None
    forgotPW                            = None

    def __init__(self, *__args):
        super(AppModel, self).__init__(*__args)

        self.setWindowIcon(LogoIcon("DAMG"))
        self.logger                     = DamgLogger(self, filepth=APP_LOG)
        self.signals                    = SignalManager(self)
        self.browser                    = Browser()
        self.settings                   = AppSettings(self)
        self.settings._settingEnable    = True

        self.database                   = sqlUtils()

        self.setCursorFlashTime(1000)
        self.setQuitOnLastWindowClosed(False)
        self.setDesktopSettingsAware(True)
        self.appStyle                   = StyleSheet(self)
        self.set_styleSheet('dark')

        self.setOrganizationName(__organization__)
        self.setApplicationName(__appName__)
        self.setOrganizationDomain(__organizationDomain__)
        self.setApplicationVersion(__version__)
        self.setApplicationDisplayName(__appName__)

        if not self._server:
            self._server                = self.configServer()

        serverReady                     = self.checkConnectServer()

        if not serverReady:
            print(p['SERVER_CONNECT_FAIL'])
            self.sys_message(None, 'Connection Failed', 'critical', p['SERVER_CONNECT_FAIL'], 'close', None)
            sys.exit()

        self.threadManager              = ThreadManager(self)

    def sys_message(self, parent=None, title="auto", level="auto", message="test message", btn='ok', flag=None):
        messBox = MessageBox(parent, title, level, message, btn, flag)
        return messBox

    def set_styleSheet(self, style):
        self._styleSheetData            = self.appStyle.getStyleSheet(style)
        self.setStyleSheet(self._styleSheetData)
        self.settings.initSetValue('styleSheet', style, self.key)

    def clearStyleSheet(self):
        self._styleSheetData            = None
        self.setStyleSheet(' ')
        self.settings.initSetValue('styleSheet', None, self.key)

    def changeStyleSheet(self, style):
        self.clearStyleSheet()
        self.set_styleSheet(style)

    def run(self):

        """
        avoids some QThread messages in the shell on exit, cancel all running tasks avoid QThread/QTimer error messages,
        on exit

        """
        self.exec_()
        self.deleteLater()

    def checkUserData(self):
        try:
            self.username, self.token, self.cookie, self.remember = self.getUserData()
        except (ValueError, IndexError):
            self.logger.info("There is no user login data")
            self.username, self.token, self.cookie, self.remember = (None, None, None, None)
            return False
        else:
            return True

    def getUserData(self):
        username, token, cookie, remember = self.database.query_table('curUser')
        return username, token, cookie, remember

    def checkConnectServer(self):
        try:
            requests.get(self._server)
        except requests.exceptions.ConnectionError:
            self.logger.info('Cannot connect to server')
            return False
        else:
            return True

    def serverAuthorization(self):
        try:
            r = requests.get(self._server, verify=self.verify, headers=self.getHeaders(), cookies=self.getCookies())
        except Exception:
            self.sys_message(self, 'Offline', p['SERVER_CONNECT_FAIL'], 'crit', 500)
            sys.exit()
        else:
            return r.status_code

    def configServer(self):
        return __localServer__

    def setVerify(self, val):
        self._verify                    = val

    def getHeaders(self):
        return {'Authorization': 'Bearer {0}'.format(self.token)}

    def getCookies(self):
        return {'connect.sid': self.cookie}

    def command(self, key):

        try:
            cmdData = self.plmInfo[key]
        except KeyError:
            return print('There is no key: {0}'.format(key))

        if cmdData.code == 'os.startfile':
            func = os.startfile
            arg = cmdData.value or cmdData['value']
        elif cmdData.code == 'os.system':
            func = os.system
            arg = cmdData.value or cmdData['value']
        elif cmdData.code == 'showUI':
            func = self.showUI
            arg = cmdData.key or cmdData['value']
        elif cmdData.code == 'openURL':
            func = self.openURL
            arg = cmdData.value or cmdData['value']
        elif cmdData.code == 'shortcut':
            func = self.shortcut
            arg = cmdData.value or cmdData['value']
        elif cmdData.code == 'appEvent':
            func = self.appEvent
            arg = cmdData.key or cmdData['value']
        elif cmdData.code == 'stylesheet':
            func = self.changeStyleSheet
            arg = cmdData.value or cmdData['value']
        else:
            if cmdData.value == 'CleanPyc':
                func = clean_file_ext
                arg = 'py'
            elif cmdData.value == 'Debug':
                func = self.mainUI.botTabUI.botTab2.test
                arg = None
            elif cmdData.value == 'Restore':
                func = self.mainUI.showNormal
                arg = None
            elif cmdData.value == 'Maximize':
                func = self.mainUI.showMaximized
                arg = None
            elif cmdData.value == 'Minimize':
                func = self.mainUI.showMinimized
                arg = None
            elif cmdData.value in ['Organisation', 'Project', 'Team', 'Task']:
                func = self.showUI
                arg = '{0}Manager'.format(cmdData.value)
            else:
                func = print
                arg = key

        if arg is None:
            return func()
        else:
            return func(arg)

    def showUI(self, key):
        try:
            ui = self.layouts[key]
        except KeyError:
            return print('There is no layout: {0}'.format(key))
        else:
            return ui.show()

    def loginChanged(self, val):
        self._login = val

        if not self._login:
            self.mainUI.close()
        else:
            self.mainUI.show()
            for layout in [self.signIn, self.signUp, self.forgotPW]:
                layout.close()

        self.sysTray.loginChanged(self._login)
        self.signIn.loginChanged(self._login)
        self.signUp.loginChanged(self._login)

        return self._login

    def showAll(self):
        for ui in self.layouts.values():
            ui.show()

    def closeAll(self):
        for ui in self.layouts.values():
            ui.close()

    def hideAll(self):
        return self.closeAll()

    def appEvent(self, event):
        if event == 'ShowAll':
            self.showAll()
        elif event == 'CloseAll':
            self.closeAll()
        elif event == 'HideAll':
            self.hideAll()
        elif event == 'SwitchAccount':
            self.switchAccountEvent()
        elif event == 'LogIn':
            self.signInEvent()
        elif event == 'LogOut':
            self.signOutEvent()
        elif event == 'Quit':
            self.exitEvent()
        elif event == 'Exit':
            self.exitEvent()
        elif event == 'ChangePassword':
            pass
        else:
            pass

    def signInEvent(self):
        self.switchAccountEvent()

    def signOutEvent(self):
        self.loginChanged(False)
        self.signIn.show()
        for layout in [self.mainUI, self.signUp, self.forgotPW] + self.layoutManager.infos + \
                      self.layoutManager.setts + self.layoutManager.tools + self.layoutManager.prjs:
            layout.hide()

    def signUpEvent(self):
        self.loginChanged(False)
        self.signUp.show()
        for layout in [self.mainUI, self.signUp, self.forgotPW] + self.layoutManager.infos + \
                      self.layoutManager.setts + self.layoutManager.tools + self.layoutManager.prjs:
            layout.hide()

    def switchAccountEvent(self):
        self.signOutEvent()

    def exitEvent(self):
        self.exit()

    @property
    def login(self):
        return self._login

    @property
    def styleSheetData(self):
        return self._styleSheetData

    @property
    def server(self):
        return self._server

    @property
    def verify(self):
        return self._verify

    @styleSheetData.setter
    def styleSheetData(self, val):
        self._styleSheetData            = val

    @login.setter
    def login(self, val):
        self._login                     = val

    @server.setter
    def server(self, val):
        self._server                    = val

    @verify.setter
    def verify(self, val):
        self._verify                    = val

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/16/2020 - 12:05 AM
# © 2017 - 2019 DAMGteam. All rights reserved