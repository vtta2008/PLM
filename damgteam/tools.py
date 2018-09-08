# -*- coding: utf-8 -*-
"""

Script Name: tools.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from .base import DAMG, OID, NAME

class CONVERTER(DAMG):

    def __init__(self):
        super(CONVERTER, self).__init__()

        self._id                            = OID(self)
        self._name                          = NAME(self)
        self.Type                           = '{0} Object'.format(self._name)

        self.__id__                         = self._id.__oid__
        self.__name__                       = self._name.__name__
        self.__type__                       = self.Type

    def year_to_month(self, years):
        return years*12

    def year_to_day(self, years):
        return years*365

    def year_to_hours(self, years):
        return years*365*24

    def year_to_minute(self, years):
        return years*365*24*60

    def year_to_second(self, years):
        return years*365*24*60*60

    def month_to_year(self, months):
        return months/12

    def month_to_day(self, months):
        return months*30

    def month_to_minute(self, months):
        return months*30*24

    def mont_to_second(self, months):
        return months*30*24*60

    def day_to_year(self, days):
        return days/365

    def day_to_month(self, days):
        return days/30

    def day_to_weeks(self, days):
        return days/7

    def day_to_hour(self, days):
        return days*24

    def day_to_minute(self, days):
        return days*24*60

    def day_to_second(self, days):
        return days*24*60*60

    def hour_to_year(self, hours):
        return hours/(12*24)

    def hour_to_month(self, hours):
        return hours/(12*24*30)

    def hour_to_day(self, hours):
        return hours/24

    def hour_to_minute(self, hours):
        return hours*60

    def hour_to_second(self, hours):
        return hours*60*60

    def minute_to_year(self, minutes):
        return minutes/(60*24*365)

    def minute_to_day(self, minutes):
        return minutes*60*24*12

    def minute_to_seconds(self, minutes):
        return minutes/60

    def second_to_year(self, seconds):
        return seconds/(60*60*24*365)

    def second_to_month(self, seconds):
        return seconds/(60*60*24*30)

    def second_to_day(self, seconds):
        return seconds/(60*60*24)

    def second_to_hour(self, seconds):
        return seconds/(60*60)

    def second_to_minute(self, seconds):
        return seconds/60


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 8/09/2018 - 8:10 PM
# © 2017 - 2018 DAMGteam. All rights reserved