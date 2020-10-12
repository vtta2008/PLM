# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:

    Test the colorlog.logging module.

"""
# -------------------------------------------------------------------------------------------------------------
from bin.loggers import models
import logging

# test_logger = models.basicConfig()



def test_logging_module(test_logger):
    test_logger(logging)


def test_colorlog_module(test_logger):
    test_logger(models)


def test_colorlog_basicConfig(test_logger):
    models.basicConfig()
    test_logger(models.getLogger())


# test_logging_module(test_logger=test_logger)



# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
