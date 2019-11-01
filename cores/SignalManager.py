# -*- coding: utf-8 -*-
"""

Script Name: UiSignals.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
""" Import """

# Python
from damg                           import DAMG

# PyQt5
from PyQt5.QtCore                   import pyqtSignal
from PyQt5.QtCore                   import Qt

# PLM
from appData                        import SiPoMin, SiPoMax, SiPoExp, SiPoIgn, SiPoPre


class SignalManager(DAMG):

    key                             = "SignalManager"

    showLayout                      = pyqtSignal(str, str, name="showLayout")
    executing                       = pyqtSignal(str, name="executing")
    regisLayout                     = pyqtSignal(DAMG, name="regisLaout")
    openBrowser                     = pyqtSignal(str, name="openBrowser")
    setSetting                      = pyqtSignal(str, str, str, name="setSetting")

    loginChange                     = pyqtSignal(bool, name="loginChange")

    sysNotify                       = pyqtSignal(str, str, str, int, name="sysNotify")

    setLoginValue                   = pyqtSignal(bool, name="setLoginValue")

    updateAvatar                    = pyqtSignal(bool, name="updateAvatar")

    cfgReport                       = pyqtSignal(str, name="cfgReport")

    def __init__(self, parent=None):
        super(SignalManager, self).__init__(parent)

        self.parent = parent

        self.objects        = ['PLMCORE', 'PLM', 'IconPth', ]

        self.notContenMargin = ['Configurations', 'ServerConfig', 'ComboBox', 'Button', 'HBoxLayout',
                                'VBoxLayout', 'ServerConfigPage1', 'ServerConfigPage2', 'ServerConfig', 'Label',
                                'Widget', 'SettingUI', 'SettingInput', 'GridLayout', 'signin', 'GroupBox', 'LineEdit',
                                'forgotPW', 'signup', 'CheckBox', 'mainUI', 'MainMenuBar', 'Action', 'SubMenuBar',
                                'mainToolBar', 'TopTab', 'topTab1', 'topTab2', 'topTab3', 'topTab4', 'topTab5', 'TabBar',
                                'TabWidget', 'tabs', 'botTab', 'GeneralSetting', 'Footer', 'statusBar']

        self.notSizePolicy = []

        self.notSpacing = []

        self.globalSetting()

    def globalSetting(self):
        if self.parent.key not in self.objects:
            if self.parent.key not in self.notContenMargin:
                try:
                    self.parent.setContentMargin(1,1,1,1)
                except AttributeError:
                    pass
            elif self.parent.key not in self.notSizePolicy:
                try:
                    self.parent.setSizePolicy(SiPoExp, SiPoExp)
                except AttributeError:
                    pass
            elif self.parent.key not in self.notSpacing:
                try:
                    self.parent.setSpacing(2)
                except AttributeError:
                    pass

        if self.parent.key == 'PipelineManager':
            self.parent.setMaximumWidth(459)

        if self.parent.key == 'TobTab' and self.parent.key == 'BotTab':
            self.parent.setMovable(True)
            self.parent.setElideMode(Qt.ElideRight)
            self.parent.setUsesScrollButtons(True)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/10/2019 - 6:59 AM
# © 2017 - 2018 DAMGteam. All rights reserved