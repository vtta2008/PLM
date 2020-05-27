# -*- coding: utf-8 -*-
"""

Script Name: CheckBox.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from .io_widgets                            import QCheckBox
from PLM.cores.SignalManager                import SignalManager
from PLM.settings                           import AppSettings

class CheckBox(QCheckBox):

    Type                                    = 'DAMGUI'
    key                                     = 'CheckBox'
    _name                                   = 'DAMG Check Box'

    def __init__(self, txt=None, preset={}, parent=None):
        QCheckBox.__init__(self)

        self.parent                         = parent
        self.settings                       = AppSettings(self)
        self.signals                        = SignalManager(self)

        self.txt                            = txt

        if self.txt is not None:
            self.setText(self.txt)
        self.stateChanged.connect(self.saveState)

        self.preset                         = preset
        if self.preset and not {}:
            self.buildUI()

    def saveState(self):
        self.setValue('checkState', self.checkState())

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
# -------------------------------------------------------------------------------------------------------------
# Created by panda on 27/10/2019 - 6:53 PM
# © 2017 - 2018 DAMGteam. All rights reserved