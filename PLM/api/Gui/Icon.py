# -*- coding: utf-8 -*-
"""

Script Name: Icon.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python

# PLM
from .io_gui                                import QIcon
from PLM.utils                              import get_tag_icon, get_logo_icon, get_app_icon
from PLM.api.Core                           import Size


class Icon(QIcon):

    Type                                    = 'DAMGUI'
    key                                     = 'Icon'
    _name                                   = 'DAMG Icon'

    def __init__(self, *__args):
        super(Icon, self).__init__(*__args)

    @property
    def iconName(self):
        return self._name

    @iconName.setter
    def iconName(self, val):
        self._name                          = val



class AppIcon(Icon):

    key                                     = 'AppIcon'
    _found                                  = False

    def __init__(self, size=32, iconName=None):
        super(AppIcon, self).__init__(get_app_icon(size, iconName))


class LogoIcon(Icon):

    key = 'LogoIcon'

    sizes = [16, 24, 32, 48, 64, 96, 128, 256, 512, 1024]

    def __init__(self, name="Logo", parent=None):
        super(LogoIcon, self).__init__()

        self.parent                         = parent
        self.name                           = name

        for s in self.sizes:
            self.addFile(get_logo_icon(s, self.name), Size(s, s))



class TagIcon(Icon):

    key                                     = 'TagIcon'
    tags                                    = ['licenceTag', 'pythonTag', 'versionTag']
    w                                       = 87
    h                                       = 20

    def __init__(self, name='Tag', parent=None):
        super(TagIcon, self).__init__()

        self.parent = parent
        self.tag = name

        self.find_tag()

    def find_tag(self):
        if self.tag in self.tags:
            self.addFile(get_tag_icon(self.tag), Size(self.w, self.h))
        return True


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 27/10/2019 - 6:31 PM
# © 2017 - 2018 DAMGteam. All rights reserved