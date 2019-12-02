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

class BaseInfo(GroupGrid):

    key                         = 'BaseInfo'

    def __init__(self, parent=None):
        super(BaseInfo, self).__init__()

        self.parent = parent
        self.setTitle('Info')

        self.createLabels()
        self.createLineEdit()

        self.layout.addWidget(self.name, 0, 1, 1, 3)
        self.layout.addWidget(self.id, 1, 1, 1, 3)
        self.layout.addWidget(self.teamID, 2, 1, 1, 3)
        self.layout.addWidget(self.projectID, 3, 1, 1, 3)
        self.layout.addWidget(self.organisationID, 4, 1, 1, 3)

        self.layout.addWidget(self.hourS, 6, 1, 1, 1)
        self.layout.addWidget(self.minuteS, 6, 2, 1, 1)
        self.layout.addWidget(self.secondS, 6, 3, 1, 1)
        self.layout.addWidget(self.dayS, 6, 4, 1, 1)
        self.layout.addWidget(self.monthS, 6, 5, 1, 1)
        self.layout.addWidget(self.yearS, 6, 6, 1, 1)

        self.layout.addWidget(self.hourE, 7, 1, 1, 1)
        self.layout.addWidget(self.minuteE, 7, 2, 1, 1)
        self.layout.addWidget(self.secondE, 7, 3, 1, 1)
        self.layout.addWidget(self.dayE, 7, 4, 1, 1)
        self.layout.addWidget(self.monthE, 7, 5, 1, 1)
        self.layout.addWidget(self.yearE, 7, 6, 1, 1)

    def createLineEdit(self):
        self.name               = LineEdit()
        self.id                 = LineEdit()

        self.teamID             = LineEdit()
        self.projectID          = LineEdit()
        self.organisationID     = LineEdit()

        self.yearS              = LineEdit()
        self.monthS             = LineEdit()
        self.dayS               = LineEdit()
        self.hourS              = LineEdit()
        self.minuteS            = LineEdit()
        self.secondS            = LineEdit()

        self.yearE              = LineEdit()
        self.monthE             = LineEdit()
        self.dayE               = LineEdit()
        self.hourE              = LineEdit()
        self.minuteE            = LineEdit()
        self.secondE            = LineEdit()

        for le in [self.yearS, self.monthS, self.dayS, self.hourS, self.minuteS, self.secondS,
                   self.yearE, self.monthE, self.dayE, self.hourE, self.minuteE, self.secondE]:
            le.setValidator(QIntValidator())

    def createLabels(self):
        self.layout.addWidget(Label({'txt': 'Name: '}), 0, 0, 1, 1)
        self.layout.addWidget(Label({'txt': 'ID: '}), 1, 0, 1, 1)
        self.layout.addWidget(Label({'txt': 'Prj ID: '}), 2, 0, 1, 1)
        self.layout.addWidget(Label({'txt': 'Org ID: '}), 3, 0, 1, 1)
        self.layout.addWidget(Label({'txt': 'Team ID: '}), 4, 0, 1, 1)

        self.layout.addWidget(Label({'txt': 'Hour'}), 5, 1, 1, 1)
        self.layout.addWidget(Label({'txt': 'Minute'}), 5, 2, 1, 1)
        self.layout.addWidget(Label({'txt': 'Second'}), 5, 3, 1, 1)
        self.layout.addWidget(Label({'txt': 'Day'}), 5, 4, 1,  1)
        self.layout.addWidget(Label({'txt': 'Month'}), 5, 5, 1, 1)
        self.layout.addWidget(Label({'txt': 'Year'}), 5, 6, 1, 1)

        self.layout.addWidget(Label({'txt': 'Start'}), 6, 0, 1, 1)
        self.layout.addWidget(Label({'txt': 'End'}), 7, 0, 1, 1)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 2/12/2019 - 10:51 AM
# © 2017 - 2018 DAMGteam. All rights reserved