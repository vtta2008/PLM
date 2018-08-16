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
# Python

# PtQt5
from PyQt5.QtWidgets import QGridLayout, QCheckBox

# Plt
from core.Loggers import SetLogger
from core.Storage import PObj

# -------------------------------------------------------------------------------------------------------------
""" Quick Setting """
class GeneralSetting(QGridLayout):

    key = 'quickSetting'

    def __init__(self, parent=None):

        super(GeneralSetting, self).__init__(parent)
        self.logger = SetLogger(self)
        self.setSpacing(2)

        self.tbTDCB = QCheckBox("TD toolbar")
        self.tbTDCB.setChecked(False)
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

        self.checkBoxes = [self.tbTDCB, self.tbCompCB, self.tbArtCB, self.tbTexCB, self.tbPostCB, self.subToolBarCB,
                           self.mainToolBarCB, self.statusBarCB, self.subMenuCB, self.serStatusCB, self.notifiCB]

        self.keys = ['toolbarTD', 'toolbarComp', 'toolbarArt', 'toolbarTex', 'toolbarPost', 'subToolbar',
                     'toolbarMain', 'toolbarStatus', 'toolbarSubMenu', 'toolbarServer', 'toolbarNotifi']

        self.settingGrp = 'mainUI'

        self.buildUI()
        self.reg = PObj(self)

    def buildUI(self):

        self.addWidget(self.tbTDCB, 0, 0, 1, 2)
        self.addWidget(self.tbCompCB, 1, 0, 1, 2)
        self.addWidget(self.tbArtCB, 2, 0, 1, 2)
        self.addWidget(self.tbTexCB, 3, 0, 1, 2)

        self.addWidget(self.tbPostCB, 0, 2, 1, 2)
        self.addWidget(self.subToolBarCB, 1, 2, 1, 2)
        self.addWidget(self.mainToolBarCB, 2, 2, 1, 2)
        self.addWidget(self.statusBarCB, 3, 2, 1, 2)

        self.addWidget(self.subMenuCB, 0, 4, 1, 2)
        self.addWidget(self.serStatusCB, 1, 4, 1, 2)
        self.addWidget(self.notifiCB, 2, 4, 1, 2)
