# -*- coding: utf-8 -*-
"""

Script Name: models.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals


from damgteam.base import DAMG, DAMGDICT

# -------------------------------------------------------------------------------------------------------------
""" Person """


class PERSON(DAMG):

    """ A new type to indentify person """

    _data                                   = DAMGDICT()
    __dict__                                = DAMGDICT()

    def __init__(self,  pid                 = None,                                 # Person id
                        firstname           = None,                                 # First name
                        lastname            = None,                                 # Last name
                        aka                 = None,                                 # As known as
                        title               = None,                                 # Mr., Mrs., Ms., etc.
                        artistTitle         = None,                                 # Modeling, designer, etc.
                        eProfile            = None,                                 # Website, blog, etc.
                        email               = None,                                 # Email adress
                        dob                 = None,                                 # Date of birth
                        coo                 = None,                                 # Country of origin,
                 ):

        DAMG.__init__(self)

        self._pid                           = pid
        self._firstname                     = firstname
        self._lastname                      = lastname
        self._aka                           = aka
        self._title                         = title
        self._artistTitle                   = artistTitle
        self._eProfile                      = eProfile
        self._email                         = email
        self._dob                           = dob
        self._coo                           = coo

        self._name                          = "{0} {1}".format(self._firstname, self._lastname)
        self._fullname                      = "{0} {1} (a.k.a {2})".format(self._firstname, self._lastname, self._aka)

        self.__fullname__                   = self._fullname
        self.__title__                      = self._title
        self.__email__                      = self._email

    @property
    def data(self):

        self._data.add_item('pid'           , self._pid)
        self._data.add_item('name'          , self._name)
        self._data.add_item('fullname'      , self._fullname)
        self._data.add_item('title'         , self._title)
        self._data.add_item('artistTitle'   , self._artistTitle)
        self._data.add_item('DOB'           , self._dob)
        self._data.add_item('email'         , self._email)
        self._data.add_item('eProfile'      , self._eProfile)
        self._data.add_item('coo'           , self._coo)

        self._data.add_item('metadata'      , self._metadata)

        return self._data

    @property
    def pid(self):
        return self._pid

    @property
    def fullname(self):
        return self._fullname

    @property
    def email(self):
        return self._email

    @property
    def title(self):
        return self._title

    @property
    def artistTitle(self):
        return self._artistTitle

    @property
    def dob(self):
        return self._dob

    @property
    def eProfile(self):
        return self._eProfile

    @property
    def profile(self):
        return self.__dict__

    @property
    def coo(self):
        return self._coo

    @pid.setter
    def pid(self, newData):
        self._pid                           = newData

    @fullname.setter
    def fullname(self, newData):
        self._fullname                      = newData

    @email.setter
    def email(self, newData):
        self._email                         = newData

    @title.setter
    def title(self, newData):
        self._title                         = newData

    @artistTitle.setter
    def artistTitle(self, newData):
        self._artistTitle                   = newData

    @dob.setter
    def dob(self, newData):
        self._dob                           = newData

    @eProfile.setter
    def eProfile(self, newData):
        self._eProfile                      = newData

    @profile.setter
    def profile(self, newData):
        self.__dict__                       = newData

    @coo.setter
    def coo(self, newData):
        self._coo                           = newData


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 11/09/2018 - 11:04 AM
# © 2017 - 2018 DAMGteam. All rights reserved