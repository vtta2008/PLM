# -*- coding: utf-8 -*-
"""

Script Name: BaseLog.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__
""" Import """

# Python
import sys, json, inspect, traceback

# PyQt5
from PyQt5.QtCore                       import QObject, QRunnable, QThread, QThreadPool


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


# -------------------------------------------------------------------------------------------------------------
""" Tuple """


class BaseTuple(tuple):

    Type                                = 'DAMGTUPLE'
    key                                 = 'BaseTuple'
    _name                               = 'DAMG Base Tuple'
    _data                               = dict()
    __count                             = 0
    _copyright                          = __copyright__()

    def __new__(cls, *args):
        cls.args = args

        return tuple.__new__(BaseTuple, tuple(cls.args))

    def __bases__(self):
        return tuple(BaseTuple, tuple(self.args))

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
    def _count(self):
        return self.__count

    @data.setter
    def data(self, newData):
        self._data                      = newData

    @_count.setter
    def _count(self, newVal):
        self.__count                    = newVal

    @name.setter
    def name(self, newName):
        self._name                      = newName


# -------------------------------------------------------------------------------------------------------------
""" Error """


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
""" Object """


class BaseObject(QObject):

    Type                                = 'DAMGOBJECT'
    key                                 = 'BaseObject'
    _name                               = 'DAMG object'
    _count                              = 0
    _data                               = dict()
    _copyright                          = __copyright__()

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


class TypeObjectError(BaseError):
    """ When object.Type is not recognisable """


# -------------------------------------------------------------------------------------------------------------
""" Worker """


class BaseWorker(QRunnable):

    Type                                    = 'DAMGWORKER'
    key                                     = 'BaseWorker'
    _name                                   = 'DAMG Worker'
    _count                                  = 0
    _copyright                              = __copyright__()
    _data                                   = dict()

    def __init__(self, task, *args, **kwargs):
        QRunnable.__init__(self)

        self.task                           = task            # Store constructor arguments (re-used for processing)
        self.args                           = args
        self.kwargs                         = kwargs

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

    def run(self):

        try:
            result = self.task(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            print(exctype, value, traceback.format_exc())
        else:
            print(result)                                    # Return the result of the processing
        finally:
            print(self)                                        # Done

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
""" Thread """


class BaseThread(QThread):

    Type                                = 'DAMGTHREAD'
    _key                                = 'BaseThread'
    _name                               = 'DAMG Thread'
    _count                              = 0
    _copyright                          = __copyright__()
    _data                               = dict()

    def __init__(self, *args, **kwargs):
        QThread.__init__(self)

        self.args = args
        self.kwargs = kwargs

    def run(self):

        pass

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

    def count_notified_change(self, val):
        self._count                         = val

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
""" ThreadPool """


class BaseThreadPool(QThreadPool):

    Type                                    = 'DAMGTHREADPOOL'
    key                                     = 'BaseThreadPool'
    _name                                   = 'DAMG Thread Pool'
    _count                                  = 0
    _copyright                              = __copyright__()
    _data                                   = dict()

    workers = []
    threads = []

    def __init__(self, parent=None):
        QThreadPool.__init__(self)

        self.parent                         = parent

    def __str__(self):
        """ Print object will return qssPths string """
        return json.dumps(self.data, cls=ObjectEncoder, indent=4, sort_keys=True)

    def __repr__(self):
        """ Print object ill return json qssPths type """
        return json.dumps(self.data, cls=ObjectEncoder, indent=4, sort_keys=True)

    def process_output(self, val):
        return print(val)

    def progress_task(self, val):
        return print('{0}% done'.format(val))

    def task_completed(self, worker):
        self.workers.remove(worker)
        return print('worker commpleted')

    def stop_thread(self, thread):
        thread.quit_thread.emit()
        return print('thread stopes')

    def error_output(self, errorTuple):
        return print(errorTuple)

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
# Created by panda on 1/17/2020 - 12:16 AM
# © 2017 - 2019 DAMGteam. All rights reserved