# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import requests

from bin.damg                   import DAMGDICT


class BaseProfile(DAMGDICT):

    key                         = 'BaseProfile'

    _ip                         = None
    _city                       = None
    _country                    = None
    _latitude                   = None
    _longtitude                 = None


    def __init__(self, parent=None):
        super(BaseProfile, self).__init__()

        self._parent        = parent


    @property
    def parent(self):
        return self._parent

    @property
    def ip(self):
        return self._ip

    @property
    def city(self):
        return self._city

    @property
    def country(self):
        return self._country

    @property
    def latitude(self):
        return self._latitude

    @property
    def longtitue(self):
        return self._longtitude

    @parent.setter
    def parent(self, val):
        self._parent            = val

    @ip.setter
    def ip(self, val):
        self._ip                = val

    @city.setter
    def city(self, val):
        self._city              = val

    @country.setter
    def country(self, val):
        self._country           = val

    @latitude.setter
    def latitude(self, val):
        self._latitude          = val

    @longtitue.setter
    def longtitue(self, val):
        self._longtitude        = val




# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
