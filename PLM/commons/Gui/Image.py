# -*- coding: utf-8 -*-
"""

Script Name: Image.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from PLM import __copyright__
""" Import """

# PyQt5
from PyQt5.QtGui                            import QImage, QPixmap

# PLM
from PLM.configs                                import AUTO_COLOR


class Image(QImage):

    Type                                    = 'DAMGIMAGE'
    key                                     = 'Image'
    _name                                   = 'DAMG Image'
    _copyright                              = __copyright__()

    def __init__(self, image=None, parent=None):
        super(Image, self).__init__(image, parent)

        self.parent                         = parent
        self._image                         = image
        self.setImage(self._image)

    def setImage(self, image):
        self._image                         = image
        self.load(image)

    @property
    def image(self):
        return self._image

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                          = newName

    @image.setter
    def image(self, imagePth):
        self._image                         = imagePth

class Pixmap(QPixmap):

    Type                                    = 'DAMGPIXMAP'
    key                                     = 'Pixmap'
    _name                                   = 'DAMG Pixel Map'
    _copyright                              = __copyright__()

    def __init__(self, imgPth=None, flag=AUTO_COLOR, parent=None):
        super(Pixmap, self).__init__(imgPth)

        self.flag                           = flag
        self.parent                         = parent

        if imgPth is None:
            self.imgPth                     = imgPth
        else:
            self.imgPth                     = QImage(imgPth)
            self.fromImage(self.imgPth, flag)

    def setImage(self, image, flags):
        return self.fromImage(image, flags)

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
# Created by panda on 30/10/2019 - 1:33 AM
# © 2017 - 2018 DAMGteam. All rights reserved