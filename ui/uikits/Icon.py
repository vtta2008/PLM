# -*- coding: utf-8 -*-
"""

Script Name: Icon.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from PyQt5.QtGui                            import QIcon
from PyQt5.QtCore                           import QSize

from appData                                import __copyright__, appIconCfg
from cores.SignalManager                    import SignalManager
from utils.utils                            import data_handler, get_logo_icon, get_app_icon, get_tag_icon

class Icon(QIcon):

    Type                                    = 'DAMGUI'
    key                                     = 'Icon'
    _name                                   = 'DAMG Icon'
    _copyright                              = __copyright__
    iconInfo                                = data_handler(filePath=appIconCfg)

    def __init__(self, parent=None):
        QIcon.__init__(self)

        self.parent                         = parent
        self.signals                        = SignalManager(self)

    @property
    def copyright(self):
        return self._copyright

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name                          = newName

class AppIcon(Icon):

    key = 'AppIcon'

    def __init__(self, size=32, name="AboutPlt"):
        super(AppIcon, self).__init__()

        self._found = False
        self.iconSize = size
        self.iconName = name

        for icon in self.iconInfo.keys():
            if self.iconName == icon:
                self._found = True

        if self._found:
            self.iconPth = get_app_icon(self.iconSize, self.iconName)
            self.addFile(self.iconPth, QSize(self.iconSize, self.iconSize))
        else:
            print("FILENOTFOUNDERROR: {0}: Could not find icon name: {1}".format(__name__, self.iconName))

class LogoIcon(Icon):

    key = 'LogoIcon'

    sizes = [16, 24, 32, 48, 64, 96, 128, 256, 512]

    def __init__(self, name="Logo", parent=None):
        super(LogoIcon, self).__init__(parent)

        self.parent = parent
        self.name =name

        self.find_icon()

    def find_icon(self):
        for s in self.sizes:
            self.addFile(get_logo_icon(s, self.name), QSize(s, s))
        return True

class TagIcon(Icon):

    key = 'TagIcon'
    tags = ['licence', 'python', 'version']
    w = 87
    h = 20

    def __init__(self, name='Tag', parent=None):
        super(TagIcon, self).__init__(parent)

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