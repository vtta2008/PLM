# -*- coding: utf-8 -*-
"""

Script Name: VBoxLayout.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
""" Import """

# PyQt5
from PyQt5.QtWidgets                        import QVBoxLayout, QHBoxLayout

# PLM
from toolkits                               import getCopyright, getSetting, getSignals, check_preset


class HBoxLayout(QHBoxLayout):

    Type                                    = 'DAMGUI'
    key                                     = 'HBoxLayout'
    _name                                   = 'DAMG H Box Layout'
    _copyright                              = getCopyright()

    def __init__(self, preset={}, parent=None):
        QHBoxLayout.__init__(self)

        self.settings                       = getSetting(self)
        self.signals                        = getSignals(self)
        self.parent                         = parent

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
                print("{0}: Unrecognise configKey: {1}".format(__name__, key))

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key):
        return self.settings.initValue(key, self.key)

    def sizeHint(self):
        size = super(HBoxLayout, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

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
    _copyright                              = copyright()

    def __init__(self, preset={}, parent=None):
        super(VBoxLayout, self).__init__(parent)

        self.settings                       = getSetting(self)
        self.signals                        = getSignals(self)
        self.parent                         = parent

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

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key):
        return self.settings.initValue(key, self.key)

    def sizeHint(self):
        size = super(VBoxLayout, self).sizeHint()
        size.setHeight(size.height())
        size.setWidth(max(size.width(), size.height()))
        return size

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