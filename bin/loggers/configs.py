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

TextFullOpt                         = "%(levelname)s: %(asctime)s \n %(name)s, line %(lineno)s: \n %(message)s \n"
TextRelative                        = "(relativeCreated:d) (levelname): (message)"
TextSimple1                         = "{asctime:[{lvelname}: :{message}"
TextSimple2                         = '%(asctime)s|%(levelname)s|%(message)s|'
TextDistance1                       = "%(asctime)s  %(name)-22s  %(levelname)-8s %(message)s"
TextDistance2                       = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'

DatetimFullOpt                      = "%d/%m/%Y %H:%M:%S"
DatetimeMDHM                        = "'%m-%d %H:%M'"


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



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/16/2020 - 7:52 PM
# © 2017 - 2019 DAMGteam. All rights reserved