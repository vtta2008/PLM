# -*- coding: utf-8 -*-
"""

Script Name: UiSignals.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtCore import pyqtSignal

from cores.base import DAMG
from appData import SiPoMin, SiPoMax, SiPoExp, SiPoIgn, SiPoPre

class SignalManager(DAMG):

    key = "SignalManager"

    showLayout = pyqtSignal(str, str)
    executing = pyqtSignal(str)
    regisLayout = pyqtSignal(DAMG)
    openBrowser = pyqtSignal(str)
    setSetting = pyqtSignal(str, str, str)
    sysNotify = pyqtSignal(str, str, str, int)

    updateAvatar = pyqtSignal(bool)
    cfgReport = pyqtSignal(str)

    def __init__(self, parent=None):
        super(SignalManager, self).__init__(parent)

        self.parent = parent

        self.objects        = ['PLMCORE', 'PLM', 'IconPth', ]

        self.notContenMargin = ['Configurations', 'ServerConfig', 'ComboBox', 'Button', 'HBoxLayout',
                                'VBoxLayout', 'ServerConfigPage1', 'ServerConfigPage2', 'ServerConfig', 'Label',
                                'Widget', 'SettingUI', 'SettingInput', 'GridLayout', 'login', 'GroupBox', 'LineEdit',
                                'forgotPW', 'signup', 'CheckBox', 'mainUI', 'MainMenuBar', 'Action', 'SubMenuBar',
                                'mainToolBar', 'TopTab', 'topTab1', 'topTab2', 'topTab3', 'topTab4', 'topTab5', 'TabBar',
                                'TabWidget', 'tabs', 'botTab', 'GeneralSetting', 'Footer', 'statusBar']

        self.notSizePolicy = []

        self.notSpacing = []

        if self.parent.key not in self.objects:
            if self.parent.key not in self.notContenMargin:
                try:
                    self.parent.setContentMargin(0,0,0,0)
                except AttributeError:
                    pass
            elif self.parent.key not in self.notSizePolicy:
                try:
                    self.parent.setSizePolicy(SiPoPre, SiPoPre)
                except AttributeError:
                    pass
            elif self.parent.key not in self.notSpacing:
                try:
                    self.parent.setSpacing(2)
                except AttributeError:
                    pass

        if self.parent.key == 'MainUI':
            self.parent.setMaximumWidth(459)





        # self.setSpacing(1)
        # self.setContentMargin(5,5,5,5)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/10/2019 - 6:59 AM
# © 2017 - 2018 DAMGteam. All rights reserved