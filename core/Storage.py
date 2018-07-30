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
    regInfo = {}
    imported = pyqtSignal(bool)

    def __init__(self, parent=None):
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

    def register(self):

        self.regInfo['name'] = self.name()
        self.regInfo['type'] = self.type()
        self.regInfo['datetime'] = self.datetime()
        self.regInfo['unix'] = self.unix()
        self.regInfo['objName'] = self.__class__.key

        if not self._register:
            with open(self.regFile, 'w') as f:
                json.dump(self.regInfo, f, indent=4)
            self._register = True

        return self._register

    def deRegister(self):
        os.remove(self.regFile)
        self._register = False
        self.regInfo = {}

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

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 23/07/2018 - 9:48 PM
# © 2017 - 2018 DAMGteam. All rights reserved