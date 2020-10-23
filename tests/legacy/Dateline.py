# -*- coding: utf-8 -*-
"""

Script Name: Due.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PLM
from pyPLM.damg import DAMG
from pyPLM.Core import Date, Time, DateTime

class DateLine(DAMG):

    key                             = 'DateLine'

    def __init__(self, hour, minute, second, day, month, year):
        super(DateLine, self).__init__()

        if not year:
            year                    = int(Date().currentDate().year())
        elif year < 99:
            year                    = int("20{0}".format(year))
        else:
            year                    = int(year)

        if month > 12:
            raise IndexError('Expect month smaller than 12: {0}'.format(month))

        if month in [1, 3, 5, 7, 8, 10, 12]:
            days                    = 31
        elif month in [2]:
            days                    = 28
        else:
            days                    = 30

        if day > days:
            raise IndexError('Expect day smaller than (0): {1}'.format(days, day))

        if hour > 24:
            raise IndexError('Expect hour smaller than 24: {0}'.format(hour))

        if minute > 60:
            raise IndexError('Expect minute smaller than 60: {0}'.format(minute))

        if second > 60:
            raise IndexError('Expect second smaller than 60: {0}'.format(second))


        self.hour                   = int(hour)
        self.minute                 = int(minute)
        self.second                 = int(second)

        self.day                    = int(day)
        self.month                  = int(month)
        self.year                   = int(year)

        self.time                   = Time(self.hour, self.minute, self.second)
        self.date                   = Date(self.year, self.month, self.day)
        self.endDate                = DateTime(self.date, self.time)

    def setTime(self, hour=0, minute=0, sec=0):
        return self.time.setHMS(hour, minute, sec)

    def setDate(self, day, month, year):
        return self.date.setDate(year, month, day)

    def setDateLine(self, hour, minute, sec, day, month, year):
        self.time.setHMS(hour, minute, sec)
        self.date.setDate(year, month, day)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 2/12/2019 - 10:25 AM
# © 2017 - 2018 DAMGteam. All rights reserved