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
        self._parent      = parent

        self.layouts = dict()
        self.layouts['app'] = self


        from ui.Settings.SettingUI import SettingUI
        self.settingUI = SettingUI()
        self.settings = self.settingUI.settings
        self.register_layout(self.settingUI)

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
        from ui.Info import Credit, About, CodeConduct, Contrubuting, Reference, Version, LicenceMIT
        from ui.Tools import Screenshot, NoteReminder, ImageViewer, FindFiles, EnglishDictionary, Calendar, Calculator
        from ui.Menus.config import Preferences, Configuration
        from ui.TextEditor import TextEditor

        self.about = About.About()
        self.calculator = Calculator.Calculator()
        self.calendar = Calendar.Calendar()
        self.codeConduct = CodeConduct.CodeConduct()
        self.configuration = Configuration.Configuration()
        self.contributing = Contrubuting.Contributing()
        self.credit = Credit.Credit()
        self.engDict = EnglishDictionary.EnglishDictionary()
        self.findFile = FindFiles.FindFiles()
        self.imageViewer = ImageViewer.ImageViewer()
        self.licence = LicenceMIT.LicenceMIT()
        self.newProj = NewProject.NewProject()
        self.noteReminder = NoteReminder.NoteReminder()
        self.preferences = Preferences.Preferences()
        self.reference = Reference.Reference()
        self.screenShot = Screenshot.Screenshot()
        self.textEditor = TextEditor.TextEditor()
        self.userSetting = UserSetting.UserSetting()
        self.version = Version.Version()

        self.set2Layout = [self.about, self.calculator, self.calendar, self.codeConduct, self.configuration,
                           self.contributing, self.credit, self.engDict, self.findFile, self.imageViewer, self.licence,
                           self.newProj, self.noteReminder, self.preferences, self.reference, self.screenShot,
                           self.textEditor, self.userSetting, self.version]

        for layout in self.set2Layout:
            self.addLayout.emit(layout)

        return self.set2Layout

    @pyqtSlot(str)
    def redirectConnection(self, param):
        print(param)

    @property
    def objects(self):
        return self.layouts

    @pyqtSlot(object)
    def register_layout(self, layout):
        key = layout.key
        if not key in self.layouts.keys():
            self.layouts[key] = layout
            self.addLayout.emit(layout)
            self.logger.debug("did emit signal to regis layout '{0}': {1}".format(key, layout))

        # self.logger.debug("Already registered: {0}".format(key))

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/07/2018 - 11:31 AM
# © 2017 - 2018 DAMGteam. All rights reserved