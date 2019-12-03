# -*- coding: utf-8 -*-
"""

Script Name: Action.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __buildtins__                          import __copyright__
""" Import """

# PyQt5
from PyQt5.QtWidgets                        import QAction

# PLM
from utils                                  import check_preset
from appData                                import SETTING_FILEPTH, ST_FORMAT
from toolkits.Core                          import Settings, SignalManager
from .Icon                                  import AppIcon

# -------------------------------------------------------------------------------------------------------------
""" Action presets """

class Action(QAction):

    Type                                    = 'DAMGACTION'
    key                                     = 'Action'
    _name                                   = 'DAMG Action'
    _copyright                              = __copyright__()

    def __init__(self, preset={}, parent=None):
        QAction.__init__(self)
        self.parent                         = parent
        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.signals = SignalManager(self)

        self.preset                         = preset
        if check_preset(self.preset):
            self.buildUI()

    def buildUI(self):
        try:
            self.preset.items()
        except AttributeError:
            pass
        else:
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

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName

class ShortCut(Action):

    key                                 = 'ShortCut'
    _name                               = 'DAMG ShortCut'

    def __init__(self, icon=None, text=None, shortcut=None, trigger=None, parent=None):
        Action.__init__(self)

        self.parent                         = parent
        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.signals = SignalManager(self)

        if text is not None:
            self.setText(text)

        if icon is not None:
            self.setIcon(AppIcon(32, icon))

        if shortcut is not None:
            self.setShortcut(shortcut)

        if trigger is not None:
            self.triggered.connect(trigger)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 18/07/2018 - 8:42 AM
# © 2017 - 2018 DAMGteam. All rights reserved