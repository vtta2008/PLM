# -*- coding: utf-8 -*-
"""

Script Name: Plm.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This script is master file of Pipeline Manager

"""
# -------------------------------------------------------------------------------------------------------------
""" Set up environment variable """

import os
os.environ["PIPELINE_MANAGER"] = os.path.join(os.path.dirname(os.path.realpath(__file__)))

# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import  sys, requests, ctypes, subprocess, qdarkgraystyle, logging, platform

# PyQt5
from PyQt5.QtCore import pyqtSignal, QCoreApplication, QObject, QThreadPool, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMessageBox, QSystemTrayIcon

# Plm
import appData as app
from appData import LocalCfg, MayaCfg   # Generate config info
from appData.logger import SETUP
preset1 = LocalCfg.LocalCfg()
preset2 = MayaCfg.MayaCfg()

from utilities import localSQL as usql
from utilities import Worker
from ui import uirc as rc

# -------------------------------------------------------------------------------------------------------------
""" Convert string to boolean and revert """

def str2bool(arg):
    return str(arg).lower() in ['true', 1, '1', 'ok', '2']

def bool2str(arg):
    if arg:
        return "True"
    else:
        return "False"

def debug_trace():
    """Set a tracepoint in the Python debugger that works with Qt."""
    from PyQt5.QtCore import pyqtRemoveInputHook

    from pdb import set_trace
    pyqtRemoveInputHook()
    set_trace()

def fix_environment():
    """Add enviroment variable on Windows systems."""
    from PyQt5 import __file__ as pyqt_path
    if platform.system() == "Windows":
        pyqt = os.path.dirname(pyqt_path)
        qt_platform_plugins_path = os.path.join(pyqt, "plugins")
        os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qt_platform_plugins_path

verbose = len(sys.argv) > 1 and sys.argv[1] in ('-v', '--verbose')
SETUP(verbose)
log = logging.getLogger(app.LOGPTH)

log.info("Running Python {} on {!r}".format(sys.version_info, sys.platform))
log.info("Running Python {0} on {1}".format(sys.version_info, sys.platform))
log.info(app.VERSION)

fix_environment()

# -------------------------------------------------------------------------------------------------------------
""" Operation """

class PlmConsole(QObject):

    updateAvatar = pyqtSignal(bool)
    start_counting_signal = pyqtSignal(int, str)

    def __init__(self):
        super(PlmConsole, self).__init__()

        self.appSetting = app.appSetting
        self.appInfo = app.APPINFO

        self.threadpool = QThreadPool()
        self.numOfThread = self.threadpool.maxThreadCount()

        self.PLMapp = QApplication(sys.argv)
        self.PLMcore = QCoreApplication

        self.PLMcore.setApplicationName(app.__appname__)
        self.PLMcore.setApplicationVersion(app.__version__)
        self.PLMcore.setOrganizationName(app.__organization__)
        self.PLMcore.setOrganizationDomain(app.__website__)

        self.PLMapp.setWindowIcon(rc.AppIcon("Logo"))                                   # Set up task bar icon
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app.PLMAPPID)     # Change taskbar icon in system
        self.PLMapp.setStyleSheet(qdarkgraystyle.load_stylesheet())                     # set theme

        self.import_uiSet1()
        self.query = usql.QuerryDB()

        try:
            self.username, token, cookie, remember = self.query.query_table('curUser')
        except ValueError:
            self.show_login(True)
        else:
            if not str2bool(remember):
                self.show_login(True)
            else:
                r = requests.get(app.__serverCheck__, verify = False,
                                 headers={'Authorization': 'Bearer {0}'.format(token)},
                                 cookies={'connect.sid': cookie})

                if r.status_code == 200:
                    self.MainUI.showPlt.emit(True)
                    self.updateAvatar.emit(True)
                    if not QSystemTrayIcon.isSystemTrayAvailable():
                        QMessageBox.critical(None, app.SYSTRAY_UNAVAI)
                        sys.exit(1)
                else:
                    self.LoginUI.show()

        self.import_uiSet2()

        QApplication.setQuitOnLastWindowClosed(False)
        sys.exit(self.PLMapp.exec_())

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

    def import_uiSet1(self):
        from ui import (SignIn, SignUp, PipelineManager, SysTrayIcon)

        self.LoginUI = SignIn.SignIn()
        self.LoginUI.showPlt.connect(self.show_plm)
        self.LoginUI.showSignup.connect(self.show_signup)

        self.SignUpUI = SignUp.SignUp()
        self.SignUpUI.showSignup.connect(self.show_signup)

        self.MainUI = PipelineManager.PipelineManager()
        self.MainUI.showPlt.connect(self.show_plm)
        self.MainUI.showLogin.connect(self.show_login)
        self.MainUI.execute.connect(self.execute)
        self.MainUI.timelogSig.connect(usql.TimeLog)
        self.updateAvatar.connect(self.MainUI.updateAvatar)
        self.SignUpUI.showPlt.connect(self.show_plm)

        self.SysTray = SysTrayIcon.SysTrayIcon()
        self.SysTray.showMin.connect(self.MainUI.showMinimized)
        self.SysTray.showMax.connect(self.MainUI.showMaximized)
        self.SysTray.showNor.connect(self.MainUI.showNormal)

    def import_uiSet2(self):

        from ui import (About, Calculator, Calendar, Credit, EnglishDictionary, FindFiles, NewProject, NoteReminder,
                        Configuration, PLMBrowser, Screenshot, TextEditor, UserSetting)

        self.textEditor = TextEditor.TextEditor()
        self.noteReminder = NoteReminder.NoteReminder()
        self.calculator = Calculator.Calculator()
        self.calendar = Calendar.Calendar()
        self.englishDictionary = EnglishDictionary.EnglishDictionary()
        self.findFiles = FindFiles.FindFiles()
        self.screenshot = Screenshot.Screenshot()
        self.preferences = Configuration.Configuration()
        self.about = About.About()
        self.browser = PLMBrowser.PLMBrowser()
        self.wiki = PLMBrowser.PLMBrowser(app.__plmWiki__)
        self.credit = Credit.Credit()
        self.userSetting = UserSetting.UserSetting()
        self.newProject = NewProject.NewProject()

    def show_plm(self, param):
        if param:
            self.MainUI.show()
            self.SysTray.show()
            self.SysTray.log_in()
            self.show_login(not param)
        else:
            self.MainUI.hide()
            self.SysTray.hide()

        self.appSetting.setValue("showPlt", param)

    def show_signup(self, param):
        if param:
            self.SignUpUI.show()
            self.show_login(not param)
        else:
            self.SignUpUI.hide()

        self.appSetting.setValue("showSignUp", param)

    def show_login(self, param):
        if param:
            self.LoginUI.show()
            self.show_plm(not param)
            self.show_signup(not param)
        else:
            self.LoginUI.hide()

        self.appSetting.setValue("showSignIn", param)

    def execute(self, param):
        if param == "Command Prompt":
            os.system("start /wait cmd")
        elif param == "TextEditor":
            self.textEditor.show()
        elif param == "NoteReminder":
            self.noteReminder.show()
        elif param == "Calculator":
            self.calculator.show()
        elif param == "Calendar":
            self.calendar.show()
        elif param == "EnglishDictionary":
            self.englishDictionary.show()
        elif param == "FindFiles":
            self.findFiles.show()
        elif param == "ImageViewer":
            from ui import ImageViewer
            self.imageViewer = ImageViewer.ImageViewer()
            self.imageViewer.show()
        elif param == "Screenshot":
            self.screenshot.show()
        elif param == "Preferences":
            self.preferences.show()
        elif param == "About":
            self.about.show()
        elif param == "PLMBrowser":
            self.browser.show()
        elif param == "PLM wiki":
            self.wiki.show()
        elif param == "Credit":
            self.credit.show()
        elif param == "UserSetting":
            self.userSetting.show()
        elif param == "NewProject":
            self.newProject.show()
        else:
            subprocess.Popen(self.appInfo[param][2])

if __name__ == '__main__':


    PlmConsole()

# ----------------------------------------------------------------------------