# -*- coding: utf-8 -*-
"""

Script Name: ToolBarDock.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PLM
from ui.uikits.ToolBar             import ToolBar
from ui.uikits.DockWidget          import DockWidget
from ui.uikits.GridLayout          import GridLayout

# -------------------------------------------------------------------------------------------------------------
""" Tool bar docking class """

class DockToolBar(DockWidget):

    key = 'dockToolBar'

    def __init__(self, name="TEXTURE", parent=None):
        super(DockToolBar, self).__init__(parent)

        self.name               = name
        self.key                = 'dockToolBar' + " {0}".format(self.name)
        self.setWindowTitle(self.name)

        self.buildUI()

    def buildUI(self):
        self.layout             = GridLayout()
        self.toolbar            = ToolBar(self.name, self)
        self.layout.addWidget(self.toolbar, 0, 0, 1, 1)
        self.setLayout(self.layout)



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 21/07/2018 - 6:43 AM
# © 2017 - 2018 DAMGteam. All rights reserved