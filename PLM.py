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
from cores.sys_config import envVariable

ROOT = os.path.abspath(os.getcwd())

try:
    os.getenv(__envKey__)
except KeyError:
    cfgable                     = False
    envVariable(__envKey__, ROOT)
else:
    if os.getenv(__envKey__)   != ROOT:
        envVariable(__envKey__, ROOT)
    cfgable                     = True

if not cfgable:
    print("CONFIGERROR: environment variable not set !!!")
    sys.exit()


# configuration = Configurations(__envKey__, os.path.join(ROOT))

# -------------------------------------------------------------------------------------------------------------
""" import """

# Python
import sys, requests, ctypes

# PyQt5
from PyQt5.QtCore                   import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets                import QApplication

# Plm
from ui.Network.ServerConfig        import ServerConfig
from ui.Settings.SettingUI          import SettingUI
from ui.Web.PLMBrowser              import PLMBrowser
from ui.uikits.UiPreset             import AppIcon

from appData                        import (__localServer__, __localPort__, __localHost__, PLMAPPID, __organization__,
                                            __appname__, __version__, __website__, __globalServer__, SETTING_FILEPTH,
                                            ST_FORMAT, SYSTRAY_UNAVAI)

from cores.Configurations           import Configurations
from cores.base                     import DAMG, DAMGDICT
from cores.StyleSheets              import StyleSheets
from cores.Settings                 import Settings
from cores.AppCore                  import AppCore
from cores.Loggers                  import Loggers
from cores.Task                     import ThreadManager
from cores.TestConnection           import TestConnection
from utils.localSQL                 import QuerryDB
from utils.utils                    import str2bool, clean_file_ext
from ui.UiSignals import UiSignals

# -------------------------------------------------------------------------------------------------------------
""" Operation """

class PLM(QApplication):

    key = 'PLM console'

    def __init__(self):
        super(PLM, self).__init__(sys.argv)

        # Run all neccessary configuration to start PLM
        self.configs          = Configurations(__envKey__, os.path.join(ROOT))

        # Setting setting tools.
        self.settings               = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)

        self.signals                = UiSignals(self)

        # Setup logging
        self.logger                 = Loggers(__file__)
        self.report                 = self.logger.report
        self.info                   = self.logger.info
        self.debug                  = self.logger.debug

        # Setup layout manager
        self.layout_manager         = DAMGDICT()

        self.serverConfig           = ServerConfig(self)
        self.serverConfig.sendToSetting.connect(self.setSetting)
        self.regisLayout(self.serverConfig)

        # Multithreading.
        self.thread_manager         = ThreadManager()

        # Check server connection.
        # self.serverConnected        = self.server_connect()
        # if not self.serverConnected:
        #     print("No server connection available")
        #     self.serverConfig.show()

        if not self.configs.cfgs:
            self.report("Configurations has not completed yet!")
        else:
            self.report("Configurations has completed", **self.configs.cfgInfo)

        self.settingUI              = SettingUI(self.settings)
        self.appCore                = AppCore(__organization__, __appname__, __version__, __website__, self)

        self.appInfo                = self.configs.appInfo                          # Configuration data

        self.database               = QuerryDB()                                    # Database tool
        self.webBrowser             = PLMBrowser()                                  # Webbrowser

        self.set_styleSheet('darkstyle')                                            # Layout style

        self.setWindowIcon(AppIcon("Logo"))                                         # Set up task bar icon

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(PLMAPPID)     # Change taskbar icon

        self.login                  = self.appCore.login
        self.forgotPW               = self.appCore.forgotPW
        self.signup                 = self.appCore.signup
        self.mainUI                 = self.appCore.mainUI
        self.sysTray                = self.appCore.sysTray

        self.mainUI.signals.showLayout.connect(self.showLayout)
        self.sysTray.signals.showLayout.connect(self.showLayout)
        self.settingUI.signals.showLayout.connect(self.showLayout)
        self.appCore.signals.showLayout.connect(self.showLayout)
        self.webBrowser.signals.showLayout.connect(self.showLayout)

        self.appCore.signals.regisLayout.connect(self.regisLayout)

        self.configs.signals.cfgReport.connect(self.get_report)

        self.sysTray.signals.executing.connect(self.executing)
        self.appCore.signals.executing.connect(self.executing)
        self.appCore.signals.setSetting.connect(self.setSetting)
        self.appCore.signals.openBrowser.connect(self.openBrowser)


        for layout in [self.login, self.forgotPW, self.signup, self. mainUI, self.sysTray, self.settingUI]:
            self.regisLayout(layout)

        try:
            self.username, token, cookie, remember = self.database.query_table('curUser')
        except (ValueError, IndexError):
            self.info("Error occur, can not query data")
            self.signals.showLayout('login', "show")
        else:
            if not str2bool(remember):
                self.signals.showLayout('login', "show")
            else:
                r = requests.get(__localServer__, verify = False, headers = {'Authorization': 'Bearer {0}'.format(token)}, cookies = {'connect.sid': cookie})

                if r.status_code == 200:
                    if not self.appCore.sysTray.isSystemTrayAvailable():
                        self.report(SYSTRAY_UNAVAI)
                        sys.exit(1)
                    self.showLayout('mainUI', "show")
                else:
                    self.showLayout('login', "show")

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

    @pyqtSlot(str, str)
    def showLayout(self, name, mode):
        if name == 'app':
            layout = self
        else:
            try:
                layout = self.layout_manager[name]
            except KeyError:
                self.report('Layout "{0}" is not registered'.format(name))
                return

        if mode == "hide":
            layout.hide()
        elif mode == "show":
            layout.show()
        elif mode == 'showNor':
            layout.showNormal()
        elif mode == 'showMin':
            layout.showMinimized()
        elif mode == 'showMax':
            layout.showMaximized()
        elif mode == 'quit' or mode == 'exit':
            layout.quit()

        self.setSetting(layout.key, mode)

    @pyqtSlot(str)
    def openBrowser(self, url):
        self.webBrowser.setUrl(url)
        self.webBrowser.update()
        self.webBrowser.show()

    @pyqtSlot(str, str, str)
    def setSetting(self, key=None, value=None, grp=None):
        # print("receive setting: key: {0}, to value: {1}, in group {2}".format(key, value, grp))
        self.settings.initSetValue(key, value, grp)

    @pyqtSlot(str)
    def executing(self, cmd):
        if cmd in self.layout_manager.keys():
            self.signals.showLayout(cmd, 'show')
        elif os.path.isdir(cmd):
            os.startfile(cmd)
        elif cmd == 'open_cmd':
            os.system('start /wait cmd')
        elif cmd == 'Remove pyc':
            self.report("clean .pyc files")
            clean_file_ext('.pyc')
        elif cmd == 'Re-config local':
            self.configs.cfg_mainPkgs()
        elif cmd == 'appExit':
            self.exit()
        else:
            print("This command is not regiested yet: {0}".format(cmd))

    @pyqtSlot(DAMG)
    def regisLayout(self, layout):
        key = layout.key
        if not key in self.layout_manager.keys():
            print("Registing layout: {0} \n {1}".format(key, layout))
            self.layout_manager[key] = layout
        else:
            self.report("Already registered: {0}".format(key))

    @pyqtSlot(str)
    def get_report(self, param):
        self.report(param)

    def server_connect(self):

        internet = self.connect_internet()

        serverConfig = self.settings.value('serverConfig')

        if serverConfig is None:
            print("No server config")
            if internet:
                globalConnect = self.connect_global_server()
                if not globalConnect:
                    return self.connect_local_server()
                else:
                    return globalConnect
            else:
                return self.connect_local_server()
        else:
            if serverConfig == 'localServer':
                return self.connect_local_server()
            else:
                return self.connect_global_server()

    def connect_internet(self):
        print("Try to connect internet")
        connection = TestConnection()

        if not connection.connectable:
            print("Connect internet failed.")
            return False
        else:
            print("Connect internet successed.")
            return True

    def connect_local_server(self):
        print("Try to connect local server")
        connection = TestConnection(__localHost__, __localPort__)

        if not connection.connectable:
            print("Connect local server failed.")
            return False
        else:
            print("Connect local server successed.")
            return True

    def connect_global_server(self):
        print("Try to connect global server")
        connection = TestConnection(__globalServer__, None)

        if not connection.connectable:
            print("Connect global sercer failed.")
            return False
        else:
            print("Connect global server successed.")
            return True

    def set_styleSheet(self, style):
        stylesheet = dict(darkstyle=StyleSheets('dark').changeStylesheet, stylesheet=StyleSheets('bright').changeStylesheet, )
        self.setStyleSheet(stylesheet[style])
        self.settings.initSetValue('styleSheet', 'dark')

    def closeEvent(self, *args, **kwargs):
        self._closing = True
        self.thread_manager.waitForDone()


if __name__ == '__main__':
    PLM()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 2:26 AM
# © 2017 - 2018 DAMGteam. All rights reserved