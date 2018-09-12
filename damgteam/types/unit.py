# -*- coding: utf-8 -*-
"""

Script Name: unit.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

# PyQt5
from PyQt5.QtCore import QDate, QTime, QDateTime

from damgteam.base import DAMG, DAMGDICT, damgvar


# -------------------------------------------------------------------------------------------------------------
""" Unit base """

class UNIT(DAMG):

    _unit = 'Unit'

    def to_unit(self):
        return self._unit

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, newUnit):
        self._unit                          = newUnit

# -------------------------------------------------------------------------------------------------------------
""" Unit --> date & time"""

class DATETIME(UNIT):

    _unit                                   = 'Duration'

    def __init__(self):
        UNIT.__init__(self)

        self.to_now()
        self.to_day()
        self.set_time()
        self.set_date()

    def days_distance(self, daystart, dayend):
        return daystart.daysTo(dayend)

    def set_date(self, day=1, month=1, year=2013):

        self._year                          = year
        self._month                         = month
        self._day                           = day

        self._setdate                       = QDate(self._year, self._month, self._day)

        self._date                          = self._setdate.toString(damgvar.fmts)
        self.__date__                       = self._setdate.toString(damgvar.fmtl)

        return self._date, self.__date__

    def set_time(self, hour=1, minute=30, second=30):
        self._hour                          = hour
        self._minute                        = minute
        self._second                        = second

        self._settime                       = QTime(self._hour, self._minute, self._second)

        self._time                          = self._settime.toString(damgvar.fmts)
        self.__time__                       = self._settime.toString(damgvar.fmtl)

        return self._time, self.__time__

    def to_now(self):
        now                                 = QTime.currentTime()
        self._now                           = now.toString(damgvar.fmts)
        self.__now__                        = now.toString(damgvar.fmtl)

        return self._now, self.__now__

    def to_day(self):

        now                                 = QDate.currentDate()
        self._today                         = now.toString(damgvar.fmts)
        self.__today__                      = now.toString(damgvar.fmtl)

        return self._today, self.__today__

    @property
    def date(self):
        return self._date

    @property
    def today(self):
        return self._today

    @property
    def totime(self):
        return self._now

    @date.setter
    def date(self, newData):
        self._date                          = newData

    @today.setter
    def today(self, newData):
        self._today                         = newData

    @totime.setter
    def totime(self, newData):
        self._now                           = newData


class DOB(DATETIME):

    _unit                                   = 'Birthday'

    def __init__(self, day=1, month=1, year=1900):
        DATETIME.__init__(self)

        self._day                           = day
        self._month                         = month
        self._year                          = year

        self._data                          = DAMGDICT()
        self.__dict__                       = DAMGDICT()

        self._dob                           =  QDate(self._year, self._month, self._day)
        self.__dob__                        = self._dob.toString(damgvar.fmtl)
        self.dobs                           = self._dob.toString(damgvar.fmts)

        self.initialize()

    @property
    def data(self):
        self._data.add_item('metadata'      , self._metadata)
        self._data.add_item('name'          , self._name)
        self._data.add_item('dob'           , self.dobs)
        self._data.add_item('__dob__'       , self.__dob__)
        self._data.add_item('unit'          , self._unit)

        return self._data

    @property
    def dob(self):
        return self._dob

    @dob.setter
    def dob(self, newDob):
        self._dob                           = newDob


class Year(DATETIME):
    _unit = 'Year(s)'


class Month(DATETIME):
    _unit = 'Month(s)'


class Week(DATETIME):
    _unit = 'Week(s)'


class Day(DATETIME):
    _unit = 'Day(s)'


class Hour(DATETIME):
    _unit = 'Hr(s)'


class Minute(DATETIME):
    _unit = 'Min(s)'


class Second(DATETIME):
    _unit = 'Sec(s)'


class Monday(Day):
    _unit = 'Mon'


class Tuesday(Day):
    _unit = 'Tue'


class Wednesday(Day):
    _unit = 'Wed'


class Thursday(Day):
    _unit = 'Thu'


class Friday(Day):
    _unit = 'Fri'


class Saturday(Day):
    _unit = 'Sat'


class Sunday(Day):
    _unit = 'Sun'


# -------------------------------------------------------------------------------------------------------------
""" Unit --> long """


class Kilometer(DAMG):
    _unit = 'km(s)'

class Meter(DAMG):
    _unit = 'm(s)'

class Decimeter(DAMG):
    _unit = 'dm(s)'

class Centimeter(DAMG):
    _unit = 'cm(s)'

class Milimeter(DAMG):
    _unit = 'mm(s)'





# -------------------------------------------------------------------------------------------------------------
# Created by panda on 31/08/2018 - 1:20 PM
# © 2017 - 2018 DAMGteam. All rights reserved