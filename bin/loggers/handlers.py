# -*- coding: utf-8 -*-
"""

Script Name: Handlers.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys, logging, pdb, traceback
from .base import BaseHandler



# -------------------------------------------------------------------------------------------------------------
""" Handler """

class DamgHandler(BaseHandler):

    key                                     = 'DamgHandler'

    def __init__(self, filename=None, mode=None, encoding=None, delay=None, level=None, stream=None, textFormat=None, datetimeFormat=None):
        self.file = filename
        self.mode = mode
        self.encoding = encoding
        self.delay = delay

        super(DamgHandler, self).__init__(self.file, self.mode, self.encoding, self.delay)

        sys.excepthook = self.exception_handler

        self.level = level
        self.setLevel(logging.DEBUG)
        self.stream = stream
        self.setStream(self.stream)

        self.textFormat = textFormat
        self.datetimeFormat = datetimeFormat

        formatter = logging.Formatter(self.textFormat, self.datetimeFormat)
        self.setFormatter(formatter)

    def exception_handler(self, exc_type, exc_value, tb):

        if hasattr(sys, 'ps1') or not sys.stderr.isatty():
            return sys.__excepthook__(exc_type, exc_value, tb)
        else:
            # traceback.print_exception(exc_type, exc_value, tb)
            exception = traceback.format_exception(exc_type, exc_value, tb)
            # if not tb is None:
            pdb.post_mortem(tb)

        return exception


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/16/2020 - 7:48 PM
# © 2017 - 2019 DAMGteam. All rights reserved