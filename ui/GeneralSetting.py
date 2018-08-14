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
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import QGridLayout, QCheckBox

# Plt
from utilities.utils import str2bool, bool2str
from core.Loggers import SetLogger
# -------------------------------------------------------------------------------------------------------------
""" Quick Setting """
class GeneralSetting(QGridLayout):

    key = 'quickSetting'

    setSetting = pyqtSignal(str, str, str)
    loadSetting = pyqtSignal(str, str)

    def __init__(self, parent=None):

        super(GeneralSetting, self).__init__(parent)
        self.logger = SetLogger(self)
        self.setSpacing(2)

        self.tbTDCB = QCheckBox("TD toolbar")
        self.tbCompCB = QCheckBox("Comp toolbar")
        self.tbArtCB = QCheckBox("Art toolbar")
        self.tbTexCB = QCheckBox("Tex toolbar")
        self.tbPostCB = QCheckBox('Post toolbar')

        self.subToolBarCB = QCheckBox("Sub Toolbar")
        self.mainToolBarCB = QCheckBox("Main Toolbar")
        self.statusBarCB = QCheckBox("Status Bar")

        self.subMenuCB = QCheckBox("Sub Menu")
        self.serStatusCB = QCheckBox("Server Status")
        self.notifiCB = QCheckBox("Notification")

        self.buildUI()

    def buildUI(self):

        self.tbTDCB.stateChanged.connect(self.set_setting)
        self.tbCompCB.stateChanged.connect(self.set_setting)
        self.tbArtCB.stateChanged.connect(self.set_setting)
        self.tbTexCB.stateChanged.connect(self.set_setting)
        self.tbPostCB.stateChanged.connect(self.set_setting)
        self.subToolBarCB.stateChanged.connect(self.set_setting)
        self.mainToolBarCB.stateChanged.connect(self.set_setting)
        self.statusBarCB.stateChanged.connect(self.set_setting)
        self.subMenuCB.stateChanged.connect(self.set_setting)
        self.serStatusCB.stateChanged.connect(self.set_setting)
        self.notifiCB.stateChanged.connect(self.set_setting)

        self.addWidget(self.tbTDCB, 0, 0, 1, 2)
        self.addWidget(self.tbCompCB, 1, 0, 1, 2)
        self.addWidget(self.tbArtCB, 2, 0, 1, 2)
        self.addWidget(self.tbTexCB, 3, 0, 1, 2)
        self.addWidget(self.tbPostCB, 4, 0, 1, 2)
        self.addWidget(self.subToolBarCB, 5, 0, 1, 2)


        self.addWidget(self.mainToolBarCB, 0, 2, 1, 2)
        self.addWidget(self.statusBarCB, 1, 2, 1, 2)
        self.addWidget(self.subMenuCB, 2, 2, 1, 2)
        self.addWidget(self.serStatusCB, 3, 2, 1, 2)
        self.addWidget(self.notifiCB, 4, 2, 1, 2)

        self.load_setting()

    def set_setting(self):
        self.setSetting.emit('mainUI/botTab/quickSetting/subToolbar/toolbarTD', bool2str(self.tbTDCB.checkState()), 'mainUI')
        self.setSetting.emit('mainUI/botTab/quickSetting/subToolbar/toolbarComp', bool2str(self.tbCompCB.checkState()), 'mainUI')
        self.setSetting.emit('mainUI/botTab/quickSetting/subToolbar/toolbarArt', bool2str(self.tbArtCB.checkState()), 'mainUI')
        self.setSetting.emit('mainUI/botTab/quickSetting/subToolbar/toolbarTex', bool2str(self.tbArtCB.checkState()), 'mainUI')
        self.setSetting.emit('mainUI/botTab/quickSetting/subToolbar/toolbarPost', bool2str(self.tbArtCB.checkState()), 'mainUI')

        self.setSetting.emit('mainUI/botTab/quickSetting/subToolbar', bool2str(self.subToolBarCB.checkState()), 'mainUI')
        self.setSetting.emit('mainUI/botTab/quickSetting/mainToolbar', bool2str(self.subToolBarCB.checkState()), 'mainUI')
        self.setSetting.emit('mainUI/botTab/quickSetting/toolbarStatus', bool2str(self.statusBarCB.checkState()), 'mainUI')

        self.setSetting.emit('mainUI/botTab/quickSetting/toolbarSubMenu', bool2str(self.subMenuCB.checkState()), 'mainUI')
        self.setSetting.emit('mainUI/botTab/quickSetting/toolbarServer', bool2str(self.serStatusCB.checkState()), 'mainUI')
        self.setSetting.emit('mainUI/botTab/quickSetting/toolbarNotifi', bool2str(self.notifiCB.checkState()), 'mainUI')

    def load_setting(self):
        self.keys = ['mainUI/botTab/quickSetting/subToolbar/toolbarTD', 'mainUI/botTab/quickSetting/subToolbar/toolbarComp',
                'mainUI/botTab/quickSetting/subToolbar/toolbarArt', 'mainUI/botTab/quickSetting/subToolbar/toolbarTex',
                'mainUI/botTab/quickSetting/subToolbar/toolbarPost', 'mainUI/botTab/quickSetting/subToolbar/subToolbar',
                'mainUI/botTab/quickSetting/toolbarStatus', 'mainUI/botTab/quickSetting/toolbarSubMenu',
                'mainUI/botTab/quickSetting/toolbarServer', 'mainUI/botTab/quickSetting/toolbarNotifi']

        for key in self.keys:
            self.loadSetting.emit(key, 'mainUI')

    @pyqtSlot(str, str)
    def return_setting(self, key, value):
        print(key, value)
        tbs = [self.tbTDCB, self.tbCompCB, self.tbArtCB, self.subToolBarCB, self.statusBarCB, self.subMenuCB, self.serStatusCB, self.notifiCB]
        tb = tbs[self.keys.index(key)]
        val = str2bool(value)
        tb.setChecked(val)
