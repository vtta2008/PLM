# -*- coding: utf-8 -*-
"""

Script Name: logger.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys, logging

from bin.loggers.configs            import DatetimFullOpt, TextFullOpt
from bin.loggers.handlers           import DamgHandler
from bin.loggers.base               import BaseLogger

class DamgLogger(BaseLogger):

    key                             = 'DamgLogger'

    def __init__(self, name=None, level='debug', textFormat=None, datetimeFormat=None, filename=None, stream=None,
                 mode='a', encoding=None, delay=None):

        if not name:
            self._name              = __name__
        else:
            self._name              = name

        self._level                 = self.config_logLevel(level)

        super(DamgLogger, self).__init__(self.name, self.level)

        self._file                  = filename
        self._textFormat            = textFormat
        self._datetimeFormat        = datetimeFormat
        self._mode                  = mode
        self._encoding              = encoding
        self._delay                 = delay
        self._stream                = stream
        self.parent                 = logging.getLogger(self.name)
        self.setLevel(self.level)

        damgHandler                 = DamgHandler(self.file, self.mode, self.encoding, self.delay, self.level,
                                                  self.stream, self.textFormat, self.datetimeFormat)
        self.addHandler(damgHandler)



if __name__ == '__main__':

    logger = DamgLogger(__file__, 'debug', TextFullOpt, DatetimFullOpt, 'testlog.log', sys.stdout, 'a+', None, None)


    logger.info('text info logging')
    logger.warning('test warn logging')
    logger.debug('test debug logging')
    logger.error('test error logging')
    logger.critical('test critical logging')
    logger.trace('test trace logging')

    print(2/0)

    from colorlog import ColoredFormatter


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 15/06/2018 - 6:49 PM
# © 2017 - 2018 DAMGteam. All rights reserved