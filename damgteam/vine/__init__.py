# -*- coding: utf-8 -*-
"""

Script Name: __init__.py.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

from __future__ import absolute_import, unicode_literals

import re

from collections import namedtuple

from damgteam.vine.abstract import Thenable, Promise
from damgteam.vine.synchronization import Barrier
from damgteam.vine.funtools import (maybe_promise, ensure_promise, ppartial, preplace, starpromise, transform, wrap, )

__version__ = '1.1.4'
__author__ = 'Ask Solem'
__contact__ = 'ask@celeryproject.org'
__homepage__ = 'http://github.com/celery/vine'
__docformat__ = 'restructuredtext'

# -eof meta-

version_info_t = namedtuple('version_info_t', (
    'major', 'minor', 'micro', 'releaselevel', 'serial',
))
# bump version can only search for {current_version}
# so we have to parse the version here.
_temp = re.match( r'(\d+)\.(\d+).(\d+)(.+)?', __version__).groups()

VERSION = version_info = version_info_t(int(_temp[0]), int(_temp[1]), int(_temp[2]), _temp[3] or '', '')

print(_temp)
print(VERSION)

del(_temp)
del(re)

__all__ = ['Thenable', 'Promise', 'Barrier', 'maybe_promise', 'ensure_promise', 'ppartial', 'preplace', 'starpromise', 'transform', 'wrap', ]

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 8/09/2018 - 4:19 PM
# © 2017 - 2018 DAMGteam. All rights reserved