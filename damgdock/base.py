# -*- coding: utf-8 -*-
"""

Script Name: types.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, division, print_function, unicode_literals

# Python
import os, json, yaml, inspect

# PyQt5
from PyQt5.QtCore import Qt, QDate, QTime, QDateTime


# -------------------------------------------------------------------------------------------------------------
""" Identification class """


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


class ID(object):

    ids                                     = dict()

    def __init__(self, cls=None):
        super(ID, self).__init__()

        if cls is None:
            key                             = self.__class__.__name__
        else:
            key                             = cls.__class__.__name__

        self.key                            = key
        self._id                            = self.generateID(self.key)
        self.Type                           = '{0} Object'.format(self._id)

        self.__id__                         = self._id
        self.__type__                       = self.Type

        self.dictID                         = '{0}.dict'.format(self._id)

    def __str__(self):
        return self._id

    def __repr__(self):
        return self._id

    def __call__(self):

        if isinstance(self, object):
            return True
        else:
            return False

    @property
    def id(self):
        return self._id

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


class DAMG(object):

    _data                                   = dict()
    __dict__                                = dict()

    def __init__(self, id=None, name=None):
        super(DAMG, self).__init__()

        if id is None:
            self._id                        = ID(self)
        else:
            self._id                        = id

        if name is None:
            self._name                      = NAME(self)
        else:
            self._name                      = name

        self.__id__                         = self._id.__id__
        self.__name__                       = self._name.__name__

        self.Type                           = '{0} Object'.format(self._name)

        self.initialize()

    def __str__(self):

        if not hasattr(self, '_name'):
            self.__init__()

        return json.dumps({self.__name__: self.data}, cls=ObjectEncoder, indent=damgvar.indent, sort_keys=damgvar.sort_keys)

    def __repr__(self):

        if not hasattr(self, '_name'):
            self.__init__()

        return json.dumps({self.__name__: self.data}, cls=ObjectEncoder, indent=damgvar.indent, sort_keys=damgvar.sort_keys)

    def __call__(self):

        if isinstance(self, object):
            return True
        else:
            return False

    def initialize(self):
        """
        Store data into __dict__
        :return: dict
        """
        for key, value in self._data.items():
            if not key in ['copyright', 'id', 'name', 'type']:
                self.__dict__[key]          = value

    def to_json(self):
        """
        Debug json serizalable error.
        """
        return {self.__class__.__name__: 'YES'}

    @property
    def data(self):

        self._data['id']                    = self._id.__id__
        self._data['name']                  = self._name.__name__
        self._data['type']                  = self.Type
        self._data['copyright']             = damgvar.COPYRIGHT

        return self._data

    @data.setter
    def data(self, newdata):
        self._data = newdata

    @property
    def id(self):
        return self._id.__id__

    @id.setter
    def id(self, newID):
        self._id = newID

    @property
    def name(self):
        return self._name.__name__

    @name.setter
    def name(self, newname):
        self._name = newname

    @property
    def type(self):
        return self.Type

    @type.setter
    def type(self, newType):
        self.Type = newType


# -------------------------------------------------------------------------------------------------------------
""" Variables class"""

class DAMGVARIABLES(object):

    COPYRIGHT                                   = 'This is an asset of DAMGTEAM'                # Copyright
    indent                                      = 4                                             # Json setting
    sort_keys                                   = True                                          # Json setting

    fmtl                                        = Qt.DefaultLocaleLongDate
    fmts                                        = Qt.DefaultLocaleShortDate

    Type                                        = 'DAMG Variable Object'

    def __init__(self):
        super(DAMGVARIABLES, self).__init__()

        self._id                                = ID(self)
        self._name                              = NAME(self)
        self.Type                               = '{0} Object'.format(self._name)

        self.__id__                             = self._id.__id__
        self.__name__                           = self._name.__name__
        self.__type__                           = self.Type

        self._data                              = dict()

        self.initialize()

    def initialize(self):
        """
        Store data into __dict__
        :return: dict
        """
        for key, value in self._data.items():
            if not key in ['copyright', 'id', 'name', 'type']:
                self.__dict__[key]              = value

    def to_json(self):
        """
        Debug json serizalable error.
        """
        return {self.__class__.__name__: 'YES'}

    def __str__(self):
        return json.dumps({self._name: self.data}, cls=ObjectEncoder, indent=4, sort_keys=True)

    def __repr__(self):
        return json.dumps({self._name: self.data}, cls=ObjectEncoder, indent=4, sort_keys=True)

    def __call__(self):

        if isinstance(self, object):
            return True
        else:
            return False

    @property
    def data(self):

        self._data['copyright']                 = self.COPYRIGHT
        self._data['id']                        = self._id
        self._data['name']                      = self._name
        self._data['type']                      = self.Type

        return self._data

    @data.setter
    def data(self, newData):
        self._data = newData

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, newID):
        self._id                                = newID

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newname):
        self._name                              = newname

    @property
    def type(self):
        return self.Type

    @type.setter
    def type(self, t):
        self.Type                               = t

    @property
    def copyright(self):
        return self._copyright

    @copyright.setter
    def copyright(self, newCopyright):
        self._copyright = newCopyright


damgvar = DAMGVARIABLES()


class DAMGError(Exception):
    """ Common subclass for all DAMG exceptions """


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
        
        self._dict                          = sorted_dict
        self._keys                          = sorted(self._dict.keys())
        self._nr_items                      = len(self._keys)
        self._idx                           = 0

    def __iter__(self):
        return self

    def next(self):
        if self._idx                       >= self._nr_items:
            raise StopIteration

        key                                 = self._keys[self._idx]
        value                               = self._dict[key]
        self._idx                          += 1

        return key, value

    __next__                                = next


# -------------------------------------------------------------------------------------------------------------
""" New style class """


class DAMGDICT(dict):

    """
    New stylist dictionary class by DAMGTEAM.

    A customised dictionary with name, id and much more extra functions.
    Dictionary now will be able to manage and identify very easily.

     Extra functions:

        id: Return id of the dict
        add_item: Add new item into dict (key, value), value will be set to none if not define.
        get_item: Get value from a key
        remove_item: Delete a value from key (or set value to None).
        edit_item: Edit a value from key
        find_item: Return list of items (str) including key and value
        find_key: Return value from key if key is in dict
        check_key: Return True if key in dict, False if key not in dict.
        load_data: Load data from a file.

    """

    _data                                   = dict()
    _details                                = dict()

    Type                                    = 'DAMG Dictionary'
    _copyright                              = damgvar.COPYRIGHT

    def __init__(self, id='', name='', seq=None, **kwargs):
        super(DAMGDICT, self).__init__(self)

        self._id                            = id
        self._name                          = name

        self.__id__                         = self._id
        self.__name__                       = self._name

        self._seq                           = seq
        self._kwargs                        = kwargs


        if len(self.keys()) > 0:
            for key, value in self.items():
                self.__dict__[key]          = value
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
        return Iterator(self)

    iterkeys                                = __iter__

    def __str__(self):
        if not hasattr(self, '_name'):
            self.__init__()

        return json.dumps({self._name: self.data}, cls=ObjectEncoder, indent=damgvar.indent, sort_keys=damgvar.sort_keys)

    def __repr__(self):
        if not hasattr(self, '_name'):
            self.__init__()

        return json.dumps({self._name: self.data}, cls=ObjectEncoder, indent=damgvar.indent, sort_keys=damgvar.sort_keys)

    def initialize(self):
        """
        Store data into __dict__
        :return: dict
        """

        for key, value in self._data.items():
            if not key in ['copyright', 'id', 'name', 'type']:
                self.__dict__[key]              = value

    def getdata(self):
        """
        Get raw data
        :return: dict
        """
        return self.__dict__

    @property
    def data(self):

        self._data['id']                    = self._id
        self._data['name']                  = self._name
        self._data['type']                  = self.Type
        self._data['copyright']             = self._copyright

        for key, value in self.items():
            self._data[key]                 = value

        return self._data

    @data.setter
    def data(self, newdata):
        self._data                          = newdata

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, newID):
        self._id                            = newID

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newname):
        self._name                          = newname

    @property
    def type(self):
        return self.Type

    @type.setter
    def type(self, t):
        self.Type                           = t

    @property
    def copyright(self):
        return self._copyright

    @copyright.setter
    def copyright(self, newCopyright):
        self._copyright                     = newCopyright

    def to_json(self):
        """
        Debug json serizalable error.
        """
        return {self.__class__.__name__: 'YES'}

    def add_item(self, key, value=None):

        """
        Create new item of dict, requires key and value, if not value defined, set value to None
        :param key: new key
        :param value: value of new key
        :return: bool
        """

        if key is None:
            raise KeyError('Please define a valid key')
        else:
            self[key]                       = value
            self._data[key]                 = value
            return True

    def get_item(self, key):
        """
        Get value from key
        :param key: key to get value
        :return: value
        """

        if self.check_key(key):
            return self[key]
        else:
            raise KeyError('Please define a valid key')

    def remove_item(self, key):
        """
        Delete item from dict
        :param key: key to identify item
        :return: bool
        """

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
        """
        Edit value of dict
        :param key: key to identify value will be edited
        :param value: edit value
        :return: bool
        """

        if key in self.keys():

            oldValue                        = self[key]

            if oldValue == value:
                raise ValueError('Can not edit new value because it is the same as current value.')
            else:
                self[key]                   = value
                print('Edited {0} = {1}'.format(key, value))
                return True
        else:
            print(KeyError('Key is not exsisted.'))
            return False

    def find_item(self, keyword):

        """
        Find matching key, value, etc., from dict if match with keyword
        :param keyword: keyword to be searching
        :return: a list of matching items
        """

        findOut = []

        for key, value in self.items():
            if keyword in key and keyword not in value:
                item                        = '{0} = {1}'.format(str(key), str(value))
                findOut.append(item)
            elif keyword in key and keyword in value:
                item                        = '{0} = {1}'.format(str(key), str(value))
                findOut.append(item)
            elif keyword not in key and keyword in value:
                item                        = '{0} = {1}'.format(str(key), str(value))
                findOut.append(item)

        return findOut

    def find_key(self, value):
        """
        Find key from value.

        :param value:
        :return:
        """

        if value in self.values():
            for key, value in self.items():
                if value == value:
                    return key
        else:
            raise ValueError('This value is not in current dict: (id: {0}, name: {1})'.format(self._id, self._name))

    def check_key(self, key):
        """
        Check if key exists in dict

        :param key: key to be checked
        :return: bool
        """

        for k in self.keys():
            if k == key:
                return True
        return False

    def add_data(self, filename, fmt='json'):
        """
        Load dict data from a file.
        Read file using format json or yaml to get preset dict, then add new data to current dict.
        If key convention, will keep both key and mark the new key.

        :param filename: should be full path of data file
        :param fmt: format to read the file, default is json. Options are json, yaml
        :return: a data has been changed after adding new data.
        """

        if os.path.exists(filename):

            with open(filename, 'r') as f:

                if fmt == 'json':
                    newData                 = json.load(f)
                else:
                    newData                 = yaml.load(f)

            for key, value in newData.items():

                if key in self.keys():
                    newkey = '{0}_(new add)'.format(key)
                else:
                    newkey = key

                self.add_item(newkey, value)

        else:
            raise ('There is no data in: {0}'.format(filename))

    def remove_data(self, filename, fmt='json'):

        """
        Remove dict data from a file.
        Read file using format json or yaml to get preset dict, then compare with current dict and remove
        match data.

        :param filename: should be full path of data file
        :param fmt: format to read the file, default is json. Options are json, yaml
        :return: a data has been changed after removing data.
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

        """
        A quick styled resume context of the dict
        """

        self._details['dict id']        = self._id
        self._details['dict name']      = self._name
        self._details['number_of_keys'] = len(self.keys())

        for key, value in self._details.items():
            print('key: {0} \nvalueType: {1} \nvalue: {2}\n'.format(key, type(value), value))

        if len(self.keys()) > 0:
            for key, value in self.items():
                print('key: {0} \nvalueType: {1} \nvalue: {2}\n'.format(key, type(value), value))

        return self._details

    __type__                                = Type
    __copyright__                           = _copyright


class DAMGLIST(list):

    _copyright                              = damgvar.COPYRIGHT
    _data                                   = dict()
    __dict__                                = dict()

    def __init__(self, id='', name='', *args):
        super(DAMGLIST, self).__init__(list)

        self._id                            = id
        self._name                          = name
        self.args                           = args

        self.__id__                         = self._id
        self.__name__                       = self._name

        if self.args and len(self.args) > 0:
            for i in self.args:
                self.append(i)

        self.initialize()

    def __str__(self):
        return json.dumps({self._name: self.data}, cls=ObjectEncoder, indent=damgvar.indent, sort_keys=damgvar.sort_keys)

    def __repr__(self):
        return json.dumps({self._name: self.data}, cls=ObjectEncoder, indent=damgvar.indent, sort_keys=damgvar.sort_keys)

    def initialize(self):
        """
        Store data into __dict__
        :return: dict
        """

        for key, value in self._data.items():
            if not key in ['copyright', 'id', 'name', 'type']:
                self.__dict__[key] = value

    def getdata(self):
        """
        Get raw data
        :return: list
        """
        return self

    def to_json(self):
        """
        Debug json serizalable error.
        """
        return {self.__class__.__name__: 'YES'}

    @property
    def data(self):

        self._data['id'] = self._id
        self._data['name'] = self._name
        self._data['type'] = self.Type
        self._data['copyright'] = self._copyright

        return self._data

    @data.setter
    def data(self, newData):
        self._data = newData

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, newID):
        self._id = newID

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newname):
        self._name = newname

    @property
    def type(self):
        return self.Type

    @type.setter
    def type(self, t):
        self.Type = t

    @property
    def copyright(self):
        return self._copyright

    @copyright.setter
    def copyright(self, newCopyright):
        self._copyright = newCopyright

    __copyright__                           = _copyright


# -------------------------------------------------------------------------------------------------------------
""" Object class """


class DATETIME(DAMG):

    def __init__(self):
        DAMG.__init__(self)
        super(DATETIME, self).__init__()

        self._id                            = ID(self)
        self._name                          = NAME(self)
        self.Type                           = '{0} Object'.format(self._name)

        self.__id__                         = self._id.__id__
        self.__name__                       = self._name.__name__
        self.__type__                       = self.Type

        self._data                          = DAMGDICT(self._id.__id__, self._name.__name__)
        self.__dict__                       = DAMGDICT(self._id.dictID, self._name.__name__)

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
        self._data.add_item('id'            , self._id.__id__)
        self._data.add_item('name'          , self._name.__name__)
        self._data.add_item('date'          , self._date)
        self._data.add_item('__date__'      , self.__date__)
        self._data.add_item('today'         , self._today)
        self._data.add_item('__today__'     , self.__today__)
        self._data.add_item('now'           , self._now)
        self._data.add_item('__now__'       , self._now)

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


class CONVERTER(DAMG):

    def __init__(self):
        super(CONVERTER, self).__init__()

        self._id                            = ID(self)
        self._name                          = NAME(self)
        self.Type                           = '{0} Object'.format(self._name)

        self.__id__                         = self._id.__id__
        self.__name__                       = self._name.__name__
        self.__type__                       = self.Type

    def year_to_month(self, years):
        return years*12

    def year_to_day(self, years):
        return years*365

    def year_to_hours(self, years):
        return years*365*24

    def year_to_minute(self, years):
        return years*365*24*60

    def year_to_second(self, years):
        return years*365*24*60*60

    def month_to_year(self, months):
        return months/12

    def month_to_day(self, months):
        return months*30

    def month_to_minute(self, months):
        return months*30*24

    def mont_to_second(self, months):
        return months*30*24*60

    def day_to_year(self, days):
        return days/365

    def day_to_month(self, days):
        return days/30

    def day_to_weeks(self, days):
        return days/7

    def day_to_hour(self, days):
        return days*24

    def day_to_minute(self, days):
        return days*24*60

    def day_to_second(self, days):
        return days*24*60*60

    def hour_to_year(self, hours):
        return hours/(12*24)

    def hour_to_month(self, hours):
        return hours/(12*24*30)

    def hour_to_day(self, hours):
        return hours/24

    def hour_to_minute(self, hours):
        return hours*60

    def hour_to_second(self, hours):
        return hours*60*60

    def minute_to_year(self, minutes):
        return minutes/(60*24*365)

    def minute_to_day(self, minutes):
        return minutes*60*24*12

    def minute_to_seconds(self, minutes):
        return minutes/60

    def second_to_year(self, seconds):
        return seconds/(60*60*24*365)

    def second_to_month(self, seconds):
        return seconds/(60*60*24*30)

    def second_to_day(self, seconds):
        return seconds/(60*60*24)

    def second_to_hour(self, seconds):
        return seconds/(60*60)

    def second_to_minute(self, seconds):
        return seconds/60


class UNIT(DATETIME):

    _unit = 'Unit'

    def __init__(self):
        super(UNIT, self).__init__()

        self._id                            = ID(self)
        self._name                          = NAME(self)
        self.Type                           = '{0} Object'.format(self._name)

        self.__id__                         = self._id.__id__
        self.__name__                       = self._name.__name__
        self.__type__                       = self.Type

        self._data                          = DAMGDICT(self._id.dictID, self.__name__)

        self.initialize()

    @property
    def data(self):
        self._data.add_item('id'            , self._id.__id__)
        self._data.add_item('name'          , self._name.__name__)
        self._data.add_item('unit'          , self._unit)

        return self._data

    @property
    def unit(self):
        return self._unit


    def initialize(self):
        """
        Store data into __dict__
        :return: dict
        """
        for key, value in self._data.items():
            if not key in ['copyright', 'id', 'name', 'type']:
                self.__dict__[key] = value

    def to_json(self):
        """
        Debug json serizalable error.
        """
        return {self.__class__.__name__: 'YES'}


class DOB(DATETIME):

    def __init__(self, day=1, month=1, year=1900):
        super(DOB, self).__init__()

        self._day                           = day
        self._month                         = month
        self._year                          = year

        self._id                            = ID(self)
        self._name                          = NAME(self)
        self.Type                           = '{0} Object'.format(self._name)

        self.__id__                         = self._id.__id__
        self.__name__                       = self._name.__name__
        self.__type__                       = self.Type

        self._data                          = DAMGDICT(self._id.__id__, self._name.__name__)
        self.__dict__                       = DAMGDICT(self._id.dictID, self._name.__name__)

        self._dob                           =  QDate(self._year, self._month, self._day)
        self.__dob__                        = self._dob.toString(damgvar.fmtl)
        self.dobs                           = self._dob.toString(damgvar.fmts)

        self.initialize()

    @property
    def data(self):
        self._data.add_item('id'            , self._id.__id__)
        self._data.add_item('name'          , self._name.__name__)
        self._data.add_item('dob'           , self.dobs)
        self._data.add_item('__dob__'       , self.__dob__)

        return self._data

    @property
    def dob(self):
        return self._dob


class Year(UNIT):
    _unit = 'Year(s)'


class Month(UNIT):
    _unit = 'Month(s)'


class Week(UNIT):
    _unit = 'Week(s)'


class Day(UNIT):
    _unit = 'Day(s)'


class Hour(UNIT):
    _unit = 'Hr(s)'


class Minute(UNIT):
    _unit = 'Min(s)'


class Second(UNIT):
    _unit = 'Sec(s)'


class Monday(UNIT):
    _unit = 'Monday'


class Tuesday(UNIT):
    _unit = 'Tuesday'


class Wednesday(UNIT):
    _unit = 'Wednesday'


class Thursday(UNIT):
    _unit = 'Thursday'


class Friday(UNIT):
    _unit = 'Friday'


class Saturday(UNIT):
    _unit = 'Saturday'


class Sunday(UNIT):
    _unit = 'Sunday'


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 30/08/2018 - 8:18 PM
# © 2017 - 2018 DAMGteam. All rights reserved