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
import sys, json, inspect, time, datetime, traceback

# PyQt5
from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal, QThread, QRunnable, QThreadPool

# PLM
from appData import __copyright__

# -------------------------------------------------------------------------------------------------------------
""" Encoder """

class ObjectEncoder(json.JSONEncoder):

    """ Make an object readable using json encoder. Return data string """

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
""" Legacy """

class Base(QObject):

    """ Example from PyQt5 documentations """

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
class BaseList(list):

    Type                                = 'DAMGLIST'
    key                                 = 'BaseList'
    _name                               = 'DAMG list'
    _count                              = 0
    _copyright                          = __copyright__
    _data                               = dict()

    def __init__(self):
        list.__init__(self)

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
class BaseDict(dict):

    Type                                = 'DAMGDICT'
    key                                 = 'BaseDict'
    _name                               = 'DAMG dict'
    _count                              = 0
    _copyright                          = __copyright__
    _data                               = dict()

    def __init__(self):
        dict.__init__(self)


    def add(self, key, value):
        self[key] = value

    def input(self, data={}):
        if data == {}:
            self.clear()
        else:
            for k, v in data.items():
                self.add(k, v)

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
        self._count                     = newVal

    @data.setter
    def data(self, newData):
        self._data                      = newData

    @name.setter
    def name(self, newName):
        self._name                      = newName

# -------------------------------------------------------------------------------------------------------------
class BaseError(Exception):

    Type                                = 'DAMGERROR'
    key                                 = 'BaseError'
    _name                               = 'DAMG error'
    _count                              = 0
    _data                               = dict()
    _copyright                          = __copyright__

    def __init__(self):
        Exception.__init__(self)

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
    key                                 = 'BaseObject'
    _name                               = 'DAMG object'
    _count                              = 0
    _data                               = dict()
    _copyright                          = __copyright__

    def __init__(self):
        QObject.__init__(self)

    def __str__(self):
        """ Print object will return data string """
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
class DuplicatedObjectError(BaseError):
    """ When an DAMG object already regiested """
    pass

# -------------------------------------------------------------------------------------------------------------
class DAMGREGIS(BaseDict):

    key = 'DAMGREGIS'

    def __init__(self):
        BaseDict.__init__(self)

        self.object_name                    = list()
        self.object_id                      = list()
        self._count                         = 0
        self._step                          = 1

    def register(self, obj):

        objName = obj.name

        if objName in self.keys():
            raise DuplicatedObjectError('Duplicated object detected!!!')
        else:
            self[objName] = obj.data
            self.object_name.append(obj.data['ObjectName'])
            self.object_id.append(obj.data['ObjectID'])
            self._count = self._count + self._step

            # print('{0}: obj registed: {1}'.format(__name__, obj))

    @pyqtSlot(int)
    def step_change_notify(self, val):
        if not self._step == val:
            self._step                      = val
            print("step has changed to {}".format(str(val)))

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
        self._count                         = newVal

    @step.setter
    def step(self, newVal):
        self._step                          = newVal

objRegistry = DAMGREGIS()

# -------------------------------------------------------------------------------------------------------------
""" Signals """

class WorkerSignals(BaseObject):

    key                                     = 'WorkerSignals'
    Type                                    = 'DAMG signals'
    _name                                   = 'WorkerSignals'

    finished                                = pyqtSignal()
    error                                   = pyqtSignal(tuple)
    result                                  = pyqtSignal(object)
    progress                                = pyqtSignal(int)

    quit_thread                             = pyqtSignal(name='close_thread')

    def __init__(self, parent=None):
        object.__init__(self)

        self.parent = parent

        self._name = "{0} {1}".format(self._name, objRegistry.count + 1)

        self._data['ObjectName'] = self._name
        self._data['ObjectID'] = str(id(self))
        self._data['datetime'] = str(datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S|%d.%m.%Y'))
        objRegistry.register(self)

# -------------------------------------------------------------------------------------------------------------
class WorkerBase(QRunnable):

    Type                                    = 'DAMGWORKER'
    key                                     = 'WorkderBase'
    _name                                   = 'DAMG worker'
    _count                                  = 0
    _copyright                              = __copyright__
    _data                                   = dict()

    def __init__(self, task, *args, **kwargs):
        QRunnable.__init__(self)

        self.task           = task                             # Store constructor arguments (re-used for processing)
        self.args           = args
        self.kwargs         = kwargs

        self.signals        = WorkerSignals()

    def __str__(self):
        """ Print object will return data string """
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

    @pyqtSlot()
    def run(self):

        try:
            self.task(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit()                                          # Return the result of the processing
        finally:
            self.signals.finished.emit()                                        # Done

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
        self._count                     = newVal

    @data.setter
    def data(self, newData):
        self._data                      = newData

    @name.setter
    def name(self, newName):
        self._name                      = newName

# -------------------------------------------------------------------------------------------------------------
class ThreadBase(QThread):

    Type                                = 'DAMGTHREAD'
    _name                               = 'DAMG thread'
    _count                              = 0
    _copyright                          = __copyright__
    _data                               = dict()

    def __init__(self, task):
        super(ThreadBase, self).__init__()

        self.task = task

    def run(self):

        if 'user' in self.task:
            self.query_user_data()
        elif 'host' in self.task:
            self.query_hosts_data()
        elif 'service' in self.task:
            self.query_services_data()
        elif 'alignakdaemon' in self.task:
            self.query_daemons_data()
        elif 'livesynthesis' in self.task:
            self.query_livesynthesis_data()
        elif 'history' in self.task:
            self.query_history_data()
        elif 'notifications' in self.task:
            self.query_notifications_data()
        else:
            pass

    def __str__(self):
        """ Print object will return data string """
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
class ThreadPoolBase(QThreadPool):

    Type                                    = 'DAMGTHREADPOOL'
    key                                     = 'ThreadPoolBase'
    _count                                  = 0
    _copyright                              = __copyright__
    _data                                   = dict()

    def __init__(self):
        super(ThreadPoolBase, self).__init__()

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
class DAMG(BaseObject):

    """ Base Damg team object. """

    key = "DAMG"

    def __init__(self, parent=None, **kwargs):
        BaseObject.__init__(self)

        self._parent                        = parent

        self._name = "{0} {1}".format(self._name, objRegistry.count + 1)
        self.setObjectName(self._name)

        self._data['ObjectName']            = self._name
        self._data['ObjectID']              = str(id(self))
        self._data['datetime']              = str(datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S|%d.%m.%Y'))

        objRegistry.register(self)

class DAMGERROR(BaseError):

    """ Base Damg team object. """

    key = 'DAMGERROR'

    def __init__(self, parent=None, **kwargs):
        BaseError.__init__(self)

        self._parent                        = parent

        self._name = "{0} {1}".format(self._name, objRegistry.count + 1)

        self._data['ObjectName']            = self._name
        self._data['ObjectID']              = str(id(self))
        self._data['datetime']              = str(datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S|%d.%m.%Y'))

        objRegistry.register(self)

class DAMGLIST(BaseList):

    """ Base Damg team dictionary """

    key = 'DAMGLIST'

    def __init__(self, parent=None, **kwargs):
        BaseList.__init__(self)

        self._parent                        = parent

        self._name = "{0} {1}".format(self._name, objRegistry.count + 1)

        self._data['ObjectName']            = self._name
        self._data['ObjectID']              = str(id(self))
        self._data['datetime']              = str(datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S|%d.%m.%Y'))

        objRegistry.register(self)

class DAMGDICT(BaseDict):

    """ Base Damg team dictionary """

    key = 'DAMGDICT'

    def __init__(self, parent=None, **kwargs):
        BaseDict.__init__(self)

        self._parent                        = parent

        self._name = "{0} {1}".format(self._name, objRegistry.count + 1)

        self._data['ObjectName'] = self._name
        self._data['ObjectID'] = str(id(self))
        self._data['datetime'] = str(datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S|%d.%m.%Y'))

        objRegistry.register(self)

# -------------------------------------------------------------------------------------------------------------
""" Worker & Thread """

class DAMGWORKER(WorkerBase):

    key = 'DAMGWORKER'

    def __init__(self, *args, **kwargs):
        super(DAMGWORKER, self).__init__(self)

        self.args           = args
        self.kwargs         = kwargs

        self._name = "{0} {1}".format(self._name, objRegistry.count + 1)

        self._data['ObjectName'] = self._name
        self._data['ObjectID'] = str(id(self))
        self._data['datetime'] = str(datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S|%d.%m.%Y'))

        objRegistry.register(self)

class DAMGTHREAD(ThreadBase):

    key = 'DAMGTHREAD'

    def __init__(self, task):
        super(DAMGTHREAD, self).__init__(self)

        self.task = task

if __name__ == '__main__':

    a = DAMG()
    b = DAMGERROR()
    c = DAMGLIST()
    d = DAMGDICT()
    e = DAMGWORKER()
    f = DAMGTHREAD(None)

    from pprint import pprint
    print(a, b, c, d, e, f)
    pprint(objRegistry)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/10/2019 - 12:22 PM
# © 2017 - 2018 DAMGteam. All rights reserved