# -*- coding: utf-8 -*-
"""

Script Name: TaskInfo.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

import json

from PyQt5.QtCore                               import QDate, QTime

from PLM.commons.Widgets import GroupBox, VBoxLayout, Label
from PLM.cores import LocalDatabase
from PLM.cores.base import DateLine
from PLM.cores import Task




class TaskInfo(GroupBox):

    key = 'TaskInfo'

    def __init__(self, task):
        super(TaskInfo, self).__init__()

        self.database                           = LocalDatabase()

        with open(task, 'r') as f:
            self._data                          = json.load(f)

        self.setMaximumWidth(100)

        self.setTitle(self._data['id'])
        self.layout                             = VBoxLayout()

        self._id                                = self._data['id']
        self._name                              = self._data['name']
        self._mode                              = self._data['mode']
        self._type                              = self._data['type']

        self._teamID                            = self._data['teamID']
        self._projectID                         = self._data['projectID']
        self._organisationID                    = self._data['organisationID']

        self._details                           = self._data['details']

        self._hour                              = int(self._data['endtime'].split(':')[0])
        self._minute                            = int(self._data['endtime'].split(':')[1])
        self._second                            = int(self._data['endtime'].split(':')[2])

        self._day                               = int(self._data['enddate'].split('/')[0])
        self._month                             = int(self._data['enddate'].split('/')[1])
        self._year                              = int(self._data['enddate'].split('/')[2])

        self.start                              = DateLine(QTime.currentTime().hour(), QTime.currentTime().minute(),
                                                           QTime.currentTime().second(), QDate.currentDate().day(),
                                                           QDate.currentDate().month(), QDate.currentDate().year())
        self.end                                = DateLine(self._hour, self._minute, self._second, self._day, self._month, self._year)

        try:
            self.username = [self.database.query_table('curUser')[0]]
        except (ValueError, IndexError):
            self.username = []

        self.task = Task(self._id, self._name, self._mode, self._type,
                         self._teamID, self._projectID, self._organisationID,
                         self.start, self.end, self._details)

        self._countdown                         = '{0}:{1}:{2}'.format(self.task.hours, self.task.minutes, self.task.seconds)
        self.task.countdown.connect(self.update_countdown)

        self.task_status                        = Label({'txt': '{0}'.format(self.task.status)})
        self.task_duedate                       = Label({'txt': '{0}'.format(self.task._enddate)})
        self.task_duetime                       = Label({'txt': '{0}'.format(self.task._endtime)})
        self.task_countdown                     = Label({'txt': '{0}'.format(self._countdown)})

        self.layout.addWidget(self.task_status)
        self.layout.addWidget(self.task_duedate)
        self.layout.addWidget(self.task_duetime)
        self.layout.addWidget(self.task_countdown)

        self.setLayout(self.layout)
        self.setMaximumSize(100, 120)

    def update_countdown(self, val):
        if self.task.status == 'Overdued':
            self.task_status.setStyleSheet('color: red')
        elif self.task.status == 'Urgent':
            self.task_status.setStyleSheet('color: orange')
        else:
            self.task_status.setStyleSheet('color: green')
        return self.task_countdown.setText(val)

    @property
    def id(self):
        return self._id

    @property
    def mode(self):
        return self._mode

    @property
    def type(self):
        return self._type

    @property
    def project(self):
        return self._projectID

    @property
    def organisation(self):
        return self._organisationID

    @property
    def hour(self):
        return self._hour

    @property
    def minute(self):
        return self._minute

    @property
    def second(self):
        return self._second

    @property
    def day(self):
        return self._day

    @property
    def month(self):
        return self._month

    @property
    def year(self):
        return self._year

    @id.setter
    def id(self, val):
        self._id = val

    @mode.setter
    def mode(self, val):
        self._mode = val

    @type.setter
    def type(self, val):
        self._type = val

    @project.setter
    def project(self, val):
        self._projectID = val

    @organisation.setter
    def organisation(self, val):
        self._organisationID = val

    @hour.setter
    def hour(self, val):
        self._hour = val

    @minute.setter
    def minute(self, val):
        self._minute = val

    @second.setter
    def second(self, val):
        self._second = val

    @day.setter
    def day(self, val):
        self._day = val

    @month.setter
    def month(self, val):
        self._month = val

    @year.setter
    def year(self, val):
        self._year = val


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 2/12/2019 - 10:49 PM
# © 2017 - 2018 DAMGteam. All rights reserved