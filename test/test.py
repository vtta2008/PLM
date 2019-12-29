# -*- coding: utf-8 -*-
"""

Script Name: test.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
import os, sys, pprint, winshell
from bin import DAMGDICT

appInfo = DAMGDICT()

programs = winshell.programs(common=1)
shortcuts = {}

for paths, dirs, names in os.walk(programs):
    relpath = paths[len(programs) + 1:]
    shortcuts.setdefault(relpath, []).extend([winshell.shortcut(os.path.join(paths, n)) for n in names])

for relpath, lnks in sorted(shortcuts.items()):
    for lnk in lnks:
        name, _ = os.path.splitext(os.path.basename(lnk.lnk_filepath))
        appInfo[str(name)] = lnk.path

pprint.pprint(appInfo)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 1:38 AM
# © 2017 - 2018 DAMGteam. All rights reserved