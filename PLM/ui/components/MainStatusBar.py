# -*- coding: utf-8 -*-
"""

Script Name: StatusBar.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
import datetime
from PLM.ui.base import DigitalClock, DigitalDate
from pyPLM.Widgets                  import StatusBar, Label, ProgressBar, Widget, GridLayout
from PLM.cores.models               import PcMonitor



class TaskTracker(Widget):

    key = 'TaskTracker'

    _currentTask                    = None
    _duedate                        = 'dd:MM:yy'
    _duetime                        = 'hh:mm:ss'
    _countdown                      = 'hh:mm:ss'

    def __iter__(self, parent=None):
        super(TaskTracker, self).__iter__(parent)

        self.parent                    = parent

        self.layout = GridLayout(self)

        self.timeClock = DigitalClock(self)
        self.dateClock = DigitalDate(self)

        d = self.dateClock.currentDate().day()
        m = self.dateClock.currentDate().month()
        y = self.dateClock.currentDate().year()
        dt = datetime.date(y, m, d)
        wk = dt.isocalendar()[1]

        self.weekNumber = Label({'txt': 'Weeknumber: {0}'.format(wk)})

        self.setLayout(self.layout)

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



class MainStatusBar(StatusBar):

    key                             = 'MainStatusBar'

    labels                          = []


    def __init__(self, parent=None):
        super(MainStatusBar, self).__init__(parent)

        self.parent                 = parent

        self.usage_cpu = Label({'txt': 'cpu: 0%'})
        self.usage_ram = Label({'txt': 'ram: 0%'})
        self.usage_gpu = Label({'txt': 'gpu: 0%'})
        self.usage_disk = Label({'txt': 'dsk: 0%'})

        worker = PcMonitor(self)
        worker.cpu.connect(self.update_cpu_useage)
        worker.ram.connect(self.update_ram_useage)
        worker.gpu.connect(self.update_gpu_useage)
        worker.disk.connect(self.update_disk_useage)
        worker.start()

        self.labels = [self.usage_cpu, self.usage_ram, self.usage_gpu, self.usage_disk]

        for widget in self.labels:
            self.addPermanentWidget(widget)


    def update_cpu_useage(self, val):
        return self.usage_cpu.setText('cpu: {0}%'.format(val))

    def update_ram_useage(self, val):
        return self.usage_ram.setText('ram: {0}%'.format(val))

    def update_gpu_useage(self, val):
        return self.usage_gpu.setText('gpu: {0}%'.format(val))

    def update_disk_useage(self, val):
        return self.usage_disk.setText('dsk: {0}%'.format(val))


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 10:39 PM
# © 2017 - 2018 DAMGteam. All rights reserved
