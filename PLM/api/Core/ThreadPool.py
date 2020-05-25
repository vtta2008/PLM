# -*- coding: utf-8 -*-
"""

Script Name: ThreadPool.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------

from .io_core import QThreadPool


class ThreadPool(QThreadPool):

    Type                                    = 'DAMGTHREADPOOL'
    key                                     = 'BaseThreadPool'
    _name                                   = 'DAMG Thread Pool'



    def __init__(self, parent=None):
        super(ThreadPool, self).__init__(parent)

        self.parent                         = parent


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name                          = val

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/20/2020 - 8:06 AM
# © 2017 - 2019 DAMGteam. All rights reserved