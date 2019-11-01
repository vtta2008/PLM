# -*- coding: utf-8 -*-
"""

Script Name: Image.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

import os

from PyQt5.QtGui                import QImage

from appData                    import __copyright__
from utils                      import get_avatar_image


class Image(QImage):

    Type                        = 'DAMGUI'
    key                         = 'Image'
    _name                       = 'DAMG Image'
    _copyright                  = __copyright__

    def __init__(self, image=None, parent=None):

        self.image              = image
        self.parent             = parent

        if self.image is None:
            print("IMAGEISNONEERROR: Image should be a name or a path, not None")
        else:
            if not os.path.exists(self.image):
                if os.path.exists(get_avatar_image(self.image)):
                    self.avata(self.image)
                else:
                    print("IMAGENOTFOUND: Could not find image: {0}".format(self.image))
            else:
                Image(self.image)

    def avata(self, image):
        return Image(get_avatar_image(image))

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name              = newName


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 30/10/2019 - 1:33 AM
# © 2017 - 2018 DAMGteam. All rights reserved