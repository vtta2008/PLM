# -*- coding: utf-8 -*-
"""

Script Name: VBoxLayout.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PyQt5
from PLM                                    import __copyright__
from .io_widgets                            import QVBoxLayout, QHBoxLayout
from PLM.utils                              import check_preset
from PLM.plugins.SignalManager              import SignalManager
from PLM.cores.Settings.app_settings import AppSettings


class HBoxLayout(QHBoxLayout):

    Type                                    = 'DAMGUI'
    key                                     = 'HBoxLayout'
    _name                                   = 'DAMG H Box Layout'
    _copyright                              = __copyright__()

    def __init__(self, parent=None, preset={}):
        QHBoxLayout.__init__(self)
        self.parent                         = parent
        self.settings                       = AppSettings(self)
        self.signals                        = SignalManager(self)
        self.preset                         = preset
        if check_preset(self.preset):
            self.buildUI()

    def buildUI(self):
        for key, value in self.preset.items():
            if key == 'addWidget':
                for widget in value:
                    self.addWidget(widget)
            elif key == 'addLayout':
                for layout in value:
                    self.addLayout(layout)
            elif key == 'addStretch':
                self.setStretch(value, 0)
            else:
                print("{0}: Unrecognise configKey: {1}".format(__name__, key))

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName


class VBoxLayout(QVBoxLayout):

    Type                                    = 'DAMGUI'
    key                                     = 'VBoxLayout'
    _name                                   = 'DAMG V Box Layout'
    _copyright                              = __copyright__()

    def __init__(self, parent=None, preset={}):
        QVBoxLayout.__init__(self)
        self.parent                         = parent
        # self.settings                       = SettingManager(self)

        self.preset                         = preset
        if check_preset(self.preset):
            self.buildUI()

    def buildUI(self):
        for key, value in self.preset.items():
            if key == 'addWidget':
                for widget in value:
                    self.addWidget(widget)
            elif key == 'addLayout':
                for layout in value:
                    self.addLayout(layout)
            elif key == 'addStretch':
                self.setStretch(value, 0)
            else:
                print("Unrecognise configKey: {}".format(key))

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
# Created by panda on 27/10/2019 - 6:57 PM
# © 2017 - 2018 DAMGteam. All rights reserved