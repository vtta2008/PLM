# -*- coding: utf-8 -*-
"""

Script Name: Organisation.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from bin import DAMG

class OrgBase(DAMG):

    key = 'Organisation'
    Type = 'DAMGORGANISATION'
    _name = None
    _id = None
    _address = None
    _website = None
    _details = None

    def __init__(self):
        super(OrgBase, self).__init__(self)

        self._data['name'] = self._name
        self._data['id'] = self._id
        self._data['adress'] = self._address
        self._data['website'] = self._website
        self._data['details'] = self._details

    @property
    def id(self):
        return self._id

    @property
    def address(self):
        return self._address

    @property
    def website(self):
        return self._website

    @property
    def details(self):
        return self._details

    @details.setter
    def details(self, val):
        self._details = val

    @website.setter
    def website(self, val):
        self._website = val

    @address.setter
    def address(self, val):
        self._address = val

    @id.setter
    def id(self, val):
        self._id = val



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 2/12/2019 - 12:42 PM
# © 2017 - 2018 DAMGteam. All rights reserved