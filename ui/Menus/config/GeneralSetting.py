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

# Plt
from ui.uikits.GridLayout import GridLayout
from ui.uikits.CheckBox import CheckBox

# -------------------------------------------------------------------------------------------------------------
""" Quick Setting """
class GeneralSetting(GridLayout):

    key = 'GeneralSetting'

    def __init__(self, parent=None):

        super(GeneralSetting, self).__init__(parent)

        self.buildUI()

    def buildUI(self):

        self.tbTDCB         = CheckBox(txt="TD toolbar")
        self.tbCompCB       = CheckBox(txt="Comp toolbar")
        self.tbArtCB        = CheckBox(txt="Art toolbar")

        self.tbTexCB        = CheckBox(txt="Tex toolbar")
        self.tbPostCB       = CheckBox(txt='Post toolbar')
        self.mainToolBarCB  = CheckBox(txt="Main Toolbar")

        self.statusBarCB    = CheckBox(txt="Status Bar")
        self.connectStatuCB = CheckBox(txt="Connect Status")
        self.notifiCB       = CheckBox(txt="Notification")

        self.addWidget(self.tbTDCB, 0, 0, 1, 2)
        self.addWidget(self.tbCompCB, 1, 0, 1, 2)
        self.addWidget(self.tbArtCB, 2, 0, 1, 2)

        self.addWidget(self.tbTexCB, 0, 2, 1, 2)
        self.addWidget(self.tbPostCB, 1, 2, 1, 2)
        self.addWidget(self.mainToolBarCB, 2, 2, 1, 2)

        self.addWidget(self.statusBarCB, 0, 4, 1, 2)
        self.addWidget(self.connectStatuCB, 1, 4, 1, 2)
        self.addWidget(self.notifiCB, 2, 4, 1, 2)

        self.checkBoxes = [self.tbTDCB, self.tbCompCB, self.tbArtCB, self.tbTexCB, self.tbPostCB,
                           self.mainToolBarCB, self.statusBarCB, self.connectStatuCB, self.notifiCB]

        self.keys = ['toolbarTD', 'toolbarComp', 'toolbarArt', 'toolbarTex', 'toolbarPost', 'subToolbar',
                     'toolbarMain', 'toolbarStatus', 'toolbarSubMenu', 'toolbarConnect', 'toolbarNotifi']
