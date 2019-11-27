# -*- coding: utf-8 -*-
"""

Script Name: Task.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtGui                        import QIntValidator

from toolkits.Widgets.Widget import Widget
from toolkits.Widgets.CheckBox import CheckBox
from toolkits.Widgets.BoxLayout import HBoxLayout, VBoxLayout
from toolkits.Widgets.GridLayout import GridLayout
from toolkits.Widgets.GroupBoxBase import GroupBox
from toolkits.Widgets.LineEdit import LineEdit, PlainTextEdit
from toolkits.Widgets.Label import Label
from toolkits.Widgets.Button import Button
from utils                              import str2bool
from cores.Task                         import duetime, duedate, Task
from functools                          import partial

class TaskInfo(GridLayout):

    key = 'TaskInfo'

    def __init__(self, parent=None):
        super(TaskInfo, self).__init__(parent)

        self.parent = parent

        self.addWidget(Label({'txt': 'Task Name: '}), 0, 0, 1, 1)
        self.taskName = LineEdit()
        self.addWidget(self.taskName, 0, 1, 1, 3)

        self.addWidget(Label({'txt': 'Task ID: '}), 1, 0, 1, 1)
        self.taskID = LineEdit()
        self.addWidget(self.taskID, 1, 1, 1, 3)

        self.addWidget(Label({'txt': 'Project ID: '}), 2, 0, 1, 1)
        self.projectID = LineEdit()
        self.addWidget(self.projectID, 2, 1, 1, 3)

        self.addWidget(Label({'txt': 'Project Name: '}), 3, 0, 1, 1)
        self.projectName = LineEdit()
        self.addWidget(self.projectName, 3, 1, 1, 3)

        self.addWidget(Label({'txt': 'Organisation ID: '}), 4, 0, 1, 1)
        self.organisationID = LineEdit()
        self.addWidget(self.organisationID, 4, 1, 1, 3)

        self.addWidget(Label({'txt': 'Organisation Name: '}), 5, 0, 1, 1)
        self.organisationName = LineEdit()
        self.addWidget(self.organisationName, 5, 1, 1, 3)

        self.addWidget(Label({'txt': 'Duetime'}), 7, 0, 1, 1)
        self.addWidget(Label({'txt': 'Hour'}), 6, 1, 1, 1)
        self.addWidget(Label({'txt': 'Minute'}), 6, 2, 1, 1)
        self.addWidget(Label({'txt': 'Second'}), 6, 3, 1, 1)
        self.addWidget(Label({'txt': 'Duedate'}), 9, 0, 1, 1)
        self.addWidget(Label({'txt': 'Day'}), 8, 1, 1, 1)
        self.addWidget(Label({'txt': 'Month'}), 8, 2, 1, 1)
        self.addWidget(Label({'txt': 'Year'}), 8, 3, 1, 1)

        self.year = LineEdit()
        self.month = LineEdit()
        self.day = LineEdit()
        self.hour = LineEdit()
        self.minute = LineEdit()
        self.second = LineEdit()

        for le in [self.year, self.month, self.day, self.hour, self.minute, self.second]:
            le.setValidator(QIntValidator())

        self.addWidget(self.hour, 7, 1, 1, 1)
        self.addWidget(self.minute, 7, 2, 1, 1)
        self.addWidget(self.second, 7, 3, 1, 1)
        self.addWidget(self.day, 9, 1, 1, 1)
        self.addWidget(self.month, 9, 2, 1, 1)
        self.addWidget(self.year, 9, 3, 1, 1)

class TaskDetails(GridLayout):

    key = 'TaskDetails'
    _taskMode = None
    _taskType = None

    def __init__(self, parent=None):
        super(TaskDetails, self).__init__(parent)

        self.parent = parent
        self.addWidget(Label({'txt': 'Task Mode: '}), 0, 0, 1, 1)
        self.addWidget(Label({'txt': 'Task Type'}), 1, 0, 1, 1)

        self.individualMode = CheckBox('Individual')
        self.groupMode = CheckBox('Group')
        self.departmentMode = CheckBox('Department')

        self.individualMode.stateChanged.connect(self.individual)
        self.groupMode.stateChanged.connect(self.group)
        self.departmentMode.stateChanged.connect(self.department)

        self.researchType = CheckBox('Research')
        self.readingType = CheckBox('Reading')
        self.vfxType = CheckBox('VFX')
        self.researchType.stateChanged.connect(self.research)
        self.readingType.stateChanged.connect(self.reading)
        self.vfxType.stateChanged.connect(self.vfx)

        self.addWidget(self.individualMode, 0, 1, 1, 1)
        self.addWidget(self.groupMode, 0, 2, 1, 1)
        self.addWidget(self.departmentMode, 0, 3, 1, 1)
        self.addWidget(self.researchType, 1, 1, 1, 1)
        self.addWidget(self.readingType, 1, 2, 1, 1)
        self.addWidget(self.vfxType, 1, 3, 1, 1)

        self.taskDetails = PlainTextEdit()
        self.addWidget(self.taskDetails, 2, 0, 8, 8)

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

    def __init__(self, parent=True):
        super(TaskManager, self).__init__(parent)

        self.parent = parent
        self.setWindowTitle('Task Manager')
        self.layout = VBoxLayout()
        line1 = HBoxLayout()
        line2 = HBoxLayout()

        self.infoGrp = GroupBox('Task Info')
        self.taskInfo = TaskInfo(self)
        self.infoGrp.setLayout(self.taskInfo)
        line1.addWidget(self.infoGrp)

        self.detailsGrp = GroupBox('Details')
        self.taskDetails = TaskDetails(self)
        self.detailsGrp.setLayout(self.taskDetails)
        line1.addWidget(self.detailsGrp)

        self.layout.addLayout(line1)
        self.layout.addLayout(line2)

        self.okButton = Button({'txt': 'Ok', 'cl': self.executeTask})
        self.cancelButton = Button({'txt': 'Cancel', 'cl': partial(self.signals.emit, 'showLayout', self.key, 'hide')})
        line2.addWidget(self.okButton)
        line2.addWidget(self.cancelButton)

        self.setLayout(self.layout)
        self.setMinimumWidth(750)

    def executeTask(self):

        h = int(self.taskInfo.hour.text())
        m = int(self.taskInfo.minute.text())
        s = int(self.taskInfo.second.text())
        self.duetime = duetime(h, m, s)

        y = int(self.taskInfo.year.text())
        mo = int(self.taskInfo.month.text())
        d = int(self.taskInfo.day.text())
        self.duedate = duedate(d, mo, y)

        id = self.taskInfo.taskID.text()
        name = self.taskInfo.taskName.text()
        type = self.taskDetails.taskType
        mode = self.taskDetails.taskMode
        project = [self.taskInfo.projectID.text(), self.taskInfo.projectName.text()]
        organisation = [self.taskInfo.organisationID.text(), self.taskInfo.organisationName.text()]
        details = self.taskDetails.taskDetails.toPlainText()

        Task(id, name, mode, type, project, organisation, self.duetime, self.duedate, details)
        self.parent.topTabUI.tab1.update_tasks()

    def resizeEvent(self, event):
        w = int(self.width())
        self.infoGrp.setMaximumWidth(w/3)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/11/2019 - 12:48 AM
# © 2017 - 2018 DAMGteam. All rights reserved