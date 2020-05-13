# -*- coding: utf-8 -*-
"""

Script Name: SplashScreen.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__
""" Import """

# PyQt5
from PyQt5.QtWidgets                        import QSplashScreen

# PLM
from PLM.plugins.SignalManager              import SignalManager
from PLM.commons.SettingManager             import SettingManager

class SplashScreen(QSplashScreen):

    Type                                    = 'DAMGSPLASHSCREEN'
    key                                     = 'SplashScreen'
    _name                                   = 'DAMG Splash Screen'
    _copyright                              = __copyright__()

    def __init__(self, app=None):
        QSplashScreen.__init__(self)

        self.app                            = app
        self.settings                       = SettingManager(self)
        self.signals                        = SignalManager(self)

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
        self._name                          = newName


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/11/2020 - 3:51 PM
# © 2017 - 2019 DAMGteam. All rights reserved