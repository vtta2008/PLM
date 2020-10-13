# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import enum, json



fmt = dict (
    NOTSET   = '%(name)s:[%(levelname)s]:: >>> %(msg)s <<< %(module)s:%(funcName)s:line %(lineno)s::%(asctime)s',
    DEBUG    = '%(name)s:[%(levelname)s]:: """ %(msg)s """ %(module)s:%(funcName)s:line %(lineno)s::%(asctime)s',
    INFO     = '%(name)s:[%(levelname)s]:: """ %(msg)s """ %(module)s:%(funcName)s:line %(lineno)s::%(asctime)s',
    TRACE    = '%(name)s:[%(levelname)s]:: """ %(msg)s """ %(module)s:%(funcName)s:line %(lineno)s::%(asctime)s',
    WARNING  = '%(name)s:[%(levelname)s]:: """ %(msg)s """ %(module)s:%(funcName)s:line %(lineno)s::%(asctime)s',
    ERROR    = '%(name)s:[%(levelname)s]::%(asctime)s::\n -> %(msg)s \n %(module)s:%(funcName)s:line %(lineno)s',
    CRITICAL = '%(name)s:[%(levelname)s]:: """ %(msg)s """ %(module)s:%(funcName)s:line %(lineno)s::%(asctime)s',
    )

datefmt     = dict (
                    NOTSET   = "%d/%m/%Y %H:%M:%S",
                    DEBUG    = "%d/%m/%Y %H:%M:%S",
                    INFO     = "%d/%m/%Y %H:%M:%S",
                    TRACE    = "%d/%m/%Y %H:%M:%S",
                    WARNING  = "%d/%m/%Y %H:%M:%S",
                    ERROR    = "%d/%m/%Y %H:%M:%S",
                    CRITICAL = "%d/%m/%Y %H:%M:%S",
                  )


logColors      = { 'NOTSET': 'gray',
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'TRACE': 'yellow',
                    'WARNING': 'red',
                    'ERROR': 'red',
                    'CRITICAL': 'purple',}

secondLogColors = {
                        'name': {
                            'NOTSET': 'gray',
                            'DEBUG': 'red',
                            'INFO': 'red',
                            'TRACE': 'yellow',
                            'WARNING': 'red',
                            'ERROR': 'red',
                            'CRITICAL': 'red',
                        },
                        'message': {
                            'NOTSET': 'gray',
                            'DEBUG': 'blue',
                            'INFO': 'blue',
                            'TRACE': 'yellow',
                            'WARNING': 'blue',
                            'ERROR': 'blue',
                            'CRITICAL': 'purple',
                        }
                    }


logColorOpts  = {'fmt': fmt,
                'datefmt': datefmt,
                'style': ['%', '{', '$'],
                'logColors': logColors,
                'reset': [True, False],
                'secondLogColors': secondLogColors}


class Encoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, set):
            return tuple(obj)

        return super(Encoder, self).default(obj)


class StyleMessage(object):

    def __init__(self, title, message, **kwargs):
        super(StyleMessage, self).__init__()
        self.title                  = title
        self.message                = message
        self.kwargs                 = kwargs

    def __str__(self):
        s = Encoder().encode(self.kwargs)
        return '{0}: >>> {1} >>> {2}'.format(self.title, self.message, s)



class LogLevel(enum.IntEnum):

    Silent                          = 0
    Debug                           = 10
    Normal                          = 20
    Trace                           = 30
    Error                           = 40
    Critical                        = 50

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


COLORS                              = ['black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white']


COLOR_ESCAPES                       = {color: '\033[{}m'.format(i) for i, color in enumerate(COLORS, start=30)}


RESET_ESCAPE                        = '\033[0m'


TextFullOpt                         = "%(levelname)s: %(asctime)s %(name)s, line %(lineno)s: %(message)s"
TextRelative                        = "(relativeCreated:d) (levelname): (message)"
TextSimple1                         = "{asctime:[{lvelname}: :{message}"
TextSimple2                         = '%(asctime)s|%(levelname)s|%(message)s|'
TextDistance1                       = "%(asctime)s  %(name)-22s  %(levelname)-8s %(message)s"
TextDistance2                       = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'

NOTSET                              = '%(log_color)s%(msg)s (%(module)s:%(lineno)d)'
DEBUG                               = '%(log_color)s %(levelname)s::%(reset)s %(log_color)s[%(name)s]: \n line %(lineno)s >>> %(reset)s %(message)s \n :: %(asctime)s '
INFO                                = '%(levelname)s: %(asctime)s \n %(name)s, line %(lineno)s: \n %(log_color)s%(msg)s \n (%(module)s:%(lineno)d)'
TRACE                               = '%(log_color)s[%(name)s]:  %(log_color)s%(msg)s :: line %(lineno)s'
WARNING                             = '%(log_color)sWARN: %(msg)s (%(module)s:%(lineno)d)'
ERROR                               = '%(log_color)sERROR: %(msg)s (%(module)s:%(lineno)d)'
CRITICAL                            = '%(log_color)sCRIT: %(msg)s (%(module)s:%(lineno)d)'


mdHM                                = "'%m-%d %H:%M'"



plainText = "%(levelname)s: %(asctime)s %(name)s, line %(lineno)s: %(message)s"

fmt1                                = { 'NOTSET': '%(log_color)s%(msg)s (%(module)s:%(lineno)d)',
                                        'DEBUG': '%(log_color)s %(levelname)s::%(reset)s %(log_color)s[%(name)s]: \n line %(lineno)s >>> %(reset)s %(message)s \n :: %(asctime)s ',
                                        'INFO': '%(levelname)s: %(asctime)s \n %(name)s, line %(lineno)s: \n %(log_color)s%(msg)s \n (%(module)s:%(lineno)d)' ,
                                        'TRACE': '%(log_color)s[%(name)s]:  %(log_color)s%(msg)s :: line %(lineno)s',
                                        'WARNING': '%(log_color)sWARN: %(msg)s (%(module)s:%(lineno)d)',
                                        'ERROR': '%(log_color)sERROR: %(msg)s (%(module)s:%(lineno)d)',
                                        'CRITICAL': '%(log_color)sCRIT: %(msg)s (%(module)s:%(lineno)d)',}


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
