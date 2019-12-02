# -*- coding: utf-8 -*-
"""

Script Name: TaskBase.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
""" Import """
# Python
import os, json
from playsound import playsound


from PyQt5.QtCore               import pyqtSignal, QDate, QTime


from bin                        import DAMG, DAMGTIMER, DAMGDICT
from appData                    import SOUND_DIR, TASK_DIR, PRJ_DIR, ORG_DIR, TEAM_DIR, TMP_DIR

class BaseType(DAMG):

    key                         = 'BaseType'
    Type                        = 'DAMGBASETYPE'
    _name                       = 'DAMG Base Type'
    _status                     = 'status'

    days                        = 0
    hours                       = 0
    minutes                     = 0
    seconds                     = 0

    countdown                   = pyqtSignal(str, name='CountDown')
    play_alarm                  = True

    dataForm                    = DAMGDICT()

    _id                         = None
    _mode                       = None
    _type                       = None

    def __init__(self, id=None, name=None, mode=None, type=None,
                       teamID=None, projectID=None, organisationID=None,
                       startdate=None, enddate=None, details={}):
        DAMG.__init__(self)

        self.date               = QDate()
        self.time               = QTime()

        self.timer              = DAMGTIMER()
        self.timer.setParent(self)

        self._id                = id
        self._name              = name
        self._mode              = mode
        self._type              = type

        self.teamID             = teamID
        self.projectID          = projectID
        self.organisationID     = organisationID

        self.startdate          = startdate
        self.enddate            = enddate
        self.details            = details

    def countter_format(self, format='sec'):
        if format in ['sec', 'second']:
            return 1000
        elif format in ['min', 'minute']:
            return 1000*60
        elif format in ['hr', 'hour']:
            return 1000*60*60
        else:
            return 1000

    def confirm_task_complete(self):
        self._status                = 'Completed'


    def update(self):
        self.days = self.start.daysTo(self.end)

        self.hours = self.end.time().hour() - self.start.time().hour()
        if self.hours <= 0:
            if self.days > 0:
                self.days = self.days - 1
                self.hours = self.hours + 24

        self.minutes = self.end.time().minute() - self.start.time().minute()
        if self.minutes <= 0:
            if self.hours > 0:
                self.hours = self.hours - 1
                self.minutes = self.minutes + 60

        self.seconds = self.end.time().second() - self.start.time().second()
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

        self._start = self.start.toString('dd/MM/yy - hh:mm:ss')
        self._startdate = self.start.date().toString('dd/MM/yy')
        self._starttime = self.start.time().toString('hh:mm:ss')

        self._end = self.end.toString('dd/MM/yy - hh:mm:ss')
        self._enddate = self.end.date().toString('dd/MM/yy')
        self._endtime = self.end.time().toString('hh:mm:ss')

        self.updateData()

    def updateData(self):

        self.dataForm.add('name', self._name)
        self.dataForm.add('id', self._id)
        self.dataForm.add('mode', self._mode)
        self.dataForm.add('type', self._type)
        self.dataForm.add('status', self.get_status())

        self.dataForm.add('teamID', self.teamID)
        self.dataForm.add('projectID', self.projectID)
        self.dataForm.add('organisationID', self.organisationID)

        self.dataForm.add('start', self._start)
        self.dataForm.add('startDate', self._startdate)
        self.dataForm.add('startTime', self._starttime)

        self.dataForm.add('end', self._end)
        self.dataForm.add('enddate', self._enddate)
        self.dataForm.add('endtime', self._endtime)

        self.dataForm.add('details', self.details)

        if self.key == 'Task':
            filePth = os.path.join(TASK_DIR, '{0}.task'.format(self._id))
        elif self.key == 'Project':
            filePth = os.path.join(PRJ_DIR, '{0}.prj'.format(self._id))
        elif self.key == 'Organisation':
            filePth = os.path.join(ORG_DIR, '{0}.org'.format(self._id))
        elif self.key == 'Team':
            filePth = os.path.join(TEAM_DIR, '{0}.team'.format(self._id))
        else:
            filePth = os.path.join(TMP_DIR, '{0}.tmp'.format(self._id))

        with open(filePth, 'w') as f:
            json.dump(self.dataForm, f, indent=4)

        return self.dataForm

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

    def change_name(self, name):
        self._name = name

    def change_id(self, id):
        self._id = id

    def change_details(self, details):
        self._details = details

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, val):
        self._status = val

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 2/12/2019 - 10:40 AM
# © 2017 - 2018 DAMGteam. All rights reserved