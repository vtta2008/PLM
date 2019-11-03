# -*- coding: utf-8 -*-
"""

Script Name: Task.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

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

    def assign_worker(self, task):
        worker = DAMGWORKER(task)
        worker.signals.result.connect(self.process_output)
        worker.signals.progress.connect(self.process_task)
        worker.signals.finished.connect(self.task_completed)
        self.workers.append(worker)

        return self.start(worker)

    def process_output(self, val):
        print(val)

    def process_task(self, val):
        print('{0}% done'.format(val))

    def task_completed(self, worker):
        self.workers.remove(worker)
        print('worker commpleted')


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 20/10/2019 - 6:23 PM
# © 2017 - 2018 DAMGteam. All rights reserved