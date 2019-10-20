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

import os, sys
from cores.Metadata import __envKey__
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

# Check for install/update python package required.
# subprocess.Popen('pip install -r requirements.txt', shell=True).wait()

if not cfgable:
    print("CONFIGERROR: environment variable not set !!!")
    sys.exit()

from cores.Configurations import Configurations
configuration = Configurations(__envKey__, os.path.join(ROOT))

# -------------------------------------------------------------------------------------------------------------
""" import """

# Python
import sys, subprocess, requests, ctypes

# PyQt5
from PyQt5.QtCore                   import QTimer, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets                import QApplication

# Plm
from ui.Settings.SettingUI          import SettingUI
from ui.Web.PLMBrowser              import PLMBrowser
from ui.uikits.UiPreset             import AppIcon

from cores.base                     import DAMG, DAMGDICT
from cores.StyleSheets              import StyleSheets
from cores.Settings                 import Settings
from cores.Cores                    import AppStoreage
from cores.Loggers                  import Loggers
from appData                        import __serverLocalCheck__, PLMAPPID, __organization__, __appname__, __version__, __website__
from cores.paths                    import SETTING_FILEPTH, ST_FORMAT
from cores.Task                     import ThreadManager

from appData.documentations._docs   import SYSTRAY_UNAVAI

from utilities.localSQL             import QuerryDB
from utilities.utils                import str2bool, clean_file_ext

# -------------------------------------------------------------------------------------------------------------
""" Operation """

class PLM(QApplication):

    key = 'PLM console'

    returnValue = pyqtSignal(str, str)

    def __init__(self):
        super(PLM, self).__init__(sys.argv)

        self.threadpool             = ThreadManager()                                 # Thread pool

        self.logger                 = Loggers(self)
        self.report                 = self.logger.report
        self.layouts                = DAMGDICT()
        self.configuration          = configuration

        if not self.configuration.cfgs:
            self.report("Configurations has not completed yet!")
        else:
            self.report("Configurations has completed", **self.configuration.cfgInfo)

        self.settings               = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.settingUI              = SettingUI(self.settings)
        self.appCore                = AppStoreage(__organization__, __appname__, __version__, __website__, self.settings, self)

        self.appInfo                = self.configuration.appInfo                    # Configuration data

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

        self.sysTray.showLayout.connect(self.showLayout)
        self.settingUI.showLayout.connect(self.showLayout)
        self.appCore.showLayout.connect(self.showLayout)
        self.webBrowser.showLayout.connect(self.showLayout)

        self.appCore.addLayout.connect(self.addLayout)

        self.configuration.cfgReport.connect(self.get_report)

        self.sysTray.executing.connect(self.executing)
        self.appCore.executing.connect(self.executing)

        self.appCore.setSetting.connect(self.setSetting)

        self.appCore.openBrowser.connect(self.openBrowser)


        for layout in [self.login, self.forgotPW, self.signup, self. mainUI, self.sysTray]:
            self.addLayout(layout)

        try:
            self.username, token, cookie, remember = self.database.query_table('curUser')
        except (ValueError, IndexError):
            self.showLayout('login', "show")
        else:
            if not str2bool(remember):
                self.showLayout('login', "show")
            else:
                r = requests.get(__serverLocalCheck__, verify = False, headers = {'Authorization': 'Bearer {0}'.format(token)}, cookies = {'connect.sid': cookie})
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
            self.addLayout(layout)

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
            configuration.cfg_mainPkgs()
        else:
            subprocess.Popen(cmd)

    @pyqtSlot(DAMG)
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
        stylesheet = dict(darkstyle=StyleSheets('dark').changeStylesheet, stylesheet=StyleSheets('bright').changeStylesheet, )
        self.setStyleSheet(stylesheet[style])

    def progress_fn(self, n):
        print("%d%% done" % n)

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE")

    def closeEvent(self, *args, **kwargs):
        self._closing = True
        self.threadpool.waitForDone()


if __name__ == '__main__':
    PLM()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 2:26 AM
# © 2017 - 2018 DAMGteam. All rights reserved