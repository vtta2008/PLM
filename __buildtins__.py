# -*- coding: utf-8 -*-
"""

Script Name: __buildins__.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

__envKey__ = "DAMGTEAM"

import os, sys

ROOT = os.path.abspath(os.getcwd())

from cores.EnvVariableManager import EnvVariableManager

try:
    os.getenv(__envKey__)
except KeyError:
    cfgable                     = False
    EnvVariableManager(__envKey__, ROOT)
else:
    if os.getenv(__envKey__)   != ROOT:
        EnvVariableManager(__envKey__, ROOT)
        cfgable                 = True
    else:
        cfgable                 = True

from cores.ConfigManager import ConfigManager
configManager = ConfigManager(__envKey__, ROOT)

if not configManager.cfgs:
    print("CONFIGERROR: configurations have not done yet.")
    sys.exit()
else:
    print('Configurations has been completed.')
# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 6:55 AM
# © 2017 - 2018 DAMGteam. All rights reserved