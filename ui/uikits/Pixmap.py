# -*- coding: utf-8 -*-
"""

Script Name: Pixmap.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

import os

from PyQt5.QtGui                import QPixmap, QImage

from appData                    import SETTING_FILEPTH, ST_FORMAT, __copyright__
from cores.SignalManager        import SignalManager
from cores.Settings             import Settings
from utils import get_avatar_image

class Pixmap(QPixmap):

    Type                        = 'DAMGUI'
    key                         = 'QPixmap'
    _name                       = 'DAMG Pixel Map'
    _copyright                  = __copyright__
    _data                       = dict()

    def __init__(self, image=None, parent=None):
        QPixmap.__init__(self)

        self.image              = image
        self.parent             = parent
        self.signals            = SignalManager(self)
        self.settings           = Settings(SETTING_FILEPTH['app'], ST_FORMAT['ini'], self)

        if self.image is None:
            print("IMAGEISNONEERROR: Image should be a name or a path, not None")
        else:
            if not os.path.exists(self.image):
                if os.path.exists(get_avatar_image(self.image)):
                    self.fromImage(QImage(get_avatar_image(self.image)))
                else:
                    print("IMAGENOTFOUND: Could not find image: {0}".format(self.image))
            else:
                self.fromImage(QImage(self.image))


    def setValue(self, key, value):
        return self.settings.initSetValue(key, value, self.key)

    def getValue(self, key):
        return self.settings.initValue(key, self.key)

    @property
    def copyright(self):
        return self._copyright

    @property
    def data(self):
        return self._data

    @property
    def name(self):
        return self._name

    @data.setter
    def data(self, newData):
        self._data                      = newData

    @name.setter
    def name(self, newName):
        self._name                      = newName



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 29/10/2019 - 3:07 PM
# © 2017 - 2018 DAMGteam. All rights reserved