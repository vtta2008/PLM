# -*- coding: utf-8 -*-
"""

Script Name: pPainter.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys, uuid

# PyQt5
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QFontMetrics, QFont


# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

from appData.config import logger

# -------------------------------------------------------------------------------------------------------------

def getTextSize(text, painter=None):

    if not painter:
        metrics = QFontMetrics(QFont())
    else:
        metrics = painter.fontMetrics()
    size = metrics.size(Qt.TextSingleLine, text)
    return size





# -------------------------------------------------------------------------------------------------------------
# Created by panda on 17/06/2018 - 6:46 PM
# © 2017 - 2018 DAMGteam. All rights reserved