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

    _name_data                              = dict()

    def __init__(self, cls=None):
        super(NAME, self).__init__()


        if cls is None:
            key                             = self.__class__.__name__
        else:
            key                             = cls.__class__.__name__

        self.key                            = key
        self._name                          = self.generateName(self.key)
        self.Type                           = '{0} Object'.format(self._name)

        self.__name__                       = self._name
        self.__type__                       = self.Type

    def __str__(self):
        return self._name

    def __repr__(self):
        return self._name

    def __call__(self):

        if isinstance(self, object):
            return True
        else:
            return False

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name = newName

    def generateName(self, key):
        return str('DAMG {0}'.format(key.lower()))


class OID(object):

    ids                                     = dict()

    def __init__(self, cls=None):
        super(OID, self).__init__()

        if cls is None:
            key                             = self.__class__.__name__
        else:
            key                             = cls.__class__.__name__

        self.key                            = key
        self._oid                           = self.generateID(self.key)
        self.Type                           = '{0} Object'.format(self._oid)

        self.__oid__                         = self._oid
        self.__type__                       = self.Type

        self.dictID                         = '{0}.dict'.format(self._oid)

    def __str__(self):
        return self._oid

    def __repr__(self):
        return self._oid

    def __call__(self):

        if isinstance(self, object):
            return True
        else:
            return False

    @property
    def id(self):
        return self._oid

    @id.setter
    def id(self, newId):
        self._oid = newId

    def generatePrefix(self, key):
        keyID = key.upper()
        if len(keyID)==1:
            return '{0}ID'.format(keyID)
        elif len(keyID) == 2:
            return 'O{0}'.format(keyID)
        elif len(keyID) == 3:
            return keyID
        elif len(keyID) == 4:
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

        for key in self.ids.keys():
            if prefix in key:
                return (str(int(key[-3:]) + 1)).zfill(3)

        return (str(1)).zfill(3)

    def generateID(self, key):
        prefix                              = self.generatePrefix(key)
        subfix                              = self.generateSubfix(prefix)

        newID = str('{0}.{1}'.format(prefix, str(subfix).zfill(3)))
        print('Created new id: {0}, check type: {1}'.format(newID, type(newID)))
        return newID


def IID(obj):
    return id(obj)


def UID():
    return uuid.uuid4()


def get_datetime(mode='long'):
    if mode == 'long':
        return QDateTime.currentDateTime().toString(Qt.DefaultLocaleLongDate).replace(', ', '_').replace(' ', '_')
    else:
        return QDateTime.currentDateTime().toString(Qt.DefaultLocaleShortDate).replace(', ', '_').replace(' ', '_')


class DAMGERROR(Exception):
    """ Common subclass for all DAMG exceptions """


class DAMG(object):
    """
    New style object.

    """

    _copyright                              = 'This is an asset of DAMGTEAM'                # Copyright
    _data                                   = dict()
    __dict__                                = dict()

    def __init__(self, oid=None, name=None):
        super(DAMG, self).__init__()

        self.nameData                       = NAME(self)
        self.oidData                        = OID(self)

        if name is None:
            self._name                      = self.nameData.__name__
        else:
            self._name                      = name

        if oid is None:
            self._oid                       = self.oidData.__oid__
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

    def __init__(self):
        super(DAMGVARIABLES, self).__init__()

        self._oid                               = OID(self)
        self._uid                               = UID()
        self._metadatetime                      = get_datetime()

        self._name                              = NAME(self)
        self.Type                               = '{0} Object'.format(self._name.__name__)

        self.__name__                           = self._name.__name__
        self.__metadata__                       = '({0}).({1}).({2}).({3})'.format(self._oid.__oid__, self._iid, self._uid, self._metadatetime)
        self.__type__                           = self.Type

        self.initialize()


damgvar = DAMGVARIABLES()


# -------------------------------------------------------------------------------------------------------------
""" Datatypes """


class DAMGDICT(dict):                                                           # Dict
    """
    New stylist dictionary class by DAMGTEAM.
    A customised dictionary with name, id and much more extra functions.
    Dictionary now will be able to manage and identify very easily.
    """

    _data                                       = dict()
    _details                                    = dict()
    _copyright                                  = damgvar.shortCopyright

    def __init__(self, oid='', name='', **kwargs):
        """
        Basic initialize to create identification data of object
        """

        super(DAMGDICT, self).__init__(self)

        self._oid                               = oid
        self._name                              = name
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

        self._data['oid']                   = self._oid
        self._data['iid']                   = self._iid
        self._data['uid']                   = self._uid
        self._data['metadatetime']          = self._metadatetime

        self._data['name']                  = self._name.__name__
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

    def __init__(self, oid='', name='', *args):
        super(DAMGLIST, self).__init__(list)

        self._oid                               = oid
        self._name                              = name
        self._iid                               = IID(self)
        self._uid                               = UID()
        self._metadatetime                      = get_datetime()

        self.Type = '{0} Object'.format(self._name.__name__)
        self._metadata = '({0}).({1}).({2}).({3})'.format(self._oid, self._iid, self._uid, self._metadatetime)

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

        self._data['oid']                   = self._oid
        self._data['iid']                   = self._iid
        self._data['uid']                   = self._uid
        self._data['metadatetime']          = self._metadatetime

        self._data['name']                  = self._name.__name__
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

    __copyright__                           = _copyright


class UNIT(DAMG):

    _unit = 'Unit'

    def __init__(self):
        super(UNIT, self).__init__()

        self.nameData                       = NAME(self)
        self.oidData                        = OID(self)

        self._name                          = self.nameData.__name__

        self._oid                           = self.oidData.__oid__
        self._iid                           = IID(self)
        self._uid                           = UID()
        self._metadatetime                  = get_datetime()

        self.Type                           = '{0} Object'.format(self._name)
        self._metadata                      = '({0}).({1}).({2}).({3})'.format(self._oid, self._iid, self._uid, self._metadatetime)

        self.__name__                       = self._name
        self.__metadata__                   = self._metadata
        self.__type__                       = self.Type

        self._data                          = DAMGDICT(self._oid, self.__name__)
        self.__dict__                       = DAMGDICT(self._oid, self.__name__)

        self.initialize()

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, newUnit):
        self._unit                              = newUnit


class DATETIME(UNIT):

    _unit                                   = 'Duration'

    def __init__(self):
        super(DATETIME, self).__init__()

        self.nameData                       = NAME(self)
        self.oidData                        = OID(self)

        self._name                          = self.nameData.__name__

        self._oid                           = self.oidData.__oid__
        self._iid                           = IID(self)
        self._uid                           = UID()
        self._metadatetime                  = get_datetime()

        self.Type                           = '{0} Object'.format(self._name)
        self._metadata                      = '({0}).({1}).({2}).({3})'.format(self._oid, self._iid, self._uid, self._metadatetime)

        self.__name__                       = self._name
        self.__metadata__                   = self._metadata
        self.__type__                       = self.Type

        self._data                          = DAMGDICT(self._oid, self._name)
        self.__dict__                       = DAMGDICT(self._oid, self._name)

        self.get_tonow()
        self.get_today()
        self.set_time()
        self.set_date()

        self.initialize()

    def days_distance(self, daystart, dayend):
        return daystart.daysTo(dayend)

    def set_date(self, day=1, month=1, year=2013):

        self._year                          = year
        self._month                         = month
        self._day                           = day

        self._setdate                       = QDate(self._year, self._month, self._day)

        self._date                          = self._setdate.toString(damgvar.fmts)
        self.__date__                       = self._setdate.toString(damgvar.fmtl)

        return self._date, self.__date__

    def set_time(self, hour=1, minute=30, second=30):
        self._hour                          = hour
        self._minute                        = minute
        self._second                        = second

        self._settime                       = QTime(self._hour, self._minute, self._second)

        self._time                          = self._settime.toString(damgvar.fmts)
        self.__time__                       = self._settime.toString(damgvar.fmtl)

        return self._time, self.__time__

    def get_tonow(self):
        now                                 = QTime.currentTime()
        self._now                           = now.toString(damgvar.fmts)
        self.__now__                        = now.toString(damgvar.fmtl)

        return self._now, self.__now__

    def get_today(self):

        now                                 = QDate.currentDate()
        self._today                         = now.toString(damgvar.fmts)
        self.__today__                      = now.toString(damgvar.fmtl)

        return self._today, self.__today__

    @property
    def data(self):

        self._data.add_item('metadata'      , self._metadata)
        self._data.add_item('name'          , self._name)
        self._data.add_item('unit'          , self._unit)

        return self._data

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, newdate):
        self._date                          = newdate

    @property
    def today(self):
        return self._today

    @today.setter
    def today(self, date):
        self._today                         = date

    @property
    def totime(self):
        return self._now

    @totime.setter
    def totime(self, newtime):
        self._now                           = newtime


class YEAR(DATETIME):
    _unit = 'Year(s)'


class MONTH(DATETIME):
    _unit = 'Month(s)'


class WEEK(DATETIME):
    _unit = 'Week(s)'


class DAY(DATETIME):
    _unit = 'Day(s)'


class HOUR(DATETIME):
    _unit = 'Hr(s)'


class MINUTE(DATETIME):
    _unit = 'Min(s)'


class SECOND(DATETIME):
    _unit = 'Sec(s)'


class Monday(DAY):
    _unit = 'Monday'


class Tuesday(DAY):
    _unit = 'Tuesday'


class Wednesday(DAY):
    _unit = 'Wednesday'


class Thursday(DAY):
    _unit = 'Thursday'


class Friday(DAY):
    _unit = 'Friday'


class Saturday(DAY):
    _unit = 'Saturday'


class Sunday(DAY):
    _unit = 'Sunday'


class DOB(DATETIME):

    _unit                                   = 'Birthday'

    def __init__(self, day=1, month=1, year=1900):
        super(DOB, self).__init__()

        self.nameData                       = NAME(self)
        self.oidData                        = OID(self)

        self._day                           = day
        self._month                         = month
        self._year                          = year

        self._name                          = self.nameData.__name__

        self._oid                           = self.oidData.__oid__
        self._iid                           = IID(self)
        self._uid                           = UID()
        self._metadatetime                  = get_datetime()

        self.Type                           = '{0} Object'.format(self._name)
        self._metadata                      = '({0}).({1}).({2}).({3})'.format(self._oid, self._iid, self._uid, self._metadatetime)

        self.__name__                       = self._name
        self.__metadata__                   = self._metadata
        self.__type__                       = self.Type

        self._data                          = DAMGDICT(self._oid, self._name)
        self.__dict__                       = DAMGDICT(self.oidData.dictID, self._name)

        self._dob                           =  QDate(self._year, self._month, self._day)
        self.__dob__                        = self._dob.toString(damgvar.fmtl)
        self.dobs                           = self._dob.toString(damgvar.fmts)

        self.initialize()

    @property
    def data(self):
        self._data.add_item('metadata'      , self._metadata)
        self._data.add_item('name'          , self._name)
        self._data.add_item('dob'           , self.dobs)
        self._data.add_item('__dob__'       , self.__dob__)
        self._data.add_item('unit'          , self._unit)

        return self._data

    @property
    def dob(self):
        return self._dob

    @dob.setter
    def dob(self, newDob):
        self._dob                           = newDob


# -------------------------------------------------------------------------------------------------------------
""" Person & People """


class USER(DAMG):

    _name                                   = 'Username'
    _data                                   = DAMGDICT(_oid, _name)

    def __init__(self, id='', firstname='', lastname='', aka='', title='', eProfile='', email='', dob=''):
        super(USER, self).__init__()

        self._id                            = id
        self._firstname                     = firstname
        self._lastname                      = lastname
        self._aka                           = aka
        self._title                         = title
        self._eProfile                      = eProfile
        self._email                         = email
        self._dob                           = dob

        self._name                          = "{0} {1}".format(self._firstname, self._lastname)
        self._fullname                      = "{0} {1} (a.k.a {2})".format(self._firstname, self._lastname, self._aka)

        self._data                          = DAMGDICT(self._id, self._name)

        self.__fullname__                   = self._fullname
        self.__title__                      = self._title
        self.__email__                      = self._email


    @property
    def data(self):
        self._data.add_item('id'            , self._id)
        self._data.add_item('name'          , self._name)
        self._data.add_item('fullname'      , self._fullname)

        self._data.add_item('title'         , self._title)
        self._data.add_item('DOB'           , self._dob)

        self._data.add_item('email'         , self._email)
        self._data.add_item('eProfile'      , self._eProfile)

        return self._data

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def email(self):
        return self._email

    @property
    def title(self):
        return self._title

    @property
    def dob(self):
        return self._dob

    @property
    def eProfile(self):
        return self._eProfile

    @property
    def profile(self):
        return self.__dict__


class FOUNDER(DAMG):

    founder                                 = "The founder of DAMGTEAM"
    _oid                                     = "JimJim"

    _lastname                               = "Trinh"
    _firstname                              = "Do"
    _aka                                    = "Jimmy"

    _name                                   = "{0} {1}".format(_firstname, _lastname)
    _fullname                               = "{0} {1} (a.k.a {2})".format(_firstname, _lastname, _aka)

    _eProfile                               = "http://dot.damgteam.com/"
    _title                                  = "PipelineTD"
    _email                                  = "dot@damgteam.com"
    _dob                                    = DOB(1, 1, 1984).__dob__

    _data                                   = DAMGDICT(_oid, _name)

    def __init__(self):
        super(FOUNDER, self).__init__()

        self.initialize()


    def __str__(self):
        return json.dumps({self._name: self.data}, indent=4)

    def __repr__(self):
        return json.dumps({self._name:self.data}, indent=4)

    def initialize(self):
        self.__dict__['id']                     = self._id
        self.__dict__['name']                   = self._name
        self.__dict__['fullname']               = self._fullname

        self.__dict__['title']                  = self._title
        self.__dict__['DOB']                    = self._dob

        self.__dict__['email']                  = self._email
        self.__dict__['eProfile']               = self._eProfile

    @property
    def data(self):
        self._data.add_item('id'                , self._id)
        self._data.add_item('name'              , self._name)
        self._data.add_item('fullname'          , self._fullname)

        self._data.add_item('title'             , self._title)
        self._data.add_item('DOB'               , self._dob)

        self._data.add_item('email'             , self._email)
        self._data.add_item('eProfile'          , self._eProfile)

        return self._data

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def email(self):
        return self._email

    @property
    def title(self):
        return self._title

    @property
    def dob(self):
        return self._dob

    @property
    def eProfile(self):
        return self._eProfile

    @property
    def profile(self):
        return self.__dict__

    __oid__                                     = _oid
    __name__                                    = _fullname
    __fullname__                                = _fullname
    __title__                                   = _title
    __email__                                   = _email

    __info__                                    = _data._copyright

class COFOUNDER(DAMG):

    coFounder                               = "The co-founder of DAMGTEAM"
    _oid                                    = "DUCDM"
    _lastname                               = "Duong"
    _firstname                              = "Minh Duc"
    _aka                                    = "Up"
    _name                                   = "{0} {1}".format(_firstname, _lastname)
    _fullname                               = "{0} {1} (a.k.a {2})".format(_firstname, _lastname, _aka)
    _eProfile                               = "https://up209d.github.io/UPPortfolio/"
    _title                                  = "Front End Developer"
    _email                                  = "up@damgteam.com"
    _dob                                    = DOB(20,9,1987).__dob__

    _data                                   = DAMGDICT(_oid, _name)

    def __init__(self):
        super(COFOUNDER, self).__init__()

        self.initialize()

    def __str__(self):
        return json.dumps({self._name: self.data}, indent=4)

    def __repr__(self):
        return json.dumps({self._name: self.data}, indent=4)

    def initialize(self):
        self.__dict__['id']                 = self._id
        self.__dict__['name']               = self._name
        self.__dict__['fullname']           = self._fullname

        self.__dict__['title']              = self._title
        self.__dict__['DOB']                = self._dob

        self.__dict__['email']              = self._email
        self.__dict__['eProfile']           = self._eProfile

    @property
    def data(self):
        self._data.add_item('id'            , self._id)
        self._data.add_item('name'          , self._name)
        self._data.add_item('fullname'      , self._fullname)

        self._data.add_item('title'         , self._title)
        self._data.add_item('DOB'           , self._dob)

        self._data.add_item('email'         , self._email)
        self._data.add_item('eProfile'      , self._eProfile)

        return self._data

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def email(self):
        return self._email

    @property
    def title(self):
        return self._title

    @property
    def dob(self):
        return self._dob

    @property
    def eProfile(self):
        return self._eProfile

    @property
    def profile(self):
        return self.__dict__

    __oid__                                 = _oid
    __name__                                = _fullname
    __fullname__                            = _fullname
    __title__                               = _title
    __email__                               = _email

    __info__                                = _data._copyright






# -------------------------------------------------------------------------------------------------------------
# Created by panda on 30/08/2018 - 8:18 PM
# © 2017 - 2018 DAMGteam. All rights reserved