# -*- coding: utf-8 -*-
"""

Script Name: Storage.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import os, datetime, time, uuid, json

from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot

class PureObject(QObject):

    stationsChanged = pyqtSignal()
    _attributes = {}

    def __init__(self):
        QObject.__init__(self)
        self.m_stations =[]

    @pyqtProperty('QVariantList', notify=stationsChanged)
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

class PureData(dict):

    def __init__(self):
        self['datetime'] = None

class PObj(PureObject):

    Type = 'object'
    _attributes = {}
    imported = pyqtSignal(bool)

    def __init__(self, parent=None, **kwargs):
        PureObject.__init__(self)
        self._name = self.__class__.__name__
        self.regFile = os.path.join(os.getenv('PIPELINE_MANAGER'), 'mtd', self.name() + ".{0}".format('pObj'))
        self._register = os.path.exists(self.regFile)

        if self._register:
            with open(self.regFile, 'r') as f:
                self._data = json.load(f)
        else:
            self._data = PureData()

        self._type = self.type()
        self._datetime = self._data['datetime']
        self._unix = self.getUnix()
        self.imported.connect(self.set_imported)
        self.register()
        self.imported.emit(True)

    def __str__(self):
        return json.dumps(self.data, default=lambda obj: obj.data, indent=4)

    def __repr__(self):
        return json.dumps(self.data, default=lambda obj: obj.data, indent=4)

    def __getattr__(self, name):
        if name in self._attributes:
            attribute = self._attributes.get(name)
            return attribute.value

        elif hasattr(self, name):
            return getattr(self, name)

        raise AttributeError('no attribute exists {0}'.format(name))

    def __setattr__(self, name, value):
        if name in self._attributes:
            super(PObj, self).__setattr__(name, value)
            attribute = self._attributes.get(name)

            if value != attribute.value:
                attribute.value = value
        else:
            super(PObj, self).__setattr__(name, value)

    @property
    def data(self):
        return self._data

    def register(self):

        self._attributes['name'] = self.name()
        self._attributes['type'] = self.type()
        self._attributes['datetime'] = self.datetime()
        self._attributes['unix'] = self.unix()
        self._attributes['objName'] = self.__class__.key

        if not self._register:
            with open(self.regFile, 'w') as f:
                json.dump(self._attributes, f, indent=4)
            self._register = True

        return self._register

    def deRegister(self):
        os.remove(self.regFile)
        self._register = False
        self._attributes = {}

    def get_datetime(self):
        datetime_stamp = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y.%m.%d||%H:%M:%S'))
        return datetime_stamp

    def getUnix(self):
        return str(uuid.uuid4())

    def name(self):
        return self._name

    def type(self):
        return self.Type

    def datetime(self):
        if self._data['datetime'] is None:
            self._datetime = self.get_datetime()
        return self._datetime

    def unix(self):
        if not self._register:
            _unix = self.getUnix()
        else:
            with open(self.regFile, 'r') as f:
                data = json.load(f)
            _unix = data['unix']
        return _unix

    @pyqtSlot(bool)
    def set_imported(self, param):
        self._import = param
        print('--- IMPORT: {0} ---'.format(self.__class__.key))

    def attributes(self, *args):
        if not args:
            return self._attributes.values()
        else:
            attrs = [x for x in self._attributes.values() if x.name in args]
            if attrs and len(attrs) == 1:
                return attrs[0]
            return attrs

    def list_attrs(self):
        return self._attributes.keys()

    def get_attr(self, name):
        if name not in self._attributes:
            self.add_attr(name)
        return self._attributes.get(name)

    def rename_attr(self, name, new_name):
        if name not in self._attributes:
            raise AttributeError(name)

        if hasattr(self, new_name):
            raise AttributeError('attribute "%s" already exists.' % new_name)

        attr = self._attributes.pop(name)
        attr.name = new_name
        self._attributes.update({attr.name: attr})

class UiObj(PureObject):

    Type = 'layout'
    _attributes = {}
    imported = pyqtSignal(bool)

    def __init__(self, parent=None, **kwargs):
        PureObject.__init__(self)
        self._parent = parent
        self._name = self._parent.__name__
        self.regFile = os.path.join(os.getenv('PIPELINE_MANAGER'), 'mtd', self.name() + ".{0}".format('pObj'))
        self._register = os.path.exists(self.regFile)

        if self._register:
            with open(self.regFile, 'r') as f:
                self._data = json.load(f)
        else:
            self._data = PureData()

        self._type = self.type()
        self._datetime = self._data['datetime']
        self._unix = self.getUnix()
        self.imported.connect(self.set_imported)
        self.register()
        self.imported.emit(True)

    def __str__(self):
        return json.dumps(self.data, default=lambda obj: obj.data, indent=4)

    def __repr__(self):
        return json.dumps(self.data, default=lambda obj: obj.data, indent=4)

    def __getattr__(self, name):
        if name in self._attributes:
            attribute = self._attributes.get(name)
            return attribute.value

        elif hasattr(self, name):
            return getattr(self, name)

        raise AttributeError('no attribute exists {0}'.format(name))

    def __setattr__(self, name, value):
        if name in self._attributes:
            super(PObj, self).__setattr__(name, value)
            attribute = self._attributes.get(name)

            if value != attribute.value:
                attribute.value = value
        else:
            super(PObj, self).__setattr__(name, value)

    @property
    def data(self):
        return self._data

    def register(self):

        self._attributes['name'] = self.name()
        self._attributes['type'] = self.type()
        self._attributes['datetime'] = self.datetime()
        self._attributes['unix'] = self.unix()
        self._attributes['objName'] = self._parent.key

        if not self._register:
            with open(self.regFile, 'w') as f:
                json.dump(self._attributes, f, indent=4)
            self._register = True

        return self._register

    def deRegister(self):
        os.remove(self.regFile)
        self._register = False
        self._attributes = {}

    def get_datetime(self):
        datetime_stamp = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y.%m.%d||%H:%M:%S'))
        return datetime_stamp

    def getUnix(self):
        return str(uuid.uuid4())

    def name(self):
        return self._name

    def type(self):
        return self.Type

    def datetime(self):
        if self._data['datetime'] is None:
            self._datetime = self.get_datetime()
        return self._datetime

    def unix(self):
        if not self._register:
            _unix = self.getUnix()
        else:
            with open(self.regFile, 'r') as f:
                data = json.load(f)
            _unix = data['unix']
        return _unix

    @pyqtSlot(bool)
    def set_imported(self, param):
        self._import = param
        print('--- IMPORT: {0} ---'.format(self.__class__.key))

    def attributes(self, *args):
        if not args:
            return self._attributes.values()
        else:
            attrs = [x for x in self._attributes.values() if x.name in args]
            if attrs and len(attrs) == 1:
                return attrs[0]
            return attrs

    def list_attrs(self):
        return self._attributes.keys()

    def get_attr(self, name):
        if name not in self._attributes:
            self.add_attr(name)
        return self._attributes.get(name)

    def rename_attr(self, name, new_name):
        if name not in self._attributes:
            raise AttributeError(name)

        if hasattr(self, new_name):
            raise AttributeError('attribute "%s" already exists.' % new_name)

        attr = self._attributes.pop(name)
        attr.name = new_name
        self._attributes.update({attr.name: attr})


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 23/07/2018 - 9:48 PM
# © 2017 - 2018 DAMGteam. All rights reserved