# -*- coding: utf-8 -*-
"""

Script Name: Application.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

import json

from PyQt5.QtWidgets                    import QApplication
from PyQt5.QtCore                       import pyqtSlot

from cores.base                         import ObjectEncoder
from appData                            import __copyright__

class Application(QApplication):

    Type                                = 'DAMGAPPLICATION'
    key                                 = 'ApplicationObject'
    _name                               = 'DAMG Application'
    _count                              = 0
    _data                               = dict()
    _copyright                          = __copyright__

    def __str__(self):
        """ Print object will return data string """
        return json.dumps(self.data, cls=ObjectEncoder, indent=4, sort_keys=True)

    def __repr__(self):
        """ Print object ill return json data type """
        return json.dumps(self.data, cls=ObjectEncoder, indent=4, sort_keys=True)

    def __call__(self):

        """ Make object callable """

        if isinstance(self, object):
            return True
        else:
            return False

    @pyqtSlot(int)
    def count_notified_change(self, val):
        self._count = val

    @property
    def copyright(self):
        return self._copyright

    @property
    def data(self):
        return self._data

    @property
    def name(self):
        return self._name

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, newVal):
        self._count                         = newVal

    @data.setter
    def data(self, newData):
        self._data                          = newData

    @name.setter
    def name(self, newName):
        self._name                          = newName

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 27/10/2019 - 7:58 PM
# © 2017 - 2018 DAMGteam. All rights reserved