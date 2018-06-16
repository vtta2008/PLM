# -*- coding: utf-8 -*-
"""

Script Name: _format.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

LOG = dict(

    default = "%(asctime)-15s: %(name)-18s - %(levelname)-8s - %(module)-15s - %(funcName)-20s - %(lineno)-6d - %(message)s",
    logFormat1 = "%(relativeCreated)d %(levelname)s: %(message)s",
    logFormat3 = "%(asctime)s %(levelname)s %(message)s",
    logFormat4 = "%(asctime)s  %(name)-22s  %(levelname)-8s %(message)s",
    logFormat5 = '%(asctime)s|%(levelname)s|%(message)s|',
    logFormat6 = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
)

DATETIME = dict(
    datetime1 = "%d/%m/%Y %H:%M:%S",
    default = "'%m-%d %H:%M'",

)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 15/06/2018 - 7:38 PM
# © 2017 - 2018 DAMGteam. All rights reserved