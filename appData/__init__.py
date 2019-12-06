#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: __init__.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" import """

from appData            import config as c
from appData.config     import *

__envKey__              = c.__envKey__

PLMAPPID                = c.PLMAPPID
VERSION                 = c.VERSION
COPYRIGHT               = c.COPYRIGHT
margin                  = 5

# -------------------------------------------------------------------------------------------------------------
""" DAMG metadata """

__copyright__           = c.__copyright__
__organization__        = c.__organization__
__groupname__           = c.__groupname__
__damgSlogan__          = c.__damgSlogan__
__website__             = c.__website__
__author1__             = c.__author1__
__author2__             = c.__author2__
__Founder__             = c.__author1__
__CoFonder1__           = c.__author2__
__email1__              = c.__email1__
__email2__              = c.__email2__

# -------------------------------------------------------------------------------------------------------------
""" PLM metadata """

__project__             = c.__project__
__appname__             = c.__appname__
__appShortcut__         = c.__appShortcut__
__version__             = c.__version__
__versionFull__         = c.__versionFull__
__cfgVersion__          = c.__cfgVersion__
__verType__             = c.__verType__
__reverType__           = c.__reverType__
__about__               = c.__about__
__homepage__            = c.__homepage__
__plmSlogan__           = c.__plmSlogan__
__plmWiki__             = c.__plmWiki__

# -------------------------------------------------------------------------------------------------------------
""" Server metadata """

__globalServer__        = c.__globalServer__
__globalServerCheck__   = c.__globalServerCheck__
__globalServerAutho__   = c.__globalServerAutho__

__localPort__           = c.__localPort__
__localHost__           = c.__localHost__
__localServer__         = c.__localServer
__localServerCheck__    = c.__localServerCheck__
__localServerAutho__    = c.__localServerAutho__

__google__              = c.__google__
__googleVN__            = c.__googleVN__
__googleNZ__            = c.__googleNZ__
__email__               = c.__email__
__packages_dir__        = c.__packages_dir__
__classifiers__         = c.__classifiers__
__download__            = c.__download__
__description__         = c.__description__
__readme__              = c.__readme__
__modules__             = c.__modules__
__pkgsReq__             = c.__pkgsReq__

# from . import dirs
# from bin import DAMGDICT
#
# ignoreKey = ['__name__', '__doc__', '__package__', '__loader__', '__spec__', ' __file__', ' __cached__',
#              '__builtins__', ' os', ' __envKey__']
#
# from __buildtins__ import ROOT
#
#
#
# class Dirs(DAMGDICT):
#
#     key = 'Dirs'
#
#     _check = False
#
#     def __init__(self):
#         super(Dirs, self).__init__()
#
#         keys = [k for k in vars(dirs).keys() if k not in ignoreKey]
#         for k, v in vars(dirs).items():
#             if k in keys:
#                 self.add(k, v)
#
#         print(self)
#
#         ext = 'cfg'
#         with open(os.path.join(ROOT, 'appData', '.config', '{0}.{1}'.format(self.__class__.__name__, ext)), 'w') as f:
#             json.dump(self, f, indent=4)
#             f.close()
#         self.check = True
#
# a = Dirs()
