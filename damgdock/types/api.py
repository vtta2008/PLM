# -*- coding: utf-8 -*-
"""

Script Name: dppl.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

import json

from damgdock.types.base import DAMGDICT, DAMG, DOB

class FOUNDER(DAMG):

    founder                                 = "The founder of DAMGTEAM"
    _id                                     = "JimJim"

    _lastname                               = "Trinh"
    _firstname                              = "Do"
    _aka                                    = "Jimmy"

    _name                                   = "{0} {1}".format(_firstname, _lastname)
    _fullname                               = "{0} {1} (a.k.a {2})".format(_firstname, _lastname, _aka)

    _eProfile                               = "http://dot.damgteam.com/"
    _title                                  = "PipelineTD"
    _email                                  = "dot@damgteam.com"
    _dob                                    = DOB(1, 1, 1984).__dob__

    _data                                   = DAMGDICT(_id, _name)

    def __init__(self):
        super(FOUNDER, self).__init__()

        self.initialize()


    def __str__(self):
        return json.dumps({self._name: self.data}, indent=4)

    def __repr__(self):
        return json.dumps({self._name:self.data}, indent=4)

    def initialize(self):
        self.__dict__['id']                     = self._id
        self.__dict__['name']                   = self._name
        self.__dict__['fullname']               = self._fullname

        self.__dict__['title']                  = self._title
        self.__dict__['DOB']                    = self._dob

        self.__dict__['email']                  = self._email
        self.__dict__['eProfile']               = self._eProfile

    @property
    def data(self):
        self._data.add_item('id'                , self._id)
        self._data.add_item('name'              , self._name)
        self._data.add_item('fullname'          , self._fullname)

        self._data.add_item('title'             , self._title)
        self._data.add_item('DOB'               , self._dob)

        self._data.add_item('email'             , self._email)
        self._data.add_item('eProfile'          , self._eProfile)

        return self._data

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def email(self):
        return self._email

    @property
    def title(self):
        return self._title

    @property
    def dob(self):
        return self._dob

    @property
    def eProfile(self):
        return self._eProfile

    @property
    def profile(self):
        return self.__dict__

    __id__                                      = _id
    __name__                                    = _fullname
    __fullname__                                = _fullname
    __title__                                   = _title
    __email__                                   = _email

    __info__                                    = _data._copyright

class COFOUNDER(DAMG):

    coFounder                               = "The co-founder of DAMGTEAM"
    _id                                     = "DUCDM"
    _lastname                               = "Duong"
    _firstname                              = "Minh Duc"
    _aka                                    = "Up"
    _name                                   = "{0} {1}".format(_firstname, _lastname)
    _fullname                               = "{0} {1} (a.k.a {2})".format(_firstname, _lastname, _aka)
    _eProfile                               = "https://up209d.github.io/UPPortfolio/"
    _title                                  = "Front End Developer"
    _email                                  = "up@damgteam.com"
    _dob                                    = DOB(20,9,1987).__dob__

    _data                                   = DAMGDICT(_id, _name)

    def __init__(self):
        super(COFOUNDER, self).__init__()

        self.initialize()

    def __str__(self):
        return json.dumps({self._name: self.data}, indent=4)

    def __repr__(self):
        return json.dumps({self._name: self.data}, indent=4)

    def initialize(self):
        self.__dict__['id']                 = self._id
        self.__dict__['name']               = self._name
        self.__dict__['fullname']           = self._fullname

        self.__dict__['title']              = self._title
        self.__dict__['DOB']                = self._dob

        self.__dict__['email']              = self._email
        self.__dict__['eProfile']           = self._eProfile

    @property
    def data(self):
        self._data.add_item('id'            , self._id)
        self._data.add_item('name'          , self._name)
        self._data.add_item('fullname'      , self._fullname)

        self._data.add_item('title'         , self._title)
        self._data.add_item('DOB'           , self._dob)

        self._data.add_item('email'         , self._email)
        self._data.add_item('eProfile'      , self._eProfile)

        return self._data

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def email(self):
        return self._email

    @property
    def title(self):
        return self._title

    @property
    def dob(self):
        return self._dob

    @property
    def eProfile(self):
        return self._eProfile

    @property
    def profile(self):
        return self.__dict__

    __id__                                  = _id
    __name__                                = _fullname
    __fullname__                            = _fullname
    __title__                               = _title
    __email__                               = _email

    __info__                                = _data._copyright

class USER(DAMG):

    _id                                         = 'User'
    _name                                       = 'Username'
    _data                                       = DAMGDICT(_id, _name)

    def __init__(self, id='', firstname='', lastname='', aka='', title='', eProfile='', email='', dob=''):
        super(USER, self).__init__()

        self._id                                = id
        self._firstname                         = firstname
        self._lastname                          = lastname
        self._aka                               = aka
        self._title                             = title
        self._eProfile                          = eProfile
        self._email                             = email
        self._dob                               = dob

        self._name                              = "{0} {1}".format(self._firstname, self._lastname)
        self._fullname                          = "{0} {1} (a.k.a {2})".format(self._firstname, self._lastname, self._aka)
        self._data                              = DAMGDICT(self._id, self._name)

        self.__fullname__                       = self._fullname
        self.__title__                          = self._title
        self.__email__                          = self._email

    def __str__(self):
        return json.dumps({self._name: self.data}, indent=4)

    def __repr__(self):
        return json.dumps({self._name: self.data}, indent=4)

    def initialize(self):
        self.__dict__['id']                     = self._id
        self.__dict__['name']                   = self._name
        self.__dict__['fullname']               = self._fullname

        self.__dict__['title']                  = self._title
        self.__dict__['DOB']                    = self._dob

        self.__dict__['email']                  = self._email
        self.__dict__['eProfile']               = self._eProfile

    @property
    def data(self):
        self._data.add_item('id'                , self._id)
        self._data.add_item('name'              , self._name)
        self._data.add_item('fullname'          , self._fullname)

        self._data.add_item('title'             , self._title)
        self._data.add_item('DOB'               , self._dob)

        self._data.add_item('email'             , self._email)
        self._data.add_item('eProfile'          , self._eProfile)

        return self._data

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def email(self):
        return self._email

    @property
    def title(self):
        return self._title

    @property
    def dob(self):
        return self._dob

    @property
    def eProfile(self):
        return self._eProfile

    @property
    def profile(self):
        return self.__dict__

    __id__                                      = _id
    __name__                                    = _name
    __info__                                    = _data._copyright

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 30/08/2018 - 8:45 PM
# © 2017 - 2018 DAMGteam. All rights reserved