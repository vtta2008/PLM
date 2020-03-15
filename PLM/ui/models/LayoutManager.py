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
from PLM.configs                            import SiPoMin
from PLM.commons                                import DAMG, DAMGLIST

from .ActionManager                     import ActionManager
from .ButtonManager                     import ButtonManager
from .Registry                          import RegistryLayout
from .EventManager                      import EventManager

from PLM.ui.base import BaseManager, ImageAvatar, PixAvatar
from ..tools import CommandUI
from PLM.ui.PipelineManager import PipelineManager
from PLM.ui.SysTray import SysTray
from PLM.ui.tools import (Calendar, Calculator, EnglishDictionary, FindFiles, ImageViewer,
                          NoteReminder, ScreenShot, TextEditor)
from PLM.ui.layouts import (ForgotPassword, SignUp, SignIn, InfoWidget, VFXProject, AppSetting, UserSetting,
                            Preferences, Configurations)

class LayoutManager(DAMG):

    key                                 = 'LayoutManager'

    _buildAll                           = False

    noShowHideAttrs                     = DAMGLIST()
    unHidableLayouts                    = DAMGLIST()
    unShowableLayouts                   = DAMGLIST()


    def __init__(self, threadManager, parent=None):
        super(LayoutManager, self).__init__(parent)

        self.parent                     = parent
        self.actionManager              = ActionManager(self.parent)
        self.buttonManager              = ButtonManager(self.parent)
        self._register                  = RegistryLayout()
        self.eventManager               = EventManager(self.parent)
        self.threadManager              = threadManager

        self.globalSetting()

    def layouts(self):
        return self._register.values()

    def keys(self):
        return self._register.keys()

    def buildLayouts(self):

        self.mains                      = self.mainLayouts()
        self.infos                      = self.infoLayouts()
        self.setts                      = self.settingLayouts()
        self.tools                      = self.toolLayouts()
        self.prjs                       = self.projectLayouts()
        self.plugins                    = self.pluginsLayouts()

        tbcbs                           = self.preferences.header.toolBarCBs
        tbs                             = self.mainUI.mainToolBar.tbs
        cncbs                           = self.preferences.header.connectCBs
        cns                             = self.mainUI.connectStatus.labels
        mncbs                           = self.preferences.header.menuCBs
        mns                             = self.mainUI.mainMenuBar.mns
        ntcbs                           = self.preferences.body.notificationCBs
        nts                             = self.mainUI.notification.labels

        for i in range(len(tbs)):
            cb = tbcbs[i+1]
            tb = tbs[i]
            cb.stateChanged.connect(tb.setVisible)
        tbcbs[0].stateChanged.connect(self.mainUI.mainToolBar.setVisible)

        for i in range(1, len(mns)):
            cb = mncbs[i+1]
            mn = mns[i]
            cb.stateChanged.connect(mn.setEnabled)
        mncbs[0].stateChanged.connect(self.mainUI.mainMenuBar.setVisible)

        for i in range(len(cns)):
            cb = cncbs[i+1]
            lb = cns[i]
            cb.stateChanged.connect(lb.setVisible)
        cncbs[0].stateChanged.connect(self.mainUI.connectStatus.setVisible)

        for i in range(len(nts)):
            cb = ntcbs[i+1]
            lb = nts[i]
            cb.stateChanged.connect(lb.setVisible)
        ntcbs[0].stateChanged.connect(self.mainUI.notification.setVisible)

        for layout in self.layouts():
            try:
                layout.isHidden()
            except AttributeError:
                self.noShowHideAttrs.append(layout)

        self.mainUI.botTabUI.botTab1.recieveSignalCB.stateChanged.connect(self.parent.setRecieveSignal)
        self.mainUI.botTabUI.botTab1.blockSignalCB.stateChanged.connect(self.parent.setBlockSignal)
        self.mainUI.botTabUI.botTab1.commandCB.stateChanged.connect(self.parent.setTrackCommand)
        self.mainUI.botTabUI.botTab1.registLayoutCB.stateChanged.connect(self.parent.setRegistLayout)
        self.mainUI.botTabUI.botTab1.jobsTodoCB.stateChanged.connect(self.parent.setJobsTodo)
        self.mainUI.botTabUI.botTab1.showLayoutErrorCB.stateChanged.connect(self.parent.setShowLayout)
        self.mainUI.botTabUI.botTab1.trackEventCB.stateChanged.connect(self.parent.setTrackEvent)

        layouts = []
        for listLayout in [self.mains, self.infos, self.setts, self.tools, self.prjs]:
            layouts = layouts + listLayout

        self._buildAll = True

        return layouts

    def mainLayouts(self):

        self.signin                         = SignIn()
        self.forgotPW                       = ForgotPassword()
        self.signup                         = SignUp()
        self.mainUI                         = PipelineManager(self.actionManager, self.buttonManager, self.threadManager, self.parent)
        self.sysTray                        = SysTray(self.actionManager, self.eventManager, self.parent)
        self.shortcutCMD                    = CommandUI(parent=self.parent)

        layouts = [self.mainUI, self.sysTray, self.shortcutCMD, self.signin, self.signup, self.forgotPW]

        for layout in layouts:
            layout.settings._settingEnable = True
            self.registLayout(layout)
        return layouts

    def infoLayouts(self):

        self.about                          = InfoWidget(key='About')
        self.codeConduct                    = InfoWidget(key='CodeOfConduct')
        self.contributing                   = InfoWidget(key='Contributing')
        self.credit                         = InfoWidget(key="Credit")
        self.licence                        = InfoWidget(key='Licence')
        self.references                     = InfoWidget(key='References')
        self.version                        = InfoWidget(key='Version')

        layouts = [self.about, self.codeConduct, self.contributing, self.credit, self.licence,
                    self.references, self.version]

        for layout in layouts:
            layout.settings._settingEnable = True
            self.registLayout(layout)

        return layouts

    def settingLayouts(self):

        self.settingUI                      = AppSetting()
        self.userSetting                    = UserSetting()

        self.mainUI.topTabUI.tab2.avatarGrp.setApp(self)
        self.userSetting.avatarGrp.setApp(self)

        layouts = [self.settingUI, self.userSetting]

        for layout in layouts:
            layout.settings._settingEnable  = True
            self.registLayout(layout)

        return layouts

    def toolLayouts(self):

        self.calculator                     = Calculator()
        self.calendar                       = Calendar()
        self.configuration                  = Configurations()
        self.engDict                        = EnglishDictionary()
        self.findFile                       = FindFiles()
        self.imageViewer                    = ImageViewer()
        self.noteReminder                   = NoteReminder()
        self.preferences                    = Preferences()
        self.screenShot                     = ScreenShot()
        self.textEditor                     = TextEditor()

        self.taskManager                    = BaseManager('TaskManager')
        self.orgManager                     = BaseManager('OrganisationManager')
        self.prjManager                     = BaseManager('ProjectManager')
        self.teamManager                    = BaseManager('TeamManager')

        layouts     = [self.calculator, self.calendar, self.configuration, self.engDict, self.findFile,
                       self.imageViewer, self.noteReminder, self.preferences, self.screenShot,
                       self.textEditor, self.taskManager, self.orgManager, self.prjManager, self.teamManager]

        for layout in layouts:
            layout.settings._settingEnable  = True
            self.registLayout(layout)

        return layouts

    def projectLayouts(self):

        self.setupVFXprj                     = VFXProject()

        layouts = [self.setupVFXprj, ]
        for layout in layouts:
            layout.settings._settingEnable  = True
            self.registLayout(layout)
        return layouts

    def pluginsLayouts(self):
        # from plugins.NodeGraph.NodeGraph import NodeGraph
        #
        # self.nodeGraph                      = NodeGraph()
        #
        # layouts = [self.nodeGraph, ]
        # for layout in layouts:
        #     layout.settings._settingEnable  = True
        #     self.registLayout(layout)
        # return layouts
        return []

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
                layout.setFixedWidth(550)
                # layout.setFixedHeight(850)
                # self.parent.setWindowFlags(STAY_ON_TOP)
                pass

            if layout.key in ['TobTab', 'BotTab']:
                layout.setMovable(True)
                layout.setElideMode(Qt.ElideRight)
                layout.setUsesScrollButtons(True)
                pass

    def updateAvatar(self, pth):
        self.mainUI.topTabUI.tab2.avatarGrp.avatar.imageAvatar = ImageAvatar(pth)
        self.mainUI.topTabUI.tab2.avatarGrp.avatar.pixAvatar = PixAvatar()
        image = self.mainUI.topTabUI.tab2.avatarGrp.avatar.imageAvatar
        pixmap = self.mainUI.topTabUI.tab2.avatarGrp.avatar.pixAvatar
        self.mainUI.topTabUI.tab2.avatarGrp.avatar.setPixmap(pixmap.fromImage(image))
        self.mainUI.topTabUI.tab2.avatarGrp.avatar.update()

        self.userSetting.avatarGrp.avatar.imageAvatar = ImageAvatar(pth)
        self.userSetting.avatarGrp.avatar.pixAvatar = PixAvatar()
        image = self.userSetting.avatarGrp.avatar.imageAvatar
        pixmap = self.userSetting.avatarGrp.avatar.pixAvatar
        self.userSetting.avatarGrp.avatar.setPixmap(pixmap.fromImage(image))
        self.userSetting.avatarGrp.avatar.update()

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