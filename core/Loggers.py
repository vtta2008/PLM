# -*- coding: utf-8 -*-
"""

Script Name: logger.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import unicode_literals
""" Import """

# Python
import sys, traceback, logging, enum, pdb, json

# Plm
from appData.scr._path import LOG_PTH
from appData.scr._format import LOG_FORMAT, DT_FORMAT

# -------------------------------------------------------------------------------------------------------------
try:
    unicode
except NameError:
    unicode = str

class Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, set):
            return tuple(o)
        elif isinstance(o, unicode):
            return o.encode('unicode_escape').decode('ascii')
        return super(Encoder, self).default(o)

class StructuredMessage(object):
    def __init__(self, message, **kwargs):
        self.message = message
        self.kwargs = kwargs

    def __str__(self):
        s = Encoder().encode(self.kwargs)
        return 'message: >>> %s >>> %s' % (self.message, s)

class OneLineExceptionFormatter(logging.Formatter):

    def formatException(self, exc_info):
        """
        Format an exception so that it prints on a single line.
        """
        result = super(OneLineExceptionFormatter, self).formatException(exc_info)
        return repr(result)  # or format into one line however you want to

    def format(self, record):
        s = super(OneLineExceptionFormatter, self).format(record)
        if record.exc_text:
            s = s.replace('\n', '') + '|'
        return s

class LogLevel(enum.IntEnum):

    Silent   = 0
    Debug    = 10
    Normal   = 20
    Trace    = 30
    Error    = 40
    Critical = 50

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

class SetLogger(logging.Logger):

    def __init__(self, parent=None, level="info", fmt=LOG_FORMAT['fullOpt'], dtfmt=DT_FORMAT['fullOpt'], filemode='a+', filename=LOG_PTH):
        super(SetLogger, self).__init__(parent)

        if parent is not None:
            logID = parent.__class__.__name__
        else:
            logID = self.__class__.__name__

        logging.getLogger(logID)

        self.level = self.define_level(level)
        self.logLevel = self.level_config(self.level)
        self.fmt = fmt                                                          # format
        self.dtfmt = dtfmt                                                      # datetime format
        self.fn = filename
        self.mode = filemode
        self.addLoggingLevel(levelName='TRACE', levelNum=LogLevel.Trace)

        sys.excepthook = self.exception_handler
        self.sh = logging.StreamHandler(sys.stdout)
        self.sh.setFormatter(logging.Formatter(self.fmt, self.dtfmt))
        self.sh.setLevel(logging.DEBUG)

        self.fh = logging.FileHandler(self.fn)
        self.fh.setFormatter(OneLineExceptionFormatter(self.fmt, self.dtfmt))
        self.fh.setLevel(logging.DEBUG)

        self.addHandler(self.sh)
        self.addHandler(self.fh)

        # logging.basicConfig(format=self.fmt, datefmt=self.dtfmt, filename=self.fn, filemode=self.mode, level=self.level)

    def define_level(self, logLevel):

        if logLevel is None or logLevel == 'not set':
            loglvl = logging.NOTSET
        elif logLevel == "info":
            loglvl = logging.INFO
        elif logLevel == "warn":
            loglvl = logging.WARNING
        elif logLevel == "debug":
            loglvl = logging.DEBUG
        elif logLevel == "error":
            loglvl = logging.ERROR
        else:
            loglvl = logging.FATAL

        return loglvl

    def level_config(self, verbosity_loglevel):

        verbose_level = LogLevel.getbyverbosity(verbosity_loglevel)

        logging_logLevel = {

            LogLevel.Silent:    logging.NOTSET,
            LogLevel.Debug:     logging.DEBUG,
            LogLevel.Normal:    logging.INFO,
            LogLevel.Trace:     logging.WARN,
            LogLevel.Error:     logging.ERROR,
            LogLevel.Critical:  logging.FATAL,

        }[verbose_level]
        return logging_logLevel

    def exception_handler(self, exc_type, exc_value, tb):
        if hasattr(sys, 'ps1') or not sys.stderr.isatty():
            exception = sys.__excepthook__(exc_type, exc_value, tb)
        else:
            exception = traceback.format_exception(exc_type, exc_value, tb)
            pdb.post_mortem(tb)

        self.critical("Unhandled exception!\n%s", "".join(exception))

        return exception

    def addLoggingLevel(self, levelName, levelNum, methodName=None):

        if not methodName:
            methodName = levelName.lower()

        if hasattr(logging, levelName):
            self.debug('AttributeError: {} already defined in logging module'.format(levelName))
        if hasattr(logging, methodName):
            self.debug('AttributeError: {} already defined in logging module'.format(methodName))
        if hasattr(logging.getLoggerClass(), methodName):
            self.debug('AttributeError: {} already defined in logger class'.format(methodName))

        def logForLevel(self, message, *args, **kwargs):
            if self.isEnabledFor(levelNum):
                self._log(levelNum, message, args, **kwargs)

        def logToRoot(message, *args, **kwargs):
            logging.log(levelNum, message, *args, **kwargs)

        logging.addLevelName(levelNum, levelName)
        setattr(logging, levelName, levelNum)
        setattr(logging.getLoggerClass(), methodName, logForLevel)
        setattr(logging, methodName, logToRoot)

    def loginfo(self, mess, *args, **kwargs):
        self.debug(StructuredMessage(mess))

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 15/06/2018 - 6:49 PM
# © 2017 - 2018 DAMGteam. All rights reserved