# -*- coding: utf-8 -*-
"""

Script Name: Widget.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from PySide2.QtWidgets                      import QDockWidget
from bin.models import DamgSignals
from bin.settings import AppSettings

# -------------------------------------------------------------------------------------------------------------
""" Dock widget """


class DockWidget(QDockWidget):

    Type                                    = 'DAMGUI'
    key                                     = 'DockWidget'
    _name                                   = 'DAMG Dock Widget'

    def __init__(self, parent=None):
        QDockWidget.__init__(self)

        self.parent                         = parent
        self.settings                       = AppSettings(self)
        self.signals                        = DamgSignals(self)

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
# Created by panda on 18/07/2018 - 10:07 AM
# © 2017 - 2018 DAMGteam. All rights reserved