# -*- coding: utf-8 -*-
"""

Script Name: AppBase.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
from PLM import globalSetting

import os, sys, requests

from PLM.configs                        import __localServer__, __google__, STAY_ON_TOP, SERVER_CONNECT_FAIL
from PLM.utils                          import LocalDatabase, clean_file_ext
from PLM.ui.layouts.SplashUI import SplashUI
from PLM.ui.models.ThreadManager        import ThreadManager
from PLM.ui.models.LayoutManager        import LayoutManager
from PLM.ui.tools.Browser import Browser
from PLM.commons.Widgets                import Application


class AppModel(Application):

    key                                 = 'AppBase'

    def __init__(self):
        Application.__init__(self)

        if not self._server:
            self._server                = self.configServer()

        serverReady                     = self.checkConnectServer()

        if not serverReady:
            if not globalSetting.modes.allowLocalMode:
                self.messageBox(None, 'Connection Failed', 'critical', SERVER_CONNECT_FAIL, 'close')
                sys.exit()

        self.splash                     = SplashUI(self)

        self.iconInfo                   = self.splash.iconInfo
        self.appInfo                    = self.splash.appInfo
        self.urlInfo                    = self.splash.urlInfo
        self.dirInfo                    = self.splash.dirInfo
        self.pthInfo                    = self.splash.pthInfo
        self.plmInfo                    = self.splash.plmInfo
        self.deviceInfo                 = self.splash.deviceInfo
        self.pythonInfo                 = self.splash.pythonInfo
        self.avatarInfo                 = self.splash.avatarInfo
        self.logoInfo                   = self.splash.logoInfo
        self.imageInfo                  = self.splash.imageInfo
        self.envInfo                    = self.splash.envInfo
        self.serverInfo                 = self.splash.serverInfo
        self.formatInfo                 = self.splash.formatInfo

        self.database                   = LocalDatabase()
        self.threadManager              = ThreadManager()
        self.layoutManager              = LayoutManager(self.threadManager, self)
        self.browser                    = Browser()
        self.layoutManager.registLayout(self.browser)

        self.layoutManager.buildLayouts()
        self.layoutManager.globalSetting()

        self.layouts                    = self.layoutManager.register

        self.mainUI, self.sysTray, self.shortcutCMD, self.signIn, self.signUp, self.forgotPW = self.layoutManager.mains

        for layout in [self.mainUI, self.sysTray, self.signIn, self.signUp, self.forgotPW]:
            layout.signals._emitable = True
            layout.signals.connect('loginChanged', self.loginChanged)

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
            if not globalSetting.modes.allowLocalMode:
                self.splash.finish(self.messageBox(self, 'Connection Failed', 'critical', SERVER_CONNECT_FAIL, 'close', STAY_ON_TOP))
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

        print(cmdData.code, cmdData.value)

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

    def showUI(self, key):
        try:
            ui = self.layouts[key]
        except KeyError:
            return print('There is no layout: {0}'.format(key))
        else:
            return ui.show()

    def openURL(self, url=__google__):
        self.browser.setUrl(url)
        self.browser.update()
        self.browser.show()

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

    def sysNotify(self, *arg):
        title, mess, iconType, timeDelay = arg
        return self.sysTray.sysNotify(title, mess, iconType, timeDelay)

    def switchAccountEvent(self):
        self.signOutEvent()

    def exitEvent(self):
        self.exit()


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/16/2020 - 12:05 AM
# © 2017 - 2019 DAMGteam. All rights reserved