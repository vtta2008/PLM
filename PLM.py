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
import os, sys, subprocess, requests, ctypes, pprint
from core.Metadata import __envKey__

key = __envKey__
ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)))

try:
    os.getenv(key)
except KeyError:
    os.environ[key] = ROOT
else:
    if os.getenv(key) != ROOT:
        os.environ[key] = ROOT

# PyQt5
from ui.Web.PLMBrowser import PLMBrowser
from PyQt5.QtCore import QThreadPool, pyqtSlot, pyqtSignal, QCoreApplication
from PyQt5.QtWidgets import QApplication

# Plm
from core.Configurations import Configurations
from core.Settings import Settings
from core.Cores import AppCores
from core.Loggers import SetLogger
from core.Metadata import __appname__, __version__, __organization__, __website__, __serverCheck__, PLMAPPID
from core.paths import SETTING_FILEPTH
from core.Storage import PObj

from appData.scr._format import ST_FORMAT
from appData.scr._docs import SYSTRAY_UNAVAI

from utilities import Worker
from utilities.localSQL import QuerryDB
from utilities.utils import str2bool, clean_file_ext
from ui.uikits.UiPreset import AppIcon

# -------------------------------------------------------------------------------------------------------------
""" Operation """

class CoreApplication(PObj):                                                    # Core metadata

    key = 'PLM core application'

    def __init__(self, parent=None):
        super(CoreApplication, self).__init__(parent)

        self.organization = __organization__
        self.appName = __appname__
        self.version = __version__
        self.website = __website__

        QCoreApplication.setOrganizationName(self.organization)
        QCoreApplication.setApplicationName(self.appName)
        QCoreApplication.setOrganizationDomain(self.website)
        QCoreApplication.setApplicationVersion(self.version)

        self.cfg = True


class PLM(QApplication):

    key = 'PLM console'
    returnValue = pyqtSignal(str, str)

    def __init__(self):
        super(PLM, self).__init__(sys.argv)

        logger = SetLogger(self)
        self.report = logger.report

        self.appCore = CoreApplication()

        self.layouts = dict()
        self.cfg = Configurations(key, ROOT)
        self.cfg.cfgReport.connect(self.get_report)
        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)

        if not self.cfg.cfgs:
            self.report("Configurations has not completed yet!")
        else:
            self.report("Configurations has completed", **self.cfg.checkInfo)

        from ui.Settings.SettingUI import SettingUI
        self.settingUI = SettingUI(self.settings)

        self.settingUI.showLayout.connect(self.showLayout)

        self.appInfo = self.cfg.appInfo

        self.cores = AppCores(self.settings, self)
        self.cores.addLayout.connect(self.addLayout)
        self.cores.showLayout.connect(self.showLayout)
        self.cores.executing.connect(self.executing)
        self.cores.setSetting.connect(self.setSetting)
        self.cores.openBrowser.connect(self.openBrowser)

        self.threadpool = QThreadPool()                                                     # Thread pool
        self.numOfThread = self.threadpool.maxThreadCount()                                 # Maximum threads available

        self.setWindowIcon(AppIcon("Logo"))                                                 # Set up task bar icon
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(PLMAPPID)             # Change taskbar icon

        self.addLayout(self.settingUI)
        self.db = QuerryDB()                                                                # Query local database
        self.webBrowser = PLMBrowser()                                                      # Webbrowser
        self.addLayout(self.webBrowser)
        self.webBrowser.showLayout.connect(self.showLayout)

        self.login, self.forgotPW, self.signup, self.mainUI, self.sysTray = self.cores.import_uiSet1()
        self.mainUI.settings = self.settings

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
                    if not self.cores.sysTray.isSystemTrayAvailable():
                        self.report(SYSTRAY_UNAVAI)
                        sys.exit(1)
                    self.showLayout('mainUI', "show")
                else:
                    self.showLayout('login', "show")

        self.sysTray.showLayout.connect(self.showLayout)
        self.sysTray.executing.connect(self.executing)

        self.about, self.calculator, self.calendar, self.codeConduct, self.configuration, self.contributing, \
        self.credit, self.engDict, self.findFile, self.imageViewer, self.licence, self.newProj, self.nodeGraph, \
        self.noteReminder, self.preferences, self.reference, self.screenShot, self.textEditor, self.userSetting, \
        self.version = self.cores.import_uiSet2()

        self.set_styleSheet('darkstyle')
        self.setQuitOnLastWindowClosed(False)
        sys.exit(self.exec_())

    @property
    def registerUI(self):
        return self.layouts

    @pyqtSlot(str, str)
    def showLayout(self, name, mode):
        # self.report('signal comes: {0}, {1}'.format(name, mode))
        if name == 'app':
            layout = self
        else:
            try:
                layout = self.layouts[name]
            except KeyError:
                self.report('Key "{0}" is not registered'.format(name))
                return
            else:
                # self.report("define layout: {0}".format(layout))
                pass

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
        # self.report("{0} layout: {1}".format(mode, layout))

    @pyqtSlot(str)
    def openBrowser(self, url):
        self.webBrowser.setUrl(url)
        self.webBrowser.update()
        self.webBrowser.show()

    @pyqtSlot(str, str, str)
    def setSetting(self, key=None, value=None, grp=None):
        # self.report('signal comes: {0}, {1}, {2}'.format(key, value, grp))
        self.settings.initSetValue(key, value, grp)

    @pyqtSlot(str)
    def executing(self, cmd):
        # self.report('signal comes: {0}'.format(cmd))
        if cmd in self.layouts.keys():
            # self.report('run showlayout: {0}'.format(cmd))
            self.showLayout(cmd, 'show')
        elif os.path.isdir(cmd):
            os.startfile(cmd)
        elif cmd == 'open_cmd':
            # self.report('open command prompt')
            os.system('start /wait cmd')
        elif cmd == 'Remove pyc':
            self.report("clean .pyc files")
            clean_file_ext('.pyc')
        elif cmd == 'Re-config local':
            from appData.LocalCfg import LocalCfg
            # self.report('re config data')
            LocalCfg()
        else:
            # self.report('execute: {0}'.format(cmd))
            subprocess.Popen(cmd)

    @pyqtSlot(object)
    def addLayout(self, layout):
        key = layout.key
        if not key in self.layouts.keys():
            self.layouts[key] = layout
            # self.report("Registered layout '{0}': {1}".format(key, layout))
        else:
            self.report("Already registered: {0}".format(key))

    @pyqtSlot(str)
    def get_report(self, param):
        self.report(param)

    def set_styleSheet(self, style):
        from core.StyleSheets import StyleSheets
        stylesheet = dict(darkstyle=StyleSheets('darkstyle').changeStylesheet, stylesheet=StyleSheets('stylesheet').changeStylesheet, )
        self.setStyleSheet(stylesheet[style])

    def multiThread(self, fn):
        worker = Worker.Worker(fn)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker)
        return worker

    def progress_fn(self, n):
        print("%d%% done" % n)

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE")

    def pPrint(self, obj):
        pprint.pprint(obj)

if __name__ == '__main__':
    PLM()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 2:26 AM
# © 2017 - 2018 DAMGteam. All rights reserved