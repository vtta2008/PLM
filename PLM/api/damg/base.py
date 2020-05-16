# -*- coding: utf-8 -*-
"""

Script Name: BaseLog.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import json, inspect

# PLM
from PLM import __copyright__



class Iterator(object):

    """ Make object Iterable """

    def __init__(self, sorted_dict):

        self._dict                      = sorted_dict
        self._keys                      = sorted(self._dict.keys())
        self._nr_items                  = len(self._keys)
        self._idx                       = 0

    def __iter__(self):
        return self

    def next(self):
        if self._idx >= self._nr_items:
            raise StopIteration

        key                             = self._keys[self._idx]
        value                           = self._dict[key]
        self._idx += 1

        return key, value

    __next__                            = next


# -------------------------------------------------------------------------------------------------------------
""" List """


class BaseList(list):

    Type                                = 'DAMGLIST'
    key                                 = 'BaseList'
    _name                               = 'DAMG list'
    _count                              = 0
    _copyright                          = __copyright__()
    _data                               = dict()

    def __init__(self):
        list.__init__(self)

    def __call__(self):

        """ Make object callable """

        if isinstance(self, object):
            return True
        else:
            return False

    @property
    def copyright(self):
        return self._copyright

    @property
    def data(self):
        return self._data

    @property
    def name(self):
        return self._name

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, newVal):
        self._count                     = newVal

    @data.setter
    def data(self, newData):
        self._data                      = newData

    @name.setter
    def name(self, newName):
        self._name                      = newName


# -------------------------------------------------------------------------------------------------------------
""" Dict """


class BaseDict(dict):

    Type                                = 'DAMGDICT'
    key                                 = 'BaseDict'
    _name                               = 'DAMG dict'
    _count                              = 0
    _copyright                          = __copyright__()
    _data                               = dict()

    def __init__(self):
        dict.__init__(self)

    def __call__(self):

        """ Make object callable """

        if isinstance(self, object):
            return True
        else:
            return False

    def add(self, key, value):
        self[key] = value
        self.update()

    def input(self, data={}):
        if data == {}:
            self.clear()
        else:
            for k, v in data.items():
                self.add(k, v)
        self.update()

    @property
    def copyright(self):
        return self._copyright

    @property
    def data(self):
        return self._data

    @property
    def name(self):
        return self._name

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, newVal):
        self._count                     = newVal

    @data.setter
    def data(self, newData):
        self._data                      = newData

    @name.setter
    def name(self, newName):
        self._name                      = newName


class BaseError(Exception):

    Type                                = 'DAMGERROR'
    key                                 = 'BaseError'
    _name                               = 'DAMG error'
    _count                              = 0
    _data                               = dict()
    _copyright                          = __copyright__()

    def __str__(self):

        """ Print object ill return json qssPths type """

        return json.dumps(self.data, cls=ObjectEncoder, indent=4, sort_keys=True)

    def __repr__(self):

        """ Print object ill return json qssPths type """

        return json.dumps(self.data, cls=ObjectEncoder, indent=4, sort_keys=True)

    def __call__(self):

        """ Make object callable """

        if isinstance(self, object):
            return True
        else:
            return False

    @property
    def copyright(self):
        return self._copyright

    @property
    def data(self):
        return self._data

    @property
    def name(self):
        return self._name

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, newVal):
        self._count                     = newVal

    @data.setter
    def data(self, newData):
        self._data                      = newData

    @name.setter
    def name(self, newName):
        self._name                      = newName


# -------------------------------------------------------------------------------------------------------------
class DuplicatedObjectError(BaseError):
    """ When an DAMG object already regiested """


class TypeObjectError(BaseError):
    """ When object.Type is not recognisable """


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/17/2020 - 12:16 AM
# © 2017 - 2019 DAMGteam. All rights reserved