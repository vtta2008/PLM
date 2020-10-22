# -*- coding: utf-8 -*-
"""

Script Name: ComboBox.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from PySide2.QtWidgets                      import QComboBox
from pyPLM.models import DamgSignals
from pyPLM.settings import AppSettings
from pyPLM.loggers import DamgLogger
from PLM import APP_LOG



class ComboBox(QComboBox):

    Type                                    = 'DAMGUI'
    key                                     = 'ComboBox'
    _name                                   = 'DAMG Combo Box'

    def __init__(self, preset={}, parent=None):
        QComboBox.__init__(self)

        self.parent                         = parent
        self.settings                       = AppSettings(self)
        self.signals                        = DamgSignals(self)
        self.logger = DamgLogger(self, filepth=APP_LOG)
        self.preset                         = preset

        if self.preset and not {}:
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
        for k, v in self.preset.items():
            if k == 'items':
                for i in v:
                    self.addItem(i)
            elif k == '2items':
                for i in v:
                    self.addItem(i[0], i[1])
            elif k == 'editable':
                self.setEditable(v)
            elif k == 'curIndex':
                self.setCurrentIndex(v)
            elif k == 'curIndexChange':
                self.currentIndexChanged.connect(v)
            elif k == 'setObjName':
                self.setObjectName(v)
            elif k =='itemData':
                self.itemData(v)
            else:
                self.logger.error("PresetKeyError: There is no key in preset: {0}".format(k))

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 27/10/2019 - 6:55 PM
# © 2017 - 2018 DAMGteam. All rights reserved