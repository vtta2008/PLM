# -*- coding: utf-8 -*-
"""

Script Name: SplashScreen.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------

from .io_widgets import QSplashScreen


class SplashScreen(QSplashScreen):

    Type                                    = 'DAMGSPLASHSCREEN'
    key                                     = 'SplashScreen'
    _name                                   = 'DAMG Splash Screen'

    def __init__(self, *__args):
        QSplashScreen.__init__(*__args)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                          = newName


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/11/2020 - 3:51 PM
# © 2017 - 2019 DAMGteam. All rights reserved