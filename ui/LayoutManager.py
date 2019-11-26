# -*- coding: utf-8 -*-
"""

Script Name: Cores.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
from bin.dependencies.damg.damg         import DAMG, DAMGLIST

from PyQt5.QtCore                       import Qt

# PLM
from appData                            import SiPoMin


class LayoutManager(DAMG):

    key                                 = 'LayoutManager'

    _buildAll                           = False

    noShowHideAttrs                     = DAMGLIST()
    unHidableLayouts                    = DAMGLIST()
    unShowableLayouts                   = DAMGLIST()

    def __init__(self, setting, registryLayout, actionManager, buttonManager, eventManager, threadManager, parent=None):
        super(LayoutManager, self).__init__(parent)

        self.parent                     = parent

        self.ignoreIDs                  = self.parent.ignoreIDs

        self.settings                   = setting
        self.actionManager              = actionManager
        self.buttonManager              = buttonManager
        self._register                  = registryLayout
        self.eventManager               = eventManager
        self.threadManager              = threadManager

        self.globalSetting()

    def layouts(self):
        return self._register.values()

    def keys(self):
        return self._register.keys()

    def buildLayouts(self):
        self.mains                      = self.mainLayouts()
        self.funcs                      = self.functionLayouts()

        self.infos                      = self.infoLayouts()
        self.setts                      = self.settingLayouts()
        self.tools                      = self.toolLayouts()
        self.prjs                       = self.projectLayouts()

        tbcbs = self.preferences.headerGrid.toolBarCBs
        tbs = self.mainUI.mainToolBar.tbs

        cncbs = self.preferences.headerGrid.connectCBs
        cns = self.mainUI.connectStatus.labels

        mncbs = self.preferences.headerGrid.menuCBs
        mns = self.mainUI.mainMenuBar.mns

        for i in range(len(tbs)):
            cb = tbcbs[i]
            tb = tbs[i]
            cb.stateChanged.connect(tb.setVisible)
        tbcbs[-1].stateChanged.connect(self.mainUI.mainToolBarSec.setVisible)

        for i in range(len(mncbs)):
            cb = mncbs[i]
            cb.stateChanged.connect(self.mainUI.mainMenuBar.showMenu)
        mncbs[-1].stateChanged.connect(self.mainUI.mainMenuSec.setVisible)

        for i in range(len(cns)):
            cb = cncbs[i]
            lb = cns[i]
            cb.stateChanged.connect(lb.setVisible)
        cncbs[-1].stateChanged.connect(self.mainUI.connectStatusSec.setVisible)

        ntcbs = self.preferences.bodyGrid.notificationCBs
        nts = self.mainUI.notification.labels

        for i in range(len(nts)):
            cb = ntcbs[i]
            lb = nts[i]
            cb.stateChanged.connect(lb.setVisible)
        ntcbs[-1].stateChanged.connect(self.mainUI.notifiSec.setVisible)

        for layout in self.layouts():
            try:
                layout.isHidden()
            except AttributeError:
                self.noShowHideAttrs.append(layout)

        self.mainUI.botTabUI.botTab1.recieveSignalCB.stateChanged.connect(self.parent.changeRecieveSignal)
        self.mainUI.botTabUI.botTab1.blockSignalCB.stateChanged.connect(self.parent.changeBlockSignal)
        self.mainUI.botTabUI.botTab1.commandCB.stateChanged.connect(self.parent.changeTrackCommand)
        self.mainUI.botTabUI.botTab1.registLayoutCB.stateChanged.connect(self.parent.changeRegistLayout)
        self.mainUI.botTabUI.botTab1.jobsTodoCB.stateChanged.connect(self.parent.changeJobsTodo)
        self.mainUI.botTabUI.botTab1.showLayoutErrorCB.stateChanged.connect(self.parent.changeShowLayout)
        self.mainUI.botTabUI.botTab1.trackEventCB.stateChanged.connect(self.parent.changeTrackEvent)

        layouts = []
        for listLayout in [self.mains, self.funcs, self.infos, self.setts, self.tools, self.prjs]:
            layouts = layouts + list(listLayout)
        self._buildAll = True

        return layouts

    def functionLayouts(self):
        from ui.subUI.Funcs.SignIn          import SignIn
        from ui.subUI.Funcs.SignUp          import SignUp
        from ui.subUI.Funcs.ForgotPassword  import ForgotPassword

        self.signin                         = SignIn()
        self.forgotPW                       = ForgotPassword()
        self.signup                         = SignUp()

        for layout in [self.signin, self.signup, self.forgotPW]:
            self.registLayout(layout)

        return self.signin, self.signup, self.forgotPW

    def mainLayouts(self):
        from ui.PipelineManager             import PipelineManager
        from ui.SysTray                     import SysTray
        from ui.subUI.ShortcutCommand       import ShortcutCommand

        self.mainUI                         = PipelineManager(self.actionManager, self.buttonManager, self.threadManager)
        self.sysTray                        = SysTray(self.actionManager, self.eventManager)
        self.shortcutLayout                 = ShortcutCommand()
        self.setLayoutUnHidable(self.sysTray)

        layouts = [self.mainUI, self.sysTray, self.shortcutLayout]

        for layout in layouts:
            layout.settings._settingEnable = True
            self.registLayout(layout)

        # for layout in self.mainUI.layouts:
        #     self.registLayout(layout)
        #
        # for layout in self.mainUI.topTabUI.tabs:
        #     key = layout.key
        #     if not key in self._register.keys():
        #         self._register[key] = layout

        return layouts

    def infoLayouts(self):
        from ui.subUI.Info.InfoWidget       import InfoWidget

        self.about                          = InfoWidget(key='About')
        self.codeConduct                    = InfoWidget(key='CodeOfConduct')
        self.contributing                   = InfoWidget(key='Contributing')
        self.credit                         = InfoWidget(key="Credit")
        self.licence                        = InfoWidget(key='Licence')
        self.reference                      = InfoWidget(key='Reference')
        self.version                        = InfoWidget(key='Version')

        layouts = [self.about, self.codeConduct, self.contributing, self.credit, self.licence,
                    self. reference, self.version]

        for layout in layouts:
            layout.settings._settingEnable = True
            self.registLayout(layout)

        return layouts

    def settingLayouts(self):
        from ui.subUI.Settings.SettingUI    import SettingUI
        from ui.subUI.Settings.UserSetting  import UserSetting

        self.settingUI                      = SettingUI()
        self.userSetting                    = UserSetting()

        layouts = [self.settingUI, self.userSetting]

        for layout in layouts:
            self.registLayout(layout)

        return layouts

    def toolLayouts(self):
        from ui.subUI.Tools                 import (Screenshot, NoteReminder, ImageViewer, FindFiles, EnglishDictionary,
                                                    Calendar, Calculator)
        from ui.subUI.Tools.NodeGraph       import NodeGraph
        from ui.subUI.Tools.TextEditor      import TextEditor
        from ui.Header.Menus.config         import Preferences
        from ui.Header.Menus.config         import Configuration
        from ui.TaskManager import TaskManager

        self.calculator                     = Calculator.Calculator()
        self.calendar                       = Calendar.Calendar()
        self.configuration                  = Configuration.Configuration()
        self.engDict                        = EnglishDictionary.EnglishDictionary()
        self.findFile                       = FindFiles.FindFiles()
        self.imageViewer                    = ImageViewer.ImageViewer()
        self.nodeGraph                      = NodeGraph.NodeGraph()
        self.noteReminder                   = NoteReminder.NoteReminder()
        self.preferences                    = Preferences.Preferences()
        self.screenShot                     = Screenshot.Screenshot()
        self.textEditor                     = TextEditor.TextEditor()
        self.taskManager                    = TaskManager(self.mainUI)

        layouts     = [self.calculator, self.calendar, self.configuration, self.engDict, self.findFile,
                       self.imageViewer, self.nodeGraph, self.noteReminder, self.preferences, self.screenShot,
                       self.textEditor, self.taskManager]

        for layout in layouts:
            layout.settings._settingEnable = True
            self.registLayout(layout)

        return layouts

    def projectLayouts(self):
        from ui.subUI.Projects.NewProject   import NewProject

        self.newProject                     = NewProject()

        for layout in [self.newProject, ]:
            layout.settings._settingEnable = True
            self.registLayout(layout)

        layouts = [self.newProject]
        return layouts

    def showOnlyLayout(self, layout):
        layouts = [l for l in self.layouts() if not l is layout and not l in self.unHidableLayouts]
        if self.isHidable(layout):
            self.show(layout)

        for l in layouts:
            self.hide(l)

    def hideOnlyLayout(self, layout):
        layouts = [l for l in self.layouts() if not l is layout and not l in self.unHidableLayouts]
        if self.isHidable(layout):
            self.hide(layout)

        for l in layouts:
            self.show(l)

    def setLayoutUnHidable(self, layout):
        if not layout in self.unHidableLayouts:
            layout.show()
            layout.setVisible(True)
            return self.unHidableLayouts.append(layout)

    def setLayoutUnShowable(self, layout):
        if not layout in self.unShowableLayouts:
            self.hide(layout)
            return self.unShowableLayouts.append(layout)

    def setLayoutHidable(self, layout):
        if layout in self.unHidableLayouts:
            self.show(layout)
            return self.unHidableLayouts.remove(layout)

    def isHidable(self, layout):
        if not layout in self.noShowHideAttrs:
            if not layout in self.unHidableLayouts:
                try:
                    layout.isHidden()
                except AttributeError:
                    return False
                else:
                    return True
            elif layout in self.unShowableLayouts:
                return False
            else:
                return False
        else:
            return False

    def hide(self, layout):
        if not layout.key in self.ignoreIDs:
            layout.hide()
            return layout.setValue('state', 'hide')

    def show(self, layout):
        if not layout.key in self.ignoreIDs:
            layout.show()
            return layout.setValue('state', 'show')

    def showNormal(self, layout):
        if not layout.key in self.ignoreIDs:
            layout.showNormal()
            return layout.setValue('state', 'showNormal')

    def showMinnimize(self, layout):
        if not layout.key in self.ignoreIDs:
            layout.showMinimize()
            return layout.setValue('state', 'showMinimize')

    def showMaximized(self, layout):
        if not layout.key in self.ignoreIDs:
            layout.showMaximized()
            return layout.setValue('state', 'showMaximized')

    def showAllLayout(self):
        for layout in self.layouts():
            self.show(layout)

    def registLayout(self, layout):
        return self._register.regisLayout(layout)

    def globalSetting(self):
        for layout in self.layouts():
            # print(layout.key)
            try:
                layout.setContentMargin(1,1,1,1)
            except AttributeError:
                pass

            try:
                layout.setSizePolicy(SiPoMin, SiPoMin)
            except AttributeError:
                pass

            try:
                layout.setSpacing(2)
            except AttributeError:
                pass

            if layout.key == 'PipelineManager':
                layout.setFixedWidth(500)
                # layout.setFixedHeight(850)
                # self.parent.setWindowFlags(STAY_ON_TOP)
                pass

            if layout.key in ['TobTab', 'BotTab']:
                layout.setMovable(True)
                layout.setElideMode(Qt.ElideRight)
                layout.setUsesScrollButtons(True)
                pass

    @property
    def buildAll(self):
        return self._buildAll

    @property
    def register(self):
        return self._register

    @buildAll.setter
    def buildAll(self, val):
        self._buildAll = val

    @register.setter
    def register(self, val):
        self._register = val

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/07/2018 - 11:31 AM
# © 2017 - 2018 DAMGteam. All rights reserved