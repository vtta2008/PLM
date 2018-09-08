# -*- coding: utf-8 -*-
"""

Script Name: unit.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

from damgdock.types import DAMG, DAMGdict

class year(DAMG):
    _id = 'Unit'
    _name = 'Year(s)'

class month(DAMG):
    _id = 'Unit'
    _name = 'Month(s)'

class week(DAMG):
    _id = 'Unit'
    _name = 'Week(s)'

class day(DAMG):
    _id = 'Unit'
    _name = 'Day(s)'

class hour(DAMG):
    _id = 'Unit'
    _name = 'Hr(s)'

class minute(DAMG):
    _id = 'Unit'
    _name = 'Min(s)'

class second(DAMG):
    _id = 'Unit'
    _name = 'Sec(s)'

class mon(DAMG):
    _id = 'Unit'
    _name = 'Monday'

class tue(DAMG):
    _id = 'Unit'
    _name = 'Tuesday'

class wed(DAMG):
    _id = 'Unit'
    _name = 'Wednesday'

class thu(DAMG):
    _id = 'Unit'
    _name = 'Thursday'

class fri(DAMG):
    _id = 'Unit'
    _name = 'Friday'

class sat(DAMG):
    _id = 'Unit'
    _name = 'Saturday'

class sun(DAMG):
    _id = 'Unit'
    _name = 'Sunday'



class km(DAMG):
    _id = 'Unit'
    _name = 'Kilometter(s)'

class m(DAMG):
    _id = 'Unit'
    _name = 'Metter(s)'

class dm(DAMG):
    _id = 'Unit'
    _name = 'Decimetter(s)'

class cm(DAMG):
    _id = 'Unit'
    _name = 'Centimeter(s)'

class mm(DAMG):
    _id = 'Unit'
    _name = 'Milimeter(s)'



class Unit(DAMG):

    _id = "Unit"
    _name = "DAMGUNIT"
    _data = DAMGdict(_id, _name)

    _year = year()
    _month = month()
    _week = week()
    _day = day()
    _hr = hour()
    _min = minute()
    _sec = second()

    _mon = mon()
    _tue = tue()
    _wed = wed()
    _thu = thu()
    _fri = fri()
    _sat = sat()
    _sun = sun()

    _km = km()
    _m = m()
    _dm = dm()
    _cm = cm()
    _mm = mm()

    def __init__(self):
        super(Unit, self).__init__()

        self.year = self._year.__name__
        self.month = self._month.__name__
        self.week = self._week.__name__
        self.day = self._day.__name__
        self.hr = self._hr.__name__
        self.min = self._min.__name__
        self.sec = self._sec.__name__

        self.mon = self._mon.__name__
        self.tue = self._tue.__name__
        self.wed = self._wed.__name__
        self.thu = self._thu.__name__
        self.fri = self._fri.__name__
        self.sat = self._sat.__name__
        self.sun = self._sun.__name__

        self.km = self._km.__name__
        self.m = self._m.__name__
        self.dm = self._dm.__name__
        self.cm = self._cm.__name__
        self.mm = self._mm.__name__

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 31/08/2018 - 1:20 PM
# © 2017 - 2018 DAMGteam. All rights reserved