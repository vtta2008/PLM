# -*- coding: utf-8 -*-
"""

Script Name: pths.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

import os

from .dirs                  import CFG_DIR, SETTING_DIR, DB_DIR, LOG_DIR, QSS_DIR, RCS_DIR, SCSS_DIR

evnInfoCfg                  = os.path.join(CFG_DIR, 'envs.cfg')
iconCfg                     = os.path.join(CFG_DIR, 'icons.cfg')
avatarCfg                   = os.path.join(CFG_DIR, 'avatars.cfg')
logoCfg                     = os.path.join(CFG_DIR, 'logo.cfg')
mayaIconCfg                 = os.path.join(CFG_DIR, 'mayaIcons.cfg')
webIconCfg                  = os.path.join(CFG_DIR, 'webIcon.cfg')
nodeIconCfg                 = os.path.join(CFG_DIR, 'nodeIcons.cfg')
picCfg                      = os.path.join(CFG_DIR, 'pics.cfg')
tagCfg                      = os.path.join(CFG_DIR, 'tags.cfg')
pythonCfg                   = os.path.join(CFG_DIR, 'python.cfg')
pipelineCfg                 = os.path.join(CFG_DIR, 'pipeline.cfg')
appsCfg                     = os.path.join(CFG_DIR, 'installed.cfg')
envVarCfg                   = os.path.join(CFG_DIR, 'envVar.cfg')
dirCfg                      = os.path.join(CFG_DIR, 'dirs.cfg')
pthCfg                      = os.path.join(CFG_DIR, 'paths.cfg')
deviceCfg                   = os.path.join(CFG_DIR, 'device.cfg')
userCfg                     = os.path.join(CFG_DIR, 'user.cfg')
PLMconfig                   = os.path.join(CFG_DIR, 'PLM.cfg')
sceneGraphCfg               = os.path.join(CFG_DIR, 'sceneGraph.cfg')

APP_SETTING                 = os.path.join(SETTING_DIR, 'PLM.ini')
USER_SETTING                = os.path.join(SETTING_DIR, 'user.ini')
FORMAT_SETTING              = os.path.join(SETTING_DIR, 'format.ini')
UNIX_SETTING                = os.path.join(SETTING_DIR, 'unix.ini')

LOCAL_DB                    = os.path.join(DB_DIR, 'local.db')
LOCAL_LOG                   = os.path.join(LOG_DIR, 'PLM.logs')

QSS_PATH                    = os.path.join(QSS_DIR, 'style.qss')
QRC_PATH                    = os.path.join(RCS_DIR, 'style.qrc')
MAIN_SCSS_PTH               = os.path.join(SCSS_DIR, 'main.scss')
STYLE_SCSS_PTH              = os.path.join(SCSS_DIR, '_styles.scss')
VAR_SCSS_PTH                = os.path.join(SCSS_DIR, '_variables.scss')

SETTING_FILEPTH = dict( app = APP_SETTING, user = USER_SETTING, unix = UNIX_SETTING, format = FORMAT_SETTING)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 28/11/2019 - 11:38 PM
# © 2017 - 2018 DAMGteam. All rights reserved