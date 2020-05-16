# -*- coding: utf-8 -*-
"""

Script Name: AppBase.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
from PLM import globals

# Python
import os, sys, requests

# PLM
from PLM.cores                          import Loggers, sqlUtils, StyleSheet, ThreadManager
from PLM.cores.models                   import Worker
from PLM.configs                        import (__version__, __appname__, __organization__, __website__, __localServer__,
                                                STAY_ON_TOP, SERVER_CONNECT_FAIL,
                                                ConfigPython, ConfigUrl, ConfigApps, ConfigPipeline, ConfigIcon,
                                                ConfigAvatar, ConfigLogo, ConfigImage, ConfigEnvVar, ConfigMachine,
                                                ConfigServer, ConfigFormats, ConfigDirectory, ConfigPath, ConfigFonts, )
from PLM.api.Widgets import Application, MessageBox
from PLM.api.Gui import LogoIcon

from PLM.utils                          import clean_file_ext
from PLM.ui.layouts                     import SplashUI
from PLM.ui.tools.Browser               import Browser


class AppModel(Application):

    key                                 = 'AppBase'

    _login                              = False
    _styleSheetData                     = None

    _server                             = None
    _verify                             = False

    threadManager                       = None
    eventManager                        = None
    layoutManager                       = None

    appInfo                             = None
    plmInfo                             = None
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

    _appID                              = None

    def __init__(self):
        Application.__init__(self)

        self.setWindowIcon(LogoIcon("DAMG"))
        self.logger                     = Loggers(__name__)
        self.browser                    = Browser()
        self.settings._settingEnable    = True
        self.setCursorFlashTime(1000)
        self.setQuitOnLastWindowClosed(False)
        self.setDesktopSettingsAware(True)
        self.appStyle                   = StyleSheet(self)
        self.set_styleSheet('dark')

        self.setOrganizationName(__organization__)
        self.setApplicationName(__appname__)
        self.setOrganizationDomain(__website__)
        self.setApplicationVersion(__version__)
        self.setApplicationDisplayName(__appname__)

        if not self._server:
            self._server                = self.configServer()

        serverReady                     = self.checkConnectServer()

        if not serverReady:
            if not globals.allowLocalMode:
                print(SERVER_CONNECT_FAIL)
                self.sys_message(None, 'Connection Failed', 'critical', SERVER_CONNECT_FAIL, 'close', None)
                sys.exit()

        self.threadManager              = ThreadManager(self)
        self.splash                     = SplashUI(self)
        self.splash.start()

        worker                          = Worker(self.runConfigs)
        self.threadManager.globalInstance().start(worker)

        # self.iconInfo                   = self.splash.iconInfo
        # self.appInfo                    = self.splash.appInfo
        # self.urlInfo                    = self.splash.urlInfo
        # self.dirInfo                    = self.splash.dirInfo
        # self.pthInfo                    = self.splash.pthInfo
        # self.plmInfo                    = self.splash.plmInfo
        # self.deviceInfo                 = self.splash.deviceInfo
        # self.pythonInfo                 = self.splash.pythonInfo
        # self.avatarInfo                 = self.splash.avatarInfo
        # self.logoInfo                   = self.splash.logoInfo
        # self.imageInfo                  = self.splash.imageInfo
        # self.envInfo                    = self.splash.envInfo
        # self.serverInfo                 = self.splash.serverInfo
        # self.formatInfo                 = self.splash.formatInfo
        # self.fontInfo                   = self.splash.fontInfo

        self.database                   = sqlUtils()

    def sys_message(self, parent=None, title="auto", level="auto", message="test message", btn='ok', flag=None):
        messBox = MessageBox(parent, title, level, message, btn, flag)
        return messBox

    def set_styleSheet(self, style):
        self._styleSheetData            = self.appStyle.getStyleSheet(style)
        self.setStyleSheet(self._styleSheetData)
        self.settings.initSetValue('styleSheet', style, self.key)

    def clearStyleSheet(self):
        self._styleSheetData            = None
        self.setStyleSheet(self._styleSheetData)
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
            r = requests.get(self._server, verify=self.getVerify(), headers=self.getHeaders(), cookies=self.getCookies())
        except Exception:
            if not globals.modes.allowLocalMode:
                self.splash.finish(self.sys_message(self, 'Connection Failed', 'critical', SERVER_CONNECT_FAIL, 'close', STAY_ON_TOP))
                sys.exit()
            else:
                self.sysNotify('Offline', 'Can not connect to Server', 'crit', 500)
                return False
        else:
            return r.status_code

    def configServer(self):
        return __localServer__

    def getVerify(self):
        return self._verify

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
            arg = cmdData.value
        elif cmdData.code == 'os.system':
            func = os.system
            arg = cmdData.value
        elif cmdData.code == 'showUI':
            func = self.showUI
            arg = cmdData.key
        elif cmdData.code == 'openURL':
            func = self.openURL
            arg = cmdData.value
        elif cmdData.code == 'shortcut':
            func = self.shortcut
            arg = cmdData.value
        elif cmdData.code == 'appEvent':
            func = self.appEvent
            arg = cmdData.key
        elif cmdData.code == 'stylesheet':
            func = self.changeStyleSheet
            arg = cmdData.value
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

    def setRecieveSignal(self, bool):
        globals.recieveSignal = bool

    def setBlockSignal(self, bool):
        globals.blockSignal = bool

    def setTrackCommand(self, bool):
        globals.command = bool

    def setRegistLayout(self, bool):
        globals.registLayout = bool

    def runConfigs(self):

        words = ['Python', 'Directories', 'File Paths', 'Urls & Links', 'Environment Variable', 'Icons', 'Avatars',
                 'Logo', 'Images', 'Servers', 'Formats', 'Fonts', 'Local Devices', 'Installed Apps', 'Pipeline Functions']

        configs = [ConfigPython, ConfigDirectory, ConfigPath, ConfigUrl, ConfigEnvVar, ConfigIcon, ConfigAvatar,
                   ConfigLogo, ConfigImage, ConfigServer, ConfigFormats, ConfigFonts, ConfigMachine, ConfigApps,
                   ConfigPipeline]

        for i in range(len(words)):
            if not i == (len(words) - 1):
                # self.splash.setText('Config {0}'.format(words[i]))
                if i == 0:
                    self.pythonInfo = configs[i]()
                elif i == 1:
                    self.dirInfo    = configs[i]()
                elif i == 2:
                    self.pthInfo    = configs[i]()
                elif i == 3:
                    self.urlInfo    = configs[i]()
                elif i == 4:
                    self.envInfo    = configs[i]()
                elif i == 5:
                    self.iconInfo   = configs[i]()
                elif i == 6:
                    self.avatarInfo = configs[i]()
                elif i == 7:
                    self.logoInfo   = configs[i]()
                elif i == 8:
                    self.imageInfo  = configs[i]()
                elif i == 9:
                    self.serverInfo = configs[i]()
                elif i == 10:
                    self.formatInfo = configs[i]()
                elif i == 11:
                    self.fontInfo   = configs[i]()
                elif i == 12:
                    self.deviceInfo = configs[i]()
                elif i == 13:
                    self.appInfo    = configs[i]()
                # self.splash.setProgress(1)
            else:
                self.splash.setText('Config {0}'.format('Pipeline Functions'))
                if self.iconInfo and self.appInfo and self.urlInfo and self.dirInfo and self.pthInfo:
                    self.plmInfo = ConfigPipeline(self.iconInfo, self.appInfo, self.urlInfo, self.dirInfo, self.pthInfo)
                    # self.splash.setProgress(2)
                else:
                    print('Can not conducting Pipeline Functions configurations, some of other configs has not been done yet.')
                    self.app.exit()

        check = True

        for info in [self.pythonInfo, self.dirInfo, self.pthInfo, self.urlInfo, self.envInfo, self.iconInfo,
                     self.avatarInfo, self.logoInfo, self.imageInfo, self.serverInfo, self.formatInfo,
                     self.fontInfo, self.deviceInfo, self.appInfo, self.plmInfo]:
            if not info:
                check = False

        globals.setCfgAll(check)

    @property
    def login(self):
        return self._login

    @property
    def styleSheetData(self):
        return self._styleSheetData

    @property
    def appID(self):
        return self._appID

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

    @appID.setter
    def appID(self, val):
        self._appID                     = val

    @server.setter
    def server(self, val):
        self._server                    = val

    @verify.setter
    def verify(self, val):
        self._verify                    = val

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/16/2020 - 12:05 AM
# © 2017 - 2019 DAMGteam. All rights reserved