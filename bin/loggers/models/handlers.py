# -*- coding: utf-8 -*-
"""

Script Name: Handlers.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

import sys, pdb, traceback
from bin.loggers.models     import logging

__all__ = ('DamgHandler', )


class BaseHandler(logging.FileHandler):

    key = 'BaseHandler'

    _file                   = None
    _stream                 = None

    def __init__(self, filename, mode, encoding, delay):
        super(BaseHandler, self).__init__(filename, mode, encoding, delay)

        # self.setStream(sys.stdout)

    @property
    def file(self):
        return self._file

    @property
    def mode(self):
        return self._mode

    @property
    def encoding(self):
        return self._encoding

    @property
    def delay(self):
        return self._delay

    @property
    def stream(self):
        return self._stream

    @stream.setter
    def stream(self, val):
        self._stream                = val

    @file.setter
    def file(self, val):
        self._file                  = val

    @delay.setter
    def delay(self, val):
        self._delay                 = val

    @encoding.setter
    def encoding(self, val):
        self._encoding              = val

    @mode.setter
    def mode(self, val):
        self._mode                  = val



class DamgHandler(BaseHandler):

    key                        = 'DamgHandler'

    def __init__(self, filename='test.log', mode='a+', encoding=None, delay=False):

        self._file             = filename
        self._mode             = mode
        self._encoding         = encoding
        self._delay            = delay

        sys.excepthook          = self.exception_handler
        super(DamgHandler, self).__init__(self.file, self.mode, self.encoding, self.delay)


    def exception_handler(self, exc_type, exc_value, tb):

        if hasattr(sys, 'ps1') or not sys.stderr.isatty():
            return sys.__excepthook__(exc_type, exc_value, tb)
        else:
            # traceback.print_exception(exc_type, exc_value, tb)
            exception = traceback.format_exception(exc_type, exc_value, tb)

        if not tb is None:
            pdb.post_mortem(tb)

        return exception


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/16/2020 - 7:48 PM
# © 2017 - 2019 DAMGteam. All rights reserved