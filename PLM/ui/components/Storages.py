# -*- coding: utf-8 -*-
"""

Script Name: Storages.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PyQt5
from PyQt5.QtCore                           import pyqtSignal

from PLM.ui.base                            import BaseStorage
from PLM.commons                            import DAMGLIST
from PLM.commons.Core                       import Thread, Worker, RequestWorker, Timer
from PLM.cores.Errors                       import (ThreadNotFoundError, WorkerNotFoundError, CreateThreadError,
                                                    CreateWorkerError)
from PLM.utils                              import get_ram_useage, get_cpu_useage, get_gpu_useage, get_disk_useage



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
        while self._monitoring:

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



class AutoRunLoading(Thread):

    key                                             = 'AutoRunLoading'
    _spinning                                       = True

    def __init__(self, widget):
        super(AutoRunLoading, self).__init__(self)

        self.widget                                 = widget
        self.timer                                  = Timer(self)
        self.timer.timeout.connect(self.widget.rotate)

    def run(self):

        while self._spinning:

            if not self.timer.isActive():
                self.timer.start(50)
                self.widget._count                  = 0

    def setWidget(self, widget):
        self.widget                                 = widget

    @property
    def spinning(self):
        return self._spinning

    @spinning.setter
    def spinning(self, val):
        self._spinning                              = val



class ThreadStorage(BaseStorage):

    key                                     = 'ThreadStorage'
    threads                                 = DAMGLIST()

    def __init__(self):
        super(ThreadStorage, self).__init__()

        for thread in [PcMonitor, AutoRunLoading, ]:
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

        for worker in [RequestWorker, ]:
            self.workers.append(RequestWorker)
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