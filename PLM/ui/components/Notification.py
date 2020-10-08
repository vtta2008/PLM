# -*- coding: utf-8 -*-
"""

Script Name: Notification.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

import datetime

from PLM.cores.models import PcMonitor
from bin.Widgets import LCDNumber, GroupGrid, Label
from bin.Core import Timer


class DigitalClock(LCDNumber):

    key = 'DigitalClock'

    def __init__(self, parent=None):
        super(DigitalClock, self).__init__(parent)

        self.parent = parent
        self.setSegmentStyle(LCDNumber.Flat)
        self.setDigitCount(8)
        timer = Timer()
        timer.setParent(self.parent)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        self.showTime()
        self.resize(70, 20)

    def showTime(self):
        time = self.currentTime()
        text = time.toString('hh:mm:ss')
        if (time.second() % 2) == 0:
            text = text[:2] + ' ' + text[3:5] + ' ' + text[6:]
        self.display(text)


class DigitalDate(LCDNumber):

    key = 'DigitalDate'

    def __init__(self, parent=None):
        super(DigitalDate, self).__init__(parent)

        self.parent = parent
        self.setSegmentStyle(LCDNumber.Flat)
        self.setDigitCount(8)
        timer = Timer()
        timer.setParent(self.parent)
        timer.timeout.connect(self.showdate)
        timer.start(1000)
        self.showdate()
        self.resize(70, 20)

    def showdate(self):
        date = self.currentDate()
        text = date.toString('dd/MM/yy')
        self.display(text)


class Notification(GroupGrid):

    _currentTask            = None
    _duedate                = 'dd:MM:yy'
    _duetime                = 'hh:mm:ss'
    _countdown              = 'hh:mm:ss'
    labels = []

    def __init__(self, threadManager, parent=None):
        super(Notification, self).__init__(parent=parent)

        self.parent         = parent
        self.threadManager  = threadManager

        self.usage_cpu      = Label({'txt': 'cpu: 0%'})
        self.usage_ram      = Label({'txt': 'ram: 0%'})
        self.usage_gpu      = Label({'txt': 'gpu: 0%'})
        self.usage_disk     = Label({'txt': 'dsk: 0%'})


        self.timeClock      = DigitalClock(self)
        self.dateClock      = DigitalDate(self)

        d                   = self.dateClock.currentDate().day()
        m                   = self.dateClock.currentDate().month()
        y                   = self.dateClock.currentDate().year()
        dt                  = datetime.date(y, m, d)
        wk                  = dt.isocalendar()[1]

        self.weekNumber     = Label({'txt': 'Weeknumber: {0}'.format(wk)})

        worker              = PcMonitor(self)
        worker.cpu.connect(self.update_cpu_useage)
        worker.ram.connect(self.update_ram_useage)
        worker.gpu.connect(self.update_gpu_useage)
        worker.disk.connect(self.update_disk_useage)
        worker.start()

        self.labels         = [self.usage_cpu, self.usage_ram, self.usage_gpu, self.usage_disk, self.weekNumber,
                               self.timeClock, self.dateClock]

        self.layout.addWidget(self.usage_cpu, 0, 0, 1, 1)
        self.layout.addWidget(self.usage_ram, 0, 1, 1, 1)
        self.layout.addWidget(self.usage_gpu, 1, 0, 1, 1)
        self.layout.addWidget(self.usage_disk, 1, 1, 1, 1)
        self.layout.addWidget(self.weekNumber, 2, 0, 1, 2)
        self.layout.addWidget(self.timeClock, 3, 0, 1, 1)
        self.layout.addWidget(self.dateClock, 3, 1, 1, 1)

    def setcurrentTask(self, task):
        self._currentTask = task

    def update_cpu_useage(self, val):
        return self.usage_cpu.setText('cpu: {0}%'.format(val))

    def update_ram_useage(self, val):
        return self.usage_ram.setText('ram: {0}%'.format(val))

    def update_gpu_useage(self, val):
        return self.usage_gpu.setText('gpu: {0}%'.format(val))

    def update_disk_useage(self, val):
        return self.usage_disk.setText('dsk: {0}%'.format(val))

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
# Created by panda on 16/11/2019 - 5:57 PM
# © 2017 - 2018 DAMGteam. All rights reserved