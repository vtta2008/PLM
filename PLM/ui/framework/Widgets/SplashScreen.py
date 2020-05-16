# -*- coding: utf-8 -*-
"""

Script Name: SplashScreen.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PyQt5
from PLM                                    import __copyright__
from PLM.api                                import QSplashScreen


class SplashScreen(QSplashScreen):

    Type                                    = 'DAMGSPLASHSCREEN'
    key                                     = 'SplashScreen'
    _name                                   = 'DAMG Splash Screen'
    _copyright                              = __copyright__()

    def __init__(self, app=None):
        QSplashScreen.__init__(self)

        self.app                            = app


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