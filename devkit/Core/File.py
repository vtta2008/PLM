# -*- coding: utf-8 -*-
"""

Script Name: File.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import __copyright__

import os

from PyQt5.QtCore                           import QFile

from appData                                import QSS_DIR

class FileBase(QFile):

    Type                                    = 'DAMGFILE'
    key                                     = 'FileBase'
    _name                                   = 'DAMG File Base'
    _copyright                              = __copyright__()
    _filePath                               = None

    def __init__(self, *__args):
        QFile.__init__(self)

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name                          = val

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, val):
        self._filePath                      = val

class QssFile(FileBase):

    key                                     = 'QssFile'

    qssPths = dict(
                    bright                   = os.path.join(QSS_DIR, 'bright.qss'),
                    chacoal                  = os.path.join(QSS_DIR, 'chacoal.qss'),
                    cmd                      = os.path.join(QSS_DIR, 'cmd.qss'),
                    dark                     = os.path.join(QSS_DIR, 'grey.qss'),
                    grey                     = os.path.join(QSS_DIR, 'grey.qss'),
                    nuker                    = os.path.join(QSS_DIR, 'nuker.qss'),
                   )

    def __init__(self, style):
        super(QssFile, self).__init__()

        self._style                         = style
        self._filePath                      = self.qssPths[self._style]
        self.setFileName(self._filePath)

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, val):
        self._style                         = val

class File(FileBase):

    key                                     = 'File'

    def __init__(self, filePth=None):
        FileBase.__init__(self)

        self._filePath                      = filePth
        self.setFileName(self._filePath)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 27/11/2019 - 4:56 PM
# © 2017 - 2018 DAMGteam. All rights reserved