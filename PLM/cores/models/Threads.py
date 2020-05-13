# -*- coding: utf-8 -*-
"""

Script Name: Threads.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PyQt5
from PyQt5.QtCore                           import pyqtSignal

# PLM
from PLM.commons.Core                       import Thread
from PLM.utils                              import get_ram_useage, get_cpu_useage, get_gpu_useage, get_disk_useage


# -------------------------------------------------------------------------------------------------------------
""" Threads """


class PcMonitor(Thread):

    key                                     = 'PcMonitor'

    cpu                                     = pyqtSignal(str, name='CPU')
    ram                                     = pyqtSignal(str, name='RAM')
    gpu                                     = pyqtSignal(str, name='GPU')
    disk                                    = pyqtSignal(str, name='DISK')

    def __init__(self, parent):
        super(PcMonitor, self).__init__(parent)

        self.parent                         = parent
        if self.parent:
            self.setParent(self.parent)

    def run(self):
        if self.running:

            cpu                             = str(get_cpu_useage())
            ram                             = str(get_ram_useage())
            gpu                             = str(get_gpu_useage())
            disk                            = str(get_disk_useage())

            self.cpu.emit(cpu)
            self.ram.emit(ram)
            self.gpu.emit(gpu)
            self.disk.emit(disk)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/25/2020 - 11:32 PM
# © 2017 - 2019 DAMGteam. All rights reserved