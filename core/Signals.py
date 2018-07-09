# -*- coding: utf-8 -*-
"""

Script Name: Signals.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python

# PyQt5
from PyQt5.QtCore import QObject, QMetaObject


# -------------------------------------------------------------------------------------------------------------
""" Import """

testData = dict(a1 = 1, a2 = "string")

class PureObj(QObject):

    def __new__(type):
        if not '_the_instance' in type.__dict__:
            type._the_instance = QObject.__new__(type)
        return type._the_instance

class ABC(PureObj):

    _data = testData

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, callbacks):
        assert isinstance(callbacks, dict)
        self._data = callbacks



q = ABC()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 5:51 AM
# © 2017 - 2018 DAMGteam. All rights reserved