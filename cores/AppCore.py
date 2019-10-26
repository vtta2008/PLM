# -*- coding: utf-8 -*-
"""

Script Name: Cores.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PyQt5
from PyQt5.QtCore           import QCoreApplication

# PLM
from cores.base             import DAMG
from cores.Loggers          import Loggers
from cores.Errors           import BuildingUIError

from ui.Settings.SettingUI  import SettingUI

from ui                     import PipelineManager, SysTrayIcon
from ui.SignalManager           import SignalManager
from ui.Funcs               import SignUp, SignIn, ForgotPassword
from ui.Settings            import UserSetting
from ui.Projects            import NewProject
from ui.Info                import Credit, About, CodeConduct, Contributing, Reference, Version, LicenceMIT
from ui.Tools               import Screenshot, NoteReminder, ImageViewer, FindFiles, EnglishDictionary, Calendar, Calculator
from ui.Menus.config        import Preferences, Configuration
from ui.Tools.TextEditor    import TextEditor
from ui.NodeGraph           import NodeGraph


class AppCore(DAMG):                                                    # Core metadata

    """ Metadata QCoreApplication """

    key = 'PLMCORE'

    def __init__(self, orgName, appName, orgWeb, version, parent=None):
        super(AppCore, self).__init__(parent)

        self.parent         = parent
        self._orgName       = orgName
        self._appName       = appName
        self._orgWeb        = orgWeb
        self._version       = version

        self.settings       = self.parent.settings
        self.logger         = Loggers(__file__)
        self.signals        = SignalManager(self)

        QCoreApplication.setOrganizationName(self._orgName)
        QCoreApplication.setApplicationName(self._appName)
        QCoreApplication.setOrganizationDomain(self._orgWeb)
        QCoreApplication.setApplicationVersion(self._version)

        self.settingUI      = SettingUI(self)

        self.buildUI()
        self.build_connection()
        self.sysTray.signals.regisLayout.emit(self)

    def buildUI(self):

        self.login          = SignIn.SignIn()
        self.forgotPW       = ForgotPassword.ForgotPassword()
        self.signup         = SignUp.SignUp()
        self.mainUI         = PipelineManager.PipelineManager(self.settings)
        self.sysTray        = SysTrayIcon.SysTrayIcon()

        self.about          = About.About()
        self.calculator     = Calculator.Calculator()
        self.calendar       = Calendar.Calendar()
        self.codeConduct    = CodeConduct.CodeConduct()
        self.configuration  = Configuration.Configuration()
        self.contributing   = Contributing.Contributing()
        self.credit         = Credit.Credit()
        self.engDict        = EnglishDictionary.EnglishDictionary()
        self.findFile       = FindFiles.FindFiles()
        self.imageViewer    = ImageViewer.ImageViewer()
        self.licence        = LicenceMIT.LicenceMIT()
        self.newProject     = NewProject.NewProject()
        self.nodeGraph      = NodeGraph.NodeGraph()
        self.noteReminder   = NoteReminder.NoteReminder()
        self.preferences    = Preferences.Preferences()
        self.reference      = Reference.Reference()
        self.screenShot     = Screenshot.Screenshot()
        self.textEditor     = TextEditor.TextEditor()
        self.userSetting    = UserSetting.UserSetting()
        self.version        = Version.Version()

        self._buildUI       = True

        return self._buildUI

    def build_connection(self):

        if self._buildUI:

            self.login.signals.showLayout.connect(self.signals.showLayout)
            self.forgotPW.signals.showLayout.connect(self.signals.showLayout)
            self.signup.signals.showLayout.connect(self.signals.showLayout)
            self.mainUI.signals.showLayout.connect(self.signals.showLayout)
            self.settingUI.signals.showLayout.connect(self.signals.showLayout)
            self.about.signals.showLayout.connect(self.signals.showLayout)
            self.calculator.signals.showLayout.connect(self.signals.showLayout)
            self.calendar.signals.showLayout.connect(self.signals.showLayout)
            self.codeConduct.signals.showLayout.connect(self.signals.showLayout)
            self.configuration.signals.showLayout.connect(self.signals.showLayout)
            self.contributing.signals.showLayout.connect(self.signals.showLayout)
            self.credit.signals.showLayout.connect(self.signals.showLayout)
            self.engDict.signals.showLayout.connect(self.signals.showLayout)
            self.findFile.signals.showLayout.connect(self.signals.showLayout)
            self.imageViewer.signals.showLayout.connect(self.signals.showLayout)
            self.licence.signals.showLayout.connect(self.signals.showLayout)
            self.newProject.signals.showLayout.connect(self.signals.showLayout)
            self.nodeGraph.signals.showLayout.connect(self.signals.showLayout)
            self.noteReminder.signals.showLayout.connect(self.signals.showLayout)
            self.preferences.signals.showLayout.connect(self.signals.showLayout)
            self.reference.signals.showLayout.connect(self.signals.showLayout)
            self.screenShot.signals.showLayout.connect(self.signals.showLayout)
            self.textEditor.signals.showLayout.connect(self.signals.showLayout)
            self.userSetting.signals.showLayout.connect(self.signals.showLayout)
            self.version.signals.showLayout.connect(self.signals.showLayout)

            self.mainUI.signals.executing.connect(self.signals.executing)
            # self.mainUI.signals.regisLayout.connect(self.signals.regisLayout)
            self.mainUI.signals.sysNotify.connect(self.sysTray.signals.sysNotify)
            self.mainUI.signals.setSetting.connect(self.signals.setSetting)
            self.mainUI.signals.openBrowser.connect(self.signals.openBrowser)

        else:
            raise BuildingUIError("UI is not built to connect")

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/07/2018 - 11:31 AM
# © 2017 - 2018 DAMGteam. All rights reserved