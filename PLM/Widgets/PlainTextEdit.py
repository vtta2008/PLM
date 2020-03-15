# -*- coding: utf-8 -*-
"""

Script Name: PlainTextEdit.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from PLM.__main__ import __copyright__

from PyQt5.QtWidgets                        import QPlainTextEdit

from PLM.utils import check_preset
from PLM.cores import SettingManager
from PLM.cores import SignalManager

class PlainTextEdit(QPlainTextEdit):

    Type                                    = 'DAMGPLAINTEXTEDIT'
    key                                     = 'PlainTextEdit'
    _name                                   = 'DAMG Plain Text Edit'
    _copyright                              = __copyright__()

    def __init__(self, preset={}, parent=None):
        QPlainTextEdit.__init__(self)

        self.parent                         = parent
        self.settings                       = SettingManager(self)
        self.signals                        = SignalManager(self)

        self.preset                         = preset
        if check_preset(self.preset):
            self.buildUI()

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key, decode=None):
        if decode is None:
            return self.settings.initValue(key, self.key)
        else:
            return self.settings.initValue(key, self.key, decode)

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName

    def buildUI(self):
        if self.preset is None or self.preset == {}:
            self.preset = {'txt': ' '}

        for key, value in self.preset.items():
            if key == 'lwm': # setLineWrapMode
                self.setLineWrapMode(value)
            elif key == 'sfh': # setFixHeight
                self.setFixedHeight(value)
            elif key == 'vsbp': # setVerticalScrollBarPolicy
                self.setVerticalScrollBarPolicy(value)
            elif key == 'adr': # setAcceptDrops
                self.setAcceptDrops(value)
            elif key == 'rol': # setReadOnly
                self.setReadOnly(value)


class Detector(PlainTextEdit):

    key                                     = 'Detector'
    _name                                   = 'DAMG Detector'

    def __init__(self):
        PlainTextEdit.__init__(self)



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 27/11/2019 - 6:44 PM
# © 2017 - 2018 DAMGteam. All rights reserved