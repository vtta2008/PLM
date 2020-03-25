# -*- coding: utf-8 -*-
"""

Script Name: ProgressBar.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__
""" Import """

# PyQt5
from PyQt5.QtWidgets                        import QProgressBar

# PLM
from PLM.plugins.SignalManager              import SignalManager
from PLM.commons.SettingManager             import SettingManager


class ProgressBar(QProgressBar):

    Type                                    = 'DAMGPROGRESSBAR'
    key                                     = 'ProgressBar'
    _name                                   = 'DAMG Progress Bar'
    _copyright                              = __copyright__()

    def __init__(self, parent=None):
        super(ProgressBar, self).__init__(parent)

        self.signals                        = SignalManager(self)
        self.settings                       = SettingManager(self)

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name = newName

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/11/2020 - 4:07 PM
# © 2017 - 2019 DAMGteam. All rights reserved