# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from PySide2.QtCore                 import QEventLoop


class EventLoop(QEventLoop):

    Type                            = 'DAMGEVENTLOOP'
    key                             = 'EventLoop'
    _name                           = 'DAMG Event Loop'

    def __init__(self, parent=None):
        super(EventLoop, self).__init__(parent)


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name                  = val

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved