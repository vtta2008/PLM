# -*- coding: utf-8 -*-
"""

Script Name: Cores.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python


# PyQt5
from PyQt5.QtCore import QObject, QCoreApplication, pyqtSignal

# Plm
from appData import __appname__, __version__, __organization__, __website__
from core.Loggers import SetLogger
from core.Specs import Specs

class AppCores(QObject):

    key = 'core'

    def __init__(self, parent=None):
        super(AppCores, self).__init__(parent)
        self.logger = SetLogger(self)
        self.specs = Specs(self.key, self)

        self.appName      = __appname__
        self.version      = __version__
        self.organization = __organization__
        self.website      = __website__
        self._parent      = parent
        self.regUI = {}

    def initMetadata(self):
        self.pCore = QCoreApplication
        self.pCore.setApplicationName(self.appName)
        self.pCore.setApplicationVersion(self.version)
        self.pCore.setOrganizationName(self.organization)
        self.pCore.setOrganizationDomain(self.website)
        self.logger.info("Finish set application metadata")
        return True

    def import_uiSet1(self):

        from ui import SignIn, SignUp, PipelineManager, SysTrayIcon

        self.login = SignIn.SignIn()
        self.signup = SignUp.SignUp()
        self.mainUI = PipelineManager.PipelineManager()
        self.sysTray = SysTrayIcon.SysTrayIcon()

        return self.login, self.signup, self.mainUI, self.sysTray

    def import_uiSet2(self):

        from ui import (About, Calculator, Calendar, Configuration, Credit, EnglishDictionary, ImageViewer, NewProject, NoteReminder, FindFiles, Screenshot, UserSetting, )
        from ui.TextEditor import TextEditor

        self.about = About.About()
        self.calculator = Calculator.Calculator()
        self.calendar = Calendar.Calendar()
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

        self.set2Layout = [self.about, self.calculator, self.calendar, self.configuration, self.credit, self.engDict,
                            self.imageViewer, self.newProj, self.noteReminder, self.findFile, self.screenShot,
                            self.textEditor, self.userSetting]

        return self.set2Layout

    def register_layouts(self, layouts):
        for layout in layouts:
            key = layout.name
            self.regUI[key] = layout
            layout.hide()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/07/2018 - 11:31 AM
# © 2017 - 2018 DAMGteam. All rights reserved