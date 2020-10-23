# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
import datetime
from .BaseLCD                       import DigitalClock, DigitalDate
from pyPLM.Widgets                  import Label, GroupHBox



class DateTimeLayout(GroupHBox):

    key = 'TaskTracker'

    _currentTask = None
    _duedate = 'dd:MM:yy'
    _duetime = 'hh:mm:ss'
    _countdown = 'hh:mm:ss'

    def __iter__(self, parent=None):
        super(DateTimeLayout, self).__iter__(parent)

        self.parent = parent

        self.timeClock = DigitalClock(self)
        self.dateClock = DigitalDate(self)

        d = self.dateClock.currentDate().day()
        m = self.dateClock.currentDate().month()
        y = self.dateClock.currentDate().year()
        dt = datetime.date(y, m, d)
        wk = dt.isocalendar()[1]

        self.weekNumber = Label({'txt': 'Weeknumber: {0}'.format(wk)})

        self.layout.addWidget(self.weekNumber)
        self.layout.addWidget(self.timeClock)
        self.layout.addWidget(self.dateClock)

    def setcurrentTask(self, task):
        self._currentTask = task

    def update_current_task(self, taskName):
        return self.task_name.setText(taskName)

    def update_task_duedate(self, date):
        return self.task_duedate.setText(date)

    def update_task_duetime(self, time):
        return self.task_duetime.setText(time)

    def update_countdown(self, val):
        return self.task_countdown.setText(val)

    @property
    def currentTask(self):
        return self._currentTask

    @property
    def duedate(self):
        return self._duedate

    @property
    def duetime(self):
        return self._duetime

    @duetime.setter
    def duetime(self, time):
        self._duetime = time

    @duedate.setter
    def duedate(self, date):
        self._duedate = date

    @currentTask.setter
    def currentTask(self, task):
        self._currentTask = task

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
