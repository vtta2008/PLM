# -*- coding: utf-8 -*-
"""

Script Name: build.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

# Python
import os
import json
import logging

# PyQt5
from PyQt5.QtCore import QSettings


# -------------------------------------------------------------------------------------------------------------

class DictBase(dict):

    _id             = 'Dict ID'
    _name           = 'Dict object'
    _objname        = 'DAMG dict'

    def __name__(self):
        return self._name

    def __id__(self):
        return self._id

    def add_item(self, key, value):
        self[key] = value

    def remove_item(self, key):
        try:
            del self[key]
            print("key deleted: {key}".format(key=key))
        except KeyError:
            self.pop(key, None)
            print("key poped: {key}".format(key=key))

    def load_item(self, key):
        if key in self.keys():
            return self[key]

    def find_key(self, value):

        if value in self.values():
            for key, value in self.items():
                if value == value:
                    return key

    def check_key(self, key):
        for k in self.keys():
            if k == key:
                return True
        return False

    def get_data(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self._data = json.load(f)
        else:
            raise("There is no data in: {0}".format(filename))

# -------------------------------------------------------------------------------------------------------------

class ObjBase(object):                                                                  # Object template

    _id             = 'Object ID'
    _name           = 'Object Name'
    _objname        = 'DAMG object'
    _data           = dict()

    def __name__(self):
        return self._name

    def __id__(self):
        return self._id

    def __str__(self):
        return json.dumps({self._name: self.data}, indent=4)

    def __repr__(self):
        return json.dumps({self._name:self.data}, indent=4)

    @property
    def data(self):
        return self._data

    def __version__(self):
        return

    def __organization__(self):
        return

    def __docker__(self):
        return

    def __host__(self):
        return

    def __info__(self):
        return json.dumps({self._name: self.data}, indent=4)

    __dict__ = _data

# -------------------------------------------------------------------------------------------------------------

class ErrorBase(Exception):

    _id             = 'Error ID'
    _name           = 'Error Name'
    _objname        = 'DAMG Error'
    _data           = dict()

    def __name__(self):
        return self._name

    def __id__(self):
        return self._id

    @property
    def data(self):
        return self._data

    def __version__(self):
        return

    def __organization__(self):
        return

    def __docker__(self):
        return

    def __host__(self):
        return

    def __info__(self):
        return

# -------------------------------------------------------------------------------------------------------------

class LoggerBase(logging.Logger):

    _id             = 'Logger ID'
    _name           = 'Logger Name'
    _objname        = 'DAMG Logger'
    _data           = dict()

    def __name__(self):
        return self._name

    def __id__(self):
        return self._id

    @property
    def data(self):
        return self._data

    def __version__(self):
        return

    def __organization__(self):
        return

    def __docker__(self):
        return

    def __host__(self):
        return

    def __info__(self):
        return

# -------------------------------------------------------------------------------------------------------------

class SettingBase(QSettings):

    _id             = 'Setting ID'
    _name           = 'Setting Name'
    _objname        = 'DAMG Setting'
    _data           = dict()

    def __name__(self):
        return self._name

    def __id__(self):
        return self._id

    @property
    def data(self):
        return self._data

    def __version__(self):
        return

    def __organization__(self):
        return

    def __docker__(self):
        return

    def __host__(self):
        return

    def __info__(self):
        return

# -------------------------------------------------------------------------------------------------------------

class DError(ErrorBase):

    _name           = 'Error'
    _objname        = 'DAMG error'

    def __new__(self, *args, **kwargs):
        self.typeName   = self._objname
        self.typeClass  = (ObjBase,)
        self.typeDict   = dict()
        self._type       = type(self.typeName, self.typeClass, self.typeDict)
        return super(ErrorBase, self).__new__(self._type)

# -------------------------------------------------------------------------------------------------------------

class DObj(ObjBase):

    _name               = 'object'
    _objname            = 'DAMG object'

    def __new__(self, *args, **kwargs):
        self.typeName   = self._objname
        self.typeClass  = (ObjBase,)
        self.typeDict   = dict()
        self._type       = type(self.typeName, self.typeClass, self.typeDict)
        return super(ObjBase, self).__new__(self._type)

# -------------------------------------------------------------------------------------------------------------

class DLogger(LoggerBase):

    _name           = 'Logger'
    _objname        = 'DAMG logger'

    def __new__(self, *args, **kwargs):
        self.typeName   = self._objname
        self.typeClass  = (ObjBase,)
        self.typeDict   = dict()
        self._type       = type(self.typeName, self.typeClass, self.typeDict)
        return super(LoggerBase, self).__new__(self._type)

# -------------------------------------------------------------------------------------------------------------

class DCfg(DObj):

    _name           = 'Config'
    _objname        = 'DAMG config'

    def __new__(self, *args, **kwargs):
        self.typeName   = self._objname
        self.typeClass  = (ObjBase,)
        self.typeDict   = dict()
        self._type       = type(self.typeName, self.typeClass, self.typeDict)
        return super(DObj, self).__new__(self._type)

# -------------------------------------------------------------------------------------------------------------

class DDict(DictBase):

    _name           = 'dict'
    _objname        = 'DAMG dict'

# -------------------------------------------------------------------------------------------------------------

class DMtd(DObj):

    _name           = 'Metadata'
    _objname        = 'DAMG metadata'

    def __new__(self, *args, **kwargs):
        self.typeName   = self._objname
        self.typeClass  = (ObjBase,)
        self.typeDict   = dict()
        self._type       = type(self.typeName, self.typeClass, self.typeDict)
        return super(DObj, self).__new__(self._type)

# -------------------------------------------------------------------------------------------------------------

class DVer(DObj):

    _name           = 'Version'
    _objname        = 'DAMG version'

    def __new__(self, *args, **kwargs):
        self.typeName   = self._objname
        self.typeClass  = (ObjBase,)
        self.typeDict   = dict()
        self._type       = type(self.typeName, self.typeClass, self.typeDict)
        return super(DObj, self).__new__(self._type)

# -------------------------------------------------------------------------------------------------------------

class DSetting(SettingBase):

    _name           = "Setting"
    _objname        = 'DAMG setting'

    def __new__(self, *args, **kwargs):
        self.typeName   = self._objname
        self.typeClass  = (ObjBase,)
        self.typeDict   = dict()
        self._type       = type(self.typeName, self.typeClass, self.typeDict)
        return super(SettingBase, self).__new__(self._type)

# -------------------------------------------------------------------------------------------------------------

class API(DObj):

    _name           = 'API'
    _objname        = 'DAMG API'

    def __new__(self, *args, **kwargs):
        self.typeName   = self._objname
        self.typeClass  = (ObjBase,)
        self.typeDict   = dict()
        self._type       = type(self.typeName, self.typeClass, self.typeDict)
        return super(DObj, self).__new__(self._type)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 24/08/2018 - 11:05 AM
# © 2017 - 2018 DAMGteam. All rights reserved