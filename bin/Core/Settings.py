# -*- coding: utf-8 -*-
"""

Script Name: Settings.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------

from PySide2.QtCore                 import QSettings


class Settings(QSettings):

    Type                            = 'DAMGSETTING'
    key                             = 'Settings'
    name                            = 'DAMG Setting'

    def __init__(self, *__args):
        super(Settings, self).__init__(*__args)


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name                  = val


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/17/2020 - 11:00 AM
# © 2017 - 2019 DAMGteam. All rights reserved