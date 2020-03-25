# -*- coding: utf-8 -*-
"""

Script Name: Threads.py
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

# PLM
from PLM.cores.base                         import WidgetThread, TaskThread
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
        self.widget.show()
        if self.running:
            self.widget.rotate()



class RealtimeUpdatingThread(WidgetThread):

    key                                             = 'RealtimeUpdatingThread'

    def __init__(self, widget, parent):
        super(RealtimeUpdatingThread, self).__init__(widget, parent)

        if self.parent:
            self.setParent(self.parent)

    def run(self):
        self.widget.show()
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
# Created by panda on 3/25/2020 - 11:32 PM
# © 2017 - 2019 DAMGteam. All rights reserved