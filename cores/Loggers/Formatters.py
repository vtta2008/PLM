# -*- coding: utf-8 -*-
"""

Script Name: Formatters.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
""" Import """

# Python
import logging, copy, html


COLORS                  = ['black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white']

COLOR_ESCAPES           = {color: '\033[{}m'.format(i) for i, color in enumerate(COLORS, start=30)}

RESET_ESCAPE            = '\033[0m'

LOG_COLORS              = {'VDEBUG': 'white',
                           'DEBUG': 'white',
                           'INFO': 'green',
                           'WARNING': 'yellow',
                           'ERROR': 'red',
                           'CRITICAL': 'red',}



# -------------------------------------------------------------------------------------------------------------
""" Fomatter """


class OneLineExceptionFormatter(logging.Formatter):

    def formatException(self, exc_info):
        """ Format an exception so that it prints on a single line. """
        result = super(OneLineExceptionFormatter, self).formatException(exc_info)

        # or format into one line however you want to
        return repr(result)

    def format(self, record):
        s = super(OneLineExceptionFormatter, self).format(record)
        if record.exc_text:
            s = s.replace('\n', '') + '|'
        return s


class ColoredFormatter(logging.Formatter):

    use_colors = True

    def format(self, record: logging.LogRecord) -> str:
        if self.use_colors:
            color_dict = dict(COLOR_ESCAPES)
            color_dict['reset'] = RESET_ESCAPE
            log_color = LOG_COLORS[record.levelname]
            color_dict['log_color'] = COLOR_ESCAPES[log_color]
        else:
            color_dict = {color: '' for color in COLOR_ESCAPES}
            color_dict['reset'] = ''
            color_dict['log_color'] = ''
        record.__dict__.update(color_dict)
        return super().format(record)


class HTMLFormatter(logging.Formatter):

    _log_colors = LOG_COLORS
    _colordict = dict()

    def __init__(self, fmt, datefmt):
        super().__init__(fmt, datefmt)

        for color in COLORS:
            self._colordict[color] = '<font color="{}">'.format(color)
        self._colordict['reset'] = '</font>'

    def format(self, record):
        record_clone = copy.copy(record)
        record_clone.__dict__.update(self._colordict)
        if record_clone.levelname in self._log_colors:
            color = self._log_colors[record_clone.levelname]
            record_clone.log_color = self._colordict[color]
        else:
            record_clone.log_color = ''
        for field in ['msg', 'filename', 'funcName', 'levelname', 'module', 'name', 'pathname', 'processName', 'threadName']:
            data = str(getattr(record_clone, field))
            setattr(record_clone, field, html.escape(data))
        msg = super().format(record_clone)
        if not msg.endswith(self._colordict['reset']):
            msg += self._colordict['reset']
        return msg

    def formatTime(self, record, datefmt):
        out = super().formatTime(record, datefmt)
        return html.escape(out)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/16/2020 - 7:44 PM
# © 2017 - 2019 DAMGteam. All rights reserved