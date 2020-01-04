# -*- coding: utf-8 -*-
"""

Script Name: pths.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import globalSetting

import os, json, pprint

from .dirs                  import CFG_DIR, SETTING_DIR, DB_DIR, LOG_DIR, QSS_DIR
from bin                    import DAMGDICT

def save_data(filePth, data):
    if os.path.exists(filePth):
        os.remove(filePth)
    with open(filePth, 'w+') as f:
        json.dump(data, f, indent=4)
    return True

# -------------------------------------------------------------------------------------------------------------
""" config file """

evnInfoCfg                  = os.path.join(CFG_DIR, 'envs.cfg')
iconCfg                     = os.path.join(CFG_DIR, 'icons.cfg')
avatarCfg                   = os.path.join(CFG_DIR, 'avatars.cfg')
logoCfg                     = os.path.join(CFG_DIR, 'logo.cfg')
mayaCfg                     = os.path.join(CFG_DIR, 'maya.cfg')
webIconCfg                  = os.path.join(CFG_DIR, 'webIcon.cfg')
nodeIconCfg                 = os.path.join(CFG_DIR, 'nodeIcons.cfg')
picCfg                      = os.path.join(CFG_DIR, 'pics.cfg')
tagCfg                      = os.path.join(CFG_DIR, 'tags.cfg')
pythonCfg                   = os.path.join(CFG_DIR, 'python.cfg')
plmCfg                      = os.path.join(CFG_DIR, 'pipeline.cfg')
appsCfg                     = os.path.join(CFG_DIR, 'installed.cfg')
envVarCfg                   = os.path.join(CFG_DIR, 'envVar.cfg')
dirCfg                      = os.path.join(CFG_DIR, 'dirs.cfg')
pthCfg                      = os.path.join(CFG_DIR, 'paths.cfg')
deviceCfg                   = os.path.join(CFG_DIR, 'device.cfg')
urlCfg                      = os.path.join(CFG_DIR, 'url.cfg')
userCfg                     = os.path.join(CFG_DIR, 'user.cfg')
PLMconfig                   = os.path.join(CFG_DIR, 'PLM.cfg')
sceneGraphCfg               = os.path.join(CFG_DIR, 'sceneGraph.cfg')

# -------------------------------------------------------------------------------------------------------------
""" setting file """

APP_SETTING                 = os.path.join(SETTING_DIR, 'PLM.ini')
USER_SETTING                = os.path.join(SETTING_DIR, 'user.ini')
FORMAT_SETTING              = os.path.join(SETTING_DIR, 'format.ini')
UNIX_SETTING                = os.path.join(SETTING_DIR, 'unix.ini')

LOCAL_DB                    = os.path.join(DB_DIR, 'local.db')
LOCAL_LOG                   = os.path.join(LOG_DIR, 'PLM.logs')

QSS_PATH                    = os.path.join(QSS_DIR, 'style.qss')
MAIN_SCSS_PTH               = os.path.join(QSS_DIR, 'main.scss')
STYLE_SCSS_PTH              = os.path.join(QSS_DIR, '_styles.scss')
VAR_SCSS_PTH                = os.path.join(QSS_DIR, '_variables.scss')

SETTING_FILEPTH = dict(app = APP_SETTING, user = USER_SETTING, unix = UNIX_SETTING, format = FORMAT_SETTING)



class ConfigPath(DAMGDICT):

    key                     = 'ConfigPath'

    def __init__(self):
        super(ConfigPath, self).__init__()

        self.add('evnInfoCfg', evnInfoCfg)
        self.add('iconCfg', iconCfg)
        self.add('avatarCfg', avatarCfg)
        self.add('logoCfg', logoCfg)
        self.add('mayaCfg', mayaCfg)
        self.add('webIconCfg', webIconCfg)
        self.add('nodeIconCfg', nodeIconCfg)
        self.add('picCfg', picCfg)
        self.add('tagCfg', tagCfg)
        self.add('pythonCfg', pythonCfg)
        self.add('plmCfg', plmCfg)
        self.add('appsCfg', appsCfg)
        self.add('envVarCfg', envVarCfg)
        self.add('dirCfg', dirCfg)
        self.add('pthCfg', pthCfg)
        self.add('deviceCfg', deviceCfg)
        self.add('urlCfg', urlCfg)
        self.add('userCfg', userCfg)
        self.add('PLMconfig', PLMconfig)
        self.add('sceneGraphCfg', sceneGraphCfg)
        self.add('APP_SETTING', APP_SETTING)
        self.add('USER_SETTING', USER_SETTING)
        self.add('FORMAT_SETTING', FORMAT_SETTING)
        self.add('UNIX_SETTING', UNIX_SETTING)
        self.add('LOCAL_DB', LOCAL_DB)
        self.add('LOCAL_LOG', LOCAL_LOG)
        self.add('QSS_PATH', QSS_PATH)
        self.add('MAIN_SCSS_PTH', MAIN_SCSS_PTH)
        self.add('STYLE_SCSS_PTH', STYLE_SCSS_PTH)
        self.add('VAR_SCSS_PTH', VAR_SCSS_PTH)
        self.add('SETTING_FILEPTH', SETTING_FILEPTH)

        if globalSetting.tracks.configInfo:
            if globalSetting.tracks.pthInfo:
                pprint.pprint(self)

        if globalSetting.defaults.save_configInfo:
            if globalSetting.defaults.save_pathInfo:
                save_data(pthCfg, self)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 28/11/2019 - 11:38 PM
# © 2017 - 2018 DAMGteam. All rights reserved