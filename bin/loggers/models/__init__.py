# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import


from .formatters import escape_codes, default_log_colors, ColoredFormatter, DamgFormatter, TTYColoredFormatter
from .logging import basicConfig, root, getLogger, log, debug, info, warning, error, exception, critical, StreamHandler
from .handlers import DamgHandler
from .logger import DamgLogger


__all__ = ('ColoredFormatter', 'default_log_colors', 'escape_codes', 'basicConfig', 'root', 'getLogger', 'debug',
           'info', 'warning', 'error', 'exception', 'critical', 'log', 'exception', 'DamgLogger', 'StreamHandler',
           'DamgFormatter', 'TTYColoredFormatter', 'DamgHandler')


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
