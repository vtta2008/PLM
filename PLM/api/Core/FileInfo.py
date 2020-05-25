# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------

from .io_core import QFileInfo


class FileInfo(QFileInfo):

    Type                                = 'DAMGFILEINFO'
    key                                 = 'FileInfo'
    _name                               = 'DAMG File Info'
    _filePath                           = None

    def __init__(self, *__args):
        super(FileInfo, self).__init__(*__args)


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, val):
        self._filePath = val

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved