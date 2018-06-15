# -*- coding: utf-8 -*-
"""

Script Name: MayaCfg.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os
import shutil


# Plm
import appData as app

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logger = app.logger

# -------------------------------------------------------------------------------------------------------------
""" Variables """

# -------------------------------------------------------------------------------------------------------------
""" MayaCfg """


class MayaCfg(object):

    def __init__(self):
        super(MayaCfg, self).__init__()

        self.settings = app.appSetting

        tk = os.path.join(os.getenv(app.__envKey__), 'tankers', 'pMaya')

        tanker = dict(modules=['anim', 'lib', 'modeling', 'rendering', 'simulating', 'surfacing', ], QtPlugins=[], )

        pVal = ""
        pyList = [os.path.join(tk, k) for k in tanker] + [os.path.join(tk, "modules", p) for p in tanker["modules"]]

        for p in pyList:
            pVal += p + ';'
        os.environ['PYTHONPATH'] = pVal

        # Copy userSetup.py from source code to properly maya folder
        usScr = os.path.join(os.getenv(app.__envKey__), 'packages', 'maya', 'userSetup.py')
        if os.path.exists(usScr):
            mayaVers = [os.path.join(tk, v) for v in app.autodeskVer if os.path.exists(os.path.join(tk, v))] or []
            if not len(mayaVers) == 0 or not mayaVers == []:
                for usDes in mayaVers:
                    shutil.copy(usScr, usDes)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 4/06/2018 - 12:59 AM
# © 2017 - 2018 DAMGteam. All rights reserved