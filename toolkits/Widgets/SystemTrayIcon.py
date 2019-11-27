# -*- coding: utf-8 -*-
"""

Script Name: SystemTrayIcon.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtWidgets                        import QSystemTrayIcon

from toolkits                               import getCopyright, getSetting, getSignals, Loggers
from toolkits.Widgets                       import AppIcon

class SystemTrayIcon(QSystemTrayIcon):

    Type                                    = 'DAMGUI'
    key                                     = 'SystemTrayIcon'
    _name                                   = 'DAMG System Tray Icon'
    _copyright                              = getCopyright()
    _data                                   = dict()

    def __init__(self, parent=None):
        super(SystemTrayIcon, self).__init__(parent)

        self.parent = parent
        self.signals = getSignals(self)
        self.logger = Loggers(self.__class__.__name__)
        self.settings = getSetting(self)

        self.setWindowTitle(self.key)
        self.setWindowIcon(AppIcon(32, self.key))

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key):
        return self.settings.initValue(key, self.key)

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
# Created by panda on 27/10/2019 - 7:51 PM
# © 2017 - 2018 DAMGteam. All rights reserved