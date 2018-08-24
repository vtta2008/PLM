# -*- coding: utf-8 -*-
"""

Script Name: TabWidget.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python


# PyQt5
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QTabWidget, QGridLayout, QTabBar, QWidget, QVBoxLayout

# PLM
from core.paths import SiPoMin
from ui.uikits.UiPreset import Label

# -------------------------------------------------------------------------------------------------------------
""" Tab layout element"""

class TabBar(QTabBar):

    def tabSizeHint(self, index):
        size = QTabBar.tabSizeHint(self, index)
        w = int(self.width()/self.count())
        return QSize(w, size.height())

class TabContent(QWidget):

    def __init__(self, layout=None, parent=None):
        super(TabContent, self).__init__(parent)

        if layout is None:
            layout = QGridLayout()
            layout.addWidget(Label())
        self.layout = layout
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.applySetting()

    def applySetting(self):
        self.setSizePolicy(SiPoMin, SiPoMin)

class TabWidget(QWidget):

    def __init__(self, parent=None):
        super(TabWidget, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        self.tabs = QTabWidget()
        self.tabs.setTabBar(TabBar())

        self.layout.addWidget(self.tabs)

        self.applySetting()

    def applySetting(self):
        self.tabs.setMovable(True)
        self.tabs.setDocumentMode(True)
        self.tabs.setElideMode(Qt.ElideRight)
        self.tabs.setUsesScrollButtons(True)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 18/07/2018 - 9:06 AM
# © 2017 - 2018 DAMGteam. All rights reserved