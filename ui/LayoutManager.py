# -*- coding: utf-8 -*-
"""

Script Name: Cores.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PyQt5
from PyQt5.QtCore                       import Qt

# PLM
from appData                            import SiPoMin
from bin                                import DAMG, DAMGLIST

class LayoutManager(DAMG):

    key                                 = 'LayoutManager'

    _buildAll                           = False

    noShowHideAttrs                     = DAMGLIST()
    unHidableLayouts                    = DAMGLIST()
    unShowableLayouts                   = DAMGLIST()

    ignoreIDs                           = DAMGLIST()

    def __init__(self, registryLayout, actionManager, buttonManager, eventManager, threadManager, parent=None):
        super(LayoutManager, self).__init__(parent)

        # self.ignoreIDs.appendList(self.parent.ignoreIDs)

        self.parent                     = parent
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

        tbcbs                           = self.preferences.headerGrid.toolBarCBs
        tbs                             = self.mainUI.mainToolBar.tbs
        cncbs                           = self.preferences.headerGrid.connectCBs
        cns                             = self.mainUI.connectStatus.labels
        mncbs                           = self.preferences.headerGrid.menuCBs
        ntcbs                           = self.preferences.bodyGrid.notificationCBs
        nts                             = self.mainUI.notification.labels

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
        from ui                             import SignIn, SignUp, ForgotPassword

        self.signin                         = SignIn()
        self.forgotPW                       = ForgotPassword()
        self.signup                         = SignUp()

        layouts = [self.signin, self.signup, self.forgotPW]
        for layout in layouts:
            self.registLayout(layout)

        return layouts

    def mainLayouts(self):
        from ui                             import PipelineManager, SysTray, ShortcutCommand

        self.mainUI                         = PipelineManager(self.actionManager, self.buttonManager, self.threadManager)
        self.sysTray                        = SysTray(self.actionManager, self.eventManager)
        self.shortcutLayout                 = ShortcutCommand()

        layouts = [self.mainUI, self.sysTray, self.shortcutLayout]

        for layout in layouts:
            layout.settings._settingEnable = True
            self.registLayout(layout)

        return layouts

    def infoLayouts(self):
        from ui                             import InfoWidget

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
        from ui                             import SettingUI, UserSetting

        self.settingUI                      = SettingUI()
        self.userSetting                    = UserSetting()

        layouts = [self.settingUI, self.userSetting]

        for layout in layouts:
            self.registLayout(layout)

        return layouts

    def toolLayouts(self):
        from ui                             import (Screenshot, NoteReminder, ImageViewer, FindFiles, EnglishDictionary,
                                                    Calendar, Calculator, NodeGraph, TextEditor, Preferences,
                                                    Configuration)
        from cores.TaskManager              import TaskManager

        self.calculator                     = Calculator()
        self.calendar                       = Calendar()
        self.configuration                  = Configuration()
        self.engDict                        = EnglishDictionary()
        self.findFile                       = FindFiles()
        self.imageViewer                    = ImageViewer()
        self.nodeGraph                      = NodeGraph()
        self.noteReminder                   = NoteReminder()
        self.preferences                    = Preferences()
        self.screenShot                     = Screenshot()
        self.textEditor                     = TextEditor()
        self.taskManager                    = TaskManager()

        layouts     = [self.calculator, self.calendar, self.configuration, self.engDict, self.findFile,
                       self.imageViewer, self.nodeGraph, self.noteReminder, self.preferences, self.screenShot,
                       self.textEditor, self.taskManager]

        for layout in layouts:
            layout.settings._settingEnable = True
            self.registLayout(layout)

        return layouts

    def projectLayouts(self):
        from ui.SubUi                       import VFXProject
        self.setupVFXprj                     = VFXProject()

        for layout in [self.setupVFXprj, ]:
            layout.settings._settingEnable = True
            self.registLayout(layout)

        layouts = [self.setupVFXprj]
        return layouts

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
                layout.setFixedWidth(525)
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