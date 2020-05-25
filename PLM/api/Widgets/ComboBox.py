# -*- coding: utf-8 -*-
"""

Script Name: ComboBox.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from .io_widgets                            import QComboBox
from PLM.utils                              import check_preset
from PLM.cores.SignalManager                import SignalManager
from PLM.settings                           import AppSettings

class ComboBox(QComboBox):

    Type                                    = 'DAMGUI'
    key                                     = 'ComboBox'
    _name                                   = 'DAMG Combo Box'

    def __init__(self, preset={}, parent=None):
        QComboBox.__init__(self)

        self.parent                         = parent
        self.settings = AppSettings(self)
        self.signals = SignalManager(self)
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
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName

    def buildUI(self):
        for key, value in self.preset.items():
            if key == 'items':
                for item in value:
                    self.addItem(item)
            elif key == 'editable':
                self.setEditable(value)
            elif key == 'curIndex':
                self.setCurrentIndex(value)
            elif key == 'setObjName':
                self.setObjectName(value)
            else:
                print("PresetKeyError: There is no key in preset: {}".format(key))

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 27/10/2019 - 6:55 PM
# © 2017 - 2018 DAMGteam. All rights reserved