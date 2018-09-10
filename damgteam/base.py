# -*- coding: utf-8 -*-
"""

Script Name: types.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, division, print_function, unicode_literals


# Python
import os, json, yaml, inspect, uuid


# PyQt5
from PyQt5.QtCore import Qt, QDate, QTime, QDateTime


# -------------------------------------------------------------------------------------------------------------
""" Debug class """


class ObjectEncoder(json.JSONEncoder):

    def default(self, obj):
        if hasattr(obj, 'to_json'):
            return self.default(obj.to_json())
        elif hasattr(obj, '__dict__'):
            d = dict(
                (key, value)
                for key, value in inspect.getmembers(obj)
                if not key.startswith('__')
                and not inspect.isabstract(value)
                and not inspect.isbuiltin(value)
                and not inspect.isfunction(value)
                and not inspect.isgenerator(value)
                and not inspect.isgeneratorfunction(value)
                and not inspect.ismethod(value)
                and not inspect.ismethoddescriptor(value)
                and not inspect.isroutine(value)
            )
            return self.default(d)
        return obj


class Iterator(object):

    def __init__(self, sorted_dict):
        self._dict = sorted_dict
        self._keys = sorted(self._dict.keys())
        self._nr_items = len(self._keys)
        self._idx = 0

    def __iter__(self):
        return self

    def next(self):
        if self._idx >= self._nr_items:
            raise StopIteration

        key = self._keys[self._idx]
        value = self._dict[key]
        self._idx += 1

        return key, value

    __next__ = next


# -------------------------------------------------------------------------------------------------------------
""" Identification """


class NAME(object):

    """ Object name """

    def generateName(self, cls=None):
        if cls is None:
            key                             = self.__class__.__name__
        else:
            key                             = cls.__class__.__name__

        return str('DAMG {0}'.format(key.lower()))


class OID(object):

    """ Object ID """

    def __init__(self):
        super(OID, self).__init__()

        self._oids                          = list()
        self._count                         = 1

    def register(self, oid):
        if oid not in self._oids:
            self._oids.append(oid)
            print('oid: {0} has been registered'.format(oid))

    def deregister(self, oid):
        if oid in self._oids:
            self._oids.remove(oid)
            print('oid: {0} has been removed'.format(oid))

    def registerable(self, oid):
        if oid not in self._oids:
            return True
        else:
            return False

    def generatePrefix(self, key):
        keyID = key.upper()
        if len(keyID)==1:
            return '{0}ID'.format(keyID)
        elif len(keyID) == 2:
            return 'O{0}'.format(keyID)
        elif len(keyID) == 3:
            return keyID
        elif len(keyID) == 4:
            if keyID == 'DAMG':
                return 'OBJ'
            else:
                return '{0}{1}S'.format(keyID[0], keyID[-1])
        elif len(keyID) == 5:
            return '{0}{1}{2}'.format(keyID[0], keyID[2], keyID[4])
        else:
            if keyID[-3:] == 'DAY':
                return keyID[:3]
            elif keyID[:4] == 'DAMG':
                return keyID[4:7]
            elif keyID[:7] == 'CONFIGS':
                return '{0}{1}S'.format(keyID[0], keyID[3])
            elif keyID[:6] == 'CONFIG' and 'PATH' in keyID:
                return '{0}{1}P'.format(keyID[0], keyID[3])
            elif 'DATE' in keyID and 'TIME' in keyID:
                return '{0}{1}{2}'.format(keyID[0], keyID[2], keyID[-2])
            else:
                return '{0}{1}{2}'.format(keyID[0], keyID[1], keyID[-1])

    def generateSubfix(self, prefix):

        matchs = []
        for oid in self._oids:
            if prefix in oid:
                matchs.append(oid)

        self._count                         = len(matchs) + 1

        tempSubfix                          = str(self._count).zfill(3)
        tempOid                             = '{0}.{1}'.format(prefix, tempSubfix)

        self._count                        += 1

        if self.registerable(tempOid):
            self.register(tempOid)
            return tempSubfix
        else:
            self.generateSubfix(prefix)

    def generateOID(self, cls):

        if cls is None:
            key                             = self.__class__.__name__
        else:
            key                             = cls.__class__.__name__

        prefix                              = self.generatePrefix(key)
        subfix                              = self.generateSubfix(prefix)

        self._oid                           = str('{0}.{1}'.format(prefix, subfix))
        self.dictID                         = '{0}.dict'.format(self._oid)
        self.Type                           = '{0} Object'.format(self._oid)
        self.__oid__                        = self._oid
        self.__type__                       = self.Type

        print('Created new id: {0}'.format(self._oid))
        return self._oid

    @property
    def oids(self):
        return self._oids

    @property
    def count(self):
        return self._count

    @oids.setter
    def oids(self, newLst):
        self._oids = newLst

    @count.setter
    def count(self, value):
        self._count = value


namesObj = NAME()
oidsObj = OID()


def IID(obj):

    """
    Return the identity of an object.

    This is guaranteed to be unique among simultaneously existing objects.
    (CPython uses the object's memory address.)

    """

    return id(obj)


def UID():

    """ Unique ID """

    return uuid.uuid4()


def get_datetime(mode='long'):

    """ Today and current time """

    if mode == 'long':
        return QDateTime.currentDateTime().toString(Qt.DefaultLocaleLongDate).replace(', ', '_').replace(' ', '_')
    else:
        return QDateTime.currentDateTime().toString(Qt.DefaultLocaleShortDate).replace(', ', '_').replace(' ', '_')


# -------------------------------------------------------------------------------------------------------------
""" Base object """


class DAMGERROR(Exception):
    """ Common subclass for all DAMG exceptions """


class DAMG(object):
    """
    Base Damg team object.

    """

    _copyright                              = 'This is an asset of DAMGTEAM'                # Copyright
    _data                                   = dict()
    __dict__                                = dict()

    def __init__(self, oid=None, name=None):
        super(DAMG, self).__init__()


        if name is None:
            self._name                      = namesObj.generateName(self)
        else:
            self._name                      = name

        if oid is None:
            self._oid                       = oidsObj.generateOID(self)
        else:
            self._oid                       = oid

        self._iid                           = IID(self)
        self._uid                           = UID()
        self._metadatetime                  = get_datetime()

        self.Type                           = '{0} Object'.format(self._name)
        self._metadata                      = '({0}).({1}).({2}).({3})'.format(self._oid, self._iid, self._uid, self._metadatetime)

        self.__name__                       = self._name
        self.__metadata__                   = self._metadata
        self.__type__                       = self.Type

        self.initialize()

    def __str__(self):

        """ Print object ill return json data type """

        return json.dumps({self._name: self.data}, cls=ObjectEncoder, indent=4, sort_keys=True)

    def __repr__(self):

        """ Print object ill return json data type """

        return json.dumps({self._name: self.data}, cls=ObjectEncoder, indent=4, sort_keys=True)

    def __call__(self):

        """ Make object callable """

        if isinstance(self, object):
            return True
        else:
            return False

    def initialize(self):

        """ Store data into __dict__ """

        for key, value in self._data.items():
            if not key in ['oid', 'iid', 'uid', 'metadatetime', 'name', 'type', 'copyright']:
                self.__dict__[key]          = value

    def to_json(self):

        """ Debug json serizalable error. """

        return {self.__class__.__name__: 'YES'}

    def to_dict(self):

        """ Return the data as a normal dict """

        return self.__dict__

    @property
    def data(self):

        self._data['name']                  = self._name
        self._data['type']                  = self.Type
        self._data['copyright']             = self._copyright
        self._data['metadata']              = self._metadata

        return self._data

    @property
    def oid(self):
        return self._oid.__oid__

    @property
    def iid(self):
        return self._iid

    @property
    def uid(self):
        return self._uid

    @property
    def metadatetime(self):
        return self._metadatetime

    @property
    def name(self):
        return self._name.__name__

    @property
    def type(self):
        return self.Type

    @property
    def copyright(self):
        return self._copyright

    @property
    def metadata(self):
        return self._metadata

    @data.setter
    def data(self, newdata):
        self._data                          = newdata

    @oid.setter
    def oid(self, newOID):
        self._oid                           = newOID

    @iid.setter
    def iid(self, newIID):
        self._iid                           = newIID

    @uid.setter
    def uid(self, newUID):
        self._uid                           = newUID

    @metadatetime.setter
    def metadatetime(self, newMetadatetime):
        self._metadatetime                  = newMetadatetime

    @name.setter
    def name(self, newname):
        self._name                          = newname

    @type.setter
    def type(self, newType):
        self.Type                           = newType

    @copyright.setter
    def copyright(self, newCopyright):
        self._copyright                     = newCopyright

    @metadata.setter
    def metadata(self, newMetadata):
        self._metadata                      = newMetadata

    __copyright__                           = _copyright


# -------------------------------------------------------------------------------------------------------------
""" Variables """


class DAMGVARIABLES(DAMG):

    shortCopyright                              = 'This is an asset of DAMGTEAM'                # Copyright
    indent                                      = 4                                             # Json setting
    sortKeys                                    = True                                          # Json setting

    fmtl                                        = Qt.DefaultLocaleLongDate
    fmts                                        = Qt.DefaultLocaleShortDate


damgvar = DAMGVARIABLES()


# -------------------------------------------------------------------------------------------------------------
""" Datatypes: dict & list """


class DAMGDICT(dict):                                                           # Dict
    """
    New stylist dictionary class by DAMGTEAM.
    A customised dictionary with name, id and much more extra functions.
    Dictionary now will be able to manage and identify very easily.
    """

    _data                                       = dict()
    _details                                    = dict()
    _copyright                                  = damgvar.shortCopyright

    def __init__(self, oid=None, name=None, **kwargs):
        """
        Basic initialize to create identification data of object
        """

        super(DAMGDICT, self).__init__(self)

        if oid is None:
            self._oid                           = oidsObj.generateOID(self)
        else:
            self._oid                           = oid

        if name is None:
            self._name                          = namesObj.generateName(self)
        else:
            self._name                          = name

        self._iid                               = IID(self)
        self._uid                               = UID()
        self._metadatetime                      = get_datetime()

        self.Type                               = '{0} Object'.format(self._name)
        self._metadata                          = '({0}).({1}).({2}).({3})'.format(self._oid, self._iid, self._uid, self._metadatetime)

        self.__name__                           = self._name
        self.__metadata__                       = self._metadata
        self.__type__                           = self.Type

        self._kwargs = kwargs

        if len(self.keys()) > 0:
            for key, value in self.items():
                self.__dict__[key] = value
        else:
            if self._kwargs:
                if len(self._kwargs.keys()) > 0:
                    for key, value in self._kwargs.items():

                        if key in self.keys():
                            newkey = '{0}_(new add)'.format(key)
                        else:
                            newkey = key

                        self.add_item(newkey, value)

        self.initialize()

    def __iter__(self):
        """ Make object iterable """
        return Iterator(self)

    iterkeys = __iter__

    def __str__(self):
        """ Print object will return data string """
        return json.dumps({self._name: self.data}, cls=ObjectEncoder, indent=damgvar.indent, sort_keys=damgvar.sortKeys)

    def __repr__(self):
        return json.dumps({self._name: self.data}, cls=ObjectEncoder, indent=damgvar.indent, sort_keys=damgvar.sortKeys)

    def initialize(self):
        """ Store data into __dict__ """
        for key, value in self._data.items():
            if not key in ['oid', 'iid', 'uid', 'metadatetime', 'name', 'type', 'copyright']:
                self.__dict__[key]          = value

    def to_json(self):
        """ Debug json serizalable error. """
        return {self.__class__.__name__: 'YES'}

    def to_dict(self):
        return self.__dict__

    @property
    def data(self):

        self._data['metadata']              = self._metadata
        self._data['name']                  = self._name
        self._data['type']                  = self.Type
        self._data['copyright']             = self._copyright

        return self._data

    @property
    def oid(self):
        return self._oid

    @property
    def iid(self):
        return self._iid

    @property
    def uid(self):
        return self._uid

    @property
    def metadatetime(self):
        return self._metadatetime

    @property
    def name(self):
        return self._name.__name__

    @property
    def type(self):
        return self.Type

    @property
    def copyright(self):
        return self._copyright

    @property
    def metadata(self):
        return self._metadata

    @data.setter
    def data(self, newdata):
        self._data                          = newdata

    @oid.setter
    def oid(self, newOID):
        self._oid                           = newOID

    @iid.setter
    def iid(self, newIID):
        self._iid                           = newIID

    @uid.setter
    def uid(self, newUID):
        self._uid                           = newUID

    @metadatetime.setter
    def metadatetime(self, newMetadatetime):
        self._metadatetime                  = newMetadatetime

    @name.setter
    def name(self, newname):
        self._name                          = newname

    @type.setter
    def type(self, newType):
        self.Type                           = newType

    @copyright.setter
    def copyright(self, newCopyright):
        self._copyright                     = newCopyright

    @metadata.setter
    def metadata(self, newMetadata):
        self._metadata                      = newMetadata

    def add_item(self, key, value=None):
        """ Create new item of dict, requires key and value, if not value defined, set value to None """
        if key is None:
            raise KeyError('Please define a valid key')
        else:
            self[key] = value
            self._data[key] = value
            return True

    def get_item(self, key):
        """ Get value from key """
        if self.check_key(key):
            return self[key]
        else:
            raise KeyError('Please define a valid key')

    def remove_item(self, key):
        """ Delete item from dict """
        try:
            del self[key]
            print('key deleted: {key}'.format(key=key))
        except KeyError:
            self.pop(key, None)
            print('key poped: {key}'.format(key=key))
        finally:
            self.pop(key)
            return True

    def edit_item(self, key, value=None):
        """ Edit value of dict """

        if key in self.keys():

            oldValue = self[key]

            if oldValue == value:
                raise ValueError('Can not edit new value because it is the same as current value.')
            else:
                self[key] = value
                print('Edited {0} = {1}'.format(key, value))
                return True
        else:
            print(KeyError('Key is not exsisted.'))
            return False

    def find_item(self, keyword):
        """ Find matching key, value, etc., from dict if match with keyword """

        findOut = []

        for key, value in self.items():
            if keyword in key and keyword not in value:
                item = '{0} = {1}'.format(str(key), str(value))
                findOut.append(item)
            elif keyword in key and keyword in value:
                item = '{0} = {1}'.format(str(key), str(value))
                findOut.append(item)
            elif keyword not in key and keyword in value:
                item = '{0} = {1}'.format(str(key), str(value))
                findOut.append(item)

        return findOut

    def find_key(self, value):
        """ Find key from value. """

        if value in self.values():
            for key, value in self.items():
                if value == value:
                    return key
        else:
            raise ValueError('This value is not in current dict: (id: {0}, name: {1})'.format(self._oid, self._name))

    def check_key(self, key):
        """ Check if key exists in dict """

        for k in self.keys():
            if k == key:
                return True
        return False

    def add_data(self, filename, fmt='json'):
        """
        Load dict data from a file.
        Read file using format json or yaml to get preset dict, then add new data to current dict.
        If key convention, will keep both key and mark the new key.

        """

        if os.path.exists(filename):

            with open(filename, 'r') as f:

                if fmt == 'json':
                    newData                 = json.load(f)
                else:
                    newData                 = yaml.load(f)

            for key, value in newData.items():

                if key in self.keys():
                    newkey                  = '{0}_(new add)'.format(key)
                else:
                    newkey                  = key

                self.add_item(newkey, value)

        else:
            raise ('There is no data in: {0}'.format(filename))

    def remove_data(self, filename, fmt='json'):
        """
        Remove dict data from a file.
        Read file using format json or yaml to get preset dict, then compare with current dict and remove
        match data.

        """
        if os.path.exists(filename):

            with open(filename, 'r') as f:

                if fmt == 'json':
                    removeData              = json.load(f)
                else:
                    removeData              = yaml.load(f)

            for key, value in removeData.items():

                if key in self.keys():
                    self.remove_item(key)
        else:
            raise ('There is no data in: {0}'.format(filename))

    def details(self):
        """ A quick styled resume context of the dict """

        self._details['dict id']            = self._oid
        self._details['dict name']          = self._name
        self._details['number_of_keys']     = len(self.keys())

        for key, value in self._details.items():
            print('key: {0} \nvalueType: {1} \nvalue: {2}\n'.format(key, type(value), value))

        if len(self.keys()) > 0:
            for key, value in self.items():
                print('key: {0} \nvalueType: {1} \nvalue: {2}\n'.format(key, type(value), value))

        return self._details

    __copyright__                           = _copyright


class DAMGLIST(list):                                                           # List

    _copyright                              = damgvar.shortCopyright
    _data                                   = dict()
    __dict__                                = dict()

    def __init__(self, oid=None, name=None, *args):
        super(DAMGLIST, self).__init__(list)

        if oid is None:
            self._oid                           = oidsObj.generateOID(self)
        else:
            self._oid                           = oid

        if name is None:
            self._name                          = namesObj.generateName(self)
        else:
            self._name                          = name

        self._iid                               = IID(self)
        self._uid                               = UID()
        self._metadatetime                      = get_datetime()

        self.Type                               = '{0} Object'.format(self._name)
        self._metadata                          = '({0}).({1}).({2}).({3})'.format(self._oid, self._iid, self._uid, self._metadatetime)

        self.__name__                           = self._name
        self.__metadata__                       = self._metadata
        self.__type__                           = self.Type

        self.args                               = args

        if self.args and len(self.args) > 0:
            for i in self.args:
                self.append(i)

        self.initialize()

    def __iter__(self):
        """ Make object iterable """
        return Iterator(self)

    iterkeys = __iter__

    def __str__(self):
        """ Print object will return data string """
        return json.dumps({self._name: self.data}, cls=ObjectEncoder, indent=damgvar.indent, sort_keys=damgvar.sortKeys)

    def __repr__(self):
        return json.dumps({self._name: self.data}, cls=ObjectEncoder, indent=damgvar.indent, sort_keys=damgvar.sortKeys)

    def initialize(self):
        """ Store data into __dict__ """
        for key, value in self._data.items():
            if not key in ['oid', 'iid', 'uid', 'metadatetime', 'name', 'type', 'copyright']:
                self.__dict__[key]          = value

    def to_json(self):
        """ Debug json serizalable error. """
        return {self.__class__.__name__: 'YES'}

    def to_dict(self):
        return self.__dict__

    @property
    def data(self):

        self._data.add_item('metadata'      , self._metadata)
        self._data.add_item('name'          , self._name)
        self._data.add_item('type'          , self.Type)
        self._data.add_item('copyright'     , self._copyright)

        return self._data

    @property
    def oid(self):
        return self._oid

    @property
    def iid(self):
        return self._iid

    @property
    def uid(self):
        return self._uid

    @property
    def metadatetime(self):
        return self._metadatetime

    @property
    def name(self):
        return self._name.__name__

    @property
    def type(self):
        return self.Type

    @property
    def copyright(self):
        return self._copyright

    @property
    def metadata(self):
        return self._metadata

    @data.setter
    def data(self, newdata):
        self._data                          = newdata

    @oid.setter
    def oid(self, newOID):
        self._oid                           = newOID

    @iid.setter
    def iid(self, newIID):
        self._iid                           = newIID

    @uid.setter
    def uid(self, newUID):
        self._uid                           = newUID

    @metadatetime.setter
    def metadatetime(self, newMetadatetime):
        self._metadatetime                  = newMetadatetime

    @name.setter
    def name(self, newname):
        self._name                          = newname

    @type.setter
    def type(self, newType):
        self.Type                           = newType

    @copyright.setter
    def copyright(self, newCopyright):
        self._copyright                     = newCopyright

    @metadata.setter
    def metadata(self, newMetadata):
        self._metadata                      = newMetadata

    __copyright__                           = _copyright

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 30/08/2018 - 8:18 PM
# © 2017 - 2018 DAMGteam. All rights reserved