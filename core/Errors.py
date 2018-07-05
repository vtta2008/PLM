# -*- coding: utf-8 -*-
"""

Script Name: ErrorManager.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os

# PyQt5
from PyQt5.QtCore import QSettings

# Plm
from utilities.utils import raise_exception
from appData.Loggers import SetLogger
logger = SetLogger()

# -------------------------------------------------------------------------------------------------------------
""" Base """

class ErrorBase(Exception):

    def __init__(self, parent=None):
        super(ErrorBase, self).__init__(parent)

        self._parent = parent

    def initialize(self, errorName, section, key, path, fm, scope):
        self.section = section
        self.key = key
        self.pth = path
        self._format = fm
        self._scope = scope
        self.errorName = str(errorName).split('class ')[-1].split('__main__.')[-1].split("'>")[0]

        if self.section == 'key':
            self.mess = self.key_error()
        elif self.section == 'path':
            self.mess = self.path_error()
        elif self.section == 'format':
            self.mess = self.format_error()
        elif self.section == 'scope':
            self.mess = self.scope_error()

        try:
            raise Exception("{0}: {1}".format(self.errorName, self.mess))
        except:
            raise_exception()

    def key_error(self):
        if self.key is None or len(self.key) == 0:
            return "Expect key as string, not None."
        else:
            return 'Could not find "{0}" in setting, key not exists.'.format(self.key)

    def path_error(self):
        if self.pth is None or len(self.pth) == 0:
            return "Path should be string, not None"
        elif not os.path.exists(self.pth):
            return "Path not exists."
        else:
            return "Could not find the file path."

    def format_error(self):
        if self._format is None or self._format == QSettings.InvalidFormat:
            return "Invalid format setting, not set or wrong format"
        elif self._format == QSettings.IniFormat:
            return "INI format setting could not work in this mode."
        elif self._format == QSettings.NativeFormat:
            return "Native format setting could not work in this mode."
        else:
            return "Unknown format setting"

    def scope_error(self):
        if self._scope is None:
            return "Expected scope type, not None."
        elif self._scope == QSettings.UserScope:
            return "User scope could not work in this mode."
        elif self._scope == QSettings.SystemScope:
            return "System scope setting could not work in this mode."
        else:
            return "Unknown scope."

# -------------------------------------------------------------------------------------------------------------
""" Setting """

class FormatSettingError(ErrorBase):
    def __init__(self, fm=QSettings.InvalidFormat):
        self._format = fm
        self.initialize(errorName=self.__class__, section='format', fm=self._format)

class PathSettingError(ErrorBase):
    def __init__(self, path=None):
        self.pth = path
        self.initialize(errorName=self.__class__, section='path', path=self.pth)

class KeySettingError(ErrorBase):
    def __init__(self, key=None):
        self.key = key
        self.initialize(errorName=self.__class__, section='key', key=self.key)

class ScopeSettingError(ErrorBase):
    def __init__(self, scope=None):
        self._scope = scope
        self.initialize(errorName=self.__class__, section='scope', key=self._scope)

# -------------------------------------------------------------------------------------------------------------
""" Setting """

class QtNodesError(ErrorBase):
    """Base custom exception."""
    def __init__(self):
        ErrorBase(errorName=self.__class__)

class UnregisteredNodeClassError(QtNodesError):
    """The Node class is not registered."""
    def __init__(self):
        ErrorBase(errorName=self.__class__)

class UnknownFlowError(QtNodesError):
    """The flow style can not be recognized."""
    def __init__(self):
        ErrorBase(errorName=self.__class__)

class KnobConnectionError(QtNodesError):
    """Something went wrong while trying to connect two Knobs."""
    def __init__(self):
        ErrorBase(errorName=self.__class__)

class DuplicateKnobNameError(QtNodesError):
    """A Node's Knobs must have unique names."""
    def __init__(self):
        ErrorBase(errorName=self.__class__)

class StandardError(ErrorBase):
    def __init__(self):
        ErrorBase(errorName=self.__class__)

class SettingError(ErrorBase):
    def __init__(self):
        ErrorBase(errorName=self.__class__)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 22/06/2018 - 6:07 AM
# © 2017 - 2018 DAMGteam. All rights reserved