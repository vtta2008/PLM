# -*- coding: utf-8 -*-
"""

Script Name: Action.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__
""" Import """

# PyQt5
from PyQt5.QtWidgets                        import QAction, QWidgetAction

# PLM
from PLM.utils                              import check_preset
from PLM.commons                            import SignalManager, SettingManager
from PLM.commons.Gui.Icon                   import AppIcon

# -------------------------------------------------------------------------------------------------------------
""" Action presets """

class WidgetAction(QWidgetAction):

    Type                                    = 'DAMGWIDGETACTION'
    key                                     = 'WidgetAction'
    _name                                   = 'DAMG Widget Action'
    _copyright                              = __copyright__()

    def __init__(self, parent=None):
        QWidgetAction.__init__(self)

        self.parent                         = parent
        self.settings                       = SettingManager(self)
        self.signals                        = SignalManager(self)


    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName

class Action(QAction):

    Type                                    = 'DAMGACTION'
    key                                     = 'Action'
    _name                                   = 'DAMG Action'
    _copyright                              = __copyright__()

    def __init__(self, preset={}, parent=None):
        QAction.__init__(self)
        self.parent                         = parent
        self.settings                       = SettingManager(self)
        self.signals                        = SignalManager(self)

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
                elif key == 'son':
                    self.setObjectName(value)
                elif key == 'vsb':
                    self.setVisible(value)

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

        self.parent                      = parent
        self.settings                    = SettingManager(self)
        self.signals                     = SignalManager(self)

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