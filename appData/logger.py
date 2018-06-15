# -*- coding: utf-8 -*-
"""

Script Name: logger.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys, logging, traceback
from logging import getLogger, INFO, WARN, DEBUG, ERROR, FATAL
from logging.handlers import RotatingFileHandler

# Plm
from appData import _path as p
from appData import _format as f
LOGFORMAT = f.LOGFORMAT
LOGPTH = p.LOGPTH

# -------------------------------------------------------------------------------------------------------------
""" logger variable """

__all__ = ['getLogger', 'INFO', 'WARN', 'DEBUG', 'TRACE', 'ERROR', 'FATAL']

levels = ['TRACE', 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL']

TRACE = logging.TRACE = DEBUG - 5

# -------------------------------------------------------------------------------------------------------------
""" logger setup """

class Handler(RotatingFileHandler):

    def __init__(self, *args, **kwargs):
        super(Handler, self).__init__(*args, **kwargs)
        self.doRollover()

class Logger(object):

    def __init__(self):
        super(Logger, self).__init__()

        self.name = __name__
        self.pth = LOGPTH
        self.format = format
        self.formatSetting = p.formatSetting
        self.logger = logging.getLogger(self.name)
        self.set_up(True)

    def set_up(self, verbose):

        logging.addLevelName(TRACE, 'TRACE')

        value = self.formatSetting.value("logFormat", True)
        if not value:
            value = 1

        logFormat = self.get_format(value)

        self.handler = Handler(self.pth, maxBytes=1e6, backupCount=0)
        self.handler.setFormatter(logging.Formatter(logFormat))

        level = self.get_level()

        self.handler.setLevel(level)
        self.logger.addHandler(self.handler)

        handler = logging.StreamHandler()

        if verbose:
            self.handler.setLevel(logging.DEBUG)
        else:
            self.handler.setLevel(logging.INFO)
            self.logger.addHandler(self.handler)

        sys.excepthook = self.exception_handler                         # hook the exception handler

    def exception_handler(self, exc_type, exc_value, tb):
        exception = traceback.format_exception(exc_type, exc_value, tb)
        logger = logging.getLogger(self.pth)
        logger.error("Unhandle exception!\n%s", "".join(exception))

    def get_format(self, num):
        if not num:
            num = 1

        keys = [k for k in LOGFORMAT]
        key = keys[num]
        return LOGFORMAT[key]


    def get_level(self, opts="DEBUG"):
        try:
            level = getattr(logging, opts.loglevel.upper())
            print(level)
        except AttributeError:
            return logging.DEBUG
        else:
            return level

if __name__ == '__main__':
    Logger()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 15/06/2018 - 6:49 PM
# © 2017 - 2018 DAMGteam. All rights reserved