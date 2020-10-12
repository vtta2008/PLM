# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
from bin.loggers.colorlog import *

def test_exports():
    assert {
        'ColoredFormatter', 'default_log_colors', 'escape_codes',
        'basicConfig', 'root', 'getLogger', 'debug', 'info', 'warning',
        'error', 'exception', 'critical', 'log', 'exception'
    } < set(globals())

test_exports()

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
