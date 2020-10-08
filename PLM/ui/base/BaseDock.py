# -*- coding: utf-8 -*-
"""

Script Name: BaseDock.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from bin.Widgets import DockWidget
from PLM.api.qtOption import FRAMELESS, dockAll

class BaseDock(DockWidget):

    key                                 = 'BaseDock'
    _name                               = 'BaseDock'

    def __init__(self, parent=None):
        super(BaseDock, self).__init__(parent)

        self.setWindowFlags(FRAMELESS)
        self.setFeatures(self.DockWidgetFloatable | self.DockWidgetMovable)
        self.setAllowedAreas(dockAll)

    def close(self):
        self.hide()

    def closeEvent(self, event):
        self.hide()
        event.ignore()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/17/2020 - 3:24 AM
# © 2017 - 2019 DAMGteam. All rights reserved