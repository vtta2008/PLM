# -*- coding: utf-8 -*-
"""

Script Name: _format.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""

from PyQt5.QtCore import QDateTime

# -------------------------------------------------------------------------------------------------------------

LOG_FORMAT = dict(

    fullOpt = "{asctime:-15s}: %{name:-18s}[{levelname:-8s}] - %{module:-15s} - %{funcName:-20s} - %{lineno:-6d} - %{message}",
    rlm = "{relativeCreated:d} [levelname}: {message}",
    tlm1 = "{asctime:[{lvelname}: :{message}",
    tnlm1 = "%(asctime)s  %(name)-22s  %(levelname)-8s %(message)s",
    tlm2 = '%(asctime)s|%(levelname)s|%(message)s|',
    tnlm2 = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
)

DT_FORMAT = dict(
    dmyhms = "%d/%m/%Y %H:%M:%S",
    mdhm = "'%m-%d %H:%M'",
    fullOpt = "hh:mm - dd MMMM yy",
)

# datestamp

datetTimeStamp = QDateTime.currentDateTime().toString("hh:mm - dd MMMM yy")

IMGEXT = "All Files (*);;Img Files (*.jpg);;Img Files (*.png)"

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 15/06/2018 - 7:38 PM
# © 2017 - 2018 DAMGteam. All rights reserved