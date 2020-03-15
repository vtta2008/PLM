# -*- coding: utf-8 -*-
"""

Script Name: Settings.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from PLM.__main__ import __copyright__
""" Import """

# PyQt5
from PyQt5.QtCore                           import QSettings


class Settings(QSettings):

    Type                                    = 'DAMGSETTING'
    key                                     = 'Settings'
    name                                    = 'DAMG Setting'
    _coyright                               = __copyright__()

    def __init__(self, filename, fmt):
        QSettings.__init__(self, filename, fmt)

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name                          = val


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/17/2020 - 11:00 AM
# © 2017 - 2019 DAMGteam. All rights reserved