# -*- coding: utf-8 -*-
"""

Script Name: logger.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import unicode_literals
""" Import """

# Python
import sys, os, logging, json, enum, traceback, linecache, pdb, collections, copy
import html as pyhtml

# PLM
from appData            import LOCAL_LOG, LOG_FORMAT, DT_FORMAT

COLORS                  = ['black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white']
COLOR_ESCAPES           = {color: '\033[{}m'.format(i) for i, color in enumerate(COLORS, start=30)}
RESET_ESCAPE            = '\033[0m'
LOG_COLORS              = {'VDEBUG': 'white',
                           'DEBUG': 'white',
                           'INFO': 'green',
                           'WARNING': 'yellow',
                           'ERROR': 'red',
                           'CRITICAL': 'red',}

VDEBUG_LEVEL            = 9

# -------------------------------------------------------------------------------------------------------------
""" utils """

class Encoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, set):
            return tuple(o)

        return super(Encoder, self).default(o)


class StyleMessage(object):

    def __init__(self, message, **kwargs):
        super(StyleMessage, self).__init__()
        self.message = message
        self.kwargs = kwargs

    def __str__(self):
        s = Encoder().encode(self.kwargs)
        return 'message: >>> {0} >>> {1}'.format(self.message, s)


class LogLevel(enum.IntEnum):

    Silent   = 0
    Debug    = 10
    Normal   = 20
    Trace    = 30
    Error    = 40
    Critical = 50

    @classmethod
    def getbyname(cls, name):
        lookup = { level.name.lower(): level for level in cls }
        return lookup[name.lower()]

    @classmethod
    def getnames(cls):
        levels = list(cls)
        levels.sort(key = lambda level: int(level))
        return [ level.name for level in levels ]

    @classmethod
    def getbyverbosity(cls, intvalue):
        maxvalue = max(int(level) for level in cls)
        if intvalue > maxvalue:
            intvalue = maxvalue
        return cls(intvalue)


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
            setattr(record_clone, field, pyhtml.escape(data))
        msg = super().format(record_clone)
        if not msg.endswith(self._colordict['reset']):
            msg += self._colordict['reset']
        return msg

    def formatTime(self, record, datefmt):
        out = super().formatTime(record, datefmt)
        return pyhtml.escape(out)

# -------------------------------------------------------------------------------------------------------------
""" Handler """

class Stream_Handler(logging.StreamHandler):

    def __init__(self, level=None, fmt=None, dtfmt=None):
        super(Stream_Handler, self).__init__(sys.stdout)

        sys.excepthook = self.exception_handler

        self.fmt      = fmt                     # Formatter
        self.dtfmt    = dtfmt                   # Datetime Fommater
        self.logLevel = level                   # Log level

        self.setFormatter(self.get_formatter())
        self.setLevel(self.logLevel)

    def get_formatter(self):
        return logging.Formatter(self.fmt, self.dtfmt)

    def exception_handler(self, exc_type, exc_value, tb):

        if hasattr(sys, 'ps1') or not sys.stderr.isatty():
            exception = sys.__excepthook__(exc_type, exc_value, tb)
        else:
            exception = traceback.format_exception(exc_type, exc_value, tb)

        if tb is None:
            pass
        else:
            pdb.post_mortem(tb)

        return exception


class File_Handler(logging.FileHandler):

    def __init__(self, filename=None, level=None, fmt=None, dtfmt=None):
        super(File_Handler, self).__init__(filename)

        self.fn       = filename                                                # File name (full path)
        self.fmt      = fmt                                                     # Formatter
        self.dtfmt    = dtfmt                                                   # Datetime Fommater
        self.logLevel = level                                                   # Log level

        self.setFormatter(self.get_formatter())
        self.setLevel(self.logLevel)

    def get_formatter(self):
        return OneLineExceptionFormatter(self.fmt, self.dtfmt)


# -------------------------------------------------------------------------------------------------------------
""" Logger """


class Loggers(logging.Logger):

    key = 'PLM super logger'

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

        self.sh = Stream_Handler(self.logLevel, self.fmt, self.dtfmt)
        self.fh = File_Handler(self.fn, self.logLevel, self.fmt, self.dtfmt)
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
        return

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 15/06/2018 - 6:49 PM
# © 2017 - 2018 DAMGteam. All rights reserved