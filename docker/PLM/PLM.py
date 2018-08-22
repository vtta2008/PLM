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

import os

ROOT = os.path.abspath(os.getcwd())

from docker.Configurations import ConfigSystem
CFG = ConfigSystem(ROOT, 'alpha')

# -------------------------------------------------------------------------------------------------------------
""" import """

# Python
import sys, subprocess, requests, ctypes, pprint

# PyQt5
from PyQt5.QtCore       import QThreadPool, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets    import QApplication

# Plm
from ui.Web.PLMBrowser  import PLMBrowser
from ui.uikits.UiPreset import AppIcon

from core.StyleSheets   import StyleSheets
from core.Settings      import Settings
from core.Cores         import AppCores, CoreApplication
from core.Loggers       import SetLogger
from core.Metadata      import __serverCheck__, PLMAPPID
from core.paths         import SETTING_FILEPTH, ST_FORMAT
from core.Worker        import Worker

from docker.data._docs import SYSTRAY_UNAVAI

from docker.data.localSQL import QuerryDB
from docker.utils import str2bool, clean_file_ext, get_file_path

pths = get_file_path(os.path.join(os.getcwd(), 'tankers'))
pprint.pprint(pths)

# -------------------------------------------------------------------------------------------------------------
""" Operation """

class PLM(QApplication):

    key = 'PLM console'
    returnValue = pyqtSignal(str, str)

    def __init__(self):
        super(PLM, self).__init__(sys.argv)

        logger = SetLogger(self)
        self.report = logger.report

        self.appCore = CoreApplication()

        self.layouts = dict()
        self.cfg = CFG
        self.cfg.cfgReport.connect(self.get_report)
        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)

        if not self.cfg.cfgs:
            self.report("Configurations has not completed yet!")
        else:
            self.report("Configurations has completed", **self.cfg.cfgInfo)

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
        except (ValueError, IndexError):
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
        if name == 'app':
            layout = self
        else:
            try:
                layout = self.layouts[name]
            except KeyError:
                self.report('Key "{0}" is not registered'.format(name))
                return
            else:
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

    @pyqtSlot(str)
    def openBrowser(self, url):
        self.webBrowser.setUrl(url)
        self.webBrowser.update()
        self.webBrowser.show()

    @pyqtSlot(str, str, str)
    def setSetting(self, key=None, value=None, grp=None):
        self.settings.initSetValue(key, value, grp)

    @pyqtSlot(str)
    def executing(self, cmd):
        if cmd in self.layouts.keys():
            self.showLayout(cmd, 'show')
        elif os.path.isdir(cmd):
            os.startfile(cmd)
        elif cmd == 'open_cmd':
            os.system('start /wait cmd')
        elif cmd == 'Remove pyc':
            self.report("clean .pyc files")
            clean_file_ext('.pyc')
        elif cmd == 'Re-config local':
            self.cfg.cfg_mainPkgs()
        else:
            subprocess.Popen(cmd)

    @pyqtSlot(object)
    def addLayout(self, layout):
        key = layout.key
        if not key in self.layouts.keys():
            self.layouts[key] = layout
        else:
            self.report("Already registered: {0}".format(key))

    @pyqtSlot(str)
    def get_report(self, param):
        self.report(param)

    def set_styleSheet(self, style):
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