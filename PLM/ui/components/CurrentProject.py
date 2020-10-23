# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from PLM                            import PRJ_DIR
from PLM.utils                      import get_file_path
from pyPLM.Widgets                  import Widget, GridLayout, Button, LineEdit, Label


class CurrentProject(Widget):

    key                             = 'CurrentProject'

    def __init__(self, parent=None):
        super(CurrentProject, self).__init__(parent=parent)

        self.parent                 = parent
        self.layout                 = GridLayout(self)

        self.get_all_projects()

        projectLabel                = Label({'txt': 'Project: '})
        self.projectName            = Label({'txt': 'Default'})
        setProjectBtn               = Button({'txt': 'Set Project'})

        pathLabel                   = Label({'txt': 'Path: '})
        self.projectPath            = LineEdit()

        self.layout.addWidget(projectLabel, 0, 0, 1, 1)
        self.layout.addWidget(self.projectName, 0, 1, 1, 1)
        self.layout.addWidget(setProjectBtn, 0, 2, 1, 1)
        self.layout.addWidget(pathLabel, 1, 0, 1, 1)
        self.layout.addWidget(self.projectPath, 1, 1, 1, 2)

        self.setLayout(self.layout)

    def updateProjectPath(self, val):
        return self.projectPath.setText(val)

    def updateProjectName(self, val):
        return self.projectName.setText(val)

    def get_all_projects(self):
        files = get_file_path(PRJ_DIR, '.projects')
        print(files)

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
