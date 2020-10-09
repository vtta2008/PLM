# -*- coding: utf-8 -*-
"""

Script Name: SystemTrayIcon.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from PySide2.QtWidgets                      import QSystemTrayIcon
from bin.Gui                                import AppIcon



class SystemTrayIcon(QSystemTrayIcon):

    Type                                    = 'DAMGUI'
    key                                     = 'SystemTrayIcon'
    _name                                   = 'DAMG System Tray Icon'

    def __init__(self, parent=None):
        super(SystemTrayIcon, self).__init__(parent)

        self.parent                         = parent

        self.setIcon(AppIcon(32, self.key))

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
# Created by panda on 27/10/2019 - 7:51 PM
# © 2017 - 2018 DAMGteam. All rights reserved