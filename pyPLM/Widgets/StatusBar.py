# -*- coding: utf-8 -*-
"""

Script Name: StatusBar.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from PySide2.QtWidgets                      import QStatusBar

# -------------------------------------------------------------------------------------------------------------
""" StatusBar """


class StatusBar(QStatusBar):

    Type                                    = "DAMGUI"
    key                                     = 'StatusBar'
    _name                                   = "DAMG Status Bar"

    def __init__(self, parent=None):
        super(StatusBar, self).__init__(parent)
        self.parent                         = parent

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 4:00 PM
# © 2017 - 2018 DAMGteam. All rights reserved