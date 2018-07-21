# -*- coding: utf-8 -*-
"""

Script Name: _format.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""

from PyQt5.QtCore import QDateTime, QSettings

# -------------------------------------------------------------------------------------------------------------

LOG_FORMAT = dict(

    fullOpt = "%(asctime)s: %(filename)s: %(levelname)s: %(funcName)s: line %(lineno)s: %(message)s",
    rlm = "{relativeCreated:d} [levelname}: {message}",
    tlm1 = "{asctime:[{lvelname}: :{message}",
    tnlm1 = "%(asctime)s  %(name)-22s  %(levelname)-8s %(message)s",
    tlm2 = '%(asctime)s|%(levelname)s|%(message)s|',
    tnlm2 = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
)

DT_FORMAT = dict(
    dmyhms = "%d/%m/%Y %H:%M:%S",
    mdhm = "'%m-%d %H:%M'",
    fullOpt = '(%d/%m/%Y %H:%M:%S)',
)

ST_FORMAT = dict(
    ini = QSettings.IniFormat,
    native = QSettings.NativeFormat,
    invalid = QSettings.InvalidFormat,
)

# datestamp

datetTimeStamp = QDateTime.currentDateTime().toString("hh:mm - dd MMMM yy")

IMGEXT = "All Files (*);;Img Files (*.jpg);;Img Files (*.png)"

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 15/06/2018 - 7:38 PM
# © 2017 - 2018 DAMGteam. All rights reserved