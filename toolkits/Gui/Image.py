# -*- coding: utf-8 -*-
"""

Script Name: Image.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import __copyright__, signals, settings

import os

from PyQt5.QtGui                            import QImage, QPixmap

from utils                                  import get_avatar_image, get_app_icon, get_logo_icon, get_tag_icon

class Image(QImage):

    Type                                    = 'DAMGIMAGE'
    key                                     = 'Image'
    _name                                   = 'DAMG Image'
    _copyright                              = __copyright__()

    def __init__(self, image=None, parent=None):
        super(Image, self).__init__(parent)

        self.pixmap                         = QPixmap()
        self._image                         = image
        self.parent                         = parent
        self.settings                       = settings
        self.signals                        = signals
        self.settings.changeParent(self)
        self.signals.changeParent(self)

        if self.image is None:
            print("ImageIsNoneError: {0}: Image should be a name or a path, not None".format(__name__))
        else:
            if not os.path.exists(self._image):
                if os.path.exists(get_avatar_image(self._image)):
                    self.image = self.pixmap.fromImage(get_avatar_image(self._image))
                else:
                    print("ImageNotFound: {0}: Could not find image: {1}".format(__name__, self.image))
            else:
                self.image = self.pixmap.fromImage(self._image)

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

        if self.mode == 'avatar':
            self.fromImage(QImage(get_avatar_image(self.image)))
        elif self.mode == 'icon':
            self.fromImage(QImage(get_app_icon(32, self.image)))
        elif self.mode == 'logo':
            self.fromImage(QImage(get_logo_icon(32, self.image)))
        elif self.mode == 'tag':
            self.fromImage(QImage(get_tag_icon(self.image)))
        else:
            self.fromImage(QImage(self.image))

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