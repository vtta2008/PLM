# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PyQt5
from PLM                                    import __copyright__, QTimeZone

class TimeZone(QTimeZone):

    Type                                    = 'DAMGTIMEZONE'
    key                                     = 'TimeZone'
    _name                                   = 'DAMG Time Zone'
    _copyright                              = __copyright__

    def __init__(self, *__args):
        super(TimeZone, self).__init__(*__args)


    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name                      = val

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved