# -*- coding: utf-8 -*-
"""

Script Name: SystemTrayIcon.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PyQt5
from PLM                                    import __copyright__
from PLM.api                                import QSystemTrayIcon
from PLM.ui.framework.Gui import AppIcon
from PLM.cores                              import Loggers
from PLM.plugins.SignalManager              import SignalManager
from PLM.data.SettingManager import SettingManager

class SystemTrayIcon(QSystemTrayIcon):

    Type                                    = 'DAMGUI'
    key                                     = 'SystemTrayIcon'
    _name                                   = 'DAMG System Tray Icon'
    _copyright                              = __copyright__()
    _data                                   = dict()

    def __init__(self, parent=None):
        super(SystemTrayIcon, self).__init__(parent)

        self.parent                         = parent
        self.settings                       = SettingManager(self)
        self.signals                        = SignalManager(self)
        self.logger                         = Loggers(self.__class__.__name__)

        self.setIcon(AppIcon(32, self.key))

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
# Created by panda on 27/10/2019 - 7:51 PM
# © 2017 - 2018 DAMGteam. All rights reserved