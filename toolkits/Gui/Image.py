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
from appData                                import SETTING_FILEPTH, ST_FORMAT
from toolkits.Core                          import Settings, SignalManager

class Image(QImage):

    Type                                    = 'DAMGIMAGE'
    key                                     = 'Image'
    _name                                   = 'DAMG Image'
    _copyright                              = __copyright__()
    loaded                                  = False

    def __init__(self, image=None, parent=None):
        super(Image, self).__init__(image)

        self._image                         = image
        self.parent                         = parent
        self.settings                       = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.signals                        = SignalManager(self)

        if self._image is None:
            print("ImageIsNoneError: {0}: Image should be a name or a path, not None".format(__name__))
        else:
            if not os.path.exists(self._image):
                if os.path.exists(get_avatar_image(self._image)):
                    self.loaded = self.load(get_avatar_image(self._image))
                elif os.path.exists(get_tag_icon(self._image)):
                    self.loaded = self.load(get_avatar_image(self._image))
                else:
                    print("ImageNotFound: {0}: Could not find image: {1}".format(__name__, self._image))
                    self.loaded = False
            else:
                self.loaded = self.load(self._image)


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

    def __init__(self, image=None, mode='avatar', parent=None):
        QPixmap.__init__(self)

        self.mode                       = mode
        self.image                      = image
        self.parent                     = parent
        self.settings                   = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)
        self.signals                    = SignalManager(self)

        if not self.image is None:
            if self.mode == 'avatar':
                self.fromImage(Image(get_avatar_image(self.image)))
            elif self.mode == 'icon':
                self.fromImage(Image(get_app_icon(32, self.image)))
            elif self.mode == 'logo':
                self.fromImage(Image(get_logo_icon(32, self.image)))
            elif self.mode == 'tag':
                self.fromImage(Image(get_tag_icon(self.image)))
            else:
                self.fromImage(Image(self.image))

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