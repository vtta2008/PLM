# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import os

from bin.damg       import DAMG, DAMGDICT, DAMGLIST

from PLM.configs import (APPDATA_DAMG ,APPDATA_PLM ,CFG_DIR, TMP_DIR ,CACHE_DIR ,PREF_DIR ,SETTING_DIR, DB_DIR ,LOG_DIR,
                         TASK_DIR ,TEAM_DIR, PRJ_DIR, ORG_DIR, USER_LOCAL_DATA, LIBRARY_DIR, APP_SETTING, USER_SETTING,
                         FORMAT_SETTING, UNIX_SETTING, LOCAL_LOG, BIN_DIR ,BIN_BASE_DIR, BIN_CORE_DIR ,BIN_DAMG_DIR,
                         BIN_GUI_DIR ,BIN_WIDGET_DIR, BIN_NETWORK_DIR ,BIN_MODEL_DIR, BIN_SETTING_DIR ,BIN_VERSION_DIR,
                         BIN_DATA_DIR ,DESIGN_DIR, FONT_DIR ,JSON_DIR ,LANGUAGE_DIR ,PROFILE_DIR ,RESOURCES_DIR,
                         AVATAR_DIR ,ICON_DIR, NODE_ICON_DIR, TAG_ICON_DIR ,WEB_ICON_DIR ,WEB_ICON_16 ,WEB_ICON_24,
                         WEB_ICON_32 ,WEB_ICON_48, WEB_ICON_64 ,WEB_ICON_128 ,ICON_DIR_12 ,ICON_DIR_16 ,ICON_DIR_24,
                         ICON_DIR_32 ,ICON_DIR_48, ICON_DIR_64 ,IMAGE_DIR ,LOGO_DIR ,ORG_LOGO_DIR, APP_LOGO_DIR,
                         SCRIPTS_DIR ,CSS_DIR ,HTML_DIR, JS_DIR ,QSS_DIR ,SOUND_DIR ,DOCS_DIR ,RAWS_DIR,
                         DOCS_READING_DIR, TEMPLATE_DIR, TEMPLATE_LICENSE, API_DIR ,PLM_CFG_DIR, CORES_DIR,
                         CORES_BASE_DIR, CORES_DATA_DIR, CORES_HANDLERS_DIR, CORES_MODELS_DIR, LOGGER_DIR, PLUGINS_DIR,
                         UI_DIR, UI_BASE_DIR, UI_COMPONENTS_DIR, UI_LAYOUTS_DIR, UI_MODELS_DIR, UI_RCS_DIR, UI_TOOLS_DIR,
                         UTILS_DIR, TESTS_DIR, HUB_DIR, BLENDER_DIR, HOUDINI_DIR, MARI_DIR, MAYA_DIR,MUDBOX_DIR, NUKE_DIR,
                         SUBSTANCES_DIR, ZBRUSH_DIR)


from PLM.loggers import Loggers


a = [APP_SETTING, USER_SETTING, FORMAT_SETTING, UNIX_SETTING, LOCAL_LOG]


appDataSpot             = [APPDATA_DAMG, APPDATA_PLM, CFG_DIR, TMP_DIR, CACHE_DIR, PREF_DIR, SETTING_DIR, DB_DIR,
                           LOG_DIR, TASK_DIR, TEAM_DIR, PRJ_DIR, ORG_DIR, USER_LOCAL_DATA, LIBRARY_DIR]

binSpot                 = [BIN_DIR ,BIN_BASE_DIR, BIN_CORE_DIR ,BIN_DAMG_DIR, BIN_GUI_DIR ,BIN_WIDGET_DIR,
                           BIN_NETWORK_DIR ,BIN_MODEL_DIR, BIN_SETTING_DIR ,BIN_VERSION_DIR, BIN_DATA_DIR ,DESIGN_DIR,
                           FONT_DIR ,JSON_DIR ,LANGUAGE_DIR ,PROFILE_DIR ,RESOURCES_DIR,]

iconSpot                = [AVATAR_DIR ,ICON_DIR, NODE_ICON_DIR, TAG_ICON_DIR ,WEB_ICON_DIR ,WEB_ICON_16 ,WEB_ICON_24,
                           WEB_ICON_32 ,WEB_ICON_48, WEB_ICON_64 ,WEB_ICON_128 ,ICON_DIR_12 ,ICON_DIR_16 ,ICON_DIR_24,
                           ICON_DIR_32 ,ICON_DIR_48, ICON_DIR_64 ,IMAGE_DIR ,LOGO_DIR ,ORG_LOGO_DIR, APP_LOGO_DIR,]

docSpot                 = [SCRIPTS_DIR ,CSS_DIR ,HTML_DIR, JS_DIR ,QSS_DIR ,SOUND_DIR ,DOCS_DIR ,RAWS_DIR,
                            DOCS_READING_DIR, TEMPLATE_DIR, TEMPLATE_LICENSE,]


plmSpot                 = [API_DIR ,PLM_CFG_DIR, CORES_DIR, CORES_BASE_DIR, CORES_DATA_DIR, CORES_HANDLERS_DIR,
                           CORES_MODELS_DIR, LOGGER_DIR, PLUGINS_DIR, UI_DIR, UI_BASE_DIR, UI_COMPONENTS_DIR,
                           UI_LAYOUTS_DIR, UI_MODELS_DIR, UI_RCS_DIR, UI_TOOLS_DIR, UTILS_DIR, TESTS_DIR,]

hookSpot                = [HUB_DIR, BLENDER_DIR, HOUDINI_DIR, MARI_DIR, MAYA_DIR,MUDBOX_DIR, NUKE_DIR, SUBSTANCES_DIR,
                           ZBRUSH_DIR]


class BaseScan(DAMG):

    key                 = 'AutoScanner'

    _missing            = DAMGLIST()
    _findout            = DAMGLIST()

    alldirs             = appDataSpot + iconSpot + docSpot + plmSpot + hookSpot

    def __init__(self, parent=None):
        super(BaseScan, self).__init__(parent)

        self.logger     = Loggers(self)

        self.logger.hasHandlers()

    def scanAndFix(self):
        return self.scan(self.alldirs, True)

    def scanAll(self):
        return self.scan(self.alldirs, False)

    def scan(self, dirs=[], fix=False):
        for d in dirs:
            if not os.path.exists(d):
                if fix:
                    return self.fixDir()
                else:
                    self._missing.append(d)
                    self.logger.info('Detect path not exists: {0}'.format(d.replace('\\', '/')))

        self.update()

    def fixDir(self):
        for d in self.missing:
            self.makeDir(d)

    def makeDir(self, pth, mode=0o770):

        if not pth or os.path.exists(pth):
            return []

        (head, tail) = os.path.split(pth)
        res = self.makeDir(head, mode)
        try:
            original_umask = os.umask(0)
            os.makedirs(pth, mode)
        except:
            os.chmod(pth, mode)
        finally:
            os.umask(original_umask)
        res += [pth]

    def clear(self):
        return self._missing.clear(), self._findout.clear()

    @property
    def missing(self):
        return self._missing

    @missing.setter
    def missing(self, val):
        self._missing   = val

    @property
    def findout(self):
        return self._findout

    @findout.setter
    def findout(self, val):
        self._findout   = val


class DirScanner(BaseScan):

    key = 'DirScanner'

    def __init__(self, parent=None):
        super(DirScanner, self).__init__(parent)


    def timelog(self, info, **kwargs):
        pass



class PthScanner(BaseScan):

    key = 'PthScanner'

    def __init__(self, parent=None):
        super(PthScanner, self).__init__(parent)


    def timelog(self, info, **kwargs):
        pass


dir = DirScanner()
pth = PthScanner()



# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
