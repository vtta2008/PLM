# -*- coding: utf-8 -*-
"""

Script Name: DateTime.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import __copyright__
""" Import """

# PyQt5
from PyQt5.QtCore import QDateTime


class DateTime(QDateTime):

    Type                            = 'DAMGDATETIME'
    key                             = 'DateTime'
    _name                           = 'DAMG DateTime'
    _copyright                      = __copyright__

    def __init__(self, *__args):
        QDateTime.__init__(self)

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/17/2020 - 12:54 AM
# © 2017 - 2019 DAMGteam. All rights reserved