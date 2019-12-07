# -*- coding: utf-8 -*-
"""

Script Name: Commands.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import __envKey__, ROOT, preSetting, __ignoreIDs__, __tobuildUis__, __tobuildCmds__
""" Import """

# Python
import os

# PyQt5
from PyQt5.QtCore                       import pyqtSlot

# PLM
from bin                                import DAMG, DAMGDICT
from appData                            import StateMax, StateMin, StateNormal
from cores.ConfigManager                import ConfigManager
from cores.Settings                     import Settings
from utils                              import clean_file_ext

class Commands(DAMG):

    key                                 = 'Commands'
    exeCount                            = 0
    timeReset                           = 5
    orders                              = DAMGDICT()

    showLayout_old                      = []
    executing_old                       = []
    setSetting_old                      = []
    openBrowser_old                     = []
    sysNotify_old                       = []

    trackRecieveSignal                  = preSetting.tracks.recieveSignal
    trackBlockSignal                    = preSetting.tracks.blockSignal
    trackCommand                        = preSetting.tracks.command
    trackRegistLayout                   = preSetting.tracks.registLayout
    trackJobsTodo                       = preSetting.tracks.jobsToDo
    trackShowLayoutError                = preSetting.tracks.showLayoutError
    trackEvents                         = preSetting.tracks.events

    ignoreIDs                           = __ignoreIDs__()
    toBuildUis                          = __tobuildUis__()
    toBuildCmds                         = __tobuildCmds__()

    TODO                                = dict(toBuildUis=toBuildUis, toBuildCmds=toBuildCmds)

    def __init__(self, app=None):
        super(Commands, self).__init__(app)

        self.app                        = app
        self.mainUI                     = self.app.mainUI
        self.sysTray                    = self.app.sysTray
        self.signIn                     = self.app.signIn
        self.signUp                     = self.app.signUp
        self.forgotPW                   = self.app.forgotPW
        self.registryLayout             = self.app.registryLayout
        self.threadManager              = self.app.threadManager
        self.dataConfig                 = self.app.dataConfig
        self.browser                    = self.app.browser

        self.settings                   = Settings(self)

    @pyqtSlot(str, name='openBrowser')
    def openBrowser(self, url):
        if self.trackRecieveSignal:
            self.logger.report("receive signal open browser: {0}".format(url))

        self.browser.setUrl(url)
        self.browser.update()
        self.browser.show()

    @pyqtSlot(str, str, str, name='setSetting')
    def setSetting(self, key=None, value=None, grp=None):
        if self.trackRecieveSignal:
            self.logger.report("receive signal setSetting: {0}, {1}, {2}".format(key, value, grp))

        self.setSetting_old, repeat = self.checkSignalRepeat(self.setSetting_old, [key, value, grp])
        if not repeat:
            self.settings.initSetValue(key, value, grp)
        else:
            limit = self.timeReset
            if self.threadManager.counter.printCounter:
                self.threadManager.setPrintCounter(False)

            if self.threadManager.counter._countLimited != limit:
                self.threadManager.setCountLimited(limit)

            if not self.threadManager.isCounting():
                self.threadManager.startCounting()

            if self.trackBlockSignal:
                self.logger.report('{3}: block signal setSetting: {0}, {1}, {2}'.format(key, value, grp, self.key))

            return self.countDownReset(limit)

    @pyqtSlot(str, str, name="showLayout")
    def showLayout(self, layoutID, mode):

        self.showLayout_old, repeat = self.checkSignalRepeat(self.showLayout_old, [layoutID, mode])

        if layoutID in ['Organisation', 'Project', 'Team', 'Task']:
            layoutID = '{0}Manager'.format(layoutID)
            repeat = False
        elif mode in ['SignIn', 'SignOut', 'SignUp', 'SwitchAccount']:
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
            layout = self.registryLayout[layoutID]
            if layout.windowState() & StateNormal:
                state = 'showNormal'
            elif layout.windowState() & StateMax:
                state = 'showMaximized'
            elif layout.windowState() & StateMin:
                state = 'showMinimized'
            else:
                state = layout.getValue('showLayout')
        else:
            state = None

        if not repeat:
            if mode == state:
                if self.trackBlockSignal:
                    self.logger.report('{2}: block signal showLayout from {0}: {1}'.format(layoutID, mode, self.key))
                repeat = True
            else:
                if mode == 'show':
                    if state in ['showNormal', 'showRestore']:
                        if self.trackBlockSignal:
                            self.logger.report(
                                '{2}: block signal showLayout from {0}: {1}'.format(layoutID, mode, self.key))
                        repeat = True
                elif mode == 'hide':
                    if state in ['hide', 'showMinimized']:
                        if self.trackBlockSignal:
                            self.logger.report(
                                '{2}: block signal showLayout from {0}: {1}'.format(layoutID, mode, self.key))
                        repeat = True
                if not repeat:
                    if self.trackRecieveSignal:
                        self.logger.report('recieve signal showLayout from {0}: {1}'.format(layoutID, mode))
        else:
            limit = self.timeReset
            if self.threadManager.counter.printCounter:
                self.threadManager.setPrintCounter(False)

            if self.threadManager.counter._countLimited != limit:
                self.threadManager.setCountLimited(limit)

            if not self.threadManager.isCounting():
                self.threadManager.startCounting()

            if self.trackBlockSignal:
                self.logger.report('{2}: block signal showLayout from {0}: {1}'.format(layoutID, mode, self.key))

            return self.countDownReset(limit)

        if layoutID in self.registryLayout.keys():
            if layoutID in self.ignoreIDs:
                if not layoutID in self.toBuildUis:
                    self.logger.report("Layout: '{0}' is not registerred yet.".format(layoutID))
                    self.toBuildUis.append(layoutID)
            else:
                layout = self.registryLayout[layoutID]
                if mode == "hide":
                    layout.hide()
                elif mode == "show":
                    layout.show()
                elif mode == 'showRestore' or mode == 'showNormal':
                    layout.showNormal()
                elif mode == 'showMinimized' or mode == 'showMin':
                    layout.showMinimized()
                elif mode == 'showMaximized' or mode == 'showMax':
                    layout.showMaximized()
                elif mode == 'quit' or mode == 'exit':
                    self.exitEvent()
                else:
                    if layout.isHidden():
                        layout.show()
                        self.setSetting('showLayout', 'show', layout.key)
                        self.mainUI.signals.states[layout.key] = mode
                    else:
                        layout.hide()
                        self.setSetting('showLayout', 'hide', layout.key)
                        self.mainUI.signals.states[layout.key] = mode

                self.setSetting('showLayout', mode, layout.key)
                self.mainUI.signals.states[layout.key] = mode

        else:
            if not layoutID in self.toBuildUis:
                self.logger.report("Layout key does not exists: {0}".format(layoutID))
                self.toBuildUis.append(layoutID)
                self.TODO.update()

    @pyqtSlot(str, str, str, int, name='sysNotify')
    def sysNotify(self, title, mess, iconType, timeDelay):

        self.sysNotify_old, repeat = self.checkSignalRepeat(self.sysNotify_old, [title, mess, iconType, timeDelay])

        if repeat:
            limit = self.timeReset
            if self.threadManager.counter.printCounter:
                self.threadManager.setPrintCounter(False)

            if self.threadManager.counter._countLimited != limit:
                self.threadManager.setCountLimited(limit)

            if not self.threadManager.isCounting():
                self.threadManager.startCounting()

            if self.trackRecieveSignal:
                self.logger.report('Receive signal sysNotify: {0} {1} {2} {3}'.format(title, mess, iconType, timeDelay))

            return self.countDownReset(limit)

        self.sysNotify_old, repeat = self.checkSignalRepeat(self.sysNotify_old, [title, mess, iconType, timeDelay])
        if not repeat:
            return self.layoutManager.sysTray.sysNotify(title, mess, iconType, timeDelay)
        else:
            if self.trackBlockSignal:
                self.logger.report(
                    '{4}: block signal setSetting: {0}, {1}, {2}, {3}'.format(title, mess, iconType, timeDelay,
                                                                              self.key))
            return

    @pyqtSlot(bool, name='loginChanged')
    def loginChanged(self, val):
        self._login = val

        if not self._login:
            self.showLayout(self.mainUI.key, 'hide')
            self.mainUI.signals.states.add(self.mainUI.key, 'hide')
        else:
            self.showLayout(self.mainUI.key, 'show')
            self.mainUI.signals.states.add(self.mainUI.key, 'show')
            for layout in [self.signIn, self.signUp, self.forgotPW]:
                self.showLayout(layout.key, 'hide')
                layout.signals.states.add(layout.key, 'hide')

        self.sysTray.loginChanged(self._login)
        self.signIn.loginChanged(self._login)
        self.signUp.loginChanged(self._login)

        return self._login

    @pyqtSlot(str, name="executing")
    def executing(self, cmd):
        if self.trackRecieveSignal:
            self.logger.report("receive signal executing: {0}".format(cmd))

        self.executing_old, repeat = self.checkSignalRepeat(self.executing_old, [cmd])

        if repeat:
            limit = self.timeReset
            if self.threadManager.counter.printCounter:
                self.threadManager.setPrintCounter(False)

            if self.threadManager.counter._countLimited != limit:
                self.threadManager.setCountLimited(limit)

            if not self.threadManager.isCounting():
                self.threadManager.startCounting()

            if self.trackBlockSignal:
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
            elif cmd == 'dark':
                return self.setStyleSheet(cmd)
            elif cmd == 'bright':
                return self.setStyleSheet(cmd)
            elif cmd == 'chacoal':
                return self.setStyleSheet(cmd)
            elif cmd == 'nuker':
                return self.setStyleSheet(cmd)
            elif cmd == 'showall':
                return self.showAllEvent()
            elif cmd == 'new task create':
                self.updateTaskEvent()
            else:
                if not cmd in self.toBuildCmds.values():
                    if self.trackCommand:
                        self.logger.report("This command is not regiested yet: {0}".format(cmd))
                    self.toBuildCmds[cmd] = cmd
                    return
                else:
                    if self.trackCommand:
                        self.logger.info("This command will be built later.".format(cmd))
                    return

    def signInEvent(self):
        self.switchAccountEvent()

    def signOutEvent(self):
        self.loginChanged(False)
        self.signIn.show()
        for layout in [self.mainUI, self.signUp, self.forgotPW] + self.layoutManager.infos + \
                      self.layoutManager.setts + self.layoutManager.tools + self.layoutManager.prjs:
            self.showLayout(layout.key, 'hide')
            layout.signals.states.add(layout.key, 'hide')

    def signUpEvent(self):
        self.loginChanged(False)
        self.showLayout(self.signUp, 'show')
        self.signUp.signals.states.add(self.signUp.key, 'show')
        for layout in [self.mainUI, self.signUp, self.forgotPW] + self.layoutManager.infos + \
                      self.layoutManager.setts + self.layoutManager.tools + self.layoutManager.prjs:
            self.showLayout(layout.key, 'hide')
            layout.signals.states.add(layout.key, 'hide')

    def switchAccountEvent(self):
        self.signOutEvent()

    def exitEvent(self):
        if self.trackJobsTodo:
            from pprint import pprint
            pprint(self.TODO)

        states = {}

        for layout in self.layoutManager.layouts():
            if layout.key not in self.ignoreIDs + ['SysTray']:
                self.showLayout(layout.key, 'hide')
                geometry = layout.saveGeometry()
                self.setSetting('geometry', geometry, layout.key)
                states[layout.key] = 'hide'

        self.mainUI.signals.states.appendDict(states)
        self.mainUI.signals.updateState()

        self.exit()

    def showAllEvent(self):
        for layout in self.layoutManager.layouts():
            layout.show()
            self.setSetting('showLayout', 'show', layout.key)
            self.mainUI.signals.states[layout.key] = 'show'

    def hideAllEvent(self):
        for layout in self.layoutManager.layouts():
            layout.hide()
            self.settings('showLayout', 'hide', layout.key)
            self.mainUI.signals.states[layout.key] = 'hide'

    def updateTaskEvent(self):
        print('update task happened')
        self.mainUI.topTabUI.tab1.update_tasks()

    def countDownReset(self, limit):
        self.count += 1
        if self.count == limit:
            self.showLayout_old     = []
            self.executing_old      = []
            self.setSetting_old     = []
            self.openBrowser_old    = []
            self.sysNotify_old      = []

    def checkSignalRepeat(self, old, data):
        new = [i for i in data]

        if len(new) == 0:
            repeat = False
        elif len(new) == len(old):
            repeat = True
            for i in range(len(new)):
                if not new[i] == old[i]:
                    repeat = False
                    break
        else:
            repeat = False

        old = new
        return old, repeat

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/12/2019 - 2:06 PM
# © 2017 - 2018 DAMGteam. All rights reserved