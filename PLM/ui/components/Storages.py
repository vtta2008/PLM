# -*- coding: utf-8 -*-
"""

Script Name: Storages.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys
import traceback

# PyQt5
from PyQt5.QtCore                           import pyqtSignal

from PLM.ui.base                            import BaseStorage
from PLM.commons                            import DAMGLIST, DAMG
from PLM.commons.Core                       import Thread, Worker, Timer
from PLM.cores.Errors                       import (ThreadNotFoundError, WorkerNotFoundError, CreateThreadError,
                                                    CreateWorkerError)
from PLM.utils                              import get_ram_useage, get_cpu_useage, get_gpu_useage, get_disk_useage


# -------------------------------------------------------------------------------------------------------------
""" Base """


class Signals(DAMG):

    key                                             = 'Signals'

    finished                                        = pyqtSignal()
    error                                           = pyqtSignal(tuple)
    result                                          = pyqtSignal(object)
    progress                                        = pyqtSignal(int)



# -------------------------------------------------------------------------------------------------------------
""" Base Worker """



class TaskWorker(Worker):

    key                                             = 'TaskWorker'
    signal                                          = Signals()

    def __init__(self, task, parent):
        Worker.__init__(self)

        self.parent                                 = parent
        self.task                                   = task
        self.timer                                  = Timer(self)

    def stop(self):
        self._running                               = False
        self.timer.stop()



# -------------------------------------------------------------------------------------------------------------
""" Base Thread """



class WidgetThread(Thread):

    key                                             = 'WidgetThread'
    signal                                          = Signals()

    def __init__(self, widget, parent):
        Thread.__init__(self)

        self.widget                                 = widget
        self.parent                                 = parent
        self.timer                                  = Timer(self)

    def stop(self):
        self.timer.stop()
        self._running                               = False



class TaskThread(Thread):

    key                                             = 'TaskThread'
    signal                                          = Signals()

    def __init__(self, task, parent):
        Thread.__init__(self)

        self.task                                   = task
        self.parent                                 = parent
        self.timer                                  = Timer(self)

    def stop(self):
        self.timer.stop()
        self._running                               = False



# -------------------------------------------------------------------------------------------------------------
""" Threads """


class PcMonitor(Thread):

    key                                     = 'PcMonitor'

    cpu                                     = pyqtSignal(str, name='CPU')
    ram                                     = pyqtSignal(str, name='RAM')
    gpu                                     = pyqtSignal(str, name='GPU')
    disk                                    = pyqtSignal(str, name='DISK')

    _monitoring                             = True

    def __init__(self, name='PC Monitor', *args, **kwargs):
        super(PcMonitor, self).__init__(self)

        self.args                           = args
        self.kwargs                         = kwargs
        self._name                          = name

    def run(self):
        if self._monitoring:

            cpu                             = str(get_cpu_useage())
            ram                             = str(get_ram_useage())
            gpu                             = str(get_gpu_useage())
            disk                            = str(get_disk_useage())

            self.cpu.emit(cpu)
            self.ram.emit(ram)
            self.gpu.emit(gpu)
            self.disk.emit(disk)

    def stop_monitoring(self):
        self._monitoring                    = False

    def start_monitoring(self):
        self._monitoring                    = True

    @property
    def monitor(self):
        return self._monitoring

    @monitor.setter
    def monitor(self, val):
        self._monitoring                    = val



class AutoLoadingThread(WidgetThread):

    key                                             = 'AutoLoadingThread'

    def __init__(self, widget, parent):
        super(AutoLoadingThread, self).__init__(widget, parent)

        if self.parent:
            self.setParent(self.parent)

    def run(self):
        if self.running:
            self.widget.rotate()


class RealtimeUpdatingThread(WidgetThread):

    key                                             = 'RealtimeUpdatingThread'

    def __init__(self, widget, parent):
        super(RealtimeUpdatingThread, self).__init__(widget, parent)

        if self.parent:
            self.setParent(self.parent)

    def run(self):
        if self.running:
            self.widget.update()

    def setText(self, v):
        return self.widget.setText(v)

    def setProgress(self, v):
        return self.widget.setProgress(v)



class ConfigTaskThread(TaskThread):

    key                                             = 'ConfigTaskThread'

    def __init__(self, task, parent):
        super(ConfigTaskThread, self).__init__(task, parent)

        if self.parent:
            self.setParent(self.parent)

    def run(self):
        if self.running:
            try:
                result = self.task()
            except:
                traceback.print_exc()
                exctype, value = sys.exc_info()[:2]
                self.signal.error.emit((exctype, value, traceback.format_exc()))
            else:
                self.signal.result.emit(result)
            finally:
                self.signal.finished.emit()


# -------------------------------------------------------------------------------------------------------------
""" Workers """



class ConfigTaskWorker(TaskWorker):

    key                                             = 'ConfigTaskWorker'

    def __init__(self, task, parent):
        super(ConfigTaskWorker, self).__init__(task, parent)


    def run(self):
        if self.running:
            try:
                result = self.task()
            except:
                traceback.print_exc()
                exctype, value = sys.exc_info()[:2]
                self.signal.error.emit((exctype, value, traceback.format_exc()))
            else:
                self.signal.result.emit(result)
            finally:
                self.signal.finished.emit()

# -------------------------------------------------------------------------------------------------------------
""" Storages """



class ThreadStorage(BaseStorage):

    key                                     = 'ThreadStorage'
    threads                                 = DAMGLIST()

    def __init__(self):
        super(ThreadStorage, self).__init__()

        for thread in [PcMonitor, AutoLoadingThread, RealtimeUpdatingThread, ConfigTaskThread, ]:
            self.threads.append(thread)
            self.register(thread)


    def getThread(self, key):
        if key in self.keys():
            return self[key]
        else:
            return ThreadNotFoundError('Could not find thread: {0}'.format(key))

    def createThread(self, key):
        if key not in self.keys():
            thread                              = Thread
            thread.key                          = key
            self.threads.append(thread)
            self.register(thread)
            return thread
        else:
            CreateThreadError('Could not create thread: {0}, key already existed'.format(key))



class WorkerStorage(BaseStorage):

    key                                     = 'WorkerStorage'
    workers                                 = DAMGLIST()

    def __init__(self):
        super(WorkerStorage, self).__init__()

        for worker in [ConfigTaskWorker, ]:
            self.workers.append(ConfigTaskWorker)
            self.register(worker)

    def getWorker(self, key):
        if key in self.keys():
            return self[key]
        else:
            return WorkerNotFoundError('Could not find worker: {0}'.format(key))

    def createWorker(self, key):
        if key not in self.keys():
            worker                              = Worker
            worker.key                          = key
            self.workers.append(worker)
            self.register(worker)
            return worker
        else:
            CreateWorkerError('Could not create worker: {0}, key already existed'.format(key))



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/21/2020 - 3:08 AM
# © 2017 - 2019 DAMGteam. All rights reserved