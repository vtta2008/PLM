# -*- coding: utf-8 -*-
"""

Script Name: Worker.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys
import traceback

# PyQt5
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QRunnable

from assets.Storage import DObj

# PLM

# -------------------------------------------------------------------------------------------------------------
""" Signals """

class Signals(DObj):

    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

        - finished: No data
        - error: `tuple` (exctype, value, traceback.format_exc() )
        - result: `object` data returned from processing, anything

    '''
    key = 'custom signal'
    workerFinished = pyqtSignal(int)
    workerReady = pyqtSignal(list, dict)
    dataReady = pyqtSignal(int, int)

    started = pyqtSignal()
    finished = pyqtSignal(int)
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)

# -------------------------------------------------------------------------------------------------------------
""" Worker QRunnable """

class Worker(QRunnable):

    key = "Runable worker"
    signals = Signals()

    def __init__(self, workerID=0, fn=None, *args, **kwargs):
        super(Worker, self).__init__()


        self.workerID = workerID
        self.fn = fn                                            # Store constructor arguments (re-used for processing)
        self.args = args
        self.kwargs = kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):

        try:
            result = self.fn(status = self.signals.status, progress = self.signals.progress, *self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)                    # Return the result of the processing
        finally:
            self.signals.finished.emit(self.workerID)            # Done


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 14/06/2018 - 9:58 PM
# © 2017 - 2018 DAMGteam. All rights reserved