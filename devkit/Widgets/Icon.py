# -*- coding: utf-8 -*-
"""

Script Name: Icon.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import __copyright__

import os

from PyQt5.QtGui                            import QIcon
from PyQt5.QtCore                           import QSize

from utils                                  import get_app_icon, get_tag_icon, get_logo_icon
from appData                                import iconInfo, IGNORE_ICON_NAME
from cores.Settings                         import Settings
from cores.SignalManager                    import SignalManager


class Icon(QIcon):

    Type                                    = 'DAMGUI'
    key                                     = 'Icon'
    _name                                   = 'DAMG Icon'
    _copyright                              = __copyright__()
    iconInfo                                = iconInfo

    def __init__(self, parent=None):
        QIcon.__init__(self)

        self.parent                         = parent
        self.settings                       = Settings(self)
        self.signals                        = SignalManager(self)

    @property
    def copyright(self):
        return self._copyright

    @property
    def iconName(self):
        return self._name

    @iconName.setter
    def iconName(self, newName):
        self._name                          = newName

class AppIcon(Icon):

    key = 'AppIcon'

    def __init__(self, size=32, name="AboutPlt"):
        super(AppIcon, self).__init__()

        self._found = False
        self.iconSize = size
        self.iconName = name

        key = 'icon{0}'.format(self.iconSize)

        for icon in self.iconInfo[key].keys():
            if self.iconName == icon:
                self.iconPth = get_app_icon(self.iconSize, self.iconName)
                self._found = True
                break
            elif os.path.exists(self.iconName):
                self.iconPth = self.iconName
                self._found = True
                break

        if not self._found:
            if not self.iconName in IGNORE_ICON_NAME:
                # print("IconNotFound: {0}: Could not find icon name: {1}".format(__name__, self.iconName))
                pass
        else:
            self.addFile(self.iconPth, QSize(self.iconSize, self.iconSize))

class LogoIcon(Icon):

    key = 'LogoIcon'

    sizes = [16, 24, 32, 48, 64, 96, 128, 256, 512, 1024]

    def __init__(self, name="Logo", parent=None):
        super(LogoIcon, self).__init__()

        self.parent = parent
        self.name =name

        self.find_icon()

    def find_icon(self):
        for s in self.sizes:
            self.addFile(get_logo_icon(s, self.name), QSize(s, s))
        return True

class TagIcon(Icon):

    key = 'TagIcon'
    tags = ['licenceTag', 'pythonTag', 'versionTag']
    w = 87
    h = 20

    def __init__(self, name='Tag', parent=None):
        super(TagIcon, self).__init__()

        self.parent = parent
        self.tag = name

        self.find_tag()

    def find_tag(self):
        if self.tag in self.tags:
            self.addFile(get_tag_icon(self.tag), QSize(self.w, self.h))
        return True
# -------------------------------------------------------------------------------------------------------------
# Created by panda on 27/10/2019 - 6:31 PM
# © 2017 - 2018 DAMGteam. All rights reserved