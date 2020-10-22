# -*- coding: utf-8 -*-
"""

Script Name: Icon.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python

# PLM
from PySide2.QtGui                          import QIcon
from pyPLM.configs                          import get_tag_icon, get_logo_icon, get_app_icon
from pyPLM.Core                             import Size


class Icon(QIcon):

    Type                                    = 'DAMGUI'
    key                                     = 'Icon'
    _fileName                               = 'DAMG Icon'

    sizes                                   = [16, 24, 32, 48, 64, 96, 128, 256, 512, 1024]

    tags                                    = ['licenceTag', 'pythonTag', 'versionTag']
    w                                       = 87
    h                                       = 20

    _filePath                               = None
    _size                                   = None
    _found                                  = False

    def __init__(self, *__args):
        QIcon.__init__(*__args)


    @property
    def fileName(self):
        return self._fileName

    @property
    def filePath(self):
        return self._filePath

    @property
    def size(self):
        return self._size

    @property
    def found(self):
        return self._found

    @found.setter
    def found(self, val):
        self._found                         = val

    @size.setter
    def size(self, val):
        self._size                          = val

    @fileName.setter
    def fileName(self, val):
        self._iname                         = val

    @filePath.setter
    def filePath(self, val):
        self._filePath                      = val



class AppIcon(Icon):

    key                                     = 'AppIcon'

    def __init__(self, size=32, fileName=None):
        super(AppIcon, self).__init__(self)

        self._size                           = size
        self._fileName                       = fileName
        self._filePath                       = get_app_icon(self.size, self.fileName)

        if self.filePath:
            self.addFile(self.filePath)
            self._found                     = True


class LogoIcon(Icon):

    key = 'LogoIcon'

    def __init__(self, logoName="PLM"):
        super(LogoIcon, self).__init__(self)

        self._fileName                      = logoName

        for s in self.sizes:
            self._filePath                  = get_logo_icon(s, self.fileName)

            if self.filePath:
                self.addFile(self.filePath)


class TagIcon(Icon):

    key                                     = 'TagIcon'

    def __init__(self, name='Tag', parent=None):
        super(TagIcon, self).__init__()

        self.parent = parent
        self.tag = name

        self.find_tag()

    def find_tag(self):
        if self.tag in self.tags:
            self.addFile(get_tag_icon(self.tag), Size(self.w, self.h))
        return True


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 27/10/2019 - 6:31 PM
# © 2017 - 2018 DAMGteam. All rights reserved