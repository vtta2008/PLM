# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:

    Test the colorlog.logging module.

"""
# -------------------------------------------------------------------------------------------------------------
from bin.loggers import colorlog
import logging



def test_logging_module(test_logger):
    test_logger(logging)


def test_colorlog_module(test_logger):
    test_logger(colorlog)


def test_colorlog_basicConfig(test_logger):
    colorlog.basicConfig()
    test_logger(colorlog.getLogger())


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
