# -*- coding: utf-8 -*-
"""

Script Name: PLM.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is master file of Pipeline Manager

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

""" Set up environment variable """

__envKey__ = "DAMGTEAM"

import os, sys

ROOT = os.path.abspath(os.getcwd())

from appData import Configurations
configurations = Configurations(__envKey__, os.path.join(ROOT))

from cores.EnvVariableManager import EnvVariableManager

try:
    os.getenv(__envKey__)
except KeyError:
    cfgable                     = False
    EnvVariableManager(__envKey__, ROOT)
else:
    if os.getenv(__envKey__)   != ROOT:
        EnvVariableManager(__envKey__, ROOT)
    cfgable                     = True

if not cfgable:
    print("CONFIGERROR: environment variable not set.")
    sys.exit()
else:
    if not configurations.cfgs:
        print("CONFIGERROR: configurations have not done yet.")
        sys.exit()
    else:
        print('Configurations has been completed.')

# -------------------------------------------------------------------------------------------------------------
""" import """

# Python
import sys, requests, ctypes

# PyQt5
from PyQt5.QtCore                   import pyqtSlot

# Plm
from ui.Network.ServerConfig        import ServerConfig
from ui.Settings.SettingUI          import SettingUI
from ui.Web.PLMBrowser              import PLMBrowser

from ui                             import LogoIcon, SignalManager

from appData                        import (__localServer__, __localPort__, PLMAPPID, __organization__,
                                            __appname__, __version__, __website__, __globalServer__, SETTING_FILEPTH,
                                            ST_FORMAT, SYSTRAY_UNAVAI)

from cores                          import DAMG, DAMGDICT, StyleSheets, AppCore, ThreadManager, Settings, Loggers
from utils.localSQL                 import QuerryDB
from utils.utils                    import str2bool, clean_file_ext
from ui                             import Application

# -------------------------------------------------------------------------------------------------------------
""" Operation """

class PLM(Application):

    key = 'PLM'

    def __init__(self):
        super(PLM, self).__init__(sys.argv)

        # Run all neccessary configuration to start PLM
        self.configs                = configurations

        self.signals                = SignalManager(self)
        self.logger                 = Loggers(self.__class__.__name__)
        self.settings               = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.report                 = self.logger.report
        self.info                   = self.logger.info
        self.debug                  = self.logger.debug
        self._login                 = False

        self.appCore                = AppCore(__organization__, __appname__, __version__, __website__, self)
        self.appInfo                = self.configs.appInfo  # Configuration data

        # Setup layout manager
        self.layout_manager         = DAMGDICT()

        self.serverConfig           = ServerConfig(self)
        self.regisLayout(self.serverConfig)

        # Multithreading.
        self.thread_manager         = ThreadManager()

        self.settingUI              = SettingUI(self.settings)
        self.database               = QuerryDB()                                    # Database tool
        self.webBrowser             = PLMBrowser()                                  # Webbrowser

        self.set_styleSheet('darkstyle')                                            # Layout style
        self.setWindowIcon(LogoIcon("Logo"))                                         # Set up task bar icon
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(PLMAPPID)     # Change taskbar icon

        self.login                  = self.appCore.login
        self.forgotPW               = self.appCore.forgotPW
        self.signup                 = self.appCore.signup
        self.mainUI                 = self.appCore.mainUI
        self.sysTray                = self.appCore.sysTray

        for layout in [self.login, self.forgotPW, self.signup, self.mainUI, self.sysTray, self.settingUI, self.webBrowser]:
            self.regisLayout(layout)

        for layout in self.mainUI.mainUI_layouts:
            self.regisLayout(layout)

        for layout in self.mainUI.topTabUI.tabLst:
            key = layout.key
            if not key in self.layout_manager.keys():
                self.layout_manager[key] = layout

        try:
            self.username, token, cookie, remember = self.database.query_table('curUser')
        except (ValueError, IndexError):
            self.info("Error occur, can not query data")
            self.showLayout('SignIn', "show")
        else:
            if not str2bool(remember):
                self.showLayout('SignIn', "show")
            else:
                r = requests.get(__localServer__, verify = False, headers = {'Authorization': 'Bearer {0}'.format(token)}, cookies = {'connect.sid': cookie})
                if r.status_code == 200:
                    if not self.appCore.sysTray.isSystemTrayAvailable():
                        self.report(SYSTRAY_UNAVAI)
                        sys.exit(1)
                    self._login = True
                    self.showLayout('PipelineManager', "show")
                else:
                    self.showLayout('SignIn', "show")

        self.about                  = self.appCore.about
        self.calculator             = self.appCore.calculator
        self.calendar               = self.appCore.calendar
        self.codeConduct            = self.appCore.codeConduct
        self.configuration          = self.appCore.configuration
        self.contributing           = self.appCore.contributing
        self.credit                 = self.appCore.credit
        self.engDict                = self.appCore.engDict
        self.findFile               = self.appCore.findFile
        self.imageViewer            = self.appCore.imageViewer
        self.licence                = self.appCore.licence
        self.newProject             = self.appCore.newProject
        self.nodeGraph              = self.appCore.nodeGraph
        self.noteReminder           = self.appCore.noteReminder
        self.preferences            = self.appCore.preferences
        self.reference              = self.appCore.reference
        self.screenShot             = self.appCore.screenShot
        self.textEditor             = self.appCore.textEditor
        self.userSetting            = self.appCore.userSetting
        self.version                = self.appCore.version

        for layout in [self.about, self.calculator, self.calendar, self.codeConduct, self.configuration,
                       self.contributing, self.credit, self.engDict, self.findFile, self.imageViewer, self.licence,
                       self.newProject, self.nodeGraph, self.noteReminder, self.preferences, self.reference,
                       self.screenShot, self.textEditor, self.userSetting, self.version]:

            self.regisLayout(layout)

        self.setQuitOnLastWindowClosed(False)
        sys.exit(self.exec_())

    @property
    def registerUI(self):
        return self.layout_manager

    @property
    def loginState(self):
        return self._login

    @loginState.setter
    def loginState(self, newVal):
        self._login = newVal

    @pyqtSlot(bool)
    def loginChanged(self, newVal):
        self._login = newVal

    @pyqtSlot(str, str)
    def showLayout(self, name, mode):
        if name == 'app':
            layout = self
        elif name in  self.layout_manager.keys():
            layout = self.layout_manager[name]
        else:
            self.info("Layout: '{0}' is not registerred yet.".format(name))
            layout = None

        if mode == "hide":
            # print('hide: {}'.format(layout))
            layout.hide()
            layout.setValue('showLayout', 'hide')
        elif mode == "show":
            # print('show: {}'.format(layout))
            try:
                layout.show()
            except AttributeError:
                pass
            else:
                layout.setValue('showLayout', 'show')

        elif mode == 'showNor':
            layout.showNormal()
            layout.setValue('state', 'showNormal')
        elif mode == 'showMin':
            layout.showMinimized()
            layout.setValue('state', 'showMinimized')
        elif mode == 'showMax':
            layout.showMaximized()
            layout.setValue('state', 'showMaximized')
        elif mode == 'quit' or mode == 'exit':
            layout.quit()

    @pyqtSlot(str)
    def openBrowser(self, url):
        self.webBrowser.setUrl(url)
        self.webBrowser.update()
        self.webBrowser.show()

    @pyqtSlot(str, str, str)
    def setSetting(self, key=None, value=None, grp=None):
        # print("receive setting: configKey: {0}, to value: {1}, in group {2}".format(configKey, value, grp))
        self.settings.initSetValue(key, value, grp)

    @pyqtSlot(str)
    def executing(self, cmd):
        if cmd in self.layout_manager.keys():
            self.signals.showLayout.emit(cmd, 'show')
        elif os.path.isdir(cmd):
            os.startfile(cmd)
        elif cmd in self.configs.appInfo.keys():
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
            self.configs.cfg_mainPkgs()
        elif cmd == 'appExit':
            self.exit()
        else:
            print("This command is not regiested yet: {0}".format(cmd))

    @pyqtSlot(DAMG)
    def regisLayout(self, layout):
        key = layout.key
        if not key in self.layout_manager.keys():
            # self.report("Registing layout: {0} \n {1}".format(configKey, layout))
            self.layout_manager[key] = layout
            layout.signals.openBrowser.connect(self.openBrowser)
            layout.signals.showLayout.connect(self.showLayout)
            layout.signals.executing.connect(self.executing)
            layout.signals.setSetting.connect(self.setSetting)
            layout.signals.regisLayout.connect(self.regisLayout)
        else:
            self.report("Already registered: {0}".format(key))

    @pyqtSlot(str)
    def get_report(self, param):
        self.report(param)

    def set_styleSheet(self, style):
        stylesheet = dict(darkstyle=StyleSheets('dark').changeStylesheet, stylesheet=StyleSheets('bright').changeStylesheet, )
        self.setStyleSheet(stylesheet[style])
        self.settings.initSetValue('styleSheet', 'dark')

    pyqtSlot()
    def closeEvent(self, event):
        self._closing = True
        self.thread_manager.waitForDone()


if __name__ == '__main__':
    PLM()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 2:26 AM
# © 2017 - 2018 DAMGteam. All rights reserved