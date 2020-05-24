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
from .logConfigs                    import LogLevel, logMissings
from .Handlers                      import StreamHandler, FileHandler



def install():

    return logging.setLoggerClass(Loggers)



class Loggers(logging.Logger):


    key                             = 'PLM super logger'


    def __init__(self, parent=None, name="debug", formatter=LOG_FORMAT['fullOpt'], datetimeFormatter=DT_FORMAT['fullOpt'],
                 filemode='a+', filename=LOCAL_LOG):

        if not parent:
            logName                 = __name__
        else:
            logName                 = parent.__name__

        for name in logMissings:
            value                   = self.getLogValue(name)
            self.addLoggingLevel(name, value)

        logValue                    = self.getLogValue(name)

        self.verboseLvl             = self.level_config(logValue)
        self.parent                 = logging.getLogger(logName)
        super(Loggers, self).__init__(logName, self.verboseLvl)

        self.formatter              = formatter
        self.datetimeFormatter      = datetimeFormatter
        self.filename               = filename
        self.filemode               = filemode

        self.streamHld              = StreamHandler(self.verboseLvl, self.formatter, self.datetimeFormatter)
        self.fileHld                = FileHandler(self.filename, self.verboseLvl, self.formatter, self.datetimeFormatter)

        self.addHandler(self.streamHld)
        self.addHandler(self.fileHld)

    def getLogValue(self, name='notset'):

        logDefines = {"silent": LogLevel.Silent, "spam": LogLevel.Spam, "debug": LogLevel.Debug,
                      "verbose": LogLevel.Verbose, "normal": LogLevel.Normal, "notice": LogLevel.Notice,
                      "trace": LogLevel.Trace, "success": LogLevel.Success, "error": LogLevel.Error,
                      "critical": LogLevel.Critical, "fatal": LogLevel.Fatal, }

        return logDefines[name]

    def level_config(self, verbosity_loglevel):

        logConfigs = {LogLevel.Silent: logging.NOTSET, LogLevel.Spam: logging.SPAM, LogLevel.Debug: logging.DEBUG,
                      LogLevel.Verbose: logging.VERBOSE, LogLevel.Normal: logging.INFO, LogLevel.Notice: logging.NOTICE,
                      LogLevel.Trace: logging.WARN, LogLevel.Success: logging.SUCCESS, LogLevel.Error: logging.ERROR,
                      LogLevel.Critical: logging.CRITICAL, LogLevel.Fatal: logging.FATAL}

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