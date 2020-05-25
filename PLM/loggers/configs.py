# -*- coding: utf-8 -*-
"""

Script Name: BaseLog.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import json, enum



COLORS                              = ['black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white']


COLOR_ESCAPES                       = {color: '\033[{}m'.format(i) for i, color in enumerate(COLORS, start=30)}


RESET_ESCAPE                        = '\033[0m'


LOG_COLORS                          = { 'SILENT': 'gray', 'SPAM': 'white', 'DEBUG': 'cyan', 'VERBOSE': 'purple',
                                        'NORMAL': 'white', 'NOTICE': 'orange', 'TRACE': 'yellow', 'SUCCESS': 'blue',
                                        'ERROR': 'red', 'CRITICAL': 'red', 'FATAL': 'red', 'VDEBUG': 'white',
                                        'WARNING': 'yellow', }

LoggingFullOpt                      = "%(levelname)s: %(asctime)s %(name)s, line %(lineno)s: %(message)s",
LoggingRelative                     = "(relativeCreated:d) (levelname): (message)",
LoggingSimpleFmt1                   = "{asctime:[{lvelname}: :{message}",
LoggingSimpleFmt2                   = '%(asctime)s|%(levelname)s|%(message)s|',
LoggingDistance1                    = "%(asctime)s  %(name)-22s  %(levelname)-8s %(message)s",
LoggingDistance2                    = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'


DATETIME_dmyhms                     = "%d/%m/%Y %H:%M:%S",
DATETIME_mdhm                       = "'%m-%d %H:%M'",
DATETIME_fullOpt                    = '(%d/%m/%Y %H:%M:%S)',



class Encoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, set):
            return tuple(obj)

        return super(Encoder, self).default(obj)


class StyleMessage(object):

    def __init__(self, message, **kwargs):
        super(StyleMessage, self).__init__()
        self.message                = message
        self.kwargs                 = kwargs

    def __str__(self):
        s = Encoder().encode(self.kwargs)
        return 'message: >>> {0} >>> {1}'.format(self.message, s)


class LogLevel(enum.IntEnum):

    Silent                          = 0
    Spam                            = 5
    Debug                           = 10
    Verbose                         = 15
    Normal                          = 20
    Notice                          = 25
    Trace                           = 30
    Success                         = 35
    Error                           = 40
    Critical                        = 45
    Fatal                           = 50

    @classmethod
    def getbyname(cls, name: str):
        lookup = { level.name.lower(): level for level in cls }
        return lookup[name.lower()]

    @classmethod
    def getnames(cls):

        levels                      = list(cls)
        levels.sort(key             = lambda level: int(level))
        return [ level.name for level in levels ]

    @classmethod
    def getbyverbosity(cls, value: int):
        maxvalue = max(int(level) for level in cls)

        if value > maxvalue:
            value = maxvalue

        return cls(value)

logMissings                         = ['spam', 'verbose', 'notice', 'success']


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/16/2020 - 7:52 PM
# © 2017 - 2019 DAMGteam. All rights reserved