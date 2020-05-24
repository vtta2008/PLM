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
from PLM.configs                    import LOG_FORMAT, DT_FORMAT, LOCAL_LOG
from .logConfigs                    import LogLevel, lvlNames, lvlNumbers
from .Handlers                      import StreamHandler, FileHandler


class Loggers(logging.Logger):

    key                             = 'PLM super logger'

    def __init__(self, parent=None, level="debug", fmt=LOG_FORMAT['fullOpt'], dtfmt=DT_FORMAT['fullOpt'], filemode='a+', filename=LOCAL_LOG):
        super(Loggers, self).__init__(parent)

        self._parent                = parent
        if not self._parent:
            logging.getLogger(__name__)
        else:
            logging.getLogger(self._parent)

        for i in range(len(lvlNames)):
            self.addLoggingLevel(levelName=lvlNames[i].lower(), levelNum=lvlNumbers[i])

        self.level                  = self.define_level(level)
        self.logLevel               = self.level_config(self.level)

        self.fmt                    = fmt                                                         # format
        self.dtfmt                  = dtfmt                                                       # datetime format
        self.fn                     = filename
        self.fm                     = filemode

        self.sh                     = StreamHandler(self.logLevel, self.fmt, self.dtfmt)
        self.fh                     = FileHandler(self.fn, self.logLevel, self.fmt, self.dtfmt)
        self.addHandler(self.sh)
        self.addHandler(self.fh)

    def define_level(self, logLevel=None):

        if  logLevel == "silent":
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
            loglvl = logging.NOTICE
        elif logLevel == "trace":
            loglvl = logging.WARN
        elif logLevel == "success":
            loglvl = logging.SUCCESS
        elif logLevel == "error":
            loglvl = logging.ERROR
        elif logLevel == "critical":
            loglvl = logging.CRITICAL
        elif logLevel == "fatal":
            loglvl = logging.FATAL
        else:
            loglvl = logging.NOTSET

        return loglvl

    def level_config(self, verbosity_loglevel):

        verbose_level = LogLevel.getbyverbosity(verbosity_loglevel)

        logging_logLevel = {

            LogLevel.Silent:    logging.NOTSET,
            LogLevel.Spam:      logging.SPAM,
            LogLevel.Debug:     logging.DEBUG,
            LogLevel.Verbose:   logging.VERBOSE,
            LogLevel.Normal:    logging.INFO,
            LogLevel.Notice:    logging.NOTICE,
            LogLevel.Trace:     logging.WARN,
            LogLevel.Error:     logging.ERROR,
            LogLevel.Critical:  logging.CRITICAL,
            LogLevel.Fatal:     logging.FATAL

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