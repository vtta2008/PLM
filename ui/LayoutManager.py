# -*- coding: utf-8 -*-
"""

Script Name: Cores.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from PyQt5.QtCore                       import pyqtSlot

# PLM
from cores.base                         import DAMGDICT

from ui.Funcs.SignIn                    import SignIn
from ui.Funcs.SignUp                    import SignUp
from ui.Funcs.ForgotPassword            import ForgotPassword

from ui.PipelineManager                 import PipelineManager
from ui.SysTray                         import SysTray

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
from ui.Tools.NodeGraph.NodeGraph       import NodeGraph

from ui.Menus.config.Configuration      import Configuration
from ui.Menus.config.Preferences        import Preferences

from ui.Info.InfoWidget                 import InfoWidget

class LayoutManager(DAMGDICT):

    key = 'LayoutManager'

    def __init__(self, parent=None):
        super(LayoutManager, self).__init__(self)

        self.parent = parent

        self.mains  = self.mainLayouts()
        self.funcs  = self.functionLayouts()

        self.infos  = self.infoLayouts()
        self.setts  = self.settingLayouts()
        self.tools  = self.toolLayouts()
        self.prjs   = self.projectLayouts()

    def functionLayouts(self):
        self.signin = SignIn()
        self.forgotPW = ForgotPassword()
        self.signup = SignUp()

        for layout in [self.signin, self.signup, self.forgotPW]:
            self.regisLayout(layout)

    def mainLayouts(self):
        self.mainUI = PipelineManager()
        self.sysTray = SysTray()

        layouts = [self.mainUI, self.sysTray]

        for layout in layouts:
            self.regisLayout(layout)

        for layout in self.mainUI.mainUI_layouts:
            self.regisLayout(layout)

        for layout in self.mainUI.topTabUI.tabLst:
            key = layout.key
            if not key in self.keys():
                self[key] = layout

        return layouts

    def infoLayouts(self):
        self.about          = InfoWidget('About')
        self.codeConduct    = InfoWidget('CodeOfConduct')
        self.contributing   = InfoWidget('Contributing')
        self.credit         = InfoWidget("Credit")
        self.licence        = InfoWidget('Licence')
        self.reference      = InfoWidget('Reference')
        self.version        = InfoWidget('Verion')

        layouts = [self.about, self.codeConduct, self.contributing, self.credit, self.licence,
                       self. reference, self.version]

        for layout in layouts:
            self.regisLayout(layout)

        return layouts

    def settingLayouts(self):
        self.settingUI      = SettingUI(self)
        self.userSetting    = UserSetting()

        layouts = [self.settingUI, self.userSetting]

        for layout in layouts:
            self.regisLayout(layout)

        return layouts

    def toolLayouts(self):
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

        layouts     = [self.calculator, self.calendar, self.configuration, self.engDict, self.findFile,
                       self.imageViewer, self.nodeGraph, self.noteReminder, self.preferences, self.screenShot,
                       self.textEditor]

        for layout in layouts:
            self.regisLayout(layout)

        return layouts

    def projectLayouts(self):
        self.newProject     = NewProject()

        for layout in [self.newProject, ]:
            self.regisLayout(layout)

    @pyqtSlot(object)
    def regisLayout(self, layout):
        key = layout.key
        if not key in self.keys():
            # self.logger.report("Registing layout: {0} \n {1}".format(configKey, layout))
            self[key] = layout
            layout.signals.showLayout.connect(self.showLayout)
        else:
            print("Already registered: {0}".format(key))

    @pyqtSlot(str, str)
    def showLayout(self, name, mode):
        if name == 'app':
            layout = self.parent
        elif name in self.keys():
            layout = self[name]
        else:
            print("Layout: '{0}' is not registerred yet.".format(name))
            layout = None
        if mode == "hide":
            # print('hide: {}'.format(layout))
            layout.hide()
            layout.setValue('showLayout', 'hide')
        elif mode == "show":
            # print('show: {}'.format(layout))
            try:
                layout.show()
            except AttributeError:
                pass
            else:
                layout.setValue('showLayout', 'show')

        elif mode == 'showNor':
            layout.showNormal()
            layout.setValue('state', 'showNormal')
        elif mode == 'showMin':
            layout.showMinimized()
            layout.setValue('state', 'showMinimized')
        elif mode == 'showMax':
            layout.showMaximized()
            layout.setValue('state', 'showMaximized')
        elif mode == 'quit' or mode == 'exit':
            layout.quit()


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/07/2018 - 11:31 AM
# © 2017 - 2018 DAMGteam. All rights reserved