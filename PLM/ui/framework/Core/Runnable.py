# -*- coding: utf-8 -*-
"""

Script Name: Runnable.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PLM
from PLM                                    import __copyright__, QRunnable



class Runnable(QRunnable):

    Type                                    = 'DAMGRUNABLE'
    key                                     = 'Runnable'
    _name                                   = 'DAMG Runnable'
    _copyright                              = __copyright__()

    def __init__(self, task, *args, **kwargs):
        super(Runnable, self).__init__()

        self.task                           = task
        self.args                           = args
        self.kwargs                         = kwargs

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