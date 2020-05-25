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

# PLM
from .formatters                            import OneLineExceptionFormatter


# -------------------------------------------------------------------------------------------------------------
""" Handler """


class StreamHandler(logging.StreamHandler):

    def __init__(self, level=None, fmt=None, dtfmt=None):
        super(StreamHandler, self).__init__(sys.stdout)

        self.fmt                            = fmt                                       # Formatter
        self.dtfmt                          = dtfmt                                     # Datetime Fommater
        self.logLevel                       = level                                     # Log level
        self.update()

    def get_formatter(self):
        return logging.Formatter(self.fmt, self.dtfmt)

    def set_formatter(self, formatter):
        self.fmt                            = formatter
        self.update()

    def set_datetimeFormatter(self, formatter):
        self.dtfmt                          = formatter
        self.update()

    def set_lever(self, level):
        self.logLevel                       = level
        self.update()

    def update(self):
        self.setFormatter(self.get_formatter())
        self.setLevel(self.logLevel)

    def exception_handler(self, exc_type, exc_value, exc_traceback):

        if hasattr(sys, 'ps1') or not sys.stderr.isatty():
            exception = sys.__excepthook__(exc_type, exc_value, exc_traceback)
        else:
            exception = traceback.format_exception(exc_type, exc_value, exc_traceback)

        if exc_traceback:
            pdb.post_mortem(exc_traceback)

        return exception




class FileHandler(logging.FileHandler):

    def __init__(self, filename=None, level=None, fmt=None, dtfmt=None):
        super(FileHandler, self).__init__(filename)

        self.fn                             = filename                                   # File name (full path)
        self.fmt                            = fmt                                        # Formatter
        self.dtfmt                          = dtfmt                                      # Datetime Fommater
        self.logLevel                       = level                                      # Log level
        self.update()

    def get_formatter(self):
        return OneLineExceptionFormatter(self.fmt, self.dtfmt)

    def set_filename(self, filename):
        self.fn                             = filename
        self.update()

    def set_formatter(self, formatter):
        self.fmt                            = formatter
        self.update()

    def set_lever(self, level):
        self.logLevel                       = level
        self.update()

    def update(self):
        self.setFormatter(self.get_formatter())
        self.setLevel(self.logLevel)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/16/2020 - 7:48 PM
# © 2017 - 2019 DAMGteam. All rights reserved