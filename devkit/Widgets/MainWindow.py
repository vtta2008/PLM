# -*- coding: utf-8 -*-
"""

Script Name: MainWindow.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import __copyright__

""" Import """

# PyQt5
from PyQt5.QtWidgets                        import QMainWindow

# PLM
from devkit.Widgets                       import AppIcon
from cores.Loggers                          import Loggers
from cores.Settings                         import Settings
from cores.SignalManager                    import SignalManager

# -------------------------------------------------------------------------------------------------------------
""" Main window layout preset """

class MainWindow(QMainWindow):

    Type                        = 'DAMGUI'
    key                         = 'MainWindow'
    _name                       = 'DAMG Main Window'
    _copyright                  = __copyright__()
    _data                       = dict()

    def __init__(self, parent=None):
        QMainWindow.__init__(self)

        self.parent             = parent
        self.settings           = Settings(self)
        self.signals            = SignalManager(self)
        self.logger             = Loggers(self.__class__.__name__)

        self.setWindowTitle(self.key)
        self.setWindowIcon(AppIcon(32, self.key))

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key, decode=None):
        if decode is None:
            return self.settings.initValue(key, self.key)
        else:
            return self.settings.initValue(key, self.key, decode)

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 25/10/2019 - 12:38 PM
# © 2017 - 2018 DAMGteam. All rights reserved