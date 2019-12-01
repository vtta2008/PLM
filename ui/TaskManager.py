# -*- coding: utf-8 -*-
"""

Script Name: Task.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals


from cores.Task                         import Task
from cores.base                         import DateLine
from .base                              import TaskInfo, TaskDetails
from functools                          import partial
from toolkits.Widgets                   import (Widget, Button, VBoxLayout, HBoxLayout, AppIcon)


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

        dateline       = DateLine(h, m, s, d, mo, y)
        newTask = Task(id, name, mode, taskType, project, organisation, dateline, details)

        self.newTaskEvent(newTask)

        return newTask

    def editTask(self, taskName):
        pass

    def resizeEvent(self, event):
        w = int(self.width())
        self.taskInfo.setMaximumWidth(w/3)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/11/2019 - 12:48 AM
# © 2017 - 2018 DAMGteam. All rights reserved