# -*- coding: utf-8 -*-
"""

Script Name: settingFormats.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtCore import QSettings, QDateTime

# -------------------------------------------------------------------------------------------------------------
""" Format """

ST_FORMAT = dict(   ini       = QSettings.IniFormat,
                    native    = QSettings.NativeFormat,
                    invalid   = QSettings.InvalidFormat, )

datetTimeStamp = QDateTime.currentDateTime().toString("hh:mm - dd MMMM yy")             # datestamp

IMGEXT = "All Files (*);;Img Files (*.jpg);;Img Files (*.png)"

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 23/10/2019 - 2:50 AM
# © 2017 - 2018 DAMGteam. All rights reserved