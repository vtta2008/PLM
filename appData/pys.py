# -*- coding: utf-8 -*-
"""

Script Name: pys.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import globalSetting
""" Import """

# Python
import os, sys, platform, pkg_resources, pprint, json

# PLM
from .pths                          import pythonCfg


def save_data(filePth, data):
    if os.path.exists(filePth):
        os.remove(filePth)
    with open(filePth, 'w+') as f:
        json.dump(data, f, indent=4)
    return True


class ConfigPython(dict):

    key                             = 'ConfigPython'

    def __init__(self):
        super(ConfigPython, self).__init__()

        self['python']              = platform.python_build()
        self['python version']      = platform.python_version()

        pths                        = [p.replace('\\', '/') for p in os.getenv('PATH').split(';')[0:]]
        sys.path                    = [p.replace('\\', '/') for p in sys.path]

        for p in pths:
            if os.path.exists(p):
                if not p in sys.path:
                    sys.path.insert(-1, p)

        for py in pkg_resources.working_set:
            self[py.project_name]   = py.version

        if globalSetting.tracks.configInfo:
            if globalSetting.tracks.pythonInfo:
                pprint.pprint(self)

        if globalSetting.defaults.save_configInfo:
            if globalSetting.defaults.save_pythonInfo:
                save_data(pythonCfg, self)



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/19/2020 - 10:40 PM
# © 2017 - 2019 DAMGteam. All rights reserved