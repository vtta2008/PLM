# -*- coding: utf-8 -*-
"""

Script Name: settingFormats.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtCore import QSettings, QDateTime

INI = QSettings.IniFormat
Native = QSettings.NativeFormat
Invalid = QSettings.InvalidFormat

# -------------------------------------------------------------------------------------------------------------
""" Format """

LOG_FORMAT = dict(

    fullOpt                 = "%(levelname)s: %(asctime)s %(name)s, line %(lineno)s: %(message)s",
    rlm                     = "(relativeCreated:d) (levelname): (message)",
    tlm1                    = "{asctime:[{lvelname}: :{message}",
    tnlm1                   = "%(asctime)s  %(name)-22s  %(levelname)-8s %(message)s",
    tlm2                    = '%(asctime)s|%(levelname)s|%(message)s|',
    tnlm2                   = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
)

DT_FORMAT = dict(

    dmyhms                  = "%d/%m/%Y %H:%M:%S",
    mdhm                    = "'%m-%d %H:%M'",
    fullOpt                 = '(%d/%m/%Y %H:%M:%S)',
)

ST_FORMAT = dict(

    ini                     = INI,
    native                  = Native,
    invalid                 = Invalid,
)

datetTimeStamp = QDateTime.currentDateTime().toString("hh:mm - dd MMMM yy")             # datestamp

IMGEXT = "All Files (*);;Img Files (*.jpg);;Img Files (*.png)"

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 23/10/2019 - 2:50 AM
# © 2017 - 2018 DAMGteam. All rights reserved