# -*- coding: utf-8 -*-
"""

Script Name: Task.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import time

# PLM
from PLM.commons                            import DAMGLIST
from PLM.commons.Core                       import ThreadPool
from PLM.cores                              import SignalManager, SettingManager
from PLM.ui.components.Counting             import Counting
from PLM.ui.components.Storages             import ThreadStorage, WorkerStorage


class ThreadManager(ThreadPool):

    key                                     = 'ThreadManager'
    tasks                                   = DAMGLIST()
    threads                                 = ThreadStorage()
    workers                                 = WorkerStorage()

    def __init__(self, parent=None):
        super(ThreadManager, self).__init__(parent)

        self.parent                         = parent
        self.counter                        = Counting()
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

    def process_output(self, val):
        return print(val)

    def progress_task(self, val):
        return print('{0}% done'.format(val))

    def task_completed(self):
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