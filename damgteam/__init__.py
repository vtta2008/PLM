# -*- coding: utf-8 -*-
"""

Script Name: __init__.py.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, print_function, unicode_literals

import os, sys, re
from collections import namedtuple

__version__ = '4.2.0'
version_info_t = namedtuple('version_info_t', ('major', 'minor', 'micro', 'releaselevel', 'serial',))

_temp = re.match(r'(\d+)\.(\d+).(\d+)(.+)?', __version__).groups()
VERSION = version_info = version_info_t(int(_temp[0]), int(_temp[1]), int(_temp[2]), _temp[3] or '', '')

print(_temp)
print(VERSION)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 31/08/2018 - 7:22 PM
# © 2017 - 2018 DAMGteam. All rights reserved