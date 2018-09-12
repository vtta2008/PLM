# -*- coding: utf-8 -*-
"""

Script Name: __init__.py.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

import os, subprocess

BASE = os.path.dirname(__file__).split(__name__)[0]

if __name__ == '__main__':
    ROOT = BASE.split('app')[0]
else:
    ROOT = (os.path.dirname(__file__).split(__name__)[0])

try:
    os.getenv('ROOT')
except KeyError:
    subprocess.Popen('SetX {} %CD%'.format('ROOT'), shell=True).wait()
else:
    if os.getenv('ROOT') != ROOT:
        subprocess.Popen('SetX {} %CD%'.format('ROOT'), shell=True).wait()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 24/08/2018 - 1:28 AM
# © 2017 - 2018 DAMGteam. All rights reserved