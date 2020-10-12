# -*- coding: utf-8 -*-
"""

Script Name: Formatters.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

    The ColoredFormatter class.

"""
# -------------------------------------------------------------------------------------------------------------

import sys
import logging
from .excape_codes        import escape_codes, parse_colors


# The default colors to use for the debug levels
default_log_colors = {'DEBUG': 'white', 'INFO': 'green', 'WARNING': 'yellow', 'ERROR': 'red', 'CRITICAL': 'bold_red', }


# The default fmt to use for each style
default_formats = {'%': '%(log_color)s%(levelname)s:%(name)s:%(message)s',
                   '{': '{log_color}{levelname}:{name}:{message}',
                   '$': '${log_color}${levelname}:${name}:${message}'}


class ColoredRecord(object):

    """
    Wraps a LogRecord, adding named escape codes to the internal dict.

    The internal dict is used when formatting the message (by the PercentStyle,
    StrFormatStyle, and StringTemplateStyle classes).
    """

    def __init__(self, record):
        """ Add attributes from the escape_codes dict and the record."""
        self.__dict__.update(escape_codes)
        self.__dict__.update(record.__dict__)

        # Keep a reference to the original record so ``__getattr__`` can
        # access functions that are not in ``__dict__``
        self.__record = record

    def __getattr__(self, name):
        return getattr(self.__record, name)


class ColoredFormatter(logging.Formatter):

    """
    A formatter that allows colors to be placed in the fmt string.

    Intended to help in creating more readable logging output.
    """

    key                                 = 'ColoredFormatter'


    def __init__(self, fmt=None, datefmt=None, style='%', logColors=None, reset=True, secondLogColors=None):
        """
        Set the fmt and colors the ColoredFormatter will use.

        The ``fmt``, ``datefmt`` and ``style`` args are passed on to the
        ``logging.Formatter`` constructor.

        secondLogColors argument can be used to create additional
        log_color attributes. Each key in the dictionary will set
        {key}_log_color, using the value to select from a different
        logColors set.

        :Parameters:
        - fmt (str): The fmt string to use
        - datefmt (str): A fmt string for the date
        - logColors (dict): A mapping of log level names to color names
        - reset (bool): Implicitly append a color reset to all records unless False
        - style ('%' or '{' or '$'): The fmt style to use.
        - secondLogColors (dict): Map secondary ``log_color`` attributes.
        """

        if fmt is None:
            if sys.version_info > (3, 2):
                fmt = default_formats[style]
            else:
                fmt = default_formats['%']

        if sys.version_info > (3, 8) and isinstance(self, ColoredFormatter) and isinstance(fmt, dict):
            super(ColoredFormatter, self).__init__(fmt, datefmt, style, validate=False)
        elif sys.version_info > (3, 2):
            super(ColoredFormatter, self).__init__(fmt, datefmt, style)
        else:
            logging.Formatter.__init__(self, fmt, datefmt)

        self.fmt                    = fmt
        self.dtfmt                  = datefmt
        self.style                  = style

        self.logColors              = (logColors if logColors is not None else default_log_colors)
        self.secondLogColors        = secondLogColors
        self.reset                  = reset

    def color(self, log_colors, level_name):
        """Return escape codes from a ``logColors`` dict."""
        return parse_colors(log_colors.get(level_name, ""))

    def format(self, record):
        record                      = ColoredRecord(record)
        record.log_color            = self.color(self.logColors, record.levelname)

        # Set secondary log colors
        if self.secondLogColors:
            for name, log_colors in self.secondLogColors.items():
                color = self.color(log_colors, record.levelname)
                setattr(record, name + '_log_color', color)

        # Format the message
        if sys.version_info > (2, 7):
            message = super(ColoredFormatter, self).format(record)
        else:
            message = logging.Formatter.format(self, record)

        # Add a reset code to the end of the message
        # (if it wasn't explicitly added in fmt str)
        if self.reset and not message.endswith(escape_codes['reset']):
            message += escape_codes['reset']

        return message



class DamgFormatter(ColoredFormatter):

    """An extension of ColoredFormatter that uses per-level fmt strings."""

    key                             = 'DamgFormatter'


    def __init__(self, fmt, datefmt, style='%', logColors={}, reset=True, secondLogColors={}):

        """
        Set the per-loglevel fmt that will be used.

        Supports fmt as a dict. All other args are passed on to the
        ``colorlog.ColoredFormatter`` constructor.

        :Parameters:
        - fmt (dict): A mapping of log levels (represented as strings, e.g. 'WARNING') to different formatters.
        - datefmt (str): A fmt string for the date
        - logColors (dict): A mapping of log level names to color names
        - reset (bool): Implicitly append a color reset to all records unless False
        - style ('%' or '{' or '$'): The fmt style to use.
        - secondLogColors (dict): Map secondary ``log_color`` attributes.

        Example:

        formatter = colorlog.LevelFormatter(fmt={
            'DEBUG':'%(log_color)s%(msg)s (%(module)s:%(lineno)d)',
            'INFO': '%(log_color)s%(msg)s',
            'WARNING': '%(log_color)sWARN: %(msg)s (%(module)s:%(lineno)d)',
            'ERROR': '%(log_color)sERROR: %(msg)s (%(module)s:%(lineno)d)',
            'CRITICAL': '%(log_color)sCRIT: %(msg)s (%(module)s:%(lineno)d)',
        })
        """
        self.formats = fmt
        self.dateformats = datefmt

        fmt = default_formats[style]

        super(DamgFormatter, self).__init__(fmt, datefmt, style, logColors, reset, secondLogColors)


        self.datefmt                = None
        self._fmt                   = None
        self.style                  = style
        self.logColors              = logColors
        self.reset                  = reset
        self.secondLogColor         = secondLogColors

    def format(self, record):

        """Customize the message format based on the log level."""
        self._fmt                   = self.formats.get(record.levelname)
        self.datefmt                = self.dateformats.get(record.levelname)

        if self.style not in logging._STYLES:
            raise ValueError('Style must be one of: %s' % ','.join(logging._STYLES.keys()))

        self._style                 = logging._STYLES[self.style][0](self._fmt)
        self._fmt                   = self._style._fmt

        return super(DamgFormatter, self).format(record)


class TTYColoredFormatter(ColoredFormatter):

    """
    Blanks all color codes if not running under a TTY.

    This is useful when you want to be able to pipe colorlog output to a file.
    """

    def __init__(self, *args, **kwargs):
        """Overwrite the `reset` argument to False if stream is not a TTY."""
        self.stream = kwargs.pop('stream')

        # Both `reset` and `isatty` must be true to insert reset codes.
        kwargs['reset'] = kwargs.get('reset', True) and self.stream.isatty()

        ColoredFormatter.__init__(self, *args, **kwargs)

    def color(self, log_colors, level_name):
        """Only returns colors if STDOUT is a TTY."""
        if not self.stream.isatty():
            log_colors = {}
        return ColoredFormatter.color(self, log_colors, level_name)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/16/2020 - 7:44 PM
# © 2017 - 2019 DAMGteam. All rights reserved