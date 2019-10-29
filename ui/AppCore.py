# -*- coding: utf-8 -*-
"""

Script Name: Cores.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PyQt5
from PyQt5.QtCore                       import QCoreApplication

# PLM
from cores.base                         import DAMG
from cores.Loggers                      import Loggers
from cores.Errors                       import BuildingUIError
from ui.Web.Browser                  import Browser
from cores.SignalManager                import SignalManager
from ui.PipelineManager                 import PipelineManager
from ui.Funcs.SignIn                    import SignIn
from ui.Funcs.SignUp                    import SignUp
from ui.Funcs.ForgotPassword            import ForgotPassword

from ui.Settings.UserSetting            import UserSetting
from ui.Settings.SettingUI              import SettingUI
from ui.Projects.NewProject             import NewProject

from ui.Tools.Screenshot                import Screenshot
from ui.Tools.NoteReminder              import NoteReminder
from ui.Tools.ImageViewer               import ImageViewer
from ui.Tools.FindFiles                 import FindFiles
from ui.Tools.EnglishDictionary         import EnglishDictionary
from ui.Tools.Calendar                  import Calendar
from ui.Tools.Calculator                import Calculator
from ui.Tools.TextEditor.TextEditor     import TextEditor
from ui.NodeGraph.NodeGraph             import NodeGraph

from ui.SysTray                         import SysTray
from ui.Menus.config.Configuration      import Configuration
from ui.Menus.config.Preferences        import Preferences

from ui.Info.InfoWidget                 import InfoWidget

class AppCore(DAMG):                                                    # Core metadata

    """ Metadata QCoreApplication """

    key = 'PLMCORE'

    def __init__(self, orgName, appName, orgWeb, version, parent=None):
        super(AppCore, self).__init__(parent)

        self.parent                     = parent
        self._orgName                   = orgName
        self._appName                   = appName
        self._orgWeb                    = orgWeb
        self._version                   = version

        self.settings                   = self.parent.settings
        self.logger                     = Loggers(__file__)
        self.signals                    = SignalManager(self)

        self.browser                    = Browser()

        QCoreApplication.setOrganizationName(self._orgName)
        QCoreApplication.setApplicationName(self._appName)
        QCoreApplication.setOrganizationDomain(self._orgWeb)
        QCoreApplication.setApplicationVersion(self._version)

        self.about          = InfoWidget('About')
        self.codeConduct    = InfoWidget('CodeOfConduct')
        self.contributing   = InfoWidget('Contributing')
        self.credit         = InfoWidget("Credit")
        self.licence        = InfoWidget('Licence')
        self.reference      = InfoWidget('Reference')
        self.version        = InfoWidget('Verion')

        self.settingUI      = SettingUI(self)
        self.userSetting    = UserSetting()
        self.newProject     = NewProject()
        self.login          = SignIn()
        self.forgotPW       = ForgotPassword()
        self.signup         = SignUp()

        self.mainUI         = PipelineManager()
        self.sysTray        = SysTray()

        self.calculator     = Calculator()
        self.calendar       = Calendar()
        self.configuration  = Configuration()
        self.engDict        = EnglishDictionary()
        self.findFile       = FindFiles()
        self.imageViewer    = ImageViewer()
        self.nodeGraph      = NodeGraph()
        self.noteReminder   = NoteReminder()
        self.preferences    = Preferences()
        self.screenShot     = Screenshot()
        self.textEditor     = TextEditor()


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/07/2018 - 11:31 AM
# © 2017 - 2018 DAMGteam. All rights reserved