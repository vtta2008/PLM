# -*- coding: utf-8 -*-
"""

Script Name: TaskDetails.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from toolkits.Widgets import GroupGrid, Label, CheckBox, PlainTextEdit
from utils import str2bool

class TaskDetails(GroupGrid):

    key = 'TaskDetails'
    _taskMode = None
    _taskType = None

    def __init__(self, parent=None):
        super(TaskDetails, self).__init__()

        self.parent                 = parent
        self.setTitle('Details')

        self.layout.addWidget(Label({'txt': 'Task Mode: '}), 0, 0, 1, 1)
        self.layout.addWidget(Label({'txt': 'Task Type'}), 1, 0, 1, 1)

        self.individualMode         = CheckBox('Individual')
        self.groupMode              = CheckBox('Group')
        self.departmentMode         = CheckBox('Department')

        self.researchType           = CheckBox('Research')
        self.readingType            = CheckBox('Reading')
        self.vfxType                = CheckBox('VFX')

        self.individualMode.stateChanged.connect(self.individual)
        self.groupMode.stateChanged.connect(self.group)
        self.departmentMode.stateChanged.connect(self.department)
        self.researchType.stateChanged.connect(self.research)
        self.readingType.stateChanged.connect(self.reading)
        self.vfxType.stateChanged.connect(self.vfx)

        self.layout.addWidget(self.individualMode, 0, 1, 1, 1)
        self.layout.addWidget(self.groupMode, 0, 2, 1, 1)
        self.layout.addWidget(self.departmentMode, 0, 3, 1, 1)
        self.layout.addWidget(self.researchType, 1, 1, 1, 1)
        self.layout.addWidget(self.readingType, 1, 2, 1, 1)
        self.layout.addWidget(self.vfxType, 1, 3, 1, 1)

        self.taskDetails = PlainTextEdit()
        self.layout.addWidget(self.taskDetails, 2, 0, 8, 8)

    def individual(self, bool):
        if str2bool(bool):
            self.groupMode.setChecked(False)
            self.departmentMode.setChecked(False)
            self._taskMode = 'individual'

    def group(self, bool):
        if str2bool(bool):
            self.individualMode.setChecked(False)
            self.departmentMode.setChecked(False)
            self._taskMode = 'group'

    def department(self, bool):
        if str2bool(bool):
            self.individualMode.setChecked(False)
            self.groupMode.setChecked(False)
            self._taskMode = 'department'

    def research(self, bool):
        if str2bool(bool):
            self.readingType.setChecked(False)
            self.vfxType.setChecked(False)
            self._taskType = 'research'

    def reading(self, bool):
        if str2bool(bool):
            self.researchType.setChecked(False)
            self.vfxType.setChecked(False)
            self._taskType = 'reading'

    def vfx(self, bool):
        if str2bool(bool):
            self.researchType.setChecked(False)
            self.readingType.setChecked(False)
            self._taskType = 'vfx'

    @property
    def taskType(self):
        return self._taskType

    @taskType.setter
    def taskType(self, val):
        self._taskType = val

    @property
    def taskMode(self):
        return self._taskMode

    @taskMode.setter
    def taskMode(self, val):
        self._taskMode = val

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 2/12/2019 - 10:55 AM
# © 2017 - 2018 DAMGteam. All rights reserved