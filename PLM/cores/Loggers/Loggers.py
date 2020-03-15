# -*- coding: utf-8 -*-
"""

Script Name: logger.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys, traceback, linecache, logging


# PLM
from PLM.configs                    import LOG_FORMAT, DT_FORMAT, LOCAL_LOG
from .base                          import StyleMessage, LogLevel
from .Handlers                      import StreamHandler, FileHandler

class Loggers(logging.Logger):

    key                             = 'PLM super logger'

    def __init__(self, parent=None, level="debug", fmt=LOG_FORMAT['fullOpt'], dtfmt=DT_FORMAT['fullOpt'], filemode='a+', filename=LOCAL_LOG):
        super(Loggers, self).__init__(parent)

        self._parent = parent

        logging.getLogger(__name__)

        self.level                  = self.define_level(level)
        self.logLevel               = self.level_config(self.level)

        self.fmt                    = fmt                                                         # format
        self.dtfmt                  = dtfmt                                                       # datetime format
        self.fn                     = filename
        self.fm                     = filemode

        self.addLoggingLevel(levelName='TRACE', levelNum=LogLevel.Trace)

        self.sh                     = StreamHandler(self.logLevel, self.fmt, self.dtfmt)
        self.fh                     = FileHandler(self.fn, self.logLevel, self.fmt, self.dtfmt)
        self.addHandler(self.sh)
        self.addHandler(self.fh)

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

    def report(self, mess, **kwargs):
        self.trace(StyleMessage(mess, **kwargs))

    def drop_exception(self):
        exc_type, exc_obj, tb = sys.exc_info()

        if exc_obj is None:
            exc_obj = self.logID

        lineno = traceback.tb_lineno(traceback)
        filename = os.path.basename(__file__)
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, globals())

        self.report("\n"
                    "--------------------------------------------------------------------------------- \n"
                        "Tracking from:   {0} \n"
                        "At line number:  {1} \n"
                        "Details code:    {2} \n"
                        "{3} \n"
                    "--------------------------------------------------------------------------------- \n".format(
            os.path.basename(filename), lineno, line.strip(), exc_obj))


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 15/06/2018 - 6:49 PM
# © 2017 - 2018 DAMGteam. All rights reserved