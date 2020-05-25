# -*- coding: utf-8 -*-
"""

Script Name: logger.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import logging

# PLM
from PLM.configs                    import LOCAL_LOG
from .configs                       import LoggingFullOpt, DATETIME_fullOpt, LogLevel
from .handlers                      import StreamHandler, FileHandler


class Loggers(logging.Logger):


    key                             = 'PLM super logger'


    def __init__(self, parent=None, level="debug", formatter=LoggingFullOpt, datetimeFormatter=DATETIME_fullOpt,
                 filemode='a+', filename=LOCAL_LOG):
        super(Loggers, self).__init__(parent)

        self.parent                 = parent

        logging.getLogger(__name__)

        self.level                  = self.define_level(level)
        self.logLevel               = self.level_config(self.level)

        self.formatter              = formatter
        self.datetimeFormatter      = datetimeFormatter
        self.filename               = filename
        self.filemode               = filemode

        self.addLoggingLevel(levelName='TRACE', levelNum=LogLevel.Trace)
        self.addLoggingLevel(levelName='SPAM', levelNum=LogLevel.Spam)
        self.addLoggingLevel(levelName='VERBOSE', levelNum=LogLevel.Verbose)
        self.addLoggingLevel(levelName='SUCCESS', levelNum=LogLevel.Success)

        self.streamHld              = StreamHandler(self.logLevel, self.formatter, self.datetimeFormatter)
        self.fileHld                = FileHandler(self.filename, self.logLevel, self.formatter, self.datetimeFormatter)

        self.addHandler(self.streamHld)
        self.addHandler(self.fileHld)

    def define_level(self, logLevel):

        if logLevel == "silent":
            loglvl = logging.NOTSET
        elif logLevel == "spam":
            loglvl = logging.SPAM
        elif logLevel == "debug":
            loglvl = logging.DEBUG
        elif logLevel == "verbose":
            loglvl = logging.VERBOSE
        elif logLevel == "normal":
            loglvl = logging.INFO
        elif logLevel == "notice":
            loglvl = logging.WARNING
        elif logLevel == "trace":
            loglvl = logging.TRACE
        elif logLevel == "success":
            loglvl = logging.SUCCESS
        elif logLevel == "error":
            loglvl = logging.ERROR
        elif logLevel == "Critical":
            loglvl = logging.CRITICAL
        elif logLevel == "Fatal":
            loglvl = logging.FATAL
        else:
            loglvl = logging.NOTSET

        return loglvl

    def level_config(self, verbosity_loglevel):

        logConfigs = {LogLevel.Silent: logging.NOTSET,
                      LogLevel.Spam: logging.INFO,
                      LogLevel.Debug: logging.DEBUG,
                      LogLevel.Verbose: logging.DEBUG,
                      LogLevel.Normal: logging.INFO,
                      LogLevel.Notice: logging.WARN,
                      LogLevel.Trace: logging.WARN,
                      LogLevel.Success: logging.INFO,
                      LogLevel.Error: logging.ERROR,
                      LogLevel.Critical: logging.CRITICAL,
                      LogLevel.Fatal: logging.FATAL}

        verbose_level = LogLevel.getbyverbosity(verbosity_loglevel)

        return logConfigs[verbose_level]

    def addLoggingLevel(self, levelName, levelNum, methodName=None):

        if not methodName or methodName is None:
            methodName = levelName.lower()

        if hasattr(logging, levelName):
            self.info('{0} registered (level)'.format(levelName))
            regisable = False
        elif hasattr(logging, methodName):
            self.info('{0} registered (method)'.format(methodName))
            regisable = False
        elif hasattr(logging.getLoggerClass(), methodName):
            self.info('{0} registered (class)'.format(methodName))
            regisable = False
        else:
            regisable = True

        def logForLevel(self, message, *args, **kwargs):
            if self.isEnabledFor(levelNum):
                self._log(levelNum, message, *args, **kwargs)

        def logToRoot(message, *args, **kwargs):
            logging.log(levelNum, message, *args, **kwargs)

        if regisable:
            logging.addLevelName(levelNum, levelName)
            setattr(logging, levelName, levelNum)
            setattr(logging.getLoggerClass(), methodName, logForLevel)
            setattr(logging, methodName, logToRoot)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 15/06/2018 - 6:49 PM
# © 2017 - 2018 DAMGteam. All rights reserved