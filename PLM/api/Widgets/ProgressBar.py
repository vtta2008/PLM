# -*- coding: utf-8 -*-
"""

Script Name: ProgressBar.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from .io_widgets import QProgressBar


class ProgressBar(QProgressBar):

    Type                                    = 'DAMGPROGRESSBAR'
    key                                     = 'ProgressBar'
    _name                                   = 'DAMG Progress Bar'

    def __init__(self, parent=None):
        super(ProgressBar, self).__init__(parent)

        self.parent = parent

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name                          = val

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/11/2020 - 4:07 PM
# © 2017 - 2019 DAMGteam. All rights reserved