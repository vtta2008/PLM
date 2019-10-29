# -*- coding: utf-8 -*-
"""

Script Name: SystemTrayIcon.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtWidgets                        import QSystemTrayIcon

from cores.SignalManager                    import SignalManager
from cores.Loggers                          import Loggers
from cores.Settings                         import Settings
from appData                                import __copyright__, ST_FORMAT, SETTING_FILEPTH

class SystemTrayIcon(QSystemTrayIcon):

    Type                                    = 'DAMGUI'
    key                                     = 'SystemTrayIcon'
    _name                                   = 'DAMG System Tray Icon'
    _copyright                              = __copyright__
    _data                                   = dict()

    def __init__(self, parent=None):
        QSystemTrayIcon.__init__(self)

        self.parent = parent

        self.signals = SignalManager(self)
        self.logger = Loggers(self.__class__.__name__)
        self.settings = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)

    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key):
        return self.settings.initValue(key, self.key)

    @property
    def copyright(self):
        return self._copyright

    @property
    def data(self):
        return self._data

    @property
    def name(self):
        return self._name

    @data.setter
    def data(self, newData):
        self._data                      = newData

    @name.setter
    def name(self, newName):
        self._name                      = newName

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 27/10/2019 - 7:51 PM
# © 2017 - 2018 DAMGteam. All rights reserved