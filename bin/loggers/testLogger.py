# -*- coding: utf-8 -*-
"""

Script Name: logger.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from bin.loggers.models import DamgFormatter, DamgHandler, DamgLogger


fmtTest1 =          {               'DEBUG':'%(log_color)s%(msg)s (%(module)s:%(lineno)d)',
                                    'INFO': '%(log_color)s%(msg)s',
                                    'WARNING': '%(log_color)sWARN: %(msg)s (%(module)s:%(lineno)d)',
                                    'ERROR': '%(log_color)sERROR: %(msg)s (%(module)s:%(lineno)d)',
                                    'CRITICAL': '%(log_color)sCRIT: %(msg)s (%(module)s:%(lineno)d)', }

fmtTest2 =         ("%(log_color)s%(levelname)s:%(name_log_color)s%(name)s:%(message_log_color)s%(message)s")

fmtTest3 =          "%(reset)s%(log_color)s%(levelname)s:%(name)s:%(message)s"

secondTest1 =       {   'name': {   'DEBUG': 'red',
                                    'INFO': 'red',
                                    'WARNING': 'red',
                                    'ERROR': 'red',
                                    'CRITICAL': 'red',},
                        'message': {'DEBUG': 'blue',
                                    'INFO': 'blue',
                                    'WARNING': 'blue',
                                    'ERROR': 'blue',
                                    'CRITICAL': 'blue',} }


def testLogger1():
    formatter = DamgFormatter()
    handler = DamgHandler()
    handler.setFormatter(formatter)
    handler.setLevel('DEBUG')
    logger = DamgLogger()
    logger.addHandler(handler)
    return logger




logger = testLogger1()

logger.info('text info logging')
logger.warning('test warn logging')
logger.debug('test debug logging')
logger.error('test error logging')
logger.critical('test critical logging')
# logger.trace('test trace logging')

# print(2/0)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 15/06/2018 - 6:49 PM
# © 2017 - 2018 DAMGteam. All rights reserved