# -*- coding: utf-8 -*-
"""

Script Name: pths.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

import os

from .dirs                  import DAMG_LOGO_DIR, PLM_LOGO_DIR, CFG_DIR, SETTING_DIR, DB_DIR, LOG_DIR

DAMG_LOGO_32                = os.path.join(DAMG_LOGO_DIR, '32x32.png')
PLM_LOGO_32                 = os.path.join(PLM_LOGO_DIR, '32x32.png')

appIconCfg                  = os.path.join(CFG_DIR, 'appIcon.cfg')
webIconCfg                  = os.path.join(CFG_DIR, 'webIcon.cfg')
logoIconCfg                 = os.path.join(CFG_DIR, 'logoIcon.cfg')
pyEnvCfg                    = os.path.join(CFG_DIR, 'envKey.cfg')
mainConfig                  = os.path.join(CFG_DIR, 'main.cfg')
PLMconfig                   = os.path.join(CFG_DIR, 'PLM.cfg')

APP_SETTING                 = os.path.join(SETTING_DIR, 'PLM.ini')
USER_SETTING                = os.path.join(SETTING_DIR, 'user.ini')
FORMAT_SETTING              = os.path.join(SETTING_DIR, 'format.ini')
UNIX_SETTING                = os.path.join(SETTING_DIR, 'unix.ini')

DB_PTH                      = os.path.join(DB_DIR, 'local.db')
LOG_PTH                     = os.path.join(LOG_DIR, 'PLM.logs')

SETTING_FILEPTH = dict( app = APP_SETTING, user = USER_SETTING, unix = UNIX_SETTING, format = FORMAT_SETTING)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 28/11/2019 - 11:38 PM
# © 2017 - 2018 DAMGteam. All rights reserved