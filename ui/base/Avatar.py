# -*- coding: utf-8 -*-
"""

Script Name: Avatar.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

# Python
import os, shutil, sqlite3

# PyQt5
from PyQt5.QtWidgets            import QFileDialog

# PLM
from devkit.Core                import Size
from devkit.Gui                 import Image, Pixmap
from devkit.Widgets             import Label, GroupBox, VBoxLayout, Button
from utils                      import LocalDatabase, get_avatar_image, resize_image
from appData                    import AUTO_COLOR, AVATAR_DIR, center, ASPEC_RATIO

db                              = LocalDatabase()

try:
    username = db.query_table('curUser')[0]
except (ValueError, IndexError, sqlite3.OperationalError):
    username = 'DemoUser'

class ImageAvatar(Image):

    Type                        = 'DAMGAVATARIMAGE'
    key                         = 'ImageAvatar'
    _name                       = 'DAMG Avatar Image: {0}'.format(username)

    def __init__(self, fileName=None, parent=None):
        if not fileName or not os.path.exists(fileName):
            fileName            = get_avatar_image('default')
        super(ImageAvatar, self).__init__(fileName, parent)

class PixAvatar(Pixmap):

    Type = 'DAMGPIXMAP'
    key = 'PixAvatar'

    def __init__(self, parent=None):
        super(PixAvatar, self).__init__()
        self.parent             = parent

class AvatarLabel(Label):

    Type                        = 'DAMGAVATARLABEL'
    key                         = 'AvatarLabel'
    _name                       = username

    def __init__(self, parent=None):
        super(AvatarLabel, self).__init__()

        self.parent             = parent
        self.pixAvatar          = PixAvatar()
        self.imageAvatar        = ImageAvatar(get_avatar_image(username))
        self.setPixmap(self.pixAvatar.fromImage(self.imageAvatar, AUTO_COLOR))
        self.setScaledContents(True)
        self.setAlignment(center)

    def resizeEvent(self, event):
        size                    = Size(1, 1)
        size.scale(100, 100, ASPEC_RATIO)
        self.resize(size)

class Avatar(GroupBox):

    key                             = 'Avatar'

    def __init__(self, parent=None):
        super(Avatar, self).__init__(parent=parent)

        self.parent                 = parent
        self.layout                 = VBoxLayout()

        self.avatar                 = AvatarLabel()
        self.changeAvatarBtn        = Button({'txt': 'Change Avatar', 'cl': self.update_avatar})
        self.changeAvatarBtn.setMaximumWidth(self.avatar.width())
        self.changeAvatarBtn.setMaximumHeight(25)

        self.layout.addWidget(self.avatar)
        self.layout.addWidget(self.changeAvatarBtn)
        self.setTitle(username)

        self.setLayout(self.layout)

    def update_avatar(self):
        options                     = QFileDialog.Options()
        options                    |= QFileDialog.DontUseNativeDialog
        fileFormat                  = "All Files (*);;Img Files (*.jpg)"
        fileName, _                 = QFileDialog.getOpenFileName(self, "Your Avatar", AVATAR_DIR, fileFormat, options=options)

        if fileName:
            scrPth                  = fileName
            baseFileName            = '{0}.avatar.jpg'.format(username)
            desPth                  = os.path.join(AVATAR_DIR, baseFileName)

            if os.path.exists(desPth):
                oldPth              = '{0}.old'.format(desPth)
                if os.path.exists(oldPth):
                    os.remove(oldPth)

                os.rename(desPth, oldPth)
                resize_image(fileName, desPth, 100, 100)
                shutil.copy2(fileName, desPth)

            self.avatar.imageAvatar.setImage(desPth)
            self.avatar.update()

class InfoPicLabel(Label):

    key = 'InfoPicLabel'

    def __init__(self, parent=None):
        super(InfoPicLabel, self).__init__()

        self.parent = parent

    def updatePicture(self, image):
        pix                         = PixAvatar()
        img                         = ImageAvatar(image)
        self.setPixmap(pix.fromImage(img, AUTO_COLOR))
        self.setScaledContents(True)
        self.setAlignment(center)
        self.update()

    def resizeEvent(self, event):
        size                        = Size(1, 1)
        size.scale(self.size(), ASPEC_RATIO)
        self.resize(size)

class InfoPicture(GroupBox):

    key = 'InfoPicture'

    def __init__(self, parent=None):
        super(InfoPicture, self).__init__(parent=parent)

        self.setTitle('Images')
        self.parent                 = parent
        self.layout                 = VBoxLayout()
        self.infoPic                = InfoPicLabel()
        self.changePictureBtn       = Button({'txt': 'Choose an Image', 'cl': self.update_image})

        self.layout.addWidget(self.infoPic)
        self.layout.addWidget(self.changePictureBtn)

    def update_image(self):
        options                     = QFileDialog.Options()
        options                    |= QFileDialog.DontUseNativeDialog
        fileFormat                  = "All Files (*);;Img Files (*.jpg)"
        fileName, _                 = QFileDialog.getOpenFileName(self, "Your Avatar", AVATAR_DIR, fileFormat, options=options)

        if fileName:
            self.infoPic.updatePicture(fileName)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 28/11/2019 - 11:09 AM
# © 2017 - 2018 DAMGteam. All rights reserved