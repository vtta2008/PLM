# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from pyPLM.Widgets                      import Widget, GridLayout
from PLM.ui.models                      import ActionManager
from .MainMenuBar                       import MainMenuBar
from .MainToolBar                       import MainToolBar
from .ConnectStatus                     import ConnectStatus
from .CurrentProject                    import CurrentProject

class MainHeader(Widget):

    key                                 = 'MainHeader'

    def __init__(self, parent=None):
        super(MainHeader, self).__init__(parent)

        self.parent                     = parent
        actionManger                    = ActionManager()
        self.layout                     = GridLayout(self)
        self.menuBar                    = MainMenuBar(actionManger, self.parent)
        self.connectStatus              = ConnectStatus(self.parent)
        self.toolBar                    = MainToolBar(actionManger, self.parent)
        self.currentProject             = CurrentProject(self.parent)

        self.layout.addWidget(self.menuBar, 0, 0, 1, 9)
        self.layout.addWidget(self.connectStatus, 1, 0, 1, 2)
        self.layout.addWidget(self.currentProject, 1, 2, 1, 4)

        self.layout.addWidget(self.toolBar, 2, 0, 1, 9)

        self.setLayout(self.layout)





# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
