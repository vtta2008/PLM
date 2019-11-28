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

from toolkits.Gui               import Image, Pixmap
from toolkits.Widgets           import Label, GroupBox, VBoxLayout, Button
from utils                      import LocalDatabase, get_avatar_image, resize_image
from appData                    import AUTO_COLOR, AVATAR_DIR, SiPoIgn, center, ASPEC_RATIO, SMOOTH_TRANS


class ImageAvatar(Image):

    Type                        = 'DAMGIMAGE'
    key                         = 'ImageAvatar'

    def __init__(self, fileName=None, parent=None):
        super(ImageAvatar, self).__init__(fileName, parent)
        self.parent             = parent
        self._image             = fileName
        self.setImage(self._image)

    def setImage(self, image):
        self.load(image)
        self.smoothScaled(100, 100)

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
        imgAvatar.scaled(100, 100, ASPEC_RATIO, SMOOTH_TRANS)
        self.setPixmap(pixAvatar.fromImage(imgAvatar, AUTO_COLOR))

        self.setScaledContents(True)
        self.setSizePolicy(SiPoIgn, SiPoIgn)
        self.setScaledContents(True)
        self.setAlignment(center)



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

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 28/11/2019 - 11:09 AM
# © 2017 - 2018 DAMGteam. All rights reserved