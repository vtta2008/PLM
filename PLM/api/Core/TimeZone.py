# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """


from .io_core import QTimeZone

class TimeZone(QTimeZone):

    Type                                    = 'DAMGTIMEZONE'
    key                                     = 'TimeZone'
    _name                                   = 'DAMG Time Zone'

    def __init__(self, *__args):
        super(TimeZone, self).__init__(*__args)


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name                      = val

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved