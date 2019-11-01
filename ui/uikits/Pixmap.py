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

from appData                    import __copyright__
from cores.SignalManager        import SignalManager
from utils                      import get_avatar_image

class Pixmap(QPixmap):

    Type                        = 'DAMGUI'
    key                         = 'QPixmap'
    _name                       = 'DAMG Pixel Map'
    _copyright                  = __copyright__

    def __init__(self, image=None, mode='avatar', parent=None):
        QPixmap.__init__(self)

        self.mode               = mode
        self.image              = image
        self.parent             = parent
        self.signals            = SignalManager(self)

        if self.mode == 'avatar':
            print('set avatar: {0}'.format(get_avatar_image(self.image)))
            self.fromImage(QImage(get_avatar_image(self.image)))
        else:
            print('set image: {}'.format(self.image))
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
# Created by panda on 29/10/2019 - 3:07 PM
# © 2017 - 2018 DAMGteam. All rights reserved