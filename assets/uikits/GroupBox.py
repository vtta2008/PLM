# -*- coding: utf-8 -*-
"""

Script Name: GroupBox.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python


# PyQt5
from PyQt5.QtWidgets import QGroupBox, QGridLayout, QHBoxLayout

from app import SiPoMin
# PLM
from assets.data._docs import WAIT_LAYOUT_COMPLETE
from ui.uikits.GridLayout import AutoPreset1, AutoPreset2, AutoPreset3
from ui.uikits.UiPreset import Label

# -------------------------------------------------------------------------------------------------------------
""" Groupbox presets """

class AutoSectionQMainGrp(QGroupBox):

    def __init__(self, title="Section Title", subLayout=None, parent=None):
        super(AutoSectionQMainGrp, self).__init__(parent)
        self.setTitle(title)
        self.subLayout = subLayout

        self.layout = QHBoxLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.layout.addWidget(self.subLayout)

        self.applySetting()

    def applySetting(self):
        self.setSizePolicy(SiPoMin, SiPoMin)
        self.setContentsMargins(5, 5, 5, 5)

class AutoSectionLayoutGrp(QGroupBox):

    def __init__(self, title="Section Title", subLayout=None, parent=None):
        super(AutoSectionLayoutGrp, self).__init__(parent)
        self.setTitle(title)
        if subLayout is None:
            self.layout = QGridLayout()
            self.layout.addWidget(Label({'txt':WAIT_LAYOUT_COMPLETE}), 0, 0, 1, 1)
        else:
            self.layout = subLayout

        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.applySetting()

    def applySetting(self):
        self.setSizePolicy(SiPoMin, SiPoMin)
        self.setContentsMargins(5, 5, 5, 5)

class GroupBox(QGroupBox):

    def __init__(self, title="Section Title", btns=[], mode="IconGrid", parent=None):
        super(GroupBox, self).__init__(parent)
        self.setTitle(title)
        self.btns = btns
        self.mode = mode

        self.buildUI()
        self.applySetting()

    def buildUI(self):
        if self.mode == "IconGrid":
            self.setLayout(AutoPreset1(self.btns))
        elif self.mode == "BtnGrid":
            self.setLayout(AutoPreset2(self.btns))
        elif self.mode == "ImageView":
            self.setLayout(AutoPreset3(self.btns[0]))

    def applySetting(self):
        self.setSizePolicy(SiPoMin, SiPoMin)
        self.setContentsMargins(5, 5, 5, 5)

def GroupGrid(txt=None):
    if txt is None:
        grp = QGroupBox()
    else:
        grp = QGroupBox(txt)

    grid = QGridLayout()
    grp.setLayout(grid)
    return grp, grid
# -------------------------------------------------------------------------------------------------------------
# Created by panda on 18/07/2018 - 8:32 AM
# © 2017 - 2018 DAMGteam. All rights reserved