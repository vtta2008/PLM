# -*- coding: utf-8 -*-
'''

Script Name: main.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

'''
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

import os, subprocess
ROOT = os.path.dirname(__file__).split(__name__)[0]

try:
    os.getenv('ROOT')
except KeyError:
    subprocess.Popen('SetX ROOT %CD%', shell=True).wait()
else:
    if ROOT != os.getenv('ROOT'):
        subprocess.Popen('SetX ROOT %CD%', shell=True).wait()


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 22/08/2018 - 12:24 AM
# © 2017 - 2018 DAMGteam. All rights reserved