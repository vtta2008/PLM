# -*- coding: utf-8 -*-
"""

Script Name: Cores.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PyQt5
from PyQt5.QtCore           import pyqtSignal, QCoreApplication

# PLM
from cores.base             import DAMG
from ui                     import PipelineManager, SysTrayIcon
from ui.Funcs               import SignUp, SignIn, ForgotPassword
from ui.Settings            import UserSetting
from ui.Projects            import NewProject
from ui.Info                import Credit, About, CodeConduct, Contributing, Reference, Version, LicenceMIT
from ui.Tools               import Screenshot, NoteReminder, ImageViewer, FindFiles, EnglishDictionary, Calendar, Calculator
from ui.Menus.config        import Preferences, Configuration
from ui.Tools.TextEditor    import TextEditor
from ui.NodeGraph           import NodeGraph


class AppStoreage(DAMG):                                                    # Core metadata

    """ Metadata QCoreApplication """

    key = 'PLM core application'

    showLayout              = pyqtSignal(str, str)

    addLayout               = pyqtSignal(DAMG)

    executing               = pyqtSignal(str)

    setSetting              = pyqtSignal(str, str, str)

    openBrowser             = pyqtSignal(str)


    def __init__(self, orgName, appName, orgWeb, version, settings, parent=None):
        super(AppStoreage, self).__init__(parent)

        self._parent        = parent

        self._orgName       = orgName
        self._appName       = appName
        self._orgWeb        = orgWeb
        self._version       = version
        self.settings       = settings

        QCoreApplication.setOrganizationName(self._orgName)
        QCoreApplication.setApplicationName(self._appName)
        QCoreApplication.setOrganizationDomain(self._orgWeb)
        QCoreApplication.setApplicationVersion(self._version)

        self.cfg = True

        from ui.Settings.SettingUI import SettingUI

        self.settingUI      = SettingUI()
        self.settings       = settings

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


        self.login.showLayout.connect(self.showLayout)
        self.forgotPW.showLayout.connect(self.showLayout)
        self.signup.showLayout.connect(self.showLayout)
        self.mainUI.showLayout.connect(self.showLayout)
        self.settingUI.showLayout.connect(self.showLayout)
        self.about.showLayout.connect(self.showLayout)
        self.calculator.showLayout.connect(self.showLayout)
        self.calendar.showLayout.connect(self.showLayout)
        self.codeConduct.showLayout.connect(self.showLayout)
        self.configuration.showLayout.connect(self.showLayout)
        self.contributing.showLayout.connect(self.showLayout)
        self.credit.showLayout.connect(self.showLayout)
        self.engDict.showLayout.connect(self.showLayout)
        self.findFile.showLayout.connect(self.showLayout)
        self.imageViewer.showLayout.connect(self.showLayout)
        self.licence.showLayout.connect(self.showLayout)
        self.newProject.showLayout.connect(self.showLayout)
        self.nodeGraph.showLayout.connect(self.showLayout)
        self.noteReminder.showLayout.connect(self.showLayout)
        self.preferences.showLayout.connect(self.showLayout)
        self.reference.showLayout.connect(self.showLayout)
        self.screenShot.showLayout.connect(self.showLayout)
        self.textEditor.showLayout.connect(self.showLayout)
        self.userSetting.showLayout.connect(self.showLayout)
        self.version.showLayout.connect(self.showLayout)

        self.mainUI.executing.connect(self.executing)

        self.mainUI.addLayout.connect(self.addLayout)

        self.mainUI.sysNotify.connect(self.sysTray.sysNotify)

        self.mainUI.setSetting.connect(self.setSetting)

        self.mainUI.openBrowser.connect(self.openBrowser)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/07/2018 - 11:31 AM
# © 2017 - 2018 DAMGteam. All rights reserved