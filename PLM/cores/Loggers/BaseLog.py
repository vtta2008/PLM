# -*- coding: utf-8 -*-
"""

Script Name: BaseLog.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import json
import enum

class Encoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, set):
            return tuple(o)

        return super(Encoder, self).default(o)


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


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/16/2020 - 7:52 PM
# © 2017 - 2019 DAMGteam. All rights reserved