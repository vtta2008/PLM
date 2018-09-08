# -*- coding: utf-8 -*-
"""

Script Name: Button.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
from functools import partial

# PyQt5
from PyQt5.QtWidgets import QPushButton, QToolButton

# PLM
from core.paths import SiPoExp, SiPoPre
from ui.uikits.UiPreset import check_preset, IconPth

# -------------------------------------------------------------------------------------------------------------
""" Button presets """

class Button(QPushButton):

    def __init__(self, preset={}, parent=None):
        super(Button, self).__init__(parent)
        self.preset = preset
        if check_preset(self.preset):
            self.procedural()

    def procedural(self):
        for key, value in self.preset.items():
            if key == 'txt':
                self.setText(value)
            elif key == 'tt':
                self.setToolTip(value)
            elif key == 'cl':
                self.clicked.connect(value)
            elif key == 'emit1':
                self.clicked.connect(partial(value[0], value[1]))
            elif key == 'emit2':
                self.clicked.connect(partial(value[0], value[1][0], value[1][1]))
            elif key == 'icon':
                self.setIcon(IconPth(32, value))
            elif key == 'icon24':
                self.setIcon(IconPth(24, value))
            elif key == 'fix':
                self.setFixedSize(value)
            elif key == 'ics':
                self.setIconSize(value)
            elif key == 'stt':
                self.setToolTip(value)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

class ToolBtn(QToolButton):

    def __init__(self, text, parent=None):
        super(ToolBtn, self).__init__(parent)
        self.setText(text)
        self.applySetting()

    def applySetting(self):
        self.setSizePolicy(SiPoExp, SiPoPre)

    def sizeHint(self):
        size = super(ToolBtn, self).sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(max(size.width(), size.height()))
        return size


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 18/07/2018 - 8:37 AM
# © 2017 - 2018 DAMGteam. All rights reserved