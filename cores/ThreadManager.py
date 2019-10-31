# -*- coding: utf-8 -*-
"""

Script Name: Task.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtCore               import QTimer

from damg                       import DAMGLIST, DAMGTHREADPOOL, DAMGTHREAD, DAMGWORKER

class ThreadManager(DAMGTHREADPOOL):

    def __init__(self):
        super(ThreadManager, self).__init__()

        self.counter = 0
        self.tasks = self.get_tasks()
        self.timer = QTimer()

        self.threads = DAMGLIST()
        self.workers = DAMGLIST()

    def startWorker(self, task):
        worker = DAMGWORKER(task)

        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        self.workers.append(worker)

        self.start(worker)

    def startThread(self):
        """ Create task to run """
        for cur_task in self.tasks:
            worker = DAMGTHREAD(cur_task)
            worker.start()
            self.threads.append(worker)

    def progress_fn(self, n):
        print("%d%% done" % n)

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE")

    def begin(self):
        """ For thread use only """

        self.startThread()

        self.timer.setInterval(10000)
        self.timer.start()
        self.timer.timeout.connect(self.startThread)

    def stop(self):

        print('Stop tasks!')

        self.timer.stop()
        for task in self.threads:
            task.quit_thread.emit()

        print('Tasks finished')

    def recurring_timmer(self):
        self.counter += 1
        print(self.counter)

    @staticmethod
    def get_tasks():
        """ Return the available tasks to run """
        return ['notifications', 'livesynthesis', 'alignakdaemon', 'history', 'service', 'host', 'user']

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 20/10/2019 - 6:23 PM
# © 2017 - 2018 DAMGteam. All rights reserved