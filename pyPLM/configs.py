# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
import os

BIN_ROOT = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), 'bin')
print(BIN_ROOT, os.path.exists(BIN_ROOT))

BIN_DATA                        = os.path.join(BIN_ROOT, 'data')
BIN_SCRIPTS                     = os.path.join(BIN_DATA, 'scripts')
BIN_RESOURCES                   = os.path.join(BIN_DATA, 'resources')

QSS_DIR                         = os.path.join(BIN_SCRIPTS, 'qss').replace('\\', '/')
LOGO_DIR                        = os.path.join(BIN_RESOURCES, 'logo')
ICON_DIR                        = os.path.join(BIN_RESOURCES, 'icons')
AVATAR_DIR                      = os.path.join(BIN_RESOURCES, 'avatar')

WEB_ICON_DIR                    = os.path.join(ICON_DIR, 'web')

TAG_ICON_DIR                    = os.path.join(ICON_DIR, 'tags')

USER_LOCAL_DATA                 = os.path.join(os.getenv('LOCALAPPDATA'), 'DAMGTEAM', 'PLM', '.configs')


IGNORE_ICONS                    = [ 'Widget', 'bright', 'dark', 'charcoal', 'nuker', 'TopTab1', 'TopTab2',
                                    'Organisation', 'Project', 'Team', 'Task', 'ShowAll','ItemWidget',
                                    'BaseManager', 'SettingInput', 'QueryPage', 'SysTray', 'Footer', 'BotTab1',
                                    'BotTab2', 'Cmd', 'User', 'Tracking']

logoDir = {'DAMG': 'DAMGTEAM', 'PLM': 'PLM'}



def get_app_icon(size=32, iconName="About"):

    if iconName not in IGNORE_ICONS:
        # Get the path to size directory
        iconPth = os.path.join(ICON_DIR, "x{0}".format(str(size)))
        # Get the icon file path
        if '.icon.png' in iconName:
            iconFilePth = os.path.join(iconPth, iconName)
        else:
            iconFilePth = os.path.join(iconPth, "{0}.icon.png".format(iconName))
        # Check icon file path
        if not os.path.exists(iconFilePth):
            FileNotFoundError('could not find: {0}'.format(iconFilePth))
        return iconFilePth



def get_logo_icon(size=32, name="DAMG"):

    try:
        pth = os.path.join(LOGO_DIR, logoDir[name])
    except KeyError:
        pth = LOGO_DIR

    logoFilePth = os.path.join(pth, "{0}x{0}.png".format(str(size)))

    if not os.path.exists(logoFilePth):
        return FileNotFoundError('could not find: {0}'.format(logoFilePth))
    else:
        return logoFilePth


def get_web_icon(size=32, webIconName=None):

    if webIconName not in IGNORE_ICONS:
        # Get the path to size directory
        iconPth = os.path.join(WEB_ICON_DIR, 'x{0}'.format(str(size)))
        # Get the icon file path
        iconFilePth = os.path.join(iconPth, "{0}.icon.png".format(webIconName))
        # Check icon file path
        if not os.path.exists(iconFilePth):
            FileNotFoundError('could not find: {0}'.format(iconFilePth))
        else:
            return iconFilePth


def get_tag_icon(tagIconName=None):

    if tagIconName not in IGNORE_ICONS:
        # Get the icon file path
        iconFilePth = os.path.join(TAG_ICON_DIR, "{0}.tag.png".format(tagIconName))
        # Check icon file path
        if not os.path.exists(iconFilePth):
            FileNotFoundError('could not find: {0}'.format(iconFilePth))
        else:
            return iconFilePth


def get_avatar_image(avatarName):

    avatarPth = os.path.join(USER_LOCAL_DATA, '{0}.avatar.jpg'.format(avatarName))

    if not os.path.exists(avatarPth):
        return os.path.join(AVATAR_DIR, 'default.avatar.jpg')
    else:
        return avatarPth


def check_preset(data):
    if data == {}:
        pass
    else:
        return True

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
