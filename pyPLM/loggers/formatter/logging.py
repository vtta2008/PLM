# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:

    Wrappers around the logging module.

"""
# -------------------------------------------------------------------------------------------------------------
import functools
import logging

from .colorlog import ColoredFormatter


BASIC_FORMAT = "%(log_color)s%(levelname)s%(reset)s:%(name)s:%(message)s"


def basicConfig(style='%', log_colors=None, reset=True, secondary_log_colors=None, **kwargs):

    """Call ``logging.basicConfig`` and override the formatter it creates."""

    logging.basicConfig(**kwargs)
    logging._acquireLock()

    try:
        stream = logging.root.handlers[0]
        stream.setFormatter(ColoredFormatter(fmt=kwargs.get('fmt', BASIC_FORMAT),
                                             datefmt=kwargs.get('datefmt', None),
                                             style=style, logColors=log_colors, reset=reset,
                                             secondLogColors=secondary_log_colors))
    finally:
        logging._releaseLock()


def ensure_configured(func):

    """Modify a function to call ``basicConfig`` first if no handlers exist."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if len(logging.root.handlers) == 0:
            basicConfig()
        return func(*args, **kwargs)
    return wrapper


root            = logging.root
getLogger       = logging.getLogger

debug           = ensure_configured(logging.debug)
info            = ensure_configured(logging.info)
warning         = ensure_configured(logging.warning)
error           = ensure_configured(logging.error)
critical        = ensure_configured(logging.critical)
log             = ensure_configured(logging.log)
exception       = ensure_configured(logging.exception)

NOTSET          = ensure_configured(logging.NOTSET)
DEBUG           = ensure_configured(logging.DEBUG)
INFO            = ensure_configured(logging.INFO)
WARN            = ensure_configured(logging.WARN)
WARNING         = ensure_configured(logging.WARNING)
ERROR           = ensure_configured(logging.ERROR)
CRITICAL        = ensure_configured(logging.CRITICAL)
FATAL           = ensure_configured(logging.FATAL)

Logger          = logging.Logger
StreamHandler   = logging.StreamHandler
FileHandler     = logging.FileHandler

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
