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

# PLM
from .base                                  import (BaseDict, BaseError, BaseList)
from PLM.api.Core                           import BaseObject

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
    def step(self):
        return self._step

    @step.setter
    def step(self, newVal):
        self._step                          = newVal

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
# Created by panda on 1/17/2020 - 12:32 AM
# © 2017 - 2019 DAMGteam. All rights reserved