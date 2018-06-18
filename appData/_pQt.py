# -*- coding: utf-8 -*-
"""

Script Name: _Qtopts.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
import os
from PyQt5.QtCore import Qt

windows = os.name == "nt"
DMK = Qt.AltModifier if windows else Qt.ControlModifier

MOUSEBTN = Qt.MouseButton
MOUSELEFTBTN = Qt.LeftButton
MOUSERIGHTBTN = Qt.RightButton
MOUSEMIDDLEBTN = Qt.MiddleButton

SIZEALLCURSOR = Qt.SizeAllCursor

KEYBOARD = Qt.Key
ALTKEY = Qt.Key_Alt
DELKEY = Qt.Key_Delete
TABKEY = Qt.Key_Tab

# Brush: painter.setBrush()
NOBRUSH = Qt.NoBrush
NOPEN = Qt.NoPen
NOARROW = Qt.NoArrow
ARROWCUSOR = Qt.ArrowCursor

RELATIVESIZE = Qt.RelativeSize

# Gradient: QLinearGradient().setColorAt()
WHITE = Qt.white
LIGHTGRAY = Qt.lightGray
GRAY = Qt.gray
DARKGRAY = Qt.darkGray
BLACK = Qt.black

# RGB
RED = Qt.red
GREEN = Qt.green
BLUE = Qt.blue

DARKRED = Qt.darkGreen
DARKGREEN = Qt.darkGreen
DARKBLUE = Qt.darkBlue

# CMYK
CYAN = Qt.cyan
MAGENTA = Qt.magenta
YELLOW = Qt.yellow

DARKCYAN = Qt.darkCyan
DARKMAGENTA = Qt.darkMagenta
DARKYELLOW = Qt.darkYellow

SCROLLBAROFF = Qt.ScrollBarAlwaysOff
SCROLLBARON = Qt.ScrollBarAlwaysOn
SCROLLBARNEED = Qt.ScrollBarAsNeeded

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 18/06/2018 - 4:27 AM
# © 2017 - 2018 DAMGteam. All rights reserved