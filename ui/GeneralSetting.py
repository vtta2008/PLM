#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: QuickSetting.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

    This script is the layout part of quick setting for main layout.

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
from functools import partial

# PtQt5
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGridLayout, QCheckBox

# Plt
from utilities.utils import str2bool, bool2str
from core.Loggers import SetLogger
from core.Specs import Specs

# -------------------------------------------------------------------------------------------------------------
""" Quick Setting """
class GeneralSetting(QGridLayout):

    key = 'quickSetting'

    setSetting = pyqtSignal(str, str, str)
    loadSetting = pyqtSignal(str, str)

    def __init__(self, parent=None):

        super(GeneralSetting, self).__init__(parent)
        self.specs = Specs(self.key, self)
        self.logger = SetLogger(self)
        self.setSpacing(2)

        self.tbTDCB = QCheckBox("TD toolbar")
        self.tbCompCB = QCheckBox("Comp toolbar")
        self.tbArtCB = QCheckBox("Art toolbar")
        self.tbMasterCB = QCheckBox("Toolbar")
        self.statusBarCB = QCheckBox("Status Bar")
        self.subMenuCB = QCheckBox("Sub Menu")
        self.serStatusCB = QCheckBox("Server Status")
        self.notifiCB = QCheckBox("Notification")

        self.buildUI()

    def buildUI(self):

        self.tbTDCB.stateChanged.connect(self.set_setting)
        self.tbCompCB.stateChanged.connect(self.set_setting)
        self.tbArtCB.stateChanged.connect(self.set_setting)
        self.tbMasterCB.stateChanged.connect(self.set_setting)
        self.statusBarCB.stateChanged.connect(self.set_setting)
        self.subMenuCB.stateChanged.connect(self.set_setting)
        self.serStatusCB.stateChanged.connect(self.set_setting)
        self.notifiCB.stateChanged.connect(self.set_setting)

        self.addWidget(self.tbTDCB, 0, 0, 1, 2)
        self.addWidget(self.tbCompCB, 1, 0, 1, 2)
        self.addWidget(self.tbArtCB, 2, 0, 1, 2)

        self.addWidget(self.tbMasterCB, 0, 2, 1, 2)
        self.addWidget(self.statusBarCB, 1, 2, 1, 2)
        self.addWidget(self.subMenuCB, 2, 2, 1, 2)

        self.addWidget(self.serStatusCB, 0, 4, 1, 2)
        self.addWidget(self.notifiCB, 1, 4, 1, 2)

        self.load_setting()

    def set_setting(self):
        self.setSetting.emit('mainUI/botTab/quickSetting/toolbarTD', bool2str(self.tbTDCB.checkState()), 'mainUI')
        self.setSetting.emit('mainUI/botTab/quickSetting/toolbarComp', bool2str(self.tbCompCB.checkState()), 'mainUI')
        self.setSetting.emit('mainUI/botTab/quickSetting/toolbarArt', bool2str(self.tbArtCB.checkState()), 'mainUI')
        self.setSetting.emit('mainUI/botTab/quickSetting/toolbar', bool2str(self.tbMasterCB.checkState()), 'mainUI')
        self.setSetting.emit('mainUI/botTab/quickSetting/toolbarStatus', bool2str(self.statusBarCB.checkState()), 'mainUI')
        self.setSetting.emit('mainUI/botTab/quickSetting/toolbarSubMenu', bool2str(self.subMenuCB.checkState()), 'mainUI')
        self.setSetting.emit('mainUI/botTab/quickSetting/toolbarServer', bool2str(self.serStatusCB.checkState()), 'mainUI')
        self.setSetting.emit('mainUI/botTab/quickSetting/toolbarNotifi', bool2str(self.notifiCB.checkState()), 'mainUI')

    def load_setting(self):
        print('run load setting')
        self.keys = ['mainUI/botTab/quickSetting/toolbarTD', 'mainUI/botTab/quickSetting/toolbarComp',
                'mainUI/botTab/quickSetting/toolbarArt', 'mainUI/botTab/quickSetting/toolbar',
                'mainUI/botTab/quickSetting/toolbarStatus', 'mainUI/botTab/quickSetting/toolbarSubMenu',
                'mainUI/botTab/quickSetting/toolbarServer', 'mainUI/botTab/quickSetting/toolbarNotifi']
        for key in self.keys:
            self.loadSetting.emit(key, 'mainUI')

    @pyqtSlot(str, str)
    def return_setting(self, key, value):
        print(key, value)
        tbs = [self.tbTDCB, self.tbCompCB, self.tbArtCB, self.tbMasterCB, self.statusBarCB, self.subMenuCB, self.serStatusCB, self.notifiCB]
        tb = tbs[self.keys.index(key)]
        val = str2bool(value)
        tb.setChecked(val)
