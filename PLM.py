# -*- coding: utf-8 -*-
"""

Script Name: PLM.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is master file of Pipeline Manager

"""
# -------------------------------------------------------------------------------------------------------------
""" Set up environment variable """

import os
try:
    os.getenv("PIPELINE_MANAGER")
except KeyError:
    os.environ["PIPELINE_MANAGER"] = os.path.join(os.path.dirname(os.path.realpath(__file__)))

# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys, requests, ctypes, subprocess

# PyQt5
from PyQt5.QtCore import QThreadPool, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication

# Plm
from appData import (APPINFO, __serverCheck__, PLMAPPID, SYSTRAY_UNAVAI, SETTING_FILEPTH, ST_FORMAT)

from core.Settings import Settings
from core.Cores import AppCores
from core.Loggers import SetLogger
from core.Specs import Specs
from utilities.localSQL import QuerryDB
from utilities.utils import str2bool
from ui.Web.PLMBrowser import PLMBrowser
from ui.uirc import AppIcon

# -------------------------------------------------------------------------------------------------------------
""" Operation """

class PLM(QApplication):

    key = 'console'
    returnValue = pyqtSignal(str, str)

    def __init__(self):
        super(PLM, self).__init__(sys.argv)

        self.specs = Specs(self.key, self)
        self.appInfo = APPINFO

        self.logger = SetLogger(self)
        self.threadpool = QThreadPool()                                                     # Thread pool
        self.numOfThread = self.threadpool.maxThreadCount()                                 # Maximum threads available
        self.regUI = dict()
        self.regUI['app'] = self
        self.core = AppCores(self)                                                          # Core metadata
        self.webBrowser = PLMBrowser()                                                         # Webbrowser

        self.setWindowIcon(AppIcon("Logo"))                                                 # Set up task bar icon
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(PLMAPPID)             # Change taskbar icon

        self.login, self.signup, self.mainUI, self.sysTray = self.core.import_uiSet1()
        for layout in [self.login, self.signup, self.mainUI, self.sysTray]:
            self.regUI[layout.key] = layout
        self.setupConn1()
        self.settings = self.setting_mode(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)    # Setting
        self.db = QuerryDB()                                                                # Query local database

        try:
            self.username, token, cookie, remember = self.db.query_table('curUser')
        except ValueError:
            self.showLayout('login', "show")
        else:
            if not str2bool(remember):
                self.showLayout('login', "show")
            else:
                r = requests.get(__serverCheck__, verify = False, headers = {'Authorization': 'Bearer {0}'.format(token)}, cookies = {'connect.sid': cookie})
                if r.status_code == 200:
                    if not self.sysTray.isSystemTrayAvailable():
                        self.logger.critical(SYSTRAY_UNAVAI)
                        sys.exit(1)
                    self.showLayout('mainUI', "show")
                else:
                    self.showLayout('login', "show")

        self.about, self.calculator, self.calendar, self.configuration, self.credit, self.engDict,\
        self.imageViewer, self.newProj, self.noteReminder, self.findFile, self.screenShot, self.textEditor, \
        self.userSetting = self.core.import_uiSet2()

        for layout in [self.about, self.calculator, self.calendar, self.configuration, self.credit, self.engDict,
                       self.imageViewer, self.newProj, self.noteReminder, self.findFile, self.screenShot,
                       self.textEditor, self.userSetting]:
            self.regUI[layout.key] = layout

        self.set_styleSheet('darkstyle')
        self.setQuitOnLastWindowClosed(False)
        sys.exit(self.exec_())

    def setupConn1(self):
        self.login.showLayout.connect(self.showLayout)
        self.signup.showLayout.connect(self.showLayout)

        self.mainUI.showLayout.connect(self.showLayout)
        self.mainUI.executing.connect(self.executing)
        self.mainUI.regLayout.connect(self.addRegLayout)
        self.mainUI.sysNotify.connect(self.sysTray.sysNotify)
        self.mainUI.setSetting.connect(self.setSetting)
        self.mainUI.openBrowser.connect(self.openBrowser)
        self.returnValue.connect(self.mainUI.returnValue)

        self.sysTray.showLayout.connect(self.showLayout)
        self.sysTray.executing.connect(self.executing)
        self.webBrowser.showLayout.connect(self.showLayout)

        self.returnValue.connect(self.mainUI.returnValue)

    @property
    def registerUI(self):
        return self.regUI

    @pyqtSlot(str, str)
    def showLayout(self, name, mode):
        if name == 'app':
            layout = QApplication
        else:
            layout = self.regUI[name]
            self.logger.debug("define layout: {0}".format(layout))

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

        self.settings.setValue(layout.objectName(), mode)

    @pyqtSlot(str)
    def openBrowser(self, url):
        self.webBrowser.setUrl(url)
        self.webBrowser.update()
        self.webBrowser.show()

    @pyqtSlot(str, str, str)
    def setSetting(self, key=None, value=None, grp=None):
        self.settings.initSetValue(key, value, grp)

    @pyqtSlot(str, str)
    def loadSetting(self, key=None, grp=None):
        value = self.settings.initValue(key, grp)
        if key is not None:
            self.returnValue.emit(key, value)

    @pyqtSlot(str)
    def executing(self, cmd):
        self.logger.debug('signal comes: {0}'.format(cmd))
        if cmd in self.regUI.keys():
            self.logger.debug('run showlayout: {0}'.format(cmd))
            self.showLayout(cmd, 'show')
        elif os.path.isdir(cmd):
            os.startfile(cmd)
        elif cmd == 'open_cmd':
            os.system('start /wait cmd')
        else:
            self.logger.trace('execute: {0}'.format(cmd))
            subprocess.Popen(cmd)

    @pyqtSlot(str, object)
    def addRegLayout(self, name, layout):

        if not name in self.regUI.keys():
            self.regUI[name] = layout
            self.logger.trace("Registered layout '{0}': {1}".format(name, layout))
        else:
            self.logger.trace("Already registered: {0}".format(name))

    def set_styleSheet(self, style):
        from core.StyleSheets import StyleSheets
        stylesheet = dict(darkstyle=StyleSheets('darkstyle').changeStylesheet,
                          stylesheet=StyleSheets('stylesheet').changeStylesheet, )
        self.setStyleSheet(stylesheet[style])

    def setting_mode(self, filename, fm, parent):
        return Settings(filename, fm, parent)

if __name__ == '__main__':
    PLM()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 2:26 AM
# © 2017 - 2018 DAMGteam. All rights reserved