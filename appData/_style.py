# -*- coding: utf-8 -*-
"""

Script Name: style.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PyQt5
from PyQt5.QtCore import QSize, Qt, QDateTime
from PyQt5.QtWidgets import QSizePolicy, QFrame

# ----------------------------------------------------------------------------------------------------------- #
""" PyQt5 setting """

# String
TXT = "No Text"                                                                     # String by default

# Value, Nummber, Float, Int ...
UNIT = 60                                                                           # Base Unit
MARG = 5                                                                            # Content margin
BUFF = 10                                                                           # Buffer size
SCAL = 1                                                                            # Scale value
STEP = 1                                                                            # Step value changing
VAL = 1                                                                             # Default value
MIN = 0                                                                             # Minimum value
MAX = 1000                                                                          # Maximum value
WMIN = 50                                                                           # Minimum width
HMIN = 20                                                                           # Minimum height
HFIX = 80
ICONSIZE = 32
ICONBUFFER = -1
BTNICONSIZE = QSize(ICONSIZE, ICONSIZE)
ICONBTNSIZE = QSize(ICONSIZE+ICONBUFFER, ICONSIZE+ICONBUFFER)

keepARM = Qt.KeepAspectRatio
ignoreARM = Qt.IgnoreAspectRatio

scrollAsNeed = Qt.ScrollBarAsNeeded
scrollOff = Qt.ScrollBarAlwaysOff
scrollOn = Qt.ScrollBarAlwaysOn

# Size policy
SiPoMin = QSizePolicy.Minimum
SiPoMax = QSizePolicy.Maximum
SiPoExp = QSizePolicy.Expanding
SiPoPre = QSizePolicy.Preferred
SiPoIgn = QSizePolicy.Ignored

frameStyle = QFrame.Sunken | QFrame.Panel

# Alignment
center = Qt.AlignCenter
right = Qt.AlignRight
left = Qt.AlignLeft
hori = Qt.Horizontal
vert = Qt.Vertical

# Docking area
dockL = Qt.LeftDockWidgetArea
dockR = Qt.RightDockWidgetArea
dockT = Qt.TopDockWidgetArea
dockB = Qt.BottomDockWidgetArea

# datestamp

datetTimeStamp = QDateTime.currentDateTime().toString("hh:mm - dd MMMM yy")

__imgExt = "All Files (*);;Img Files (*.jpg);;Img Files (*.png)"

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 14/06/2018 - 9:58 PM
# © 2017 - 2018 DAMGteam. All rights reserved