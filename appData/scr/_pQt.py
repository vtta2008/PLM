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

PATTERN_SOLID = Qt.SolidPattern
LINE_SOLID = Qt.SolidLine

MOUSEBTN = Qt.MouseButton
MOUSE_LEFT = Qt.LeftButton
MOUSE_RIGHT = Qt.RightButton
MOUSE_MIDDLE = Qt.MiddleButton

CURSOR_SIZEALL = Qt.SizeAllCursor

KEYBOARD = Qt.Key
KEY_ALT = Qt.Key_Alt
KEY_DEL = Qt.Key_Delete
KEY_TAB = Qt.Key_Tab

# Brush: painter.setBrush()
BRUSH_NONE = Qt.NoBrush
PEN_NONE = Qt.NoPen
ARROW_NONE = Qt.NoArrow
CURSOR_ARROW = Qt.ArrowCursor

RELATIVE_SIZE = Qt.RelativeSize

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