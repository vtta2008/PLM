# -*- coding: utf-8 -*-
"""

Script Name: ConnectionIcon.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

from PLM.commons.Gui                import Image, Pixmap
from PLM.commons.Widgets            import Label
from PLM.utils                      import get_app_icon
from PLM.configs                    import AUTO_COLOR, center

class ConnectionImage(Image):

    Type = 'DAMGCONNECTEDIMAGE'
    key = 'ConnectedImage'
    _name = 'DAMG Connected Image'

    def __init__(self, fileName='Connected', parent=None):
        super(ConnectionImage, self).__init__(fileName, parent)
        self.parent = parent
        self._image = fileName
        self.setImage(self._image)

    def setImage(self, image):
        self.load(image)

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, imagePth):
        self._image = imagePth

class PixConnection(Pixmap):

    Type = 'DAMGCONNECTEDPIXMAP'
    key = 'PixConnected'
    _name = 'DAMG Connected Pixmap'

    def __init__(self, parent=None):
        super(PixConnection, self).__init__(parent)
        self.parent = parent

    def setImage(self, image, flags):
        return self.fromImage(image, flags)

class Conection(Label):

    Type = 'DAMGCONNECTEDICON'
    key = 'Connected'

    def __init__(self, connection, stt, parent=None):
        super(Conection, self).__init__()

        self.parent = parent
        self.setStatusTip(stt)
        image = get_app_icon(16, connection)
        pix = PixConnection()
        img = ConnectionImage(image)
        self.setPixmap(pix.fromImage(img, AUTO_COLOR))
        self.setMaximumSize(16, 16)
        self.setScaledContents(True)
        self.setAlignment(center)



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 2/12/2019 - 7:39 AM
# © 2017 - 2018 DAMGteam. All rights reserved