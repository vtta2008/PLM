# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
import os

from PLM.configs        import LOGO_DIR, WEB_ICON_DIR, TAG_ICON_DIR, AVATAR_DIR, USER_LOCAL_DATA, ICON_DIR
from .utils             import get_file_path


def get_app_icon(size=32, iconName="About"):
    # Get the right directory base on icon size
    iconPth = os.path.join(ICON_DIR, "x{0}".format(str(size)))

    # Get the icon file path
    iconFilePth = os.path.join(iconPth, "{0}.icon.png".format(iconName))

    # Check icon file path
    if not os.path.exists(iconFilePth):
        print('could not find: {0}, please try a gain'.format(iconFilePth))

    return iconFilePth


def get_logo_icon(size=32, name="DAMG"):
    if name == "PLM":
        logoPth = os.path.join(LOGO_DIR, 'PLM')
    elif name == 'DAMG':
        logoPth = os.path.join(LOGO_DIR, 'DAMGTEAM')
    else:
        logoPth = os.path.join(LOGO_DIR, 'PLM')

    logoFilePth = os.path.join(logoPth, "{0}x{0}.png".format(str(size)))

    if not os.path.exists(logoFilePth):
        return FileNotFoundError('{} not exists'.format(logoFilePth))
    else:
        return logoFilePth


def get_web_icon(name):
    icons = [i for i in get_file_path(WEB_ICON_DIR) if ".icon" in i]
    for i in icons:
        if name in i:
            # print(i, os.path.exists(i))
            return i


def get_avatar_image(name):
    avatarPth = os.path.join(USER_LOCAL_DATA, '{0}.avatar.jpg'.format(name))
    if not os.path.exists(avatarPth):
        avatarPth = os.path.join(AVATAR_DIR, 'default.avatar.jpg')
    return avatarPth


def get_tag_icon(name):
    tags = [t for t in get_file_path(TAG_ICON_DIR) if '.icon' in t]
    for t in tags:
        if name in t:
            # print(t, os.path.exists(t))
            return t

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved