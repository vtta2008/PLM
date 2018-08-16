# -*- coding: utf-8 -*-
"""

Script Name: GridLayout.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python


# PyQt5
from PyQt5.QtWidgets import QGridLayout

# PLM


# -------------------------------------------------------------------------------------------------------------
""" Gridlayout presets """

class AutoPreset1(QGridLayout):

    def __init__(self, btns=[], parent=None):
        super(AutoPreset1, self).__init__(parent)
        self.btns = btns
        self.buildUI()

    def buildUI(self):
        if not len(self.btns) == 0:
            for i in range(len(self.btns)):
                if i == 0:
                    self.addWidget(self.btns[i], 0, 0, 1, 1)
                elif i == 1:
                    self.addWidget(self.btns[i], 0, 1, 1, 1)
                elif i == 2:
                    self.addWidget(self.btns[i], 0, 2, 1, 1)
                elif i == 3:
                    self.addWidget(self.btns[i], 1, 0, 1, 1)
                elif i == 4:
                    self.addWidget(self.btns[i], 1, 1, 1, 1)
                elif i == 5:
                    self.addWidget(self.btns[i], 1, 2, 1, 1)
                elif i == 6:
                    self.addWidget(self.btns[i], 2, 0, 1, 1)
                elif i == 7:
                    self.addWidget(self.btns[i], 2, 1, 1, 1)
                elif i == 8:
                    self.addWidget(self.btns[i], 2, 2, 1, 1)
                i += 1

    def sizeHint(self):
        size = super(AutoPreset1, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

class AutoPreset2(QGridLayout):

    def __init__(self, btns=[], parent=None):
        super(AutoPreset2, self).__init__(parent)
        self.btns = btns
        self.buildUI()

    def buildUI(self):
        if not len(self.btns) == 0:
            for i in range(len(self.btns)):
                if i == 0:
                    self.addWidget(self.btns[i], 0, 0, 1, 2)
                elif i == 1:
                    self.addWidget(self.btns[i], 1, 0, 1, 2)
                elif i == 2:
                    self.addWidget(self.btns[i], 2, 0, 1, 2)
                elif i == 3:
                    self.addWidget(self.btns[i], 3, 0, 1, 2)
                elif i == 4:
                    self.addWidget(self.btns[i], 4, 0, 1, 2)
                elif i == 5:
                    self.addWidget(self.btns[i], 5, 0, 1, 2)
                elif i == 6:
                    self.addWidget(self.btns[i], 6, 0, 1, 2)
                elif i == 7:
                    self.addWidget(self.btns[i], 7, 0, 1, 2)
                elif i == 8:
                    self.addWidget(self.btns[i], 8, 0, 1, 2)
                i += 1

    def sizeHint(self):
        size = super(AutoPreset2, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

class AutoPreset3(QGridLayout):

    def __init__(self, imageView, parent=None):
        super(AutoPreset3, self).__init__(parent)
        self.img = imageView
        self.buildUI()

    def buildUI(self):
        if self.img:
            self.addWidget(self.img, 0, 0, 1, 1)

    def sizeHint(self):
        size = super(AutoPreset3, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 18/07/2018 - 8:35 AM
# © 2017 - 2018 DAMGteam. All rights reserved