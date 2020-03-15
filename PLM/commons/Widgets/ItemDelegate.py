# -*- coding: utf-8 -*-
"""

Script Name: IntemDelegate.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from PLM.__main__ import __copyright__

from PyQt5.QtWidgets                        import QItemDelegate

from PLM.cores import SettingManager
from PLM.cores import SignalManager

class ItemDelegate(QItemDelegate):

    key                                     = 'ItemDelegate'
    Type                                    = 'DAMGITEMDELEGATE'
    _name                                   = 'DAMG Item Delegate'
    _copyright                              = __copyright__()

    def __init__(self, parent=None):
        QItemDelegate.__init__(self)

        self.parent                         = parent
        self.settings                       = self.settings = SettingManager(self)
        self.signals                        = SignalManager(self)

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                          = newName

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 29/11/2019 - 1:03 AM
# © 2017 - 2018 DAMGteam. All rights reserved