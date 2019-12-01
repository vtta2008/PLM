# -*- coding: utf-8 -*-
"""

Script Name: TaskBase.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtCore import pyqtSignal, QDate, QTime
from bin import DAMG, DAMGTIMER

class TaskBase(DAMG):

    key                         = 'Task'
    Type                        = 'DAMGTASK'
    _name                       = 'Task Name'
    _status                     = 'status'
    days                        = 0
    hours                       = 0
    minutes                     = 0
    seconds                     = 0
    countdown                   = pyqtSignal(str, name='CountDown')
    play_alarm                  = False

    def __init__(self):
        super(TaskBase, self).__init__(self)

        self.date = QDate()
        self.time = QTime()

        self.timer = DAMGTIMER()
        self.timer.setParent(self)

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

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, val):
        self._status = val

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 2/12/2019 - 10:40 AM
# © 2017 - 2018 DAMGteam. All rights reserved