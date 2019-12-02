# -*- coding: utf-8 -*-
"""

Script Name: Avatar.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

import os, shutil

from PyQt5.QtWidgets            import QFileDialog
from PyQt5.QtCore               import QSize

from toolkits.Gui               import Image, Pixmap
from toolkits.Widgets           import Label, GroupBox, VBoxLayout, Button
from utils                      import LocalDatabase, get_avatar_image, resize_image
from appData                    import AUTO_COLOR, AVATAR_DIR, center, ASPEC_RATIO


class ImageAvatar(Image):

    Type                        = 'DAMGAVATARIMAGE'
    key                         = 'ImageAvatar'
    _name                       = 'DAMG Avatar Image'

    def __init__(self, fileName=None, parent=None):
        super(ImageAvatar, self).__init__(fileName, parent)
        self.parent             = parent
        self._image             = fileName
        self.setImage(self._image)

    def setImage(self, image):
        self.load(image)
        # self.smoothScaled(100, 100)

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, imagePth):
        self._image = imagePth

class PixAvatar(Pixmap):

    Type = 'DAMGPIXMAP'
    key = 'PixAvatar'

    def __init__(self, parent=None):
        super(PixAvatar, self).__init__()
        self.parent             = parent

    def setImage(self, image, flags):
        return self.fromImage(image, flags)

class AvatarLabel(Label):

    Type = 'DAMGAVATARLABEL'
    key = 'AvatarLabel'

    db = LocalDatabase()

    try:
        username = db.query_table('curUser')[0]
    except (ValueError, IndexError):
        username = 'DemoUser'

    _name = username

    def __init__(self, parent=None):
        super(AvatarLabel, self).__init__()

        self.parent = parent
        image = get_avatar_image(self.username)
        pixAvatar = PixAvatar()
        imgAvatar = ImageAvatar(image)
        self.setPixmap(pixAvatar.fromImage(imgAvatar, AUTO_COLOR))

        self.setScaledContents(True)
        self.setAlignment(center)

    def resizeEvent(self, event):
        size = QSize(1, 1)
        size.scale(100, 100, ASPEC_RATIO)
        self.resize(size)

class Avatar(GroupBox):

    key = 'Avatar'

    def __init__(self, parent=None):
        super(Avatar, self).__init__(parent=parent)

        self.parent                 = parent
        self.layout                 = VBoxLayout()

        self.avatar                 = AvatarLabel()
        self.changeAvatarBtn        = Button({'txt': 'Change Avatar', 'cl': self.update_avatar})
        self.layout.addWidget(self.avatar)
        self.layout.addWidget(self.changeAvatarBtn)

        self.username               = self.avatar.username
        self.setTitle(self.username)

        self.setLayout(self.layout)

    def update_avatar(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileFormat = "All Files (*);;Img Files (*.jpg)"

        fileName, _ = QFileDialog.getOpenFileName(self, "Your Avatar", AVATAR_DIR, fileFormat, options=options)

        if fileName:
            baseFileName = self.username + '.avatar.jpg'
            desPth = os.path.join(AVATAR_DIR, baseFileName)

            if desPth == fileName:
                pass
            elif os.path.exists(desPth):
                if os.path.exists(desPth + '.old'):
                    os.remove(desPth + '.old')

                os.rename(desPth, desPth + '.showLayout_old')
                resize_image(fileName, desPth)
                shutil.copy2(fileName, desPth)

            self.avatar.pixAvatar._imageAvatar.setImage(desPth)
            self.avatar.update()

    def resizeEvent(self, event):
        self.changeAvatarBtn.setMaximumWidth(self.avatar.width())
        self.changeAvatarBtn.setMaximumHeight(25)

class InfoPicLabel(Label):

    key = 'InfoPicLabel'

    def __init__(self, parent=None):
        super(InfoPicLabel, self).__init__()

        self.parent = parent


    def updatePicture(self, image):
        pix = PixAvatar()
        img = ImageAvatar(image)
        self.setPixmap(pix.fromImage(img, AUTO_COLOR))
        self.setScaledContents(True)
        self.setAlignment(center)
        self.update()

    def resizeEvent(self, event):
        size = QSize(1, 1)
        size.scale(self.size(), ASPEC_RATIO)
        self.resize(size)

class InfoPicture(GroupBox):

    key = 'InfoPicture'

    def __init__(self, parent=None):
        super(InfoPicture, self).__init__(parent=parent)

        self.parent = parent
        self.setTitle('Images')
        self.layout = VBoxLayout()
        self.infoPic = InfoPicLabel()
        self.changePictureBtn = Button({'txt': 'Choose an Image', 'cl': self.update_image})
        self.layout.addWidget(self.infoPic)
        self.layout.addWidget(self.changePictureBtn)

    def update_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileFormat = "All Files (*);;Img Files (*.jpg)"

        fileName, _ = QFileDialog.getOpenFileName(self, "Your Avatar", AVATAR_DIR, fileFormat, options=options)

        if fileName:
            self.infoPic.updatePicture(fileName)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 28/11/2019 - 11:09 AM
# © 2017 - 2018 DAMGteam. All rights reserved