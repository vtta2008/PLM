# -*- coding: utf-8 -*-
"""

Script Name: Task.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtGui                        import QIntValidator

from utils                              import str2bool
from cores.Task                         import duetime, duedate, Task
from functools                          import partial
from toolkits.Widgets                   import (GridLayout, Label, LineEdit, GroupBox, CheckBox, PlainTextEdit, Widget,
                                                Button, VBoxLayout, HBoxLayout, AppIcon)

class TaskInfo(GroupBox):

    key = 'TaskInfo'

    def __init__(self, parent=None):
        super(TaskInfo, self).__init__(parent)

        self.parent = parent
        self.layout = GridLayout()
        self.setLayout(self.layout)

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

class TaskDetails(GroupBox):

    key = 'TaskDetails'
    _taskMode = None
    _taskType = None

    def __init__(self, parent=None):
        super(TaskDetails, self).__init__(parent)

        self.parent                 = parent
        self.setTitle('Details')

        self.layout                 = GridLayout()

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

        self.setLayout(self.layout)

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

class TaskManager(Widget):

    key = 'TaskManager'

    def __init__(self, parent=None):
        super(TaskManager, self).__init__(parent)

        self.parent = parent
        self.setWindowTitle('Task Manager')
        self.setWindowIcon(AppIcon(32, 'TaskManager'))

        self.layout = VBoxLayout()
        self.layout.addLayout(self.buildLine1())
        self.layout.addLayout(self.buildLine2())
        self.setLayout(self.layout)

    def buildLine1(self):
        self.taskInfo       = TaskInfo()
        self.taskDetails    = TaskDetails()
        return HBoxLayout({'addWidget': [self.taskInfo, self.taskDetails]})

    def buildLine2(self):
        self.okButton       = Button({'txt': 'Ok', 'cl': self.createTask})
        self.editButton     = Button({'txt': 'Edit', 'cl': self.editTask})
        self.cancelButton   = Button({'txt': 'Cancel', 'cl': partial(self.signals.emit, 'showLayout', self.key, 'hide')})
        return HBoxLayout({'addWidget': [self.okButton, self.editButton, self.cancelButton]})

    def createTask(self):

        h                   = int(self.taskInfo.hour.text())
        m                   = int(self.taskInfo.minute.text())
        s                   = int(self.taskInfo.second.text())
        y                   = int(self.taskInfo.year.text())
        mo                  = int(self.taskInfo.month.text())
        d                   = int(self.taskInfo.day.text())

        id                  = self.taskInfo.taskID.text()
        name                = self.taskInfo.taskName.text()
        taskType            = self.taskDetails.taskType
        mode                = self.taskDetails.taskMode
        project             = [self.taskInfo.projectID.text(), self.taskInfo.projectName.text()]
        organisation        = [self.taskInfo.organisationID.text(), self.taskInfo.organisationName.text()]
        details             = self.taskDetails.taskDetails.toPlainText()

        self.duetime        = duetime(h, m, s)
        self.duedate        = duedate(d, mo, y)

        newTask = Task(id, name, mode, taskType, project, organisation, self.duetime, self.duedate, details)
        self.newTaskEvent(newTask)
        return newTask

    def editTask(self, taskName):
        pass

    # def resizeEvent(self, event):
    #     w = int(self.width())
    #     self.taskInfo.setMaximumWidth(w/3)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/11/2019 - 12:48 AM
# © 2017 - 2018 DAMGteam. All rights reserved