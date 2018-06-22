# -*- coding: utf-8 -*-
"""

Script Name: logger.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys, traceback, logging, enum, pdb

# Plm
from appData._path import LOGPTH
from appData._format import LOG_FORMAT, DT_FORMAT

# -------------------------------------------------------------------------------------------------------------

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
        return

class LogLevel(enum.IntEnum):

    Silent = 0
    Normal = 1
    Verbose = 2
    Debug = 3
    Trace = 4
    Error = 5
    Critical = 6

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

    def __init__(self, level="debug", format=LOG_FORMAT['fullOpt'], datefmt=DT_FORMAT['fullOpt'], filemode='w', filename=LOGPTH):
        super(SetLogger, self).__init__(filename)

        self.level = self.define_level(level=level)
        self.logLevel = self.level_config(self.level)

        self.handler = logging.StreamHandler(sys.stdout)
        self.addHandler(self.handler)

        sys.excepthook = self.exception_handler

        logging.basicConfig(format=format, datefmt=datefmt, filename=filename, filemode=filemode, level=level, style="{")

    def define_level(self, level):
        if level == "info":
            loglvl = logging.INFO
        elif level == "warn":
            loglvl = logging.WARNING
        elif level == "debug":
            loglvl = logging.DEBUG
        elif level == "error":
            loglvl = logging.ERROR
        else:
            loglvl = logging.FATAL

        return loglvl

    def level_config(self, verbosity_loglevel):

        logLevel = LogLevel.getbyverbosity(verbosity_loglevel)

        self.addLoggingLevel('TRACE', logging.DEBUG)

        logging_logLevel = {

            LogLevel.Silent:    logging.WARNING,
            LogLevel.Normal:    logging.INFO,
            LogLevel.Verbose:   logging.DEBUG,
            LogLevel.Debug:     logging.TRACE,
            LogLevel.Error:     logging.ERROR,
            LogLevel.Critical:  logging.FATAL,

        }[logLevel]

        return logging_logLevel

    def exception_handler(self, exc_type, exc_value, tb):
        if hasattr(sys, 'ps1') or not sys.stderr.isatty():
            exception = sys.__excepthook__(exc_type, exc_value, tb)
        else:
            exception = traceback.format_exception(exc_type, exc_value, tb)
            pdb.post_mortem(tb)

        self.error("Unhandled exception!\n%s", "".join(exception))

        return exception

    def addLoggingLevel(self, levelName, levelNum, methodName=None):
        """
        Comprehensively adds a new logging level to the `logging` module and the
        currently configured logging class.

        `levelName` becomes an attribute of the `logging` module with the value
        `levelNum`. `methodName` becomes a convenience method for both `logging`
        itself and the class returned by `logging.getLoggerClass()` (usually just
        `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
        used.

        To avoid accidental clobberings of existing attributes, this method will
        raise an `AttributeError` if the level name is already an attribute of the
        `logging` module or if the method name is already present

        Example
        -------
        >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
        >>> logging.getLogger(__name__).setLevel("TRACE")
        >>> logging.getLogger(__name__).trace('that worked')
        >>> logging.trace('so did this')
        >>> logging.TRACE
        5

        """
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

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 15/06/2018 - 6:49 PM
# © 2017 - 2018 DAMGteam. All rights reserved