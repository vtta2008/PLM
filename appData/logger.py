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

# Plm
from appData import _path as p
from appData import _format as f

LOGFORMAT = f.LOG
DATETIMEFORMAT = f.DATETIME
LOGPTH = p.LOGPTH

# -------------------------------------------------------------------------------------------------------------
""" logger variable """

__all__ = ['getLogger', 'INFO', 'WARN', 'DEBUG', 'TRACE', 'ERROR', 'FATAL']
levels = ['TRACE', 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL']
TRACE = logging.TRACE = DEBUG - 5

# -------------------------------------------------------------------------------------------------------------
""" Logging """

logging.addLevelName(TRACE, 'TRACE')
logging.basicConfig(level=logging.DEBUG, format=f.LOG['default'], datefmt=DATETIMEFORMAT['default'], filename=LOGPTH, filemode='w')
logger = logging.getLogger(LOGPTH)

# -------------------------------------------------------------------------------------------------------------
""" Exception format """

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

def exception_handler(self, exc_type, exc_value, tb):
    exception = traceback.format_exception(exc_type, exc_value, tb)
    logger.error("Unhandled exception!\n%s", "".join(exception))
    return logger

def online_exception_logging():
    handler = logging.FileHandler(LOGPTH)
    handler.setFormatter(OneLineExceptionFormatter())
    logger.addHandler(handler)

    return logger

def SETUP(verbose):

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter("%(asctime)s  %(name)-22s  %(levelname)-8s %(message)s")
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    if verbose:
        handler.setLevel(logging.DEBUG)
    else:
        handler.setLevel(logging.INFO)
    logger.addHandler(handler)

    # hook the exception handler
    sys.excepthook = exception_handler

    return logger

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 15/06/2018 - 6:49 PM
# © 2017 - 2018 DAMGteam. All rights reserved