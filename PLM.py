# -*- coding: utf-8 -*-
"""

Script Name: PLM.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is master file of Pipeline Manager

"""
# -------------------------------------------------------------------------------------------------------------
""" Set up environment variable """

# Python
import os, sys, subprocess, requests, ctypes, pkg_resources
from core.Loggers import SetLogger
logger = SetLogger()
report = logger.report

key = "PIPELINE_MANAGER"
ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)))

try:
    os.getenv(key)
except KeyError:
    report("Environment key has not been set !!!")
    os.environ[key] = ROOT
    report("set key: {0} = {1}".format(key, os.getenv(key)))
else:
    if not  os.environ[key] == ROOT:
        report("wrong local path directory !!!, relocate environment variable")
        os.environ[key] = ROOT
        report("set key: {0} = {1}".format(key, os.getenv(key)))
    else:
        report("Env key setup corrected")
        report("Environment configuration finished: {0}: {1}".format(key, os.getenv(key)))

# PyQt5
from ui.Web.PLMBrowser import PLMBrowser
from PyQt5.QtCore import QThreadPool, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication

# Plm
from appData import (APPINFO, __serverCheck__, PLMAPPID, SYSTRAY_UNAVAI, SETTING_FILEPTH, ST_FORMAT, __appname__,
                     __version__, __organization__, __website__)

from core.Settings import Settings
from core.Cores import AppCores
from core.Specs import Specs
from utilities.localSQL import QuerryDB
from utilities.utils import str2bool, clean_file_ext
from ui.uikits.UiPreset import AppIcon

# -------------------------------------------------------------------------------------------------------------
""" Operation """

class PLM(QApplication):

    key = 'console'
    returnValue = pyqtSignal(str, str)

    def __init__(self):
        super(PLM, self).__init__(sys.argv)

        self.organization = __organization__
        self.appName = __appname__
        self.version = __version__
        self.website = __website__
        self.core = QApplication
        self.core.setOrganizationName(self.organization)
        self.core.setApplicationName(self.appName)
        self.core.setOrganizationDomain(self.website)
        self.core.setApplicationVersion(self.version)
        self.layouts = dict()

        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.appInfo = APPINFO
        self.specs = Specs(self.key, self)
        self.core = AppCores(self)                                                          # Core metadata

        self.logger = SetLogger(self)
        self.threadpool = QThreadPool()                                                     # Thread pool
        self.numOfThread = self.threadpool.maxThreadCount()                                 # Maximum threads available

        self.setWindowIcon(AppIcon("Logo"))                                                 # Set up task bar icon
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(PLMAPPID)             # Change taskbar icon

        from ui.Settings.SettingUI import SettingUI
        self.settingUI = SettingUI()
        self.core.addLayout.connect(self.addLayout)
        self.addLayout(self.settingUI)
        self.db = QuerryDB()                                                                # Query local database
        self.webBrowser = PLMBrowser()                                                      # Webbrowser
        self.addLayout(self.webBrowser)
        self.login, self.signup, self.mainUI, self.sysTray = self.core.import_uiSet1()
        self.uiSet1 = [self.login, self.signup, self.mainUI, self.sysTray]
        self.mainUI.settings = self.settings
        self.setupConn1()

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
                    if not self.core.sysTray.isSystemTrayAvailable():
                        self.logger.critical(SYSTRAY_UNAVAI)
                        sys.exit(1)
                    self.showLayout('mainUI', "show")
                else:
                    self.showLayout('login', "show")

        self.sysTray.showLayout.connect(self.showLayout)
        self.sysTray.executing.connect(self.executing)

        self.uiSet2 = [self.about, self.calculator, self.calendar, self.codeConduct, self.configuration, self.contributing,
                       self.credit, self.engDict, self.findFile, self.imageViewer, self.licence, self.newProj,
                       self.nodeGraph, self.noteReminder, self.preferences, self.reference, self.screenShot,
                       self.textEditor, self.userSetting, self.version] = self.core.import_uiSet2()

        self.setupConn2()
        self.set_styleSheet('darkstyle')
        self.setQuitOnLastWindowClosed(False)
        sys.exit(self.exec_())

    def setupConn1(self):
        self.login.showLayout.connect(self.showLayout)
        self.signup.showLayout.connect(self.showLayout)

        self.mainUI.showLayout.connect(self.showLayout)
        self.mainUI.executing.connect(self.executing)
        self.mainUI.addLayout.connect(self.addLayout)
        self.mainUI.sysNotify.connect(self.sysTray.sysNotify)
        self.mainUI.setSetting.connect(self.setSetting)
        self.mainUI.openBrowser.connect(self.openBrowser)

        self.returnValue.connect(self.mainUI.returnValue)

        self.webBrowser.showLayout.connect(self.showLayout)
        self.settingUI.showLayout.connect(self.showLayout)

        print("setup connected 1")

        self.returnValue.connect(self.mainUI.returnValue)

    def setupConn2(self):
        for layout in self.uiSet2:
            layout.showLayout.connect(self.showLayout)

        print("setup connected 2")

    @property
    def registerUI(self):
        return self.layouts

    @pyqtSlot(str, str)
    def showLayout(self, name, mode):
        self.logger.trace('signal comes: {0}, {1}'.format(name, mode))
        if name == 'app':
            layout = self
        else:
            layout = self.layouts[name]
            self.logger.trace("define layout: {0}".format(layout))

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
        self.logger.trace("{0} layout: {1}".format(mode, layout))

    @pyqtSlot(str)
    def openBrowser(self, url):
        self.webBrowser.setUrl(url)
        self.webBrowser.update()
        self.webBrowser.show()

    @pyqtSlot(str, str, str)
    def setSetting(self, key=None, value=None, grp=None):
        self.logger.trace('signal comes: {0}, {1}, {2}'.format(key, value, grp))
        self.settings.initSetValue(key, value, grp)

    @pyqtSlot(str, str)
    def loadSetting(self, key=None, grp=None):
        self.logger.trace('signal comes: {0}, {1}'.format(key, grp))
        value = self.settings.initValue(key, grp)
        if key is not None:
            self.returnValue.emit(key, value)

    @pyqtSlot(str)
    def executing(self, cmd):
        self.logger.trace('signal comes: {0}'.format(cmd))
        if cmd in self.layouts.keys():
            self.logger.trace('run showlayout: {0}'.format(cmd))
            self.showLayout(cmd, 'show')
        elif os.path.isdir(cmd):
            os.startfile(cmd)
        elif cmd == 'open_cmd':
            self.logger.trace('open command prompt')
            os.system('start /wait cmd')
        elif cmd == 'Remove pyc':
            self.logger.trace("clean .pyc files")
            clean_file_ext('.pyc')
        elif cmd == 'Re-config local':
            from appData.LocalCfg import LocalCfg
            self.logger.trace('re config data')
            LocalCfg()
        else:
            self.logger.trace('execute: {0}'.format(cmd))
            subprocess.Popen(cmd)

    @pyqtSlot(object)
    def addLayout(self, layout):
        key = layout.key
        if not key in self.layouts.keys():
            self.layouts[key] = layout
            self.logger.debug("Registered layout '{0}': {1}".format(key, layout))
        else:
            self.logger.debug("Already registered: {0}".format(key))

    def set_styleSheet(self, style):
        from core.StyleSheets import StyleSheets
        stylesheet = dict(darkstyle=StyleSheets('darkstyle').changeStylesheet, stylesheet=StyleSheets('stylesheet').changeStylesheet, )
        self.setStyleSheet(stylesheet[style])

if __name__ == '__main__':
    PLM()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 2:26 AM
# © 2017 - 2018 DAMGteam. All rights reserved