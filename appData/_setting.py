# -*- coding: utf-8 -*-
"""

Script Name: _setting.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys

# PyQt5
from PyQt5.QtCore import pyqtSignal, QSettings
from PyQt5.QtWidgets import QApplication, QWidget

# Plt
import appData as app
from ui import uirc as rc
from utilities import utils as func

# -------------------------------------------------------------------------------------------------------------
""" Set up Setting """


class _setting(QWidget):

    _settingSig = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(_setting, self).__init__(parent)

        self.appSetting = app.appSetting

        self.buildUI()

    def buildUI(self):
        self.applySetting()

    def applySetting(self):
        pass

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 15/06/2018 - 7:50 PM
# © 2017 - 2018 DAMGteam. All rights reserved