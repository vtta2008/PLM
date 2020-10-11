# -*- coding: utf-8 -*-
"""

Script Name: Formatters.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import logging

# -------------------------------------------------------------------------------------------------------------
""" Fomatter """

def esc(*x):
    return '\033[' + ';'.join(x) + 'm'

escape_codes = {'reset': esc('0'), 'bold': esc('01'), 'thin': esc('02')}

default_log_colors = {'DEBUG': 'white', 'INFO': 'green', 'WARNING': 'yellow', 'ERROR': 'red', 'CRITICAL': 'bold_red',
}

def parse_colors(sequence):
    """Return escape codes from a color sequence."""
    return ''.join(escape_codes[n] for n in sequence.split(',') if n)


class ColoredRecord(object):
    """
    Wraps a LogRecord, adding named escape codes to the internal dict.

    The internal dict is used when formatting the message (by the PercentStyle,
    StrFormatStyle, and StringTemplateStyle classes).
    """

    def __init__(self, record):
        """Add attributes from the escape_codes dict and the record."""
        self.__dict__.update(escape_codes)
        self.__dict__.update(record.__dict__)

        # Keep a reference to the original record so ``__getattr__`` can
        # access functions that are not in ``__dict__``
        self.__record = record

    def __getattr__(self, name):
        return getattr(self.__record, name)



class ColorFormatter(logging.Formatter):
    """
    A formatter that allows colors to be placed in the format string.

    Intended to help in creating more readable logging output.
    """

    key = 'ColorFormatter'

    def __init__(self, textFormat, datetimeFormat, style, log_colors, reset, secondary_log_colors):
        super(ColorFormatter, self).__init__(textFormat, datetimeFormat, style, validate=True)
        """
        Set the format and colors the ColoredFormatter will use.

        The ``fmt``, ``datefmt`` and ``style`` args are passed on to the
        ``logging.Formatter`` constructor.

        The ``secondary_log_colors`` argument can be used to create additional
        ``log_color`` attributes. Each key in the dictionary will set
        ``{key}_log_color``, using the value to select from a different
        ``log_colors`` set.

        :Parameters:
        - fmt (str): The format string to use
        - datefmt (str): A format string for the date
        - log_colors (dict):
            A mapping of log level names to color names
        - reset (bool):
            Implicitly append a color reset to all records unless False
        - style ('%' or '{' or '$'):
            The format style to use. (*No meaning prior to Python 3.2.*)
        - secondary_log_colors (dict):
            Map secondary ``log_color`` attributes. (*New in version 2.6.*)
        """


        self.log_colors = (log_colors if log_colors is not None else default_log_colors)
        self.secondary_log_colors = secondary_log_colors
        self.reset = reset

    def color(self, log_colors, level_name):
        """Return escape codes from a ``log_colors`` dict."""
        return parse_colors(log_colors.get(level_name, ""))

    def format(self, record):
        record = ColoredRecord(record)
        record.log_color = self.color(self.log_colors, record.levelname)

        # Set secondary log colors
        if self.secondary_log_colors:
            for name, log_colors in self.secondary_log_colors.items():
                color = self.color(log_colors, record.levelname)
                setattr(record, name + '_log_color', color)

        message = super(ColorFormatter, self).format(record)

        # Add a reset code to the end of the message
        # (if it wasn't explicitly added in format str)
        if self.reset and not message.endswith(escape_codes['reset']):
            message += escape_codes['reset']

        return message


class DamgFormatter(ColorFormatter):

    """An extension of ColoredFormatter that uses per-level format strings."""

    key = 'DamgFormatter'

    def __init__(self, textFormat=None, datetimeFormat=None, style='%', log_colors=None, reset=True, secondary_log_colors=None):
        """
        Set the per-loglevel format that will be used.

        Supports fmt as a dict. All other args are passed on to the
        ``colorlog.ColoredFormatter`` constructor.

        :Parameters:
        - fmt (dict):
            A mapping of log levels (represented as strings, e.g. 'WARNING') to
            different formatters. (*New in version 2.7.0)
        (All other parameters are the same as in colorlog.ColoredFormatter)

        Example:

        formatter = colorlog.LevelFormatter(fmt={
            'DEBUG':'%(log_color)s%(msg)s (%(module)s:%(lineno)d)',
            'INFO': '%(log_color)s%(msg)s',
            'WARNING': '%(log_color)sWARN: %(msg)s (%(module)s:%(lineno)d)',
            'ERROR': '%(log_color)sERROR: %(msg)s (%(module)s:%(lineno)d)',
            'CRITICAL': '%(log_color)sCRIT: %(msg)s (%(module)s:%(lineno)d)',
        })
        """

        super(DamgFormatter, self).__init__(textFormat, datetimeFormat, style, log_colors, reset, secondary_log_colors)

        self.style = style
        self.textFormat = textFormat

    def format(self, record):
        """Customize the message format based on the log level."""

        if isinstance(self.textFormat, dict):
            self._textFormat = self.textFormat[record.levelname]
            if self.style not in logging._STYLES:
                raise ValueError('Style must be one of {0}'.format(','.join(logging._STYLES.keys())))


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/16/2020 - 7:44 PM
# © 2017 - 2019 DAMGteam. All rights reserved