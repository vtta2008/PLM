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
from PyQt5.QtCore import pyqtSignal, QCoreApplication

# PLM
from core.Loggers import SetLogger
from core.Storage import PObj
from core.Metadata import __organization__, __appname__, __version__, __website__

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

# -------------------------------------------------------------------------------------------------------------
""" Object handle importing task """

class AppCores(PObj):

    key = 'coreService'

    showLayout = pyqtSignal(str, str)
    executing = pyqtSignal(str)
    setSetting = pyqtSignal(str, str, str)
    openBrowser = pyqtSignal(str)
    addLayout = pyqtSignal(object)

    def __init__(self, settings, parent=None):

        PObj.__init__(self)
        super(AppCores, self).__init__(parent)
        logger              = SetLogger()
        self.report         = logger.report
        self._parent        = parent

        self.layouts        = dict()
        self.layouts['app'] = self

        from ui.Settings.SettingUI import SettingUI
        self.settingUI = SettingUI()
        self.settings = settings
        self.addLayout.emit(self.settingUI)

    def import_uiSet1(self):

        from ui import PipelineManager, SysTrayIcon
        from ui.Funcs import SignUp, SignIn, ForgotPassword

        self.login = SignIn.SignIn()
        self.signup = SignUp.SignUp()
        self.forgotPW = ForgotPassword.ForgotPassword()
        self.mainUI = PipelineManager.PipelineManager(self.settings)
        self.sysTray = SysTrayIcon.SysTrayIcon()

        self.setupConn1()

        for layout in [self.login, self.forgotPW, self.signup, self.mainUI, self.sysTray]:
            self.addLayout.emit(layout)

        return self.login, self.forgotPW, self.signup, self.mainUI, self.sysTray

    def import_uiSet2(self):

        from ui.Settings import UserSetting
        from ui.Projects import NewProject
        from ui.Info import Credit, About, CodeConduct, Contrubuting, Reference, Version, LicenceMIT
        from ui.Tools import Screenshot, NoteReminder, ImageViewer, FindFiles, EnglishDictionary, Calendar, Calculator
        from ui.Menus.config import Preferences, Configuration
        from ui.Tools.TextEditor import TextEditor
        from ui.NodeGraph import NodeGraph

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
        self.nodeGraph = NodeGraph.NodeGraph()
        self.noteReminder = NoteReminder.NoteReminder()
        self.preferences = Preferences.Preferences()
        self.reference = Reference.Reference()
        self.screenShot = Screenshot.Screenshot()
        self.textEditor = TextEditor.TextEditor()
        self.userSetting = UserSetting.UserSetting()
        self.version = Version.Version()

        self.set2Layout = [self.about, self.calculator, self.calendar, self.codeConduct, self.configuration,
                           self.contributing, self.credit, self.engDict, self.findFile, self.imageViewer, self.licence,
                           self.newProj, self.nodeGraph, self.noteReminder, self.preferences, self.reference,
                           self.screenShot, self.textEditor, self.userSetting, self.version]

        self.setupConn2()

        for layout in self.set2Layout:
            self.addLayout.emit(layout)

        return self.set2Layout

    @property
    def objects(self):
        return self.layouts

    def setupConn1(self):

        self.login.showLayout.connect(self.showLayout)
        self.forgotPW.showLayout.connect(self.showLayout)
        self.signup.showLayout.connect(self.showLayout)

        self.mainUI.showLayout.connect(self.showLayout)
        self.mainUI.executing.connect(self.executing)
        self.mainUI.addLayout.connect(self.addLayout)
        self.mainUI.sysNotify.connect(self.sysTray.sysNotify)
        self.mainUI.setSetting.connect(self.setSetting)
        self.mainUI.openBrowser.connect(self.openBrowser)

        self.settingUI.showLayout.connect(self.showLayout)

    def setupConn2(self):
        for layout in self.set2Layout:
            layout.showLayout.connect(self.showLayout)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/07/2018 - 11:31 AM
# © 2017 - 2018 DAMGteam. All rights reserved