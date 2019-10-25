# -*- coding: utf-8 -*-
"""

Script Name: UiSignals.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtCore import pyqtSignal

from cores.base import DAMG

class UiSignals(DAMG):

    showLayout = pyqtSignal(str, str)
    executing = pyqtSignal(str)
    regisLayout = pyqtSignal(DAMG)
    openBrowser = pyqtSignal(str)
    setSetting = pyqtSignal(str, str, str)
    sysNotify = pyqtSignal(str, str, str, int)

    updateAvatar = pyqtSignal(bool)
    cfgReport = pyqtSignal(str)

    def __init__(self, parent=None):
        super(UiSignals, self).__init__(parent)

        self.parent = parent
        self._id = self.parent.__class__.__name__

    @property
    def id(self):
        return self._id


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/10/2019 - 6:59 AM
# © 2017 - 2018 DAMGteam. All rights reserved