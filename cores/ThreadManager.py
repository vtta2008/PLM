# -*- coding: utf-8 -*-
"""

Script Name: Task.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtCore               import pyqtSlot

from damg                       import DAMGLIST, DAMGTHREADPOOL, DAMGTIMER, DAMGWORKER, DAMGTHREAD

class Counting(DAMGTIMER):

    key = 'Counting'

    def __init__(self, interval=10000):
        super(Counting, self).__init__()

        self._interval = interval
        self.counter = 0
        self.setInterval(self._interval)

    def begin(self):
        print("Start counting")
        # self.timeout.connect(self.start_thread)
        self.start()

    def counting(self):
        self.counter += 1
        print(self.counter)

    def finish(self):
        print("Stop counting")
        return self.stop()

class ThreadManager(DAMGTHREADPOOL):

    tasks = DAMGLIST()

    def __init__(self):
        super(ThreadManager, self).__init__()

        self.counter                = Counting()

    def startCounting(self):
        self.counter.begin()

    def stopCounting(self):
        self.counter.finish()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 20/10/2019 - 6:23 PM
# © 2017 - 2018 DAMGteam. All rights reserved