# -*- coding: utf-8 -*-
"""

Script Name: base.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
""" Import """

# Python
import json, inspect, time, datetime, uuid

# PyQt5
from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal

# PLM
from appData import __copyright__
from cores.Loggers import Loggers

# -------------------------------------------------------------------------------------------------------------
""" Legacy """

class Base(QObject):

    stationsChanged = pyqtSignal()
    _attributes = {}

    def __init__(self):
        QObject.__init__(self)
        self.m_stations =[]

    @pyqtProperty('QVariant', notify=stationsChanged)
    def stations(self):
        return self.m_stations

    @stations.setter
    def set_stations(self, val):
        if self.m_stations == val:
            return
        self.m_stations = val[:]
        self.stationsChanged.emit()

    def list_fill(self, my_list):
        self.stations = my_list

# -------------------------------------------------------------------------------------------------------------
""" Encoder """

class ObjectEncoder(json.JSONEncoder):

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

# -------------------------------------------------------------------------------------------------------------
""" Iterable """

class Iterator(object):

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
class BaseList(list):

    Type                                = 'DAMGLIST'
    _name                               = 'DAMG list'
    _count                              = 0

    def __init__(self):
        list.__init__(self)

        self._copyright                 = __copyright__

    @pyqtSlot(int)
    def count_notified_change(self, val):
        self._count = val

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name = newName

# -------------------------------------------------------------------------------------------------------------
class BaseDict(dict):

    Type                                = 'DAMGDICT'
    _name                               = 'DAMG dict'
    _count                              = 0

    def __init__(self, *args, **kwargs):
        dict.__init__(self)

        self._copyright                 = __copyright__

    def add(self, key, value):
        self[key] = value

    def input(self, data={}):
        if data == {}:
            self.clear()
        else:
            for k, v in data.items():
                self.add(k, v)

    def __iter__(self):
        """ Make object iterable """
        return Iterator(self)

    @pyqtSlot(int)
    def count_notified_change(self, val):
        self._count = val

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, newVal):
        self._count = newVal

    @name.setter
    def name(self, newName):
        self._name = newName

    iterkeys = __iter__

# -------------------------------------------------------------------------------------------------------------
class BaseError(Exception):

    Type                                = 'DAMGERROR'
    _name                               = 'DAMG error'

    _count                              = 0
    _data                               = dict()

    def __init__(self):
        Exception.__init__(self)

        self._copyright = __copyright__

    def __str__(self):

        """ Print object ill return json data type """

        return json.dumps(self.data, cls=ObjectEncoder, indent=4, sort_keys=True)

    def __repr__(self):

        """ Print object ill return json data type """

        return json.dumps(self.data, cls=ObjectEncoder, indent=4, sort_keys=True)

    def __call__(self):

        """ Make object callable """

        if isinstance(self, object):
            return True
        else:
            return False

    @pyqtSlot(int)
    def count_notified_change(self, val):
        self._count = val

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
        self._count                         = newVal

    @data.setter
    def data(self, newData):
        self._data                          = newData

    @name.setter
    def name(self, newName):
        self._name                          = newName

# -------------------------------------------------------------------------------------------------------------
class BaseObject(QObject):

    Type                                = 'DAMGOBJECT'
    _name                               = 'DAMG object'

    _count                              = 0
    _data                               = dict()

    def __init__(self):
        QObject.__init__(self)

        self._copyright = __copyright__

    def __str__(self):

        """ Print object ill return json data type """

        return json.dumps(self.data, cls=ObjectEncoder, indent=4, sort_keys=True)

    def __repr__(self):

        """ Print object ill return json data type """

        return json.dumps(self.data, cls=ObjectEncoder, indent=4, sort_keys=True)

    def __call__(self):

        """ Make object callable """

        if isinstance(self, object):
            return True
        else:
            return False

    @pyqtSlot(int)
    def count_notified_change(self, val):
        self._count = val

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
        self._count                         = newVal

    @data.setter
    def data(self, newData):
        self._data                          = newData

    @name.setter
    def name(self, newName):
        self._name                          = newName


class DuplicatedObjectError(BaseError):
    """ When an DAMG object already regiested """
    pass
# -------------------------------------------------------------------------------------------------------------
class DAMGREGIS(BaseDict):

    def __init__(self):
        BaseDict.__init__(self)

        logger                          = Loggers()
        self.report                     = logger.report

        self.object_name                = list()
        self.object_id                  = list()

        self._count                     = 0
        self._step                      = 1

    def register(self, obj):

        objName = obj.name

        if objName in self.keys():
            raise DuplicatedObjectError('Duplicated object detected!!!')
        else:
            try:
                self[objName] = obj.data
            except AttributeError:
                self.object_name.append(obj.name)
                self.object_id.append(str(uuid.uuid4()))
            else:
                self.object_name.append(obj.data['ObjectName'])
                self.object_id.append(obj.data['ObjectID'])
            finally:
                self._count = self._count + self._step

            # self.report('objName registered')

    @pyqtSlot(int)
    def step_change_notify(self, val):
        if not self._step == val:
            self._step                  = val

    def str2bool(self, arg):
        return str(arg).lower() in ['true', 1, '1', 'ok', '2']

    def bool2str(self, arg):
        if arg:
            return "True"
        else:
            return "False"

    @property
    def count(self):
        return self._count

    @property
    def step(self):
        return self._step

    @count.setter
    def count(self, newVal):
        self._count                     = newVal

    @step.setter
    def step(self, newVal):
        self._step                      = newVal

objRegistry = DAMGREGIS()

# -------------------------------------------------------------------------------------------------------------
class DAMG(BaseObject):

    """ Base Damg team object. """

    def __init__(self, parent=None, **kwargs):
        BaseObject.__init__(self)

        self._parent                        = parent

        self._name = "{0} {1}".format(self._name, objRegistry.count + 1)
        self.setObjectName(self._name)

        self._data['ObjectName']            = self._name
        self._data['ObjectID']              = str(uuid.uuid4())
        self._data['datetime']              = str(datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S|%d.%m.%Y'))

        objRegistry.register(self)

class DAMGERROR(BaseError):

    """ Base Damg team object. """

    def __init__(self, parent=None, **kwargs):
        BaseError.__init__(self)

        self._parent                        = parent

        self._name = "{0} {1}".format(self._name, objRegistry.count + 1)

        self._data['ObjectName']            = self._name
        self._data['ObjectID']              = str(uuid.uuid4())
        self._data['datetime']              = str(datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S|%d.%m.%Y'))

        objRegistry.register(self)

class DAMGLIST(BaseList):

    """ Base Damg team dictionary """

    def __init__(self, parent=None, **kwargs):
        BaseList.__init__(self)

        self._parent                        = parent

        self._name = "{0} {1}".format(self._name, objRegistry.count + 1)

        objRegistry.register(self)

class DAMGDICT(BaseDict):

    """ Base Damg team dictionary """

    def __init__(self, parent=None, *args, **kwargs):
        BaseDict.__init__(self)

        self._parent                        = parent

        self._name = "{0} {1}".format(self._name, objRegistry.count + 1)

        objRegistry.register(self)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/10/2019 - 12:22 PM
# © 2017 - 2018 DAMGteam. All rights reserved