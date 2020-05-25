# -*- coding: utf-8 -*-
"""

Script Name: Time.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------

from .io_core import QTime


class Time(QTime):

    Type                                    = 'DAMGTIME'
    key                                     = 'Time'
    _name                                   = 'DAMG Time'



    def __init__(self, *__args):
        super(Time, self).__init__(*__args)


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name              = val



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/17/2020 - 1:47 AM
# © 2017 - 2019 DAMGteam. All rights reserved