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
from appData                                import SETTING_FILEPTH, ST_FORMAT, __copyright__
from cores.Settings                         import Settings
from ui.uikits.Icon                         import AppIcon
from ui.uikits.uiUtils                      import check_preset

# -------------------------------------------------------------------------------------------------------------
""" Action presets """

class Action(QAction):

    Type                                    = 'DAMGUI'
    key                                     = 'Action'
    _name                                   = 'DAMG Action'
    _copyright                              = __copyright__
    _data                                   = dict()

    def __init__(self, preset={}, parent=None):
        super(Action, self).__init__(parent)

        self.parent         = parent
        self.preset         = preset
        self.settings       = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)

        if check_preset(self.preset):
            self.buildUI()

    def buildUI(self):
        for key, value in self.preset.items():
            if key == 'icon':
                self.setIcon(AppIcon(32, value))
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
            elif key == 'tt':
                self.setToolTip(value)

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key):
        return self.settings.initValue(key, self.key)

    @property
    def copyright(self):
        return self._copyright

    @property
    def data(self):
        return self._data

    @property
    def name(self):
        return self._name

    @data.setter
    def data(self, newData):
        self._data                      = newData

    @name.setter
    def name(self, newName):
        self._name                      = newName

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 18/07/2018 - 8:42 AM
# © 2017 - 2018 DAMGteam. All rights reserved