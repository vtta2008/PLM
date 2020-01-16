# -*- coding: utf-8 -*-
"""

Script Name: icons.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import globalSetting
""" Import """

# Python
import os, pprint

# PLM
from .dirs                              import (AVATAR_DIR, DAMG_LOGO_DIR, PLM_LOGO_DIR, PIC_DIR, ICON_DIR_12,
                                                ICON_DIR_16, ICON_DIR_24, ICON_DIR_32, ICON_DIR_48, ICON_DIR_64,
                                                MAYA_ICON_DIR, TAG_ICON_DIR, WEB_ICON_128, WEB_ICON_32, NODE_ICON_DIR, )



class ConfigAvatar(dict):

    key                                 = 'ConfigAvatar'

    def __init__(self):
        super(ConfigAvatar, self).__init__()

        for root, dirs, names in os.walk(AVATAR_DIR, topdown=False):
            for name in names:
                self[name.split('.avatar')[0]] = os.path.join(root, name).replace('\\', '/')


class ConfigLogo(dict):

    key                                 = 'ConfigLogo'

    def __init__(self):
        super(ConfigLogo, self).__init__()

        damgLogos                       = dict()
        plmLogos                        = dict()

        for root, dirs, names in os.walk(DAMG_LOGO_DIR, topdown=False):
            for name in names:
                damgLogos[name.split('.png')[0]] = os.path.join(root, name).replace('\\', '/')

        for root, dirs, names in os.walk(PLM_LOGO_DIR, topdown=False):
            for name in names:
                plmLogos[name.split('.png')[0]] = os.path.join(root, name).replace('\\', '/')

        self['DAMGTEAM']                = damgLogos
        self['PLM']                     = plmLogos


class ConfigPics(dict):

    key                                 = 'ConfigPics'

    def __init__(self):
        super(ConfigPics, self).__init__()

        for root, dirs, names, in os.walk(PIC_DIR, topdown=False):
            for name in names:
                self[name.split('.node')[0]] = os.path.join(root, name).replace('\\', '/')


class ConfigIcon(dict):

    key                                 = 'ConfigIcon'

    def __init__(self):
        super(ConfigIcon, self).__init__()

        self['icon12']                  = self.get_icons(ICON_DIR_12)
        self['icon16']                  = self.get_icons(ICON_DIR_16)
        self['icon24']                  = self.get_icons(ICON_DIR_24)
        self['icon32']                  = self.get_icons(ICON_DIR_32)
        self['icon48']                  = self.get_icons(ICON_DIR_48)
        self['icon64']                  = self.get_icons(ICON_DIR_64)

        self['maya']                    = self.get_icons(MAYA_ICON_DIR)

        self['node']                    = self.get_icons(NODE_ICON_DIR)

        self['tag']                     = self.get_icons(TAG_ICON_DIR)

        self['web32']                   = self.get_icons(WEB_ICON_32)
        self['web128']                  = self.get_icons(WEB_ICON_128)

        self['avatar']                  = ConfigAvatar()
        self['logo']                    = ConfigLogo()
        self['pic']                     = ConfigPics()

        if globalSetting.tracks.configInfo:
            if globalSetting.tracks.iconInfo:
                pprint.pprint(self)

    def get_icons(self, dir):
        icons = dict()
        for root, dirs, names in os.walk(dir, topdown=False):
            for name in names:
                icons[name.split('.icon')[0]] = os.path.join(root, name).replace('\\', '/')
        return icons




# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/17/2020 - 1:34 AM
# © 2017 - 2019 DAMGteam. All rights reserved