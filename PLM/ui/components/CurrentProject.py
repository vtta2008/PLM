# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
from pyPLM.Widgets                  import GroupHBox, Button, LineEdit


class CurrentProject(GroupHBox):

    key                             = 'CurrentProject'

    def __init__(self, parent=None):
        super(CurrentProject, self).__init__(parent=parent)

        self.parent                 = parent
        setProjectBtn               = Button({'txt': 'Set Project'})
        self.projectPath            = LineEdit()
        self.layout.addWidget(setProjectBtn)
        self.layout.addWidget(self.projectPath)

    def updateProjectPath(self, val):
        return self.projectPath.setText(val)

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
