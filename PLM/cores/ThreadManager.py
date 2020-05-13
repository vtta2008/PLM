# -*- coding: utf-8 -*-
"""

Script Name: Task.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python

# PLM
from PLM.commons.Core                       import ThreadPool
from PLM.plugins.SignalManager              import SignalManager
from PLM.commons.SettingManager             import SettingManager
from PLM.cores.Storages                     import ThreadStorage, WorkerStorage, TaskStorage


class ThreadManager(ThreadPool):

    key                                     = 'ThreadManager'
    tasks                                   = TaskStorage()
    threads                                 = ThreadStorage()
    workers                                 = WorkerStorage()

    def __init__(self, parent=None):
        super(ThreadManager, self).__init__(parent)

        self.parent                         = parent
        self.settings                       = SettingManager(self)
        self.signals                        = SignalManager(self)

    def getThread(self, key):
        return self.threads.getThread(key)

    def getWorker(self, key):
        return self.workers.getWorker(key)

    def startCounting(self):
        self.counter.begin()

    def stopCounting(self):
        self.counter.finish()

    def setCountLimited(self, val):
        return self.counter.setCountLimited(val)

    def setPrintCounter(self, bool):
        return self.counter.setPrintCounter(bool)

    def isCounting(self):
        return self.counter.isCounting

    def print_output(self, val):
        return print(val)

    def progress_fn(self, val):
        return print('{0}% done'.format(val))

    def worker_completed(self, worker):
        return print('worker commpleted')

    def stop_thread(self, thread):
        thread.quit_thread.emit()
        return print('thread stopes')

    def error_output(self, errorTuple):
        return print(errorTuple)

    def execute_multi_tasks(self, tasks):
        for task in tasks:
            self.tasks.append(task)
            self.execute_task(task)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 20/10/2019 - 6:23 PM
# © 2017 - 2018 DAMGteam. All rights reserved