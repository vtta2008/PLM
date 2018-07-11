# -*- coding: utf-8 -*-
"""

Script Name: Cores.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys, subprocess

# PyQt5
from PyQt5.QtCore import QObject, QCoreApplication, pyqtSlot, pyqtSignal

# Plm
from appData import __appname__, __version__, __organization__, __website__
from core.Loggers import SetLogger
from core.Specs import Specs

class AppCores(QObject):

    key = 'core'
    returnValue = pyqtSignal(str, str)
    addLayout = pyqtSignal(object)

    def __init__(self, parent=None):
        super(AppCores, self).__init__(parent)
        self.logger = SetLogger(self)
        self.specs = Specs(self.key, self)

        self.appName      = __appname__
        self.version      = __version__
        self.organization = __organization__
        self.website      = __website__
        self._parent      = parent

        self.pCore = QCoreApplication
        self.initMetadata()

        self.layouts = dict()
        self.layouts['app'] = self
        from ui.Web.PLMBrowser import PLMBrowser
        self.webBrowser = PLMBrowser()  # Webbrowser
        self.register_layout(self.webBrowser)
        self.addLayout.emit(self.webBrowser)

        from ui.Settings.SettingUI import SettingUI
        self.settingUI = SettingUI()
        self.settings = self.settingUI.settings
        self.register_layout(self.settingUI)

    def initMetadata(self):
        self.pCore.setApplicationName(self.appName)
        self.pCore.setApplicationVersion(self.version)
        self.pCore.setOrganizationName(self.organization)
        self.pCore.setOrganizationDomain(self.website)
        self.logger.info("Finish setup application metadata")

    def import_uiSet1(self):

        from ui import PipelineManager, SysTrayIcon
        from ui.Funcs import SignIn
        from ui.Funcs import SignUp

        self.login = SignIn.SignIn()
        self.signup = SignUp.SignUp()
        self.mainUI = PipelineManager.PipelineManager()
        self.sysTray = SysTrayIcon.SysTrayIcon()

        for layout in [self.login, self.signup, self.mainUI, self.sysTray]:
            self.register_layout(layout)

        return self.login, self.signup, self.mainUI, self.sysTray

    def import_uiSet2(self):

        from ui.Settings import UserSetting
        from ui.Projects import NewProject
        from ui.Info import Credit, About
        from ui.Tools import Screenshot, NoteReminder, ImageViewer, FindFiles, EnglishDictionary, Calendar, Calculator
        from ui.Menus.config import Preferences, Configuration
        from ui.TextEditor import TextEditor

        self.about = About.About()
        self.calculator = Calculator.Calculator()
        self.calendar = Calendar.Calendar()
        self.preferences = Preferences.Preferences()
        self.configuration = Configuration.Configuration()
        self.credit = Credit.Credit()
        self.engDict = EnglishDictionary.EnglishDictionary()
        self.imageViewer = ImageViewer.ImageViewer()
        self.newProj = NewProject.NewProject()
        self.noteReminder = NoteReminder.NoteReminder()
        self.findFile = FindFiles.FindFiles()
        self.screenShot = Screenshot.Screenshot()
        self.textEditor = TextEditor.TextEditor()
        self.userSetting = UserSetting.UserSetting()

        self.set2Layout = [self.about, self.calculator, self.calendar, self.preferences, self.configuration, self.credit,
                           self.engDict, self.imageViewer, self.newProj, self.noteReminder, self.findFile, self.screenShot,
                           self.textEditor, self.userSetting]

        for layout in self.set2Layout:
            self.addLayout.emit(layout)

        return self.set2Layout

    @property
    def objects(self):
        return self.layouts

    @pyqtSlot(object)
    def register_layout(self, layout):
        key = layout.key
        if not key in self.layouts.keys():
            self.layouts[key] = layout
            self.addLayout.emit(layout)
            # self.logger.debug("Registered layout '{0}': {1}".format(key, layout))

        # self.logger.debug("Already registered: {0}".format(key))

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/07/2018 - 11:31 AM
# © 2017 - 2018 DAMGteam. All rights reserved