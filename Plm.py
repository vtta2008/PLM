# -*- coding: utf-8 -*-
"""

Script Name: PLM.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is master file of Pipeline Manager

"""
# -------------------------------------------------------------------------------------------------------------
""" Set up environment variable """

from os import environ as env
from os import path, system, startfile, getenv

try:
    getenv("PIPELINE_MANAGER")
except KeyError:
    env["PIPELINE_MANAGER"] = path.join(path.dirname(path.realpath(__file__)))

# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys, requests, ctypes, subprocess
from functools import partial

# PyQt5
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QCoreApplication, QThreadPool
from PyQt5.QtWidgets import QApplication, QMessageBox, QSystemTrayIcon

# Plm
import appData as app
from appData.Loggers import SetLogger
logger = SetLogger()

from core.SettingManager import Settings
from utilities import localSQL as usql
from utilities import Worker
from ui import uirc as rc
from core.StyleSheetManager import StyleSheetManager

from ui.Web import PLMBrowser


# -------------------------------------------------------------------------------------------------------------
""" Convert string to boolean and revert """

def str2bool(arg):
    return str(arg).lower() in ['true', 1, '1', 'ok', '2']

# -------------------------------------------------------------------------------------------------------------
""" Operation """

stylesheet = dict(darkstyle = StyleSheetManager('darkstyle').changeStylesheet,
                  stylesheet = StyleSheetManager('stylesheet').changeStylesheet, )

class PlmConsole(QApplication):

    updateAvatar = pyqtSignal(bool)
    resizeSig = pyqtSignal(int, int)
    setValueSig = pyqtSignal(str, str)
    valueSig = pyqtSignal(str)
    executeSig = pyqtSignal(str)

    def __init__(self):
        super(PlmConsole, self).__init__(sys.argv)

        self.appInfo = app.APPINFO
        self.appName = app.__appname__
        self.version = app.__version__
        self.organization = app.__organization__
        self.website = app.__website__
        self.hostCheck = app.__serverCheck__

        self.settings = Settings(section='app', parent=self)
        self.settings.setvalueSig.connect(self.settings_setvalue)

        # self.threadpool = QThreadPool()
        # self.numOfThread = self.threadpool.maxThreadCount()

        self.setWindowIcon(rc.AppIcon("Logo"))                                       # Set up task bar icon
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app.PLMAPPID)  # Change taskbar icon in system

        try:
            self.import_uiSet1()
            self.query = usql.QuerryDB()
            self.username, token, cookie, remember = self.query.query_table('curUser')
        except ValueError:
            self.executeSig.emit("Login")
        else:
            if not str2bool(remember):
                self.show_login(True)
            else:
                r = requests.get(self.hostCheck, verify=False, headers={'Authorization': 'Bearer {0}'.format(token)},
                                 cookies={'connect.sid': cookie})
                if r.status_code == 200:
                    self.executeSig.emit("MainUI")
                    self.updateAvatar.emit(True)
                    if not QSystemTrayIcon.isSystemTrayAvailable():
                        QMessageBox.critical(None, app.SYSTRAY_UNAVAI)
                        sys.exit(1)
                else:
                    self.executeSig.emit("Login")

        self.import_uiSet2()

        self.PLMcore = QCoreApplication
        self.PLMcore.setApplicationName(self.appName)
        self.PLMcore.setApplicationVersion(self.version)
        self.PLMcore.setOrganizationName(self.organization)
        self.PLMcore.setOrganizationDomain(self.website)

        self.settings.setvalueSig.emit('stylesheet', 'darkstyle')

        self.setQuitOnLastWindowClosed(False)
        sys.exit(self.exec_())

    def import_uiSet1(self):

        from ui.SignIn import SignIn
        from ui.SignUp import SignUp
        from ui.PipelineManager import PipelineManager
        from ui.SysTrayIcon import SysTrayIcon

        self.MainUI = PipelineManager()
        self.LoginUI = SignIn()
        self.SignUpUI = SignUp()
        self.SysTray = SysTrayIcon()
        self.LoginUI.showPlt.connect(self.show_plm)
        self.LoginUI.showSignup.connect(self.show_signup)

        self.SignUpUI.showSignup.connect(self.show_signup)

        self.MainUI.showPlt.connect(self.show_plm)
        self.MainUI.showLogin.connect(self.show_login)
        self.MainUI.execute.connect(self.execute)
        self.MainUI.timelogSig.connect(usql.TimeLog)

        self.SignUpUI.showPlt.connect(self.show_plm)

        self.SysTray.showMin.connect(self.MainUI.showMinimized)
        self.SysTray.showMax.connect(self.MainUI.showMaximized)
        self.SysTray.showNor.connect(self.MainUI.showNormal)

        self.executeSig.connect(self.execute)
        # self.resizeSig.connect(self.MainUI.resize)
        self.updateAvatar.connect(self.MainUI.updateAvatar)

    def import_uiSet2(self):

        self.browser = PLMBrowser.PLMBrowser()
        self.wiki = PLMBrowser.PLMBrowser(app.__plmWiki__)

        from ui.About import About
        self.about = About()

        from ui.Configuration import Configuration
        self.configuration = Configuration()

        from ui.Screenshot import Screenshot
        self.screenshot = Screenshot()

        from ui.UserSetting import UserSetting
        self.userSetting = UserSetting()

        from ui.Credit import Credit
        self.credit = Credit()

        from ui.EnglishDictionary import EnglishDictionary
        self.englishDictionary = EnglishDictionary()

        from ui.FindFiles import FindFiles
        self.findFiles = FindFiles()

        from ui.NewProject import NewProject
        self.newProject = NewProject()

        from ui.NoteReminder import NoteReminder
        self.noteReminder = NoteReminder()

        from ui.Calculator import  Calculator
        self.calculator = Calculator()

        from ui.Calendar import Calendar
        self.calendar = Calendar()

        from ui.TextEditor.TextEditor import TextEditor
        self.textEditor = TextEditor()

        from ui.NodeGraph.pNodeGraph import pNodeGraph
        self.NodeGraph = pNodeGraph()

    def show_plm(self, param):
        if param:
            self.show_login(not param)
            self.MainUI.show()
            self.SysTray.show()
            self.SysTray.log_in()
        else:
            self.MainUI.hide()
            self.SysTray.hide()
        self.settings.setValue("showPlt", param)

    def show_signup(self, param):
        if param:
            self.SignUpUI.show()
            self.show_login(not param)
        else:
            self.SignUpUI.hide()
        self.setting.setValue("showSignUp", param)

    def show_login(self, param):
        if param:
            self.show_plm(not param)
            self.show_signup(not param)
            self.LoginUI.show()
        else:
            self.LoginUI.hide()
        self.settings.setValue("showSignIn", param)

    @pyqtSlot(str, str)
    def settings_setvalue(self, key, value):
        if key == 'stylesheet':
            stylesheet = StyleSheetManager(value)
            self.setStyleSheet(stylesheet.changeStylesheet)
        elif key == 'login':
            if value == 'show':
                self.loginUI.show()

    @pyqtSlot(str)
    def execute(self, param):
        print("A signal just came: {0}".format(param))
        if param == "Command Prompt":
            system("start /wait cmd")
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
            from ui.ImageViewer import ImageViewer
            self.imageViewer = ImageViewer()
            self.imageViewer.show()
        elif param == "Screenshot":
            self.screenshot.show()
        elif param == "Preferences":
            self.configuration.show()
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
        elif param == "NodeNetwork":
            self.NodeGraph.show()
        elif param == "Go to config folder":
            startfile(app.CONFIGDIR)
        elif param == "Exit":
            self.quit()
        elif param == "Login":
            self.LoginUI.show()
        elif param == "MainUI":
            self.MainUI.show()
            self.SysTray.show()
        else:
            subprocess.Popen(self.appInfo[param][2])
        return True

if __name__ == '__main__':
    PlmConsole()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 2:26 AM
# © 2017 - 2018 DAMGteam. All rights reserved