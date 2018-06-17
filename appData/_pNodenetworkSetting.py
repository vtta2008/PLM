# -*- coding: utf-8 -*-
"""

Script Name: _setting.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os

# PyQt5
from PyQt5.QtCore import Qt

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 15/06/2018 - 7:50 PM
# © 2017 - 2018 DAMGteam. All rights reserved

# Node network grahphic
windows = os.name == "nt"

FLTR = "flow_left_to_right"
FRTL = "flow_right_to_left"
DMK = Qt.AltModifier if windows else Qt.ControlModifier

LMBTN = Qt.MouseButton.LeftButton
RMBTN = Qt.MouseButton.RightButton