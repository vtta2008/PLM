# -*- coding: utf-8 -*-
"""

Script Name: Process.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import __copyright__

import os

from PyQt5.QtCore                           import QProcess

from cores.Settings                         import Settings
from cores.SignalManager                    import SignalManager

class Process(QProcess):

    Type                                    = 'DAMGPROCESS'
    key                                     = 'Process'
    _name                                   = 'DAMG Process'
    __copyright__                           = __copyright__()

    def __init__(self, readyReadFn=None, StandardErrorFn=None, StandardOutPutFn=None, finishFn=None, parent=None):
        super(Process, self).__init__(parent)

        self.parent                         = parent
        self.preSetting                     = Settings(self.parent)
        self.signals                        = SignalManager(self.parent)

        self.setProcessChannelMode(self.MergedChannels)
        self.setWorkingDirectory(os.getcwd())

        if readyReadFn is not None:
            self.readyRead.connect(readyReadFn)

        if StandardErrorFn is not None:
             self.readyReadStandardError.connect(StandardErrorFn)

        if StandardOutPutFn is not None:
            self.readyReadStandardOutput.connect(StandardOutPutFn)

        if finishFn is not None:
            self.finished.connect(finishFn)

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
# Created by panda on 10/11/2019 - 12:06 AM
# © 2017 - 2018 DAMGteam. All rights reserved