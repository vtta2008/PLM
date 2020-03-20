# -*- coding: utf-8 -*-
"""

Script Name: Runnable.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys
import traceback

# PyQt5
from PyQt5.QtCore                           import QRunnable

# PLM
from PLM                                    import __copyright__

class Runnable(QRunnable):

    Type                                    = 'DAMGWORKER'
    key                                     = 'BaseWorker'
    _name                                   = 'DAMG Worker'
    _copyright                              = __copyright__()

    def __init__(self, task, *args, **kwargs):
        QRunnable.__init__(self)

        self.task                           = task              # Store constructor arguments (re-used for processing)
        self.args                           = args
        self.kwargs                         = kwargs

    def run(self):

        try:
            result = self.task(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            print(exctype, value, traceback.format_exc())
        else:
            print(result)                                       # Return the result of the processing
        finally:
            print(self)                                         # Done

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name                          = val


class Worker(Runnable):

    Type                                    = 'DAMGWORKER'
    key                                     = 'Worker'
    _name                                   = 'DAMG Worker'
    _copyright                              = __copyright__()

    def __init__(self, task, *args, **kwargs):
        Runnable.__init__(self)

        self.task                           = task
        self.args                           = args
        self.kwargs                         = kwargs




class RequestWorker(QRunnable):

    Type                                    = 'DAMGWORKER'
    key                                     = 'RequestWorker'
    _name                                   = 'DAMG Request Worker'
    _copyright                              = __copyright__()

    def __init__(self, widget):
        QRunnable.__init__(self)
        self.widget             = widget

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name                          = val


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/20/2020 - 6:17 AM
# © 2017 - 2019 DAMGteam. All rights reserved