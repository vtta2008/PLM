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

        self.streamHld              = StreamHandler(self.logLevel, self.formatter, self.datetimeFormatter)
        self.fileHld                = FileHandler(self.filename, self.logLevel, self.formatter, self.datetimeFormatter)

        self.addHandler(self.streamHld)
        self.addHandler(self.fileHld)

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
                self._log(levelNum, message, args, **kwargs)

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