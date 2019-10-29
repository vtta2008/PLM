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

class LayoutManager(DAMGDICT):

    key = 'LayoutManager'

    def __init__(self, parent=None):
        super(LayoutManager, self).__init__(parent)

        self.parent = parent

    def buildLayouts(self):
        self.mains      = self.mainLayouts()
        self.funcs      = self.functionLayouts()

        self.infos      = self.infoLayouts()
        self.setts      = self.settingLayouts()
        self.tools      = self.toolLayouts()
        self.prjs       = self.projectLayouts()

    def functionLayouts(self):
        from ui.Funcs import SignIn, SignUp, ForgotPassword

        self.signin     = SignIn.SignIn()
        self.forgotPW   = ForgotPassword.ForgotPassword()
        self.signup     = SignUp.SignUp()

        for layout in [self.signin, self.signup, self.forgotPW]:
            self.regisLayout(layout)

    def mainLayouts(self):
        from ui import PipelineManager, SysTray

        self.mainUI     = PipelineManager.PipelineManager(self.parent.settings)
        self.sysTray    = SysTray.SysTray()

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
        from ui.Info.InfoWidget import InfoWidget

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
        from ui.Settings import UserSetting, SettingUI

        self.settingUI      = SettingUI.SettingUI(self)
        self.userSetting    = UserSetting.UserSetting()

        layouts = [self.settingUI, self.userSetting]

        for layout in layouts:
            self.regisLayout(layout)

        return layouts

    def toolLayouts(self):
        from ui.Tools import (Screenshot, NoteReminder, ImageViewer, FindFiles, EnglishDictionary,
                              Calendar, Calculator)
        from ui.Tools.NodeGraph import NodeGraph
        from ui.Tools.TextEditor import TextEditor
        from ui.Menus.config import Configuration, Preferences

        self.calculator     = Calculator.Calculator()
        self.calendar       = Calendar.Calendar()
        self.configuration  = Configuration.Configuration()
        self.engDict        = EnglishDictionary.EnglishDictionary()
        self.findFile       = FindFiles.FindFiles()
        self.imageViewer    = ImageViewer.ImageViewer()
        self.nodeGraph      = NodeGraph.NodeGraph()
        self.noteReminder   = NoteReminder.NoteReminder()
        self.preferences    = Preferences.Preferences()
        self.screenShot     = Screenshot.Screenshot()
        self.textEditor     = TextEditor.TextEditor()

        layouts     = [self.calculator, self.calendar, self.configuration, self.engDict, self.findFile,
                       self.imageViewer, self.nodeGraph, self.noteReminder, self.preferences, self.screenShot,
                       self.textEditor]

        for layout in layouts:
            self.regisLayout(layout)

        return layouts

    def projectLayouts(self):
        from ui.Projects import NewProject

        self.newProject     = NewProject.NewProject()

        for layout in [self.newProject, ]:
            self.regisLayout(layout)

    @pyqtSlot(object)
    def regisLayout(self, layout):
        key = layout.key
        if not key in self.keys():
            # self.logger.report("Registing layout: {0} \n {1}".format(configKey, layout))
            self[key] = layout
        else:
            print("Already registered: {0}".format(key))


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/07/2018 - 11:31 AM
# © 2017 - 2018 DAMGteam. All rights reserved