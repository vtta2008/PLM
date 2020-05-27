# -*- coding: utf-8 -*-
"""

Script Name: MainWindow.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from .io_widgets import QMainWindow
from PLM.loggers import Loggers
from PLM.cores.SignalManager import SignalManager
from PLM.settings import AppSettings

# -------------------------------------------------------------------------------------------------------------
""" Main window layout preset """


class MainWindow(QMainWindow):

    Type                        = 'DAMGUI'
    key                         = 'MainWindow'
    _name                       = 'DAMG Main Window'

    _data                       = dict()

    def __init__(self, parent=None):
        QMainWindow.__init__(self)

        self.parent             = parent
        self.settings           = AppSettings(self)
        self.signals            = SignalManager(self)
        self.logger             = Loggers()

        self.setWindowTitle(self.key)

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key, decode=None):
        if decode is None:
            return self.settings.initValue(key, self.key)
        else:
            return self.settings.initValue(key, self.key, decode)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/10/2019 - 12:38 PM
# © 2017 - 2018 DAMGteam. All rights reserved