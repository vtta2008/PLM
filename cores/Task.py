# -*- coding: utf-8 -*-
"""

Script Name: Task.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

import os, json
from playsound                          import playsound

from bin                                import DAMGDICT, DAMGLIST
from cores.base                         import TaskBase
from appData                            import SOUND_DIR, TASK_DIR
from PyQt5.QtCore                       import QDateTime


class Task(TaskBase):

    taskData                = DAMGDICT()

    def __init__(self, taskID=None, taskName=None, taskMode=None, taskType=None, assigned = None,
                       project=None, organisation=None,
                       dateline=None,
                       details={}):

        super(Task, self).__init__()

        self.taskID         = taskID
        self.taskName       = taskName
        self.taskMode       = taskMode
        self.taskType       = taskType

        self.assigned       = assigned
        if not self.assigned:
            self.assigned   = DAMGLIST()

        self.project        = project
        self.details        = details
        self.organisation   = organisation

        self.dateline       = dateline

        self.duetime        = self.dateline.time
        self.duedate        = self.dateline.date
        self.endDate        = self.dateline.endDate

        self.update()

        format = self.countter_format()
        self.timer.timeout.connect(self.update)
        self.timer.start(format)

    def update(self):
        self.startDate = QDateTime(self.date.currentDate(), self.time.currentTime())
        self.days = self.startDate.daysTo(self.endDate)

        self.hours = self.endDate.time().hour() - self.startDate.time().hour()
        if self.hours <= 0:
            if self.days > 0:
                self.days = self.days - 1
                self.hours = self.hours + 24

        self.minutes = self.endDate.time().minute() - self.startDate.time().minute()
        if self.minutes <= 0:
            if self.hours > 0:
                self.hours = self.hours - 1
                self.minutes = self.minutes + 60

        self.seconds = self.endDate.time().second() - self.startDate.time().second()
        if self.seconds <= 0:
            if self.minutes > 0:
                self.minutes = self.minutes - 1
                self.seconds = self.seconds + 60

        self._status = self.get_status()

        if self.days == 0:
            if self.hours == 0:
                if self.minutes == 0:
                    if self.seconds <= 30:
                        pth = os.path.join(SOUND_DIR, 'bell.wav')
                        if not self.play_alarm:
                            playsound(pth)
                            self.play_alarm = True
        if self.days != 0:
            hrs = self.hours + self.days*24
        else:
            hrs = self.hours

        countdown = '{0}:{1}:{2}'.format(hrs, self.minutes, self.seconds)
        self.countdown.emit(countdown)

        self._dateline = self.endDate.toString('dd/MM/yy - hh:mm:ss')
        self._enddate = self.endDate.date().toString('dd/MM/yy')
        self._endtime = self.endDate.time().toString('hh:mm:ss')

        self.updateData()

    def updateData(self):
        self.taskData.add('name', self.taskName)
        self.taskData.add('id', self.taskID)
        self.taskData.add('mode', self.taskMode)
        self.taskData.add('type', self.taskType)
        self.taskData.add('status', self.get_status())
        self.taskData.add('project', self.project)
        self.taskData.add('organisation', self.organisation)
        self.taskData.add('dateline', self._dateline)
        self.taskData.add('enddate', self._enddate)
        self.taskData.add('endtime', self._endtime)
        self.taskData.add('details', self.details)

        with open(os.path.join(TASK_DIR, '{0}.task'.format(self.taskID)), 'w') as f:
            json.dump(self.taskData, f, indent=4)

        return self.taskData

    def get_status(self):
        if self.days < 0:
            self._status = 'Overdued'
        elif self.days == 0:
            if self.hours < 0:
                self._status = 'Overdued'
            elif self.hours == 0:
                if self.minutes <= 0:
                    self._status = 'Overdued'
                else:
                    self._status = 'Urgent'
            else:
                self._status = 'Urgent'
        elif self.days <= 2:
            self._status = 'Tomorrow'
        elif self.days > 2 and self.days < 7:
            self._status = '{0} days'.format(self.days)
        elif self.days == 7:
            self._status = '1 Week'
        else:
            self._status = '{0} days'.format(self.days)

        return self._status

    def dateline(self):
        return self._dateline

    def enddate(self):
        return self._enddate

    def endtime(self):
        return self._endtime

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 16/11/2019 - 7:00 PM
# © 2017 - 2018 DAMGteam. All rights reserved