# -*- coding: utf-8 -*-
"""

Script Name: Process.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
import os

from .io_core import QProcess


class Process(QProcess):

    Type                                    = 'DAMGPROCESS'
    key                                     = 'Process'
    _name                                   = 'DAMG Process'

    def __init__(self, readyReadFn=None, StandardErrorFn=None, StandardOutPutFn=None, finishFn=None, parent=None):
        super(Process, self).__init__(parent)

        self.parent                         = parent

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