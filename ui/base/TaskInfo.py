# -*- coding: utf-8 -*-
"""

Script Name: TaskInfo.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtGui import QIntValidator
from toolkits.Widgets import GroupGrid, LineEdit, Label

class TaskInfo(GroupGrid):

    key = 'TaskInfo'

    def __init__(self, parent=None):
        super(TaskInfo, self).__init__()

        self.parent = parent

        self.createLabels()
        self.createLineEdit()

        self.layout.addWidget(self.taskName, 0, 1, 1, 3)
        self.layout.addWidget(self.taskID, 1, 1, 1, 3)
        self.layout.addWidget(self.projectID, 2, 1, 1, 3)
        self.layout.addWidget(self.projectName, 3, 1, 1, 3)
        self.layout.addWidget(self.organisationID, 4, 1, 1, 3)
        self.layout.addWidget(self.organisationName, 5, 1, 1, 3)
        self.layout.addWidget(self.hour, 7, 1, 1, 1)
        self.layout.addWidget(self.minute, 7, 2, 1, 1)
        self.layout.addWidget(self.second, 7, 3, 1, 1)
        self.layout.addWidget(self.day, 9, 1, 1, 1)
        self.layout.addWidget(self.month, 9, 2, 1, 1)
        self.layout.addWidget(self.year, 9, 3, 1, 1)

    def createLineEdit(self):
        self.taskName = LineEdit()
        self.taskID = LineEdit()
        self.projectID = LineEdit()
        self.projectName = LineEdit()
        self.organisationID = LineEdit()
        self.organisationName = LineEdit()
        self.year = LineEdit()
        self.month = LineEdit()
        self.day = LineEdit()
        self.hour = LineEdit()
        self.minute = LineEdit()
        self.second = LineEdit()

        for le in [self.year, self.month, self.day, self.hour, self.minute, self.second]:
            le.setValidator(QIntValidator())

    def createLabels(self):
        self.layout.addWidget(Label({'txt': 'Task Name: '}), 0, 0, 1, 1)
        self.layout.addWidget(Label({'txt': 'Task ID: '}), 1, 0, 1, 1)
        self.layout.addWidget(Label({'txt': 'Project ID: '}), 2, 0, 1, 1)
        self.layout.addWidget(Label({'txt': 'Project Name: '}), 3, 0, 1, 1)
        self.layout.addWidget(Label({'txt': 'Organisation ID: '}), 4, 0, 1, 1)
        self.layout.addWidget(Label({'txt': 'Organisation Name: '}), 5, 0, 1, 1)
        self.layout.addWidget(Label({'txt': 'Duetime'}), 7, 0, 1, 1)
        self.layout.addWidget(Label({'txt': 'Hour'}), 6, 1, 1, 1)
        self.layout.addWidget(Label({'txt': 'Minute'}), 6, 2, 1, 1)
        self.layout.addWidget(Label({'txt': 'Second'}), 6, 3, 1, 1)
        self.layout.addWidget(Label({'txt': 'Duedate'}), 9, 0, 1, 1)
        self.layout.addWidget(Label({'txt': 'Day'}), 8, 1, 1, 1)
        self.layout.addWidget(Label({'txt': 'Month'}), 8, 2, 1, 1)
        self.layout.addWidget(Label({'txt': 'Year'}), 8, 3, 1, 1)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 2/12/2019 - 10:51 AM
# © 2017 - 2018 DAMGteam. All rights reserved