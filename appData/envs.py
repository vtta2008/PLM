# -*- coding: utf-8 -*-
"""

Script Name: envs.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import globalSetting, save_data
""" Import """

# Python
import os, pprint

# PLM
from .pths import envVarCfg

class ConfigEnvVar(dict):

    key                                 = 'ConfigEnvVar'

    def __init__(self):
        super(ConfigEnvVar, self).__init__()
        for k, v in os.environ.items():
            self[k]                     = v.replace('\\', '/')

        if globalSetting.tracks.configInfo:
            if globalSetting.tracks.envInfo:
                pprint.pprint(self)

        if globalSetting.defaults.save_configInfo:
            if globalSetting.defaults.save_envInfo:
                save_data(envVarCfg, self)

    def update(self):
        for k, v in os.environ.items():
            self[k]                     = v.replace('\\', '/')

        if globalSetting.defaults.save_configInfo:
            if globalSetting.defaults.save_envInfo:
                save_data(envVarCfg, self)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/20/2020 - 4:51 AM
# © 2017 - 2019 DAMGteam. All rights reserved