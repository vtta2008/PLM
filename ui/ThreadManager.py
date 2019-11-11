# -*- coding: utf-8 -*-
"""

Script Name: Task.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from bin.data.damg                       import DAMGLIST, DAMGTHREADPOOL, DAMGTIMER, DAMGTHREAD
from utils                               import get_ram_useage, get_cpu_useage, create_signal_slot

signal_cpu, slot_cpu = create_signal_slot(argType=str, name='CPU')
signal_ram, slot_ram = create_signal_slot(argType=str, name='RAM')

class BackgroundService(DAMGTHREAD):

    key = 'FooterWorker'
    cpu = signal_cpu
    ram = signal_ram

    slotCpu = slot_cpu
    slotRam = slot_ram

    def __init__(self, name='CPU useage', *args, **kwargs):
        super(BackgroundService, self).__init__(self)

        self.args = args
        self.kwargs = kwargs
        self._name = name

    def run(self):
        while True:
            cpu = str(get_cpu_useage())
            ram = str(get_ram_useage())
            self.cpu.emit(cpu)
            self.ram.emit(ram)

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

    def serviceThread(self):
        thread = BackgroundService()
        self.threads.append(thread)
        return thread

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 20/10/2019 - 6:23 PM
# © 2017 - 2018 DAMGteam. All rights reserved