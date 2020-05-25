# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from .io_gui import QWheelEvent

class WheelEvent(QWheelEvent):

    Type                        = 'DAMGWHEELEVENT'
    key                         = 'WheelEvent'
    _name                       = 'DAMG Wheel Event'

    def __init__(self, *__args):
        super(WheelEvent, self).__init__(*__args)


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name              = val

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved