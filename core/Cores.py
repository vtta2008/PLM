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
from core.Loggers import Loggers
from assets import __appname__, __version__, __website__
from bin.scr.element import DObj


class CoreApplication(DObj):                                                    # Core metadata

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

class AppCores(DObj):

    key = 'coreService'

    showLayout = pyqtSignal(str, str)
    executing = pyqtSignal(str)
    setSetting = pyqtSignal(str, str, str)
    openBrowser = pyqtSignal(str)
    addLayout = pyqtSignal(object)

    def __init__(self, settings, parent=None):

        DObj.__init__(self)
        super(AppCores, self).__init__(parent)

        logger              = Loggers()
        self.report         = logger.report
        self._parent        = parent

        self.layouts        = dict()
        self.layouts['app'] = self

        from assets.PLM.Settings.SettingUI import SettingUI
        self.settingUI = SettingUI()
        self.settings = settings
        self.addLayout.emit(self.settingUI)

    def import_uiSet1(self):

        from assets.PLM import PipelineManager, SysTrayIcon
        from assets.PLM.Funcs import SignUp, SignIn, ForgotPassword

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

        from assets.PLM.Settings import UserSetting
        from assets.PLM.Projects import NewProject
        from assets.PLM.Info import Credit, About, CodeConduct, Contributing, Reference, Version, LicenceMIT
        from assets.PLM.Tools import FindFiles
        from apps.Storyboarder import Screenshot
        from apps.Calendar import NoteReminder
        from apps.Iimageviewer import ImageViewer
        from apps.Dictionary import EnglishDictionary
        from apps.Calendar import Calendar
        from apps.Calculator import Calculator
        from assets.PLM.Menus.config import Preferences, Configuration
        from assets.PLM.Funcs.Tools.TextEditor import TextEditor
        from assets.PLM.NodeGraph import NodeGraph

        self.about = About.About()
        self.calculator = Calculator.Calculator()
        self.calendar = Calendar.Calendar()
        self.codeConduct = CodeConduct.CodeConduct()
        self.configuration = Configuration.Configuration()
        self.contributing = Contributing.Contributing()
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

        self.maindocker.PLMshowLayout.connect(self.showLayout)
        self.maindocker.PLMexecuting.connect(self.executing)
        self.maindocker.PLMaddLayout.connect(self.addLayout)
        self.maindocker.PLMsysNotify.connect(self.sysTray.sysNotify)
        self.maindocker.PLMsetSetting.connect(self.setSetting)
        self.maindocker.PLMopenBrowser.connect(self.openBrowser)

        self.settingdocker.PLMshowLayout.connect(self.showLayout)

    def setupConn2(self):
        for layout in self.set2Layout:
            layout.showLayout.connect(self.showLayout)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/07/2018 - 11:31 AM
# © 2017 - 2018 DAMGteam. All rights reserved