# -*- coding: utf-8 -*-
"""

Script Name: mayas.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

""" Import """

# Python
import os, sys, shutil

# PLM
from .dirs import MAYA_DIR
from .keys import autodeskVer

class ConfigMaya(dict):

    key                                 = 'ConfigMaya'

    def __init__(self):
        super(ConfigMaya, self).__init__()
        modules = ['anim', 'lib', 'modeling', 'rendering', 'simulating', 'surfacing']
        modulePth = os.path.join(MAYA_DIR, 'modules')
        paths = [os.path.join(modulePth, m) for m in modules]
        sys.path.insert(-1, ';'.join(paths))

        usScr = os.path.join(MAYA_DIR, 'userSetup.py')

        if os.path.exists(usScr):
            mayaVers = [os.path.join(MAYA_DIR, v) for v in autodeskVer if os.path.exists(os.path.join(MAYA_DIR, v))] or []
            if not len(mayaVers) == 0 or not mayaVers == []:
                for usDes in mayaVers:
                    shutil.copy(usScr, usDes)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/20/2020 - 5:10 AM
# © 2017 - 2019 DAMGteam. All rights reserved