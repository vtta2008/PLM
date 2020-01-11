# -*- coding: utf-8 -*-
"""

Script Name: ProgressBar.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import __copyright__
""" Import """

# PyQt5
from PyQt5.QtWidgets import QProgressBar

# PLM
from cores.SignalManager                    import SignalManager


class ProgressBar(QProgressBar):

    Type                                    = 'DAMGPROGRESSBAR'
    key                                     = 'ProgressBar'
    _name                                   = 'DAMG Progress Bar'
    _copyright                              = __copyright__()

    def __init__(self, parent=None):
        QProgressBar.__init__(self)

        self.parent                         = parent
        self.signals                        = SignalManager(self)

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