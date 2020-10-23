# -*- coding: utf-8 -*-
"""

Script Name: ConnectionIcon.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from pyPLM.Gui                      import Image, Pixmap
from pyPLM.Core                     import Size
from pyPLM.Widgets                  import Label
from PLM.options                    import AUTO_COLOR, center, ASPEC_RATIO
from pyPLM.configs                  import get_app_icon


class ConnectionImage(Image):

    Type                            = 'DAMGCONNECTEDIMAGE'
    key                             = 'ConnectedImage'
    _name                           = 'DAMG Connected Image'

    def __init__(self, fileName='Connected', parent=None):
        super(ConnectionImage, self).__init__(fileName, parent)
        self.parent                 = parent
        self._image                 = fileName
        self.setImage(self._image)

    def setImage(self, image):
        self.load(image)

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, val):
        self._image                 = val

class PixConnection(Pixmap):

    Type = 'DAMGCONNECTEDPIXMAP'
    key = 'PixConnected'
    _name = 'DAMG Connected Pixmap'

    def __init__(self, parent=None):
        super(PixConnection, self).__init__(parent)
        self.parent                 = parent

    def setImage(self, image, flags):
        return self.fromImage(image, flags)

class Conection(Label):

    key                             = 'Connected'

    def __init__(self, connection, stt, parent=None):
        super(Conection, self).__init__()

        self.parent                 = parent
        self.setStatusTip(stt)
        self.setMaximumSize(32, 32)

        image                       = get_app_icon(16, connection)
        pix                         = PixConnection()
        img                         = ConnectionImage(image)

        self.setPixmap(pix.fromImage(img, AUTO_COLOR))
        self.setScaledContents(True)
        self.setAlignment(center)

    def resizeEvent(self, event):
        new_size = Size(16, 16)
        new_size.scale(event.size(), ASPEC_RATIO)
        self.resize(new_size)
        return super(Conection, self).resizeEvent(event)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 2/12/2019 - 7:39 AM
# © 2017 - 2018 DAMGteam. All rights reserved