# -*- coding: utf-8 -*-
"""

Script Name: PLM.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is master file of Pipeline Manager

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import glsetting
# -------------------------------------------------------------------------------------------------------------
""" import """

# Python
import sys, requests
# print(1)
# PLM
from appData                            import (__localServer__, SYSTRAY_UNAVAI, KEY_RELEASE, SERVER_CONNECT_FAIL,
                                                configs)
from bin                                import DAMGDICT
# print(2)
from utils                              import LocalDatabase
# print(3)
from ui.assets                          import (ActionManager, ButtonManager, RegistryLayout, ThreadManager,
                                                EventManager, Commands)
from ui.LayoutManager                   import LayoutManager
from ui.SubUi.Browser                   import Browser
# print(4)
from toolkits.Application               import Application
from toolkits.Widgets                   import MessageBox
# print(5)

# -------------------------------------------------------------------------------------------------------------
""" Operation """

class DAMGTEAM(Application):

    key                                 = 'PLM'
    dataConfig                          = configs
    count                               = 0
    onlyExists                          = True
    events                              = DAMGDICT()

    def __init__(self):
        Application.__init__(self)

        self.browser                    = Browser()

        # Multithreading.
        self.threadManager              = ThreadManager()
        self.database                   = LocalDatabase()                                            # Database tool

        self.eventManager               = EventManager(self)
        self.buttonManager              = ButtonManager()
        self.actionManager              = ActionManager()
        self.registryLayout             = RegistryLayout()
        self.layoutManager              = LayoutManager(self.registryLayout, self.actionManager, self.buttonManager,
                                                        self.eventManager, self.threadManager, self)

        self.layoutManager.registLayout(self.browser)
        self.layoutManager.buildLayouts()
        self.layoutManager.globalSetting()

        self.signIn                     = self.layoutManager.signin
        self.signUp                     = self.layoutManager.signup
        self.forgotPW                   = self.layoutManager.forgotPW
        self.sysTray                    = self.layoutManager.sysTray
        self.mainUI                     = self.layoutManager.mainUI
        self.shortcutCMD                = self.layoutManager.shortcutCMD

        self.commander                  = Commands(self)
        self.signinEvent                = self.commander.signInEvent
        self.signoutEvent               = self.commander.signOutEvent
        self.signupEvent                = self.commander.signUpEvent
        self.switchEvent                = self.commander.switchAccountEvent

        self.events.add('signin', self.signinEvent)
        self.events.add('signout', self.signoutEvent)
        self.events.add('signup', self.signupEvent)
        self.events.add('switch', self.switchEvent)

        self.loginChanged               = self.commander.loginChanged
        self.ignoreIDs                  = self.commander.ignoreIDs
        self.showLayout                 = self.commander.showLayout

        for layout in self.layoutManager.layouts():
            key = layout.key
            if not key in self.ignoreIDs:
                # print('{0}: start connecting signals'.format(key))
                if key in ['SignIn', 'SignUp', 'SysTray', 'ForgotPassword']:
                    # print('{0}: connect to login event'.format(key))
                    layout.signals.connect('loginChanged', self.commander.loginChanged)
                # print('{0} start connecting show layout'.format(key))
                layout.signals.connect('showLayout', self.commander.showLayout)
                # print('{0} start connecting executing'.format(key))
                layout.signals.connect('executing', self.commander.executing)
                # print('{0} start connecting open browser'.format(key))
                layout.signals.connect('openBrowser', self.commander.openBrowser)
                # print('{0} start connecting set setting'.format(key))
                layout.signals.connect('setSetting', self.commander.setSetting)
                # print('{0} start connecting sys notify'.format(key))
                layout.signals.connect('sysNotify', self.commander.sysNotify)
                # print('{0} setting has been enabled: {1}'.format(key, layout.settings.key))
                layout.settings._settingEnable = True

        try:
            r = requests.get(__localServer__)
        except requests.exceptions.ConnectionError:
            self.logger.info('Cannot connect to server')
            connectServer = False
        else:
            connectServer = True

        try:
            self.username, token, cookie, remember = self.database.query_table('curUser')
        except (ValueError, IndexError):
            self.logger.info("There is no user login data")
            self.username, token, cookie, remember = (None, None, None, None)
            queryUserLogin = False
        else:
            queryUserLogin = True

        if queryUserLogin:
            if connectServer:
                try:
                    r = requests.get(__localServer__, verify=False,
                                     headers={'Authorization': 'Bearer {0}'.format(token)},
                                     cookies={'connect.sid': cookie})
                except Exception:
                    if not glsetting.modes.allowLocalMode:
                        MessageBox(None, 'Connection Failed', 'critical', SERVER_CONNECT_FAIL, 'close')
                        sys.exit()
                    else:
                        self.sysNotify('Offline', 'Can not connect to Server', 'crit', 500)
                        self.showLayout(self.mainUI.key, 'show')
                else:
                    if r.status_code == 200:
                        if not self.sysTray.isSystemTrayAvailable():
                            self.logger.report(SYSTRAY_UNAVAI)
                            self.exitEvent()
                        else:
                            self.loginChanged(True)
                            self.sysTray.log_in()
                            self.showLayout(self.mainUI.key, "show")
                    else:
                        self.signinEvent()
            else:
                if not glsetting.modes.allowLocalMode:
                    MessageBox(None, 'Connection Failed', 'critical', SERVER_CONNECT_FAIL, 'close')
                    sys.exit()
                else:
                    self.sysNotify('Offline', 'Can not connect to Server', 'crit', 500)
                    self.showLayout(self.mainUI.key, 'show')
        else:
            if connectServer:
                self.signinEvent()
            else:
                if not glsetting.modes.allowLocalMode:
                    MessageBox(None, 'Connection Failed', 'critical', SERVER_CONNECT_FAIL, 'close')
                    sys.exit()
                else:
                    self.sysNotify('Offline', 'Can not connect to Server', 'crit', 500)
                    self.showLayout(self.mainUI.key, 'show')

        self.set_styleSheet('dark')


        # if glsetting.modes.login == 'Offline':
        #     self.showLayout(self.mainUI.key, "show")
        # else:
        #     try:
        #         self.username, token, cookie, remember = self.database.query_table('curUser')
        #     except (ValueError, IndexError):
        #         self.logger.info("Error occur, can not query qssPths")
        #         self.signInEvent()
        #     else:
        #         if not str2bool(remember):
        #             self.signInEvent()
        #
        #     try:
        #         r = requests.get(__localServer__, verify = False, headers = {'Authorization': 'Bearer {0}'.format(token)}, cookies = {'connect.sid': cookie})
        #     except Exception:
        #         if not glsetting.modes.allowLocalMode:
        #             MessageBox(None, 'Connection Failed', 'critical', SERVER_CONNECT_FAIL, 'close')
        #             sys.exit()
        #         else:
        #             self.commander.sysNotify('Offline', 'Can not connect to Server', 'crit', 500)
        #             self.showLayout(self.mainUI.key, 'show')
        #     else:
        #         if r.status_code == 200:
        #             if not self.sysTray.isSystemTrayAvailable():
        #                 self.logger.report(SYSTRAY_UNAVAI)
        #                 self.exitEvent()
        #             else:
        #                 self.loginChanged(True)
        #                 self.sysTray.log_in()
        #                 self.showLayout(self.mainUI.key, "show")
        #         else:
        #             self.showLayout('SignIn', "show")

        # self.startLoop()

    def notify(self, receiver, event):
        if event.type() == KEY_RELEASE:
            if event.key() == 16777249 and 32:
                pos = self.cursor.pos()
                self.shortcutCMD.show()
                self.shortcutCMD.move(pos)

        return super(DAMGTEAM, self).notify(receiver, event)

    def sysNotify(self, title, mess, iconType, timeDelay):
        return self.commander.sysNotify(title, mess, iconType, timeDelay)

# print(6)
app = DAMGTEAM()
# print(7)
app.startLoop()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 2:26 AM
# © 2017 - 2018 DAMGteam. All rights reserved