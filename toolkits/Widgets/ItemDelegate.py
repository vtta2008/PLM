# -*- coding: utf-8 -*-
"""

Script Name: IntemDelegate.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtWidgets import QItemDelegate

from toolkits.Core                          import Settings, SignalManager
from appData                                import SETTING_FILEPTH, ST_FORMAT

class ItemDelegate(QItemDelegate):

    key = 'ItemDelegate'

    def __init__(self, parent=None):
        QItemDelegate.__init__(self)

        self.parent = parent
        self.settings = self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.signals = SignalManager(self)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 29/11/2019 - 1:03 AM
# © 2017 - 2018 DAMGteam. All rights reserved