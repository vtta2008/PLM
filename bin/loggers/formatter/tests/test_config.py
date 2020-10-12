# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:

    Test using colorlog with logging.config

"""
# -------------------------------------------------------------------------------------------------------------

import logging
import logging.config
import os.path
import sys

import pytest


def path(filename):
    """Return an absolute path to a file in the current directory."""
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)


def test_build_from_file(test_logger):
    logging.config.fileConfig(path("test_config.ini"))
    test_logger(logging.getLogger(), lambda l: ':test_config.ini' in l)


@pytest.mark.skipif(sys.version_info < (2, 7), reason="requires python2.7")
def test_build_from_dictionary(test_logger):
    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'colored': {
                '()': 'colorlog.ColoredFormatter',
                'fmt':
                    "%(log_color)s%(levelname)s:%(name)s:%(message)s:dict",
            }
        },
        'handlers': {
            'stream': {
                'class': 'logging.StreamHandler',
                'formatter': 'colored',
                'level': 'DEBUG'
            },
        },
        'loggers': {
            '': {
                'handlers': ['stream'],
                'level': 'DEBUG',
            },
        },
    })
    test_logger(logging.getLogger(), lambda l: ':dict' in l)

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
