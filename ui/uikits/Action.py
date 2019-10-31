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
from PyQt5.QtWidgets                        import QAction

# PLM
from appData                                import __copyright__
from ui.uikits.Icon                         import AppIcon
from ui.uikits.uiUtils                      import check_preset

# -------------------------------------------------------------------------------------------------------------
""" Action presets """

class Action(QAction):

    Type                                    = 'DAMGUI'
    key                                     = 'Action'
    _name                                   = 'DAMG Action'
    _copyright                              = __copyright__

    def __init__(self, preset={}, parent=None):
        super(Action, self).__init__(parent)

        self.parent         = parent
        self.preset         = preset

        if check_preset(self.preset):
            self.buildUI()

    def buildUI(self):
        for key, value in self.preset.items():
            if key == 'icon':
                self.setIcon(AppIcon(32, value))
            elif key == 'txt':
                self.setText(value)
            elif key == 'trg':
                try:
                    self.triggered.disconnect()
                except:
                    pass
                self.triggered.connect(value)
            elif key == 'shortcut':
                self.setShortcut(value)
            elif key == 'checkable':
                self.setChecked(value)
            elif key == 'enabled':
                self.setDisabled(value)
            elif key == 'stt':
                self.setStatusTip(value)
            elif key == 'tt':
                self.setToolTip(value)

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 18/07/2018 - 8:42 AM
# © 2017 - 2018 DAMGteam. All rights reserved