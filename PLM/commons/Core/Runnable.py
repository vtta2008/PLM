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

    Type                                    = 'DAMGRUNABLE'
    key                                     = 'Runnable'
    _name                                   = 'DAMG Runnable'
    _copyright                              = __copyright__()
    _running                                = True

    def __init__(self, *args, **kwargs):
        QRunnable.__init__(self)

        self.args                           = args
        self.kwargs                         = kwargs

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, val):
        self._running                       = val

    @name.setter
    def name(self, val):
        self._name                          = val


class Worker(Runnable):

    Type                                    = 'DAMGWORKER'
    key                                     = 'Worker'
    _name                                   = 'DAMG Worker'

    def __init__(self, *args, **kwargs):
        Runnable.__init__(self, *args, **kwargs)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/20/2020 - 6:17 AM
# © 2017 - 2019 DAMGteam. All rights reserved