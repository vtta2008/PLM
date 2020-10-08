# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import os

BIN_ROOT                        = os.path.dirname(__file__)
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


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
