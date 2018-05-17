#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: uirc.py
Author: Do Trinh/Jimmy - 3D artist.
Description: This script is the place for every ui elements

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys, os
import json
import subprocess
from functools import partial

# PyQt5
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QSettings
from PyQt5.QtGui import QIntValidator, QFont, QIcon
from PyQt5.QtWidgets import (QFrame, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout, QWidget, QSizePolicy, QSlider,
                             QLineEdit, QPushButton, QAction)

# Plt
import appData as app
from utilities import utils as func

# -------------------------------------------------------------------------------------------------------------
""" Variables """

# String
TXT = "No Text" # String by default

# Value, Nummber, Float, Int ...
UNIT = 60   # Base Unit
MARG = 5    # Content margin
BUFF = 10   # Buffer size
SCAL = 1    # Scale value
STEP = 1    # Step value changing
VAL = 1     # Default value
MIN = 0     # Minimum value
MAX = 1000  # Maximum value
WMIN = 50   # Minimum width
HMIN = 20   # Minimum height
ICON_SIZE = 30
ICON_BUFFRATE = 10
ICON_BUFFREGION = -1
ICON_BUFF = ICON_BUFFREGION*(ICON_SIZE*ICON_BUFFRATE/100)
ICON_SET_SIZE = QSize(ICON_SIZE + ICON_BUFF, ICON_SIZE + ICON_BUFF)

# Alignment
ALGC = Qt.AlignCenter
ALGR = Qt.AlignRight
ALGL = Qt.AlignLeft
HORZ = Qt.Horizontal
VERT = Qt.Vertical

# Style
frameStyle = QFrame.Sunken | QFrame.Panel

# Path
pth = os.path.join(os.getenv(app.__envKey__), 'appData', 'config', 'main.json')
with open(pth, 'r') as f:
    APPINFO = json.load(f)

# -------------------------------------------------------------------------------------------------------------

def iconBtn(key):
    iconBtn = QPushButton()
    iconBtn.setToolTip(APPINFO[key][0])
    iconBtn.setIcon(QIcon(APPINFO[key][1]))
    iconBtn.setFixedSize(ICON_SIZE, ICON_SIZE)
    iconBtn.setIconSize(ICON_SET_SIZE)
    iconBtn.clicked.connect(partial(func.openProcess, APPINFO[key][2]))
    return iconBtn

def action(key, parent=None):
    action = QAction(QIcon(func.get_icon(key)), APPINFO[key][0], parent)
    action.setStatusTip(APPINFO[key][1])
    action.triggered.connect(partial(subprocess.Popen, APPINFO[key][2]))
    return action

def Clabel(txt=TXT, wmin=WMIN, alg = None, font=None):
    if alg == None:
        alg = Qt.AlignCenter

    if font == None:
        font = QFont("Arial, 10")

    label = QLabel(txt)
    label.setMinimumWidth(wmin)
    label.setAlignment(alg)
    label.setFont(font)
    return label