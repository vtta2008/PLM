# -*- coding: utf-8 -*-
"""

Script Name: models.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
# Python
import time
import datetime
import re

# PLM
from .base                                  import (BaseDict, BaseObject, BaseWorker, BaseThread, BaseThreadPool,
                                                    BaseError, BaseTuple, BaseList)

# -------------------------------------------------------------------------------------------------------------
""" Registry """


STEP                                        = 1
START                                       = 0


class DAMGREGISTER(BaseDict):
    """
    This is the class to manage all of DAMG object type.
    Whenever a DAMGobject is create, it will be registerd to this class with metadata info.
    """

    key                                     = 'DAMGREGISTER'
    Type                                    = 'DAMGREGISTER'

    _count                                  = START
    _step                                   = STEP

    object_types                             = ['DAMGOBJECT', 'DAMGDICT', 'DAMGLIST', 'DAMGWORKER', 'DAMGTHREAD',
                                                'DAMGPOOL', 'DAMGERROR', ]

    object_names                            = list()
    object_ids                              = list()
    object_datetimes                        = list()
    object_keys                             = list()
    awaitingSlots                           = list()

    def __init__(self):
        dict.__init__(self)

        # Counting base on object type via object.Type
        self._DAMGcount                     = 0
        self._DICTcount                     = 0
        self._ERRORcount                    = 0
        self._LISTcount                     = 0
        self._WORKERcount                   = 0
        self._THREADcount                   = 0
        self._POOLcount                     = 0
        self._TUPLEcount                    = 0

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

        # Register object to qssPths
        self.object_names.append(obj.data['ObjectName'])
        self.object_ids.append(obj.data['ObjectID'])
        self.object_datetimes.append(obj.data['Datetime'])
        self.object_keys.append(obj.data['key'])

        self[obj._name] = [obj.data, obj]

        # Report register complete.
        # print('{0} registed'.format(obj.name))
        return True

    def deRegister(self, obj):
        """ Remove/unregister obj from qssPths """

        if self.isTypeRegisted(obj):
            self.object_types.remove(obj.Type)

        if self.isRegisted(obj._name):
            # Remember empty slot before remove object
            # will be used when other obj has same name, or register again.
            if not self.isAwaitingSlot(obj._name):
                self.awaitingSlots.append(obj._name)
            # Remove object from qssPths
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
        obj._data['key'] = obj.key
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
    def DATEcount(self):
        return self._DATEcount

    @property
    def DATETIMEcount(self):
        return self._DATETIMEcount

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

    @DATEcount.setter
    def DATEcount(self, newVal):
        self._DATEcount                     = newVal

    @DATETIMEcount.setter
    def DATETIMEcount(self, newVal):
        self._DATETIMEcount                 = newVal


objRegistry = DAMGREGISTER()


# -------------------------------------------------------------------------------------------------------------
""" List """


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


# -------------------------------------------------------------------------------------------------------------
""" Dict """


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


# -------------------------------------------------------------------------------------------------------------
""" Tuple """


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
""" Error """


class DAMGERROR(BaseError):

    """ Base Damg team object. """

    key                                     = 'DAMGERROR'

    def __init__(self, parent=None, **kwargs):
        BaseError.__init__(self)

        self._parent                        = parent
        objRegistry.register(self)


# -------------------------------------------------------------------------------------------------------------
""" Object """


class DAMG(BaseObject):

    """ Base Damg team object. """

    key                                     = "DAMG"

    def __init__(self, parent=None, **kwargs):
        super(DAMG, self).__init__()

        self._parent                        = parent
        objRegistry.register(self)



# -------------------------------------------------------------------------------------------------------------
""" Worker """


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



# -------------------------------------------------------------------------------------------------------------
""" Thread """


class DAMGTHREAD(BaseThread):

    key                                     = 'DAMGTHREAD'

    def __init__(self, task):
        super(DAMGTHREAD, self).__init__()

        self.task = task

        objRegistry.register(self)


# -------------------------------------------------------------------------------------------------------------
""" ThreadPool """


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

    def execute_task(self, task, args, worker=True):

        if worker:
            worker = self.create_worker(task, args)
            return self.start(worker)
        else:
            thread = self.create_thread(task)
            return thread.start()

    def execute_multi_tasks(self, tasks):
        for task in tasks:
            self.tasks.append(task)
            self.execute_task(task)

    def create_worker(self, task, args):
        worker = DAMGWORKER(task, args)
        self.workers.append(worker)
        return worker

    def create_thread(self, task):
        thread = DAMGTHREAD(task)
        self.threads.append(thread)
        return thread


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/17/2020 - 12:32 AM
# © 2017 - 2019 DAMGteam. All rights reserved