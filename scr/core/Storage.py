# -*- coding: utf-8 -*-
"""

Script Name: Storage.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, datetime, time, uuid, json, inspect

# PyQt5
from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot

# PLM
from scr.core.Metadata import __envKey__
print(os.path.dirname(__file__))

# -------------------------------------------------------------------------------------------------------------
""" Dataset template """

cfgPth = os.path.join(os.getenv(__envKey__), 'cfg')
metadataPth = os.path.join(cfgPth, 'mtd')

if not os.path.exists(metadataPth):
    try:
        os.mkdir(metadataPth)
    except FileNotFoundError:
        os.mkdir(cfgPth)
    finally:
        os.mkdir(metadataPth)

# -------------------------------------------------------------------------------------------------------------
""" Original object """

class Base(QObject):

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


# -------------------------------------------------------------------------------------------------------------
""" PLM object type """

class PObj(Base):

    Type = 'PLM object'
    _attributes = {}
    imported = pyqtSignal(bool)

    def __init__(self, parent=None, **kwargs):
        Base.__init__(self)
        self._parent = parent
        if parent is None:
            self.cls = self.__class__
        else:
            self.cls = self._parent.__class__

        self._name = self.cls.__name__
        self.regFile = os.path.join(metadataPth, self.name() + ".{0}".format('mtd'))
        self._register = os.path.exists(self.regFile)
        self.imported.connect(self.set_imported)

        if self._register:
            with open(self.regFile, 'r') as f:
                self._attributes = json.load(f)
        else:
            self._type = self.type()
            self._datetime = self.get_datetime()
            self._unix = self.getUnix()
            self.register()

    def __str__(self):
        return json.dumps(self.data, default=lambda obj: obj.data, indent=4)

    def __repr__(self):
        return json.dumps(self.data, default=lambda obj: obj.data, indent=4)

    @property
    def data(self):
        return self._attributes

    def register(self):

        self._attributes['class name'] = self.name()
        self._attributes['type'] = self.type()
        self._attributes['datetime'] = self.datetime()
        self._attributes['unix'] = self.unix()
        self._attributes['objName'] = self.cls.key
        self._attributes['attrs'] = [a for a in inspect.getmembers(self.cls, lambda a:not(inspect.isroutine(a))) if not a[0].startswith('__') and a[0].endswith('__')]

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
        try:
            self._attributes['datetime']
        except KeyError:
            self._datetime = self.get_datetime()
        finally:
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


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 23/07/2018 - 9:48 PM
# © 2017 - 2018 DAMGteam. All rights reserved