# -*- coding: utf-8 -*-
"""

Script Name: Notification.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from ui.uikits.GridLayout import GridLayout
from ui.uikits.Label import LCDNumber, Label

class DigitalClock(LCDNumber):

    key = 'DigitalClock'

    def __init__(self, parent=None):
        super(DigitalClock, self).__init__(parent)

        self.parent = parent
        self.setSegmentStyle(LCDNumber.Flat)
        self.setDigitCount(8)
        # timer = DAMGTIMER()
        # timer.setParent(self.parent)
        # timer.timeout.connect(self.showTime)
        # timer.start(1000)
        self.showTime(True)
        self.resize(70, 20)

    def showTime(self, val):
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
        self.showdate(True)
        self.resize(70, 20)

    def showdate(self, val):
        date = self.currentDate()
        text = date.toString('dd:MM:yy')
        self.display(text)

class Notification(GridLayout):

    _currentTask = 'No Task'
    _duedate = 'dd:MM:yy'
    _duetime = 'hh:mm:ss'
    _countdown = 'hh:mm:ss'

    def __init__(self, threadManager, parent=None):
        super(Notification, self).__init__(parent)

        self.parent         = parent
        self.threadManager  = threadManager

        self.usage_cpu      = Label({'txt': 'cpu: 0%'})
        self.usage_ram      = Label({'txt': 'ram: 0%'})
        self.usage_gpu      = Label({'txt': 'gpu: 0%'})
        self.usage_disk     = Label({'txt': 'dsk: 0%'})

        self.task_name      = Label({'txt': '{0}'.format(self._currentTask)})
        self.task_duedate   = Label({'txt': '{0}'.format(self._duedate)})
        self.task_duetime   = Label({'txt': '{0}'.format(self._duetime)})
        self.task_countdown = Label({'txt': '{0}'.format(self._countdown)})

        self.timeClock      = DigitalClock(self)
        self.dateClock      = DigitalDate(self)

        worker = self.threadManager.serviceThread()
        worker.cpu.connect(self.update_cpu_useage)
        worker.ram.connect(self.update_ram_useage)
        worker.gpu.connect(self.update_gpu_useage)
        worker.disk.connect(self.update_disk_useage)
        worker.time.connect(self.timeClock.showTime)
        worker.date.connect(self.dateClock.showdate)
        worker.start()

        self.addWidget(self.usage_cpu, 0, 0, 1, 1)
        self.addWidget(self.usage_ram, 1, 0, 1, 1)
        self.addWidget(self.usage_gpu, 2, 0, 1, 1)
        self.addWidget(self.usage_disk, 3, 0, 1, 1)
        self.addWidget(self.timeClock, 4, 0, 1, 1)

        self.addWidget(self.task_name, 0, 1, 1, 1)
        self.addWidget(self.task_duedate, 1, 1, 1, 1)
        self.addWidget(self.task_duetime, 2, 1, 1, 1)
        self.addWidget(self.task_countdown, 3, 1, 1, 1)
        self.addWidget(self.dateClock, 4, 1, 1, 1)

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