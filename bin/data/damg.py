# -*- coding: utf-8 -*-
"""

Script Name: base.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys, json, inspect, time, datetime, traceback, re
from functools import partial

# PyQt5
from PyQt5.QtCore   import pyqtSignal, pyqtSlot, QObject, pyqtProperty, QThreadPool, QThread, QRunnable, QTimer

__copyright__   = "Copyright (c) 2017 - 2019 Trinh Do & Duong Minh Duc"

# -------------------------------------------------------------------------------------------------------------
STEP = 1
START = 0

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
    def stations(self, val):
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
class BaseDict(dict):

    Type                                = 'DAMGDICT'
    key                                 = 'BaseDict'
    _name                               = 'DAMG dict'
    _count                              = 0
    _copyright                          = __copyright__
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

    def input(self, data={}):
        if data == {}:
            self.clear()
        else:
            for k, v in data.items():
                self.add(k, v)


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
class BaseTuple(tuple):

    Type                                = 'DAMGTUPLE'
    key                                 = 'BaseTuple'
    _name                               = 'DAMG Base Tuple'
    _data                               = dict()
    __count                             = 0
    _copyright                          = __copyright__

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
class BaseError(Exception):

    Type                                = 'DAMGERROR'
    key                                 = 'BaseError'
    _name                               = 'DAMG error'
    _count                              = 0
    _data                               = dict()
    _copyright                          = __copyright__

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

# -------------------------------------------------------------------------------------------------------------
class TypeObjectError(BaseError):
    """ When object.Type is not recognisable """

# -------------------------------------------------------------------------------------------------------------
class DamgWorkerSignals(BaseObject):

    key                                     = 'DamgWorkerSignals'
    Type                                    = 'DAMGWORKERSIGNAL'
    _name                                   = 'DAMG Worker Signal'

    finished                                = pyqtSignal(object)
    error                                   = pyqtSignal(tuple)
    result                                  = pyqtSignal(object)
    progress                                = pyqtSignal(int)

    def __init__(self, parent=None):
        BaseObject.__init__(self)

        self.parent                         = parent
        objRegistry.register(self)

# -------------------------------------------------------------------------------------------------------------
class BaseWorker(QRunnable):

    Type                                    = 'DAMGWORKER'
    key                                     = 'BaseWorker'
    _name                                   = 'DAMG Worker'
    _count                                  = 0
    _copyright                              = __copyright__
    _data                                   = dict()

    def __init__(self, task, *args, **kwargs):
        QRunnable.__init__(self)

        self.task                           = task            # Store constructor arguments (re-used for processing)
        self.args                           = args
        self.kwargs                         = kwargs
        self.signals                        = DamgWorkerSignals()

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
            result = self.task(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)                                    # Return the result of the processing
        finally:
            self.signals.finished.emit(self)                                        # Done

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
class BaseThread(QThread):

    Type                                = 'DAMGTHREAD'
    _key                                = 'BaseThread'
    _name                               = 'DAMG Thread'
    _count                              = 0
    _copyright                          = __copyright__
    _data                               = dict()

    quit_thread                         = pyqtSignal(name='close_thread')

    def __init__(self, *args, **kwargs):
        QThread.__init__(self)

        self.args = args
        self.kwargs = kwargs

    def run(self):

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
class BaseThreadPool(QThreadPool):

    Type                                    = 'DAMGTHREADPOOL'
    key                                     = 'BaseThreadPool'
    _name                                   = 'DAMG Thread Pool'
    _count                                  = 0
    _copyright                              = __copyright__
    _data                                   = dict()

    workers = []
    threads = []

    def __init__(self):
        QThreadPool.__init__(self)

    def __str__(self):
        """ Print object will return data string """
        return json.dumps(self.data, cls=ObjectEncoder, indent=4, sort_keys=True)

    def __repr__(self):
        """ Print object ill return json data type """
        return json.dumps(self.data, cls=ObjectEncoder, indent=4, sort_keys=True)

    @pyqtSlot(object)
    def process_output(self, val):
        return print(val)

    @pyqtSlot(int)
    def progress_task(self, val):
        return print('{0}% done'.format(val))

    @pyqtSlot(object)
    def task_completed(self, worker):
        self.workers.remove(worker)
        return print('worker commpleted')

    def create_worker(self, task):
        worker = DAMGWORKER(task)
        worker.signals.result.connect(self.process_output)
        worker.signals.progress.connect(self.progress_task)
        worker.signals.finished.connect(partial(self.task_completed, worker))
        self.workers.append(worker)
        return worker

    def create_thread(self, task):
        thread = DAMGTHREAD(task)
        thread.quit_thread.connect()
        self.threads.append(thread)
        return thread

    def stop_thread(self, thread):
        thread.quit_thread.emit()
        return print('thread stopes')

    @pyqtSlot(tuple)
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
class BaseTimer(QTimer):

    Type                            = 'DAMGTIMER'
    key                             = 'BaseTimer'
    _name                           = 'DAMG Timer'
    _count                          = 0
    _copyright                      = __copyright__
    _data                           = dict()

    def __init__(self):
        QTimer.__init__(self)

    def __str__(self):
        """ Print object will return data string """
        return json.dumps(self.data, cls=ObjectEncoder, indent=4, sort_keys=True)

    def __repr__(self):
        """ Print object ill return json data type """
        return json.dumps(self.data, cls=ObjectEncoder, indent=4, sort_keys=True)

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
class DAMGREGISTER(BaseDict):
    """
    This is the class to manage all of DAMG object type.
    Whenever a DAMGobject is create, it will be registerd to this class with metadata info.
    """

    key                                     = 'DAMGREGISTER'
    Type                                    = 'DAMGREGISTER'

    _count                                  = START
    _step                                   = STEP

    object_types                             = ['DAMGOBJECT', 'DAMGDICT', 'DAMGLIST', 'DAMGWORKER',
                                                'DAMGWORKERSIGNAL', 'DAMGTHREAD', 'DAMGPOOL', 'DAMGERROR',
                                                'DAMGTIMER', ]

    object_names                            = list()
    object_ids                              = list()
    object_datetimes                        = list()
    awaitingSlots                           = list()

    def __init__(self):
        dict.__init__(self)

        # Counting base on object type via object.Type
        self._DAMGcount                     = 0
        self._DICTcount                     = 0
        self._ERRORcount                    = 0
        self._LISTcount                     = 0
        self._SIGNALcount                   = 0
        self._WORKERcount                   = 0
        self._THREADcount                   = 0
        self._POOLcount                     = 0
        self._TUPLEcount                    = 0
        self._TIMERcount                    = 0

    def register(self, obj):
        """ Conduct register for object """
        # Check obj.Type, if not, create one
        if not self.isTypeRegisted(obj):
            self.object_types.append(obj.Type)

        # Start counting
        self.isCountable(obj)

        obj._count = self.stepUp(obj)

        # Update object name
        obj._name = '{0} {1}'.format(obj._name, obj._count)

        # Check empty slot
        if self.isAwaitingSlot(obj._name):
            # Register object to database
            self.awaitingSlots.remove(obj._name)
            self.doRegister(obj)
        else:
            # Check if object name is registed:
            if self.isRegisted(obj):
                # Restart the register procedural
                self.register(obj)
            else:
                # Register object to database
                self.doRegister(obj)

    def doRegister(self, obj):
        """ Register object to DAMGREGISTER """

        # Create object profile
        obj = self.generate_obj_profiles(obj)

        # Register object to data
        self.object_names.append(obj.data['ObjectName'])
        self.object_ids.append(obj.data['ObjectID'])
        self.object_datetimes.append(obj.data['Datetime'])

        self[obj._name] = [obj.data, obj]

        # Report register complete.
        # print('{0} registed'.format(obj.name))
        return True

    def deRegister(self, obj):
        """ Remove/unregister obj from data """

        if self.isTypeRegisted(obj):
            self.object_types.remove(obj.Type)

        if self.isRegisted(obj._name):
            # Remember empty slot before remove object
            # will be used when other obj has same name, or register again.
            if not self.isAwaitingSlot(obj._name):
                self.awaitingSlots.append(obj._name)
            # Remove object from data
            try:
                del self[obj._name]
            except KeyError:
                self.pop(obj._name, None)
            return True
        else:
            return False

    def generate_obj_profiles(self, obj):
        """ Generate object profile """
        obj._data['ObjectName'] = obj._name
        obj._data['ObjectID'] = id(obj)
        obj._data['Datetime'] = str(datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S|%d.%m.%Y'))
        return obj

    def stepUp(self, obj):
        """ Counting if object is registered """

        # for DAMG class
        if obj.Type == 'DAMGOBJECT':
            self._DAMGcount += self._step
            obj._count      = self._DAMGcount
        # for DAMGDICT class
        elif obj.Type == 'DAMGDICT':
            self._DICTcount += self._step
            obj._count = self._DICTcount
        # for DAMGLIST class
        elif obj.Type == 'DAMGLIST':
            self._LISTcount += self._step
            obj._count = self._LISTcount
        # for DAMGWORKERSIGNAL class
        elif obj.Type == 'DAMGWORKERSIGNAL':
            self._SIGNALcount += self._step
            obj._count = self._SIGNALcount
        # for DAMGWORKER class
        elif obj.Type == 'DAMGWORKER':
            self._WORKERcount += self._step
            obj._count = self._WORKERcount
        # for DAMGTHREAD clas
        elif obj.Type == 'DAMGTHREAD':
            self._THREADcount += self._step
            obj._count = self._THREADcount
        # for DAMGTHREADPOOL class
        elif obj.Type == 'DAMGTHREADPOOL':
            self._POOLcount += self._step
            obj._count = self._POOLcount
        # for DAMGTUPLE class
        elif obj.Type == 'DAMGTUPLE':
            self._TUPLEcount += self._step
            obj.__count = self._TUPLEcount
        elif obj.Type == 'DAMGTIMER':
            self._TIMERcount += self._step
            obj._count = self._TIMERcount
        else:
            # for DAMGERROR class
            self._ERRORcount += self._step
            obj._count = self._ERRORcount

        return obj._count

    def isAwaitingSlot(self, objName):
        """ Check if object name is in empty slot list """
        if objName in self.awaitingSlots:
            return True
        else:
            return False

    def isTyped(self, obj):
        try:
            obj.Type
        except AttributeError:
            return False
        else:
            return True

    def isTypeRegisted(self, obj):
        """ Fix obj.Type attribute obj, and check obj.Type registered """

        # Fix obj.Type attribute
        if not self.isTyped(obj):
            obj.__setattr__('Type', obj.__class__.__name__)

        # Check if obj.Type is registered/
        if not obj.Type in self.object_types:
            return False
        else:
            return True

    def isNamed(self, obj):
        try:
            obj._name
        except AttributeError:
            return False
        else:
            return True

    def isRegisted(self, obj):
        """ Check obj name is registered. """

        # Check have name
        if not self.isNamed(obj):
            obj.__setattr__('_name', obj.__class__.__name__)

        objName = obj._name

        if objName in self.keys():
            return True
        else:
            return False

    def isCounted(self, obj):
        try:
            obj._count
        except AttributeError:
            return False
        else:
            return True

    def isCountable(self, obj):
        if not self.isCounted(obj):
            obj.__setatt__('_count', 0)
            return False
        else:
            return True

    @property
    def DAMGcount(self):
        return self._DAMGcount

    @property
    def DICTcount(self):
        return self._DICTcount

    @property
    def ERRORcount(self):
        return self._ERRORcount

    @property
    def LISTcount(self):
        return self._LISTcount

    @property
    def SIGNALcount(self):
        return self._SIGNALcount

    @property
    def WOKERcount(self):
        return self._WORKERcount

    @property
    def THREADcount(self):
        return self._THREADcount

    @property
    def POOLcount(self):
        return self._POOLcount

    @property
    def TUPLEcount(self):
        return self._TUPLEcount

    @property
    def TIMMERcount(self):
        return self._TIMERcount

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, newVal):
        self._step                          = newVal

    @TUPLEcount.setter
    def TUPLEcount(self, newVal):
        self._TUPLEcount                    = newVal

    @DAMGcount.setter
    def DAMGcount(self, newVal):
        self._DAMGcountcount                = newVal

    @DICTcount.setter
    def DICTcount(self, newVal):
        self._DICTcount                     = newVal

    @ERRORcount.setter
    def ERRORcount(self, newVal):
        self._ERRORcount                    = newVal

    @LISTcount.setter
    def LISTcount(self, newVal):
        self._LISTcount                     = newVal

    @SIGNALcount.setter
    def SIGNALcount(self, newVal):
        self._SIGNALcount                   = newVal

    @WOKERcount.setter
    def WOKERcount(self, newVal):
        self._WORKERcount                   = newVal

    @THREADcount.setter
    def THREADcount(self, newVal):
        self._THREADcount                   = newVal

    @POOLcount.setter
    def POOLcount(self, newVal):
        self._POOLcount                     = newVal

    @TIMMERcount.setter
    def TIMMERcount(self, newVal):
        self._TIMERcount                    = newVal

objRegistry = DAMGREGISTER()

# -------------------------------------------------------------------------------------------------------------
class DAMG(BaseObject):

    """ Base Damg team object. """

    key                                     = "DAMG"

    def __init__(self, parent=None, **kwargs):
        super(DAMG, self).__init__()

        self._parent                        = parent
        objRegistry.register(self)

class DAMGERROR(BaseError):

    """ Base Damg team object. """

    key                                     = 'DAMGERROR'

    def __init__(self, parent=None, **kwargs):
        BaseError.__init__(self)

        self._parent                        = parent
        objRegistry.register(self)

class DAMGLIST(BaseList):

    """ Base Damg team dictionary """

    key                                     = 'DAMGLIST'

    def __init__(self, listData=[], parent=None):
        BaseList.__init__(self)

        self._parent                        = parent
        self.listData                       = listData
        self.appendList(listData)
        objRegistry.register(self)

    def appendList(self, lst=[]):
        if len(lst) > 0:
            for i in lst:
                self.append(i)

class DAMGDICT(BaseDict):

    """ Base Damg team dictionary """

    key                                     = 'DAMGDICT'

    def __init__(self, dictData={}, parent=None):
        BaseDict.__init__(self)

        self._parent                        = parent
        self.dictData                       = dictData
        self.appendDict(self.dictData)
        objRegistry.register(self)

    def appendDict(self, dct={}):
        if not dct == {}:
            for key, value in dct.items():
                self.add(key, value)

class DAMGTUPLE(BaseTuple):

    key                                 = 'DAMGTUPLE'

    def __init__(self, *args, **kwargs):
        BaseTuple.__new__(self)

        self.metadata = kwargs
        self.args = args
        objRegistry.register(self)

    def parse(self, pattern):
        return re.search(pattern, self.metadata).group(1).replace('"', '').strip()

# -------------------------------------------------------------------------------------------------------------
""" Worker & Thread """

class DAMGWORKER(BaseWorker):

    key                                     = 'DAMGWORKER'

    def __init__(self, task=None, *args, **kwargs):
        super(DAMGWORKER, self).__init__(task)

        self.args                           = args
        self.kwargs                         = kwargs
        self.task                           = task

        if not self.task or self.task is None:
            print("TaskErrorWorker: {0} at {1} : task should be specific type, not {2}".format(self.__class__.__name__, __file__, type(self.task)))

        objRegistry.register(self)

class DAMGTHREAD(BaseThread):

    key                                     = 'DAMGTHREAD'

    def __init__(self, task):
        super(DAMGTHREAD, self).__init__()

        self.task = task

        objRegistry.register(self)

class DAMGTHREADPOOL(BaseThreadPool):

    key                                     = 'DAMGTHREADPOOL'
    workers                                 = DAMGLIST()
    threads                                 = DAMGLIST()

    def __init__(self):
        BaseThreadPool.__init__(self)

        objRegistry.register(self)

    def test_task(self, progres_callback):
        for n in range(0, 5):
            time.sleep(1)
            progres_callback.emit(n*100/4)
        return 'Done.'

    def run_test(self):
        return self.execute_task(self.test_task)

    def execute_task(self, task, thread=False, worker=True):

        if worker:
            worker = self.create_worker(task)
            return self.start(worker)
        else:
            thread = self.create_thread(task)
            return thread.start()

    def execute_multi_tasks(self, tasks):
        for task in tasks:
            self.tasks.append(task)
            self.execute_task(task)

# -------------------------------------------------------------------------------------------------------------
""" Timer """

class DAMGTIMER(BaseTimer):

    key                                     = 'DAMGTIMER'

    def __init__(self):
        BaseTimer.__init__(self)

        objRegistry.register(self)

if __name__ == '__main__':

    a = DAMG()
    b = DAMGERROR()
    c = DAMGLIST()
    d = DAMGDICT()
    e = DAMGWORKER('Your_task')
    f = DAMGTHREAD('My_task')
    g = DAMGTHREADPOOL()
    h = DamgWorkerSignals()
    i = DAMGTUPLE(['a', 'b', 'c'])
    j = DAMGTIMER()
#
#     print(a, b, c, d, e, f, g, h, i, j)

    from pprint import pprint
    pprint(objRegistry)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 21/10/2019 - 3:06 AM
# © 2017 - 2018 DAMGteam. All rights reserved