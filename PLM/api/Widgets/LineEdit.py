# -*- coding: utf-8 -*-
"""

Script Name: Label.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from .io_widgets import QLineEdit
from PLM.api.Gui import IntValidator
from PLM.api.qtOption import PRS


class LineEdit(QLineEdit):

    Type                                    = 'DAMGUI'
    key                                     = 'LineEdit'
    _name                                   = 'DAMG Line Edit'

    def __init__(self, preset=None, parent=None):
        QLineEdit.__init__(self)

        self.parent                         = parent
        self.preset                         = preset
        if self.preset:
            self.buildUI()

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key, decode=None):
        if decode is None:
            return self.settings.initValue(key, self.key)
        else:
            return self.settings.initValue(key, self.key, decode)

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
            if key == 'fn':
                self.setEchoMode(PRS[value])
            elif key == 'txt':
                self.setText(value)
            elif key == 'validator':
                if value == 'int':
                    self.setValidator(IntValidator())
            elif key == 'echo':
                if value == 'password':
                    self.setEchoMode(QLineEdit.Password)
            else:
                print("PresetKeyError at {0}: No such key registed in preset: {1}: {2}".format(__name__, key, value))

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 27/10/2019 - 6:40 PM
# © 2017 - 2018 DAMGteam. All rights reserved