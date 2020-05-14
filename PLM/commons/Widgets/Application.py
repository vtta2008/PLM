# -*- coding: utf-8 -*-
"""

Script Name: Application.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
from PLM                                import __copyright__

# Python
import sys

# PyQt5
from PyQt5.QtWidgets                    import QApplication

# PLM
from PLM.plugins.SignalManager          import SignalManager
from PLM.commons.SettingManager         import SettingManager



class Application(QApplication):

    Type                                = 'DAMGAPPLICATION'
    key                                 = 'Application'
    _name                               = 'DAMG Application'
    _copyright                          = __copyright__()

    def __init__(self):
        super(Application, self).__init__(sys.argv)

        self.settings                   = SettingManager(self)
        self.signals                    = SignalManager(self)


    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name                      = val


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/12/2019 - 8:49 AM
# © 2017 - 2018 DAMGteam. All rights reserved