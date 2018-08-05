# -*- coding: utf-8 -*-
"""

Script Name: ErrorManager.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys, linecache

# PyQt5
from PyQt5.QtCore import QSettings

# Plm
from core.Loggers import SetLogger


# -------------------------------------------------------------------------------------------------------------
""" Base """

class ErrorBase(Exception):

    key = 'errorBase'

    def __init__(self, parent=None):
        super(ErrorBase, self).__init__(parent)
        logger = SetLogger(self)
        self.report = logger.report
        self._parent = parent

    def initialize(self, errorName=None, section=None, key=None, path=None, fm=None, scope=None, value=None):
        self.section = section
        self.key = key
        self.pth = path
        self._format = fm
        self._scope = scope
        self.value = value
        self.errorName = str(errorName).split('class ')[-1].split('__main__.')[-1].split("'>")[0]

        self.mess = self._message()

        try:
            raise Exception("{0}: {1}".format(self.errorName, self.mess))
        except:
            self.raise_exception()

    def _message(self):
        if self.section == 'key':
            mess = self.key_error()
        elif self.section == 'path':
            mess = self.path_error()
        elif self.section == 'format':
            mess = self.format_error()
        elif self.section == 'scope':
            mess = self.scope_error()
        elif self.section == 'metavalue':
            mess = self.meta_value_error()
        else:
            mess = self.drop_exception_error()
        return mess

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
            return "INI format setting could not work in this fm."
        elif self._format == QSettings.NativeFormat:
            return "Native format setting could not work in this fm."
        else:
            return "Unknown format setting"

    def scope_error(self):
        if self._scope is None:
            return "Expected scope type, not None."
        elif self._scope == QSettings.UserScope:
            return "User scope could not work in this fm."
        elif self._scope == QSettings.SystemScope:
            return "System scope setting could not work in this fm."
        else:
            return "Unknown scope."

    def meta_value_error(self):
        if self.value is None or len(self.value) == 0:
            return "A value of a static meta object can not be None"
        else:
            return "Wrong type, meta value is only string type."

    def drop_exception_error(self):
        return "Drop an exception here"

    def raise_exception(self):

        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)

        self.report(" \n"
              "Caught error: {0} \n"
              "--------------------------------------------------------------------------------- \n"
              "   Tracking from:   {1} \n"
              "   At line number:  {2} \n"
              "   Details code:    [line {3}]: {4} \n"
              "   {5} \n"
              "--------------------------------------------------------------------------------- \n"
              " \n ".format(self.errorName.upper(), filename, lineno, lineno, line.strip(), exc_obj))
        return

#-------------------------------------------------------------------------------------------------------------
""" Error handle """

def handle_path_error(directory=None):
    if not os.path.exists(directory) or directory is None:
        try:
            raise IsADirectoryError("Path is not exists: {directory}".format(directory=directory))
        except IsADirectoryError as error:
            raise('Caught error: ' + repr(error))

# -------------------------------------------------------------------------------------------------------------
""" Utilities """

class IsADirectoryError(ErrorBase):
    def __init__(self, dir = None):
        self.dir = dir
        self.initialize(errorName=self.__class__, section='directory', value=self.dir)

class FileNotFoundError(ErrorBase):
    def __init__(self, dir=None):
        self.dir = dir
        self.initialize(errorName=self.__class__, section='directory', value=self.dir)

class DropException(ErrorBase):
    def __init__(self):
        self.initialize(errorName=self.__class__)

# -------------------------------------------------------------------------------------------------------------
""" Metadata """

class MetaValueError(ErrorBase):
    def __init__(self, value=None):
        self.value = value
        self.initialize(errorName=self.__class__, section='metavalue', value=self.value)

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