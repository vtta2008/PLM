# -*- coding: utf-8 -*-
"""

Script Name: element.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

from __rc__.base import ErrorBase, LoggerBase, DictBase, ObjBase, SettingBase

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
# Created by panda on 22/08/2018 - 5:08 PM
# © 2017 - 2018 DAMGteam. All rights reserved