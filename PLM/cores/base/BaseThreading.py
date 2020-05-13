# -*- coding: utf-8 -*-
"""

Script Name: BaseThreading.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PyQt5
from PyQt5.QtCore                           import pyqtSignal

from PLM.commons                            import DAMG
from PLM.commons.Core                       import Thread, Worker, Timer

# -------------------------------------------------------------------------------------------------------------
""" Base """


class Signals(DAMG):

    key                                             = 'Signals'

    finished                                        = pyqtSignal(str)
    error                                           = pyqtSignal(tuple)
    result                                          = pyqtSignal(object)
    progress                                        = pyqtSignal(int)



# -------------------------------------------------------------------------------------------------------------
""" Base Worker """


class WidgetWorker(Worker):

    key                                             = 'WidgetWorker'
    signal                                          = Signals()

    def __init__(self, widget, parent):
        Worker.__init__(self)

        self.parent                                 = parent
        self.task                                   = widget
        self.timer                                  = Timer(self)

    def stop(self):
        self._running                               = False
        self.timer.stop()


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
        self.widget.show()
        self.parent                                 = parent

    def stop(self):
        self._running                               = False



class TaskThread(Thread):

    key                                             = 'TaskThread'
    signal                                          = Signals()

    def __init__(self, task, parent):
        Thread.__init__(self)

        self.task                                   = task
        self.parent                                 = parent

    def stop(self):
        self._running                               = False




# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/25/2020 - 11:28 PM
# © 2017 - 2019 DAMGteam. All rights reserved