# -*- coding: utf-8 -*-
"""

Script Name: apps.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import globalSetting, save_data
""" Import """

# Python
import os, winshell, pprint

# PLM
from .pths                      import appsCfg


class ConfigApps(dict):

    key                         = 'ConfigApps'

    def __init__(self):
        super(ConfigApps, self).__init__()

        shortcuts               = {}
        programs                = winshell.programs(common=1)

        for paths, dirs, names in os.walk(programs):
            relpath = paths[len(programs) + 1:]
            shortcuts.setdefault(relpath, []).extend([winshell.shortcut(os.path.join(paths, n)) for n in names])

        for relpath, lnks in sorted(shortcuts.items()):
            for lnk in lnks:
                name, _ = os.path.splitext(os.path.basename(lnk.lnk_filepath))
                self[str(name)] = lnk.path

        if globalSetting.tracks.configInfo:
            if globalSetting.tracks.appInfo:
                pprint.pprint(self)

        if globalSetting.defaults.save_configInfo:
            if globalSetting.defaults.save_appInfo:
                save_data(appsCfg, self)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/20/2020 - 5:07 AM
# © 2017 - 2019 DAMGteam. All rights reserved