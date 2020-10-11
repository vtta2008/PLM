# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
import logging, enum



class LogLevel(enum.IntEnum):

    Silent                          = 0
    Debug                           = 10
    Normal                          = 20
    Trace                           = 30
    Error                           = 40
    Critical                        = 50

    @classmethod
    def getbyname(cls, name):
        lookup = { level.name.lower(): level for level in cls }
        return lookup[name.lower()]

    @classmethod
    def getnames(cls):
        levels = list(cls)
        levels.sort(key = lambda level: int(level))
        return [ level.name for level in levels ]

    @classmethod
    def getbyverbosity(cls, intvalue):
        maxvalue = max(int(level) for level in cls)
        if intvalue > maxvalue:
            intvalue = maxvalue
        return cls(intvalue)


class BaseLogger(logging.Logger):

    key                             = 'BaseLogger'

    _name                           = None
    _level                          = None
    _file                           = None
    _stream                         = None
    _textFormat                     = None
    _datetimeFormat                 = None

    logLevel = {LogLevel.Silent: logging.NOTSET,
                LogLevel.Debug: logging.DEBUG,
                LogLevel.Normal: logging.INFO,
                LogLevel.Trace: logging.WARN,
                LogLevel.Error: logging.ERROR,
                LogLevel.Critical: logging.CRITICAL, }

    def __init__(self, name, level):
        self._name                  = name
        self._level                 = level
        self.addLoggingLevel(levelName='TRACE', levelNum=LogLevel.Trace)
        super(BaseLogger, self).__init__(name, level)


    def addLoggingLevel(self, levelName, levelNum, methodName=None):

        if not methodName or methodName is None:
            methodName = levelName.lower()

        if hasattr(logging, levelName):
            # self.info('{0} registered (level)'.format(levelName))
            regisable = False
        elif hasattr(logging, methodName):
            # self.info('{0} registered (method)'.format(methodName))
            regisable = False
        elif hasattr(logging.getLoggerClass(), methodName):
            # self.info('{0} registered (class)'.format(methodName))
            regisable = False
        else:
            regisable = True

        def logForLevel(self, message, *args, **kwargs):
            if self.isEnabledFor(levelNum):
                self._log(levelNum, message, args, **kwargs)

        def logToRoot(message, *args, **kwargs):
            logging.log(levelNum, message, *args, **kwargs)

        if regisable:
            logging.addLevelName(levelNum, levelName)
            setattr(logging, levelName, levelNum)
            setattr(logging.getLoggerClass(), methodName, logForLevel)
            setattr(logging, methodName, logToRoot)

    def config_logLevel(self, level):

        if level is None or level == 'not set':
            verbose_level = logging.NOTSET
        elif level == "info":
            verbose_level = logging.INFO
        elif level == "warn":
            verbose_level = logging.WARNING
        elif level == "debug":
            verbose_level = logging.DEBUG
        elif level == "error":
            verbose_level = logging.ERROR
        else:
            verbose_level = logging.FATAL

        verbose_level = LogLevel.getbyverbosity(verbose_level)

        return self.logLevel[verbose_level]

    @property
    def name(self):
        return self._name

    @property
    def level(self):
        return self._level

    @property
    def file(self):
        return self._file

    @property
    def textFormat(self):
        return self._textFormat

    @property
    def datetimeFormat(self):
        return self._datetimeFormat

    @property
    def mode(self):
        return self._mode

    @property
    def encoding(self):
        return self._encoding

    @property
    def delay(self):
        return self._delay

    @property
    def stream(self):
        return self._stream

    @stream.setter
    def stream(self, val):
        self._stream                = val

    @delay.setter
    def delay(self, val):
        self._delay                 = val

    @encoding.setter
    def encoding(self, val):
        self._encoding              = val

    @mode.setter
    def mode(self, val):
        self._mode                  = val

    @file.setter
    def file(self, val):
        self._file                  = val

    @name.setter
    def name(self, val):
        self._name                  = val

    @level.setter
    def level(self, val):
        self._level                 = val

    @textFormat.setter
    def textFormat(self, val):
        self._textFormat            = val

    @datetimeFormat.setter
    def datetimeFormat(self, val):
        self._datetimeFormat        = val

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
