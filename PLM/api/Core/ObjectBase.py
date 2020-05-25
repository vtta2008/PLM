# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
import json, inspect
from .io_core                           import QObject


# -------------------------------------------------------------------------------------------------------------
""" Encoder """


class ObjectEncoder(json.JSONEncoder):

    """ Make an object readable using json encoder. Return qssPths string """

    def default(self, obj):
        if hasattr(obj, 'to_json'):
            return self.default(obj.to_json())

        elif hasattr(obj, '__dict__'):

            d = dict(
                (key, value) for key, value in inspect.getmembers(obj) if not key.startswith('__')
                and not inspect.isabstract(value) and not inspect.isbuiltin(value) and not inspect.isfunction(value)
                and not inspect.isgenerator(value) and not inspect.isgeneratorfunction(value)
                and not inspect.ismethod(value) and not inspect.ismethoddescriptor(value)
                and not inspect.isroutine(value)
            )

            return self.default(d)

        return obj


class BaseObject(QObject):

    Type                                = 'DAMGOBJECT'
    key                                 = 'BaseObject'
    _name                               = 'DAMG object'
    _count                              = 0
    _data                               = dict()

    def __init__(self):
        QObject.__init__(self)

    def __str__(self):
        """ Print object will return qssPths string """
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
        self._count                         = newVal

    @data.setter
    def data(self, newData):
        self._data                          = newData

    @name.setter
    def name(self, newName):
        self._name                          = newName

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved