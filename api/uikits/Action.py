# -*- coding: utf-8 -*-
"""

Script Name: Action.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python

# PyQt5
from PyQt5.QtWidgets import QAction

# PLM
from ui.uikits.UiPreset import check_preset, IconPth

# -------------------------------------------------------------------------------------------------------------
""" Action presets """

class Action(QAction):

    def __init__(self, preset={}, parent=None):
        super(Action, self).__init__(parent)
        self.preset = preset
        if check_preset(self.preset):
            self.procedural()

    def procedural(self):
        for key, value in self.preset.items():
            if key == 'icon':
                self.setIcon(IconPth(32, value))
            elif key == 'txt':
                self.setText(value)
            elif key == 'trg':
                self.triggered.connect(value)
            elif key == 'shortcut':
                self.setShortcut(value)
            elif key == 'checkable':
                self.setChecked(value)
            elif key == 'enabled':
                self.setDisabled(value)
            elif key == 'stt':
                self.setStatusTip(value)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 18/07/2018 - 8:42 AM
# © 2017 - 2018 DAMGteam. All rights reserved