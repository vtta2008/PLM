# -*- coding: utf-8 -*-
"""

Script Name: VBoxLayout.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtWidgets                        import QVBoxLayout

from appData                                import SETTING_FILEPTH, ST_FORMAT, __copyright__
from ui.uikits.uiUtils                      import check_preset
from cores.SignalManager                    import SignalManager
from cores.Loggers                          import Loggers
from cores.Settings                         import Settings


class HBoxLayout(QHBoxLayout):

    Type                                    = 'DAMGUI'
    key                                     = 'HBoxLayout'
    _name                                   = 'DAMG H Box Layout'
    _copyright                              = __copyright__
    _data                                   = dict()

    def __init__(self, preset={}, parent=None):
        QHBoxLayout.__init__(self)

        self.signals = SignalManager(self)
        self.logger = Loggers(self.__class__.__name__)
        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.parent = parent

        self.preset = preset

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

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key):
        return self.settings.initValue(key, self.key)

    def sizeHint(self):
        size = super(HBoxLayout, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

class VBoxLayout(QVBoxLayout):

    Type                                    = 'DAMGUI'
    key                                     = 'VBoxLayout'
    _name                                   = 'DAMG V Box Layout'
    _copyright                              = __copyright__

    def __init__(self, preset={}, parent=None):
        super(VBoxLayout, self).__init__(parent)

        self.signals = SignalManager(self)
        self.logger = Loggers(self.__class__.__name__)
        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.parent = parent

        self.preset = preset
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

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key):
        return self.settings.initValue(key, self.key)

    def sizeHint(self):
        size = super(VBoxLayout, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 27/10/2019 - 6:57 PM
# © 2017 - 2018 DAMGteam. All rights reserved