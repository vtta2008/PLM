# -*- coding: utf-8 -*-
"""

Script Name: DateTime.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from .io_core import QDateTime


class DateTime(QDateTime):

    Type                            = 'DAMGDATETIME'
    key                             = 'DateTime'
    _name                           = 'DAMG DateTime'

    def __init__(self, *__args):
        super(DateTime, self).__init__(*__args)


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/17/2020 - 12:54 AM
# © 2017 - 2019 DAMGteam. All rights reserved