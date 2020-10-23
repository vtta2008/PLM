# -*- coding: utf-8 -*-
"""

Script Name: Threads.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PyQt5

from pyPLM.Core import Thread, Signal, Timer
from PLM.utils import get_ram_useage, get_cpu_useage, get_gpu_useage, get_disk_useage


# -------------------------------------------------------------------------------------------------------------
""" Threads """


class ConnectMonitor(Thread):

    key                                     = 'ConnectMonitor'
    updateServer                            = Signal(name='update server')
    updateInternet                          = Signal(name='update internet')

    def run(self):

        def update():
            self.updateServer.emit()
            self.updateInternet.emit()


        if self.running:
            timer = Timer()
            timer.timeout.connect(update)
            timer.start(1000)
            self.exec_()



class PcMonitor(Thread):

    key                                     = 'PcMonitor'

    cpu                                     = Signal(str, name='CPU')
    ram                                     = Signal(str, name='RAM')
    gpu                                     = Signal(str, name='GPU')
    disk                                    = Signal(str, name='DISK')

    def run(self):

        def update():

            cpu = str(get_cpu_useage())
            ram = str(get_ram_useage())
            gpu = str(get_gpu_useage())
            disk = str(get_disk_useage())

            self.cpu.emit(cpu)
            self.ram.emit(ram)
            self.gpu.emit(gpu)
            self.disk.emit(disk)

        if self.running:

            timer = Timer()
            timer.timeout.connect(update)
            timer.start(1000)
            self.exec_()



class SplashMonitor(Thread):

    key                                     = 'SplashMonitor'

    numOfitems                              = 15
    revolutionPerSec                        = 1.57079632679489661923

    rotate                                  = Signal(name='rotate')

    def run(self):

        def update():
            self.rotate.emit()

        if self.running:

            timer = Timer()
            timer.timeout.connect(update)
            timer.start(1000 / (self.numOfitems * self.revolutionPerSec))
            self.exec_()




# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/25/2020 - 11:32 PM
# © 2017 - 2019 DAMGteam. All rights reserved