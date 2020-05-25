# -*- coding: utf-8 -*-
"""

Script Name: Application.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys

from .io_widgets                            import QApplication
from PLM.cores                              import SignalManager
from PLM.settings                           import AppSettings



class Application(QApplication):

    Type                                    = 'DAMGAPPLICATION'
    key                                     = 'Application'
    _name                                   = 'DAMG Application'

    def __init__(self):
        super(Application, self).__init__(sys.argv)

        self.settings                   = AppSettings(self)
        self.signals                    = SignalManager(self)


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name                      = val


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/12/2019 - 8:49 AM
# © 2017 - 2018 DAMGteam. All rights reserved