# -*- coding: utf-8 -*-
"""

Script Name: Thread.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from PySide2.QtCore                 import QThread


class Thread(QThread):

    Type                                = 'DAMGTHREAD'
    key                                 = 'BaseThread'
    _name                               = 'DAMG Thread'

    _running                            = True

    def __init__(self, *args, **kwargs):
        QThread.__init__(self)

        self.args = args
        self.kwargs = kwargs

    def __del__(self):
        self.wait()

    def start_running(self):
        self._running                       = True

    def stop_running(self):
        self._running                       = False

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


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/20/2020 - 6:23 AM
# © 2017 - 2019 DAMGteam. All rights reserved