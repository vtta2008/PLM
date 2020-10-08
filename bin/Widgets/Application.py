# -*- coding: utf-8 -*-
"""

Script Name: Application.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

from PySide2.QtWidgets                      import QApplication


class Application(QApplication):

    Type                                    = 'DAMGAPPLICATION'
    key                                     = 'Application'
    _name                                   = 'DAMG Application'

    def __init__(self, *__args):
        super(Application, self).__init__(*__args)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name                      = val


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/12/2019 - 8:49 AM
# © 2017 - 2018 DAMGteam. All rights reserved