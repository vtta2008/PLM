# -*- coding: utf-8 -*-
"""

Script Name: _format.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""

from PyQt5.QtCore import QDateTime, QSettings

# -------------------------------------------------------------------------------------------------------------

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