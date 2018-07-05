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
from os import path, getenv, mkdir

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
from appData import (APPINFO, __appname__, __version__, __organization__, __website__, __serverCheck__, PLMAPPID,
                     SYSTRAY_UNAVAI, __plmWiki__)

from appData.Loggers import SetLogger
logger = SetLogger()

from core.Settings import Settings
from core.Signals import Signals
from utilities import localSQL as usql
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

    def __init__(self):
        super(PlmConsole, self).__init__(sys.argv)

        self.appInfo = APPINFO
        self.appName = __appname__
        self.version = __version__
        self.organization = __organization__
        self.website = __website__
        self.hostCheck = __serverCheck__

        self.PLMcore = QCoreApplication
        self.PLMcore.setApplicationName(self.appName)
        self.PLMcore.setApplicationVersion(self.version)
        self.PLMcore.setOrganizationName(self.organization)
        self.PLMcore.setOrganizationDomain(self.website)

        self.settings = Settings(section='app', parent=self)

        self.threadpool = QThreadPool()
        self.numOfThread = self.threadpool.maxThreadCount()

        self.setWindowIcon(rc.AppIcon("Logo"))                                       # Set up task bar icon
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(PLMAPPID)  # Change taskbar icon in system

        self.import_uiSet1()

        try:
            self.query = usql.QuerryDB()
            self.username, token, cookie, remember = self.query.query_table('curUser')
        except ValueError:
            self.executeSig.emit("Login")
        else:
            if not str2bool(remember):
                self.executeSig.emit("Login")
            else:
                r = requests.get(self.hostCheck, verify=False, headers={'Authorization': 'Bearer {0}'.format(token)}, cookies={'connect.sid': cookie})
                if r.status_code == 200:
                    print(r.status_code)
                    if not QSystemTrayIcon.isSystemTrayAvailable():
                        QMessageBox.critical(None, SYSTRAY_UNAVAI)
                        sys.exit(1)
                    self.executeSig.emit("MainUI")
                    self.updateAvatar.emit(True)

                else:
                    print(r.status_code)
                    self.setValueSig.emit("Login", "True")

        self.import_uiSet2()



        self.settings.saveSetting.emit('stylesheet', 'darkstyle')

        self.setQuitOnLastWindowClosed(False)
        sys.exit(self.exec_())

    def import_uiSet1(self):

        from ui.SignIn import SignIn
        from ui.SignUp import SignUp
        from ui.PipelineManager import PipelineManager
        from ui.SysTrayIcon import SysTrayIcon

        self.MainUI = PipelineManager()
        self.MainUI.hide()

        self.LoginUI = SignIn()
        self.LoginUI.hide()

        self.SignUpUI = SignUp()
        self.SignUpUI.hide()

        self.SysTray = SysTrayIcon()
        self.SysTray.hide()

    def import_uiSet2(self):

        self.browser = PLMBrowser.PLMBrowser()
        self.wiki = PLMBrowser.PLMBrowser(__plmWiki__)

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

    def settingActions(self, mode, key, value):
        if mode == "save":
            self.settings.setValue(key, value)
            logger.warning("Saving setting: {0} = {0}".format(key, value))
            return True
        elif mode == "load":
            val = self.settings.value(key)
            logger.warning("Loading setting: {0}".format(key))
            return val
        elif mode == "change":
            logger.warning("Setting has been modified: {0} = {1}".format(key, value))
            return True


if __name__ == '__main__':
    PlmConsole()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 2:26 AM
# © 2017 - 2018 DAMGteam. All rights reserved