# -*- coding: utf-8 -*-
"""

Script Name: Image.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import __copyright__

import os

from PyQt5.QtGui                            import QImage, QPixmap

from utils                                  import get_avatar_image, get_app_icon, get_logo_icon, get_tag_icon

class Image(QImage):

    Type                                    = 'DAMGIMAGE'
    key                                     = 'Image'
    _name                                   = 'DAMG Image'
    _copyright                              = __copyright__()
    loaded                                  = False

    def __init__(self, *__args):
        QImage.__init__(self)

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name              = newName

class Pixmap(QPixmap):

    Type                                = 'DAMGPIXMAP'
    key                                 = 'Pixmap'
    _name                               = 'DAMG Pixel Map'
    _copyright                          = __copyright__()

    def __init__(self, *__args):
        QPixmap.__init__(self)

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                      = newName

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 30/10/2019 - 1:33 AM
# © 2017 - 2018 DAMGteam. All rights reserved