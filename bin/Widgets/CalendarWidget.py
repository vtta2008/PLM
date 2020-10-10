# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from PySide2.QtWidgets          import QCalendarWidget
from bin.models.SignalManager   import SignalManager
from bin.settings               import AppSettings


class CalendarWidget(QCalendarWidget):


    key                         = 'CalendarWidget'
    Type                        = 'DAMGCALENDAR'
    _name                       = 'DAMG CALENDAR'


    def __init__(self, parent=None):
        super(CalendarWidget, self).__init__(parent)

        self.parent = parent
        self.settings = AppSettings(self)
        self.signals = SignalManager(self)

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key, decode=None):
        if decode is None:
            return self.settings.initValue(key, self.key)
        else:
            return self.settings.initValue(key, self.key, decode)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
