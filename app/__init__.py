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
    ROOT = BASE.split('appData')[0]
else:
    ROOT = (os.path.dirname(__file__).split(__name__)[0])

try:
    os.getenv('ROOT')
except KeyError:
    subprocess.Popen('SetX {} %CD%'.format('ROOT'), shell=True).wait()
else:
    if os.getenv('ROOT') != ROOT:
        subprocess.Popen('SetX {} %CD%'.format('ROOT'), shell=True).wait()

from bin.damgdock.types import damg_dirs

DAMG_DIR = damg_dirs['DAMG_DIR']
DAMG_CFG_DIR = damg_dirs['DAMG_CFG_DIR']
DAMG_CFG_SETTING_DIR = damg_dirs['DAMG_CFG_SETTING_DIR']
DAMG_CFG_LOG_DIR = damg_dirs['DAMG_CFG_LOG_DIR']
DAMG_CFG_CACHE_DIR = damg_dirs['DAMG_CFG_CACHE_DIR']
DAMG_CFG_PREF_DIR = damg_dirs['DAMG_CFG_PREF_DIR']
BIN_DIR = damg_dirs['BIN_DIR']
DEPENDANCIES_DIR = damg_dirs['DEPENDANCIES_DIR']
SCRIPTS_DIR = damg_dirs['SCRIPTS_DIR']
DATA_DIR = damg_dirs['DATA_DIR']
DATA_JSON_DIR = damg_dirs['DATA_JSON_DIR']
DATA_DOC_DIR = damg_dirs['DATA_DOC_DIR']
DATA_SCR_DIR = damg_dirs['DATA_SCR_DIR']
DATA_SCR_DOC_DIR = damg_dirs['DATA_SCR_DOC_DIR']
QSS_DIR = damg_dirs['QSS_DIR']
IMG_DIR = damg_dirs['IMG_DIR']
ICON_DIR = damg_dirs['ICON_DIR']
ICON_DIR_16 = damg_dirs['ICON_DIR_16']
ICON_DIR_24 = damg_dirs['ICON_DIR_24']
ICON_DIR_32 = damg_dirs['ICON_DIR_32']
ICON_DIR_48 = damg_dirs['ICON_DIR_48']
ICON_DIR_64 = damg_dirs['ICON_DIR_64']
WEB_ICON_DIR = damg_dirs['WEB_ICON_DIR']
WEB_ICON_16 = damg_dirs['WEB_ICON_16']
WEB_ICON_24 = damg_dirs['WEB_ICON_24']
WEB_ICON_32 = damg_dirs['WEB_ICON_32']
WEB_ICON_48 = damg_dirs['WEB_ICON_48']
WEB_ICON_64 = damg_dirs['WEB_ICON_64']
WEB_ICON_128 = damg_dirs['WEB_ICON_128']
AVATAR_DIR = damg_dirs['AVATAR_DIR']
LOGO_DIR = damg_dirs['LOGO_DIR']
PIC_DIR = damg_dirs['PIC_DIR']
TAG_DIR = damg_dirs['TAG_DIR']
DAMG_LOGO_DIR = damg_dirs['DAMG_LOGO_DIR']
PLM_LOGO_DIR = damg_dirs['PLM_LOGO_DIR']
DAMG_LOGO_32 = damg_dirs['DAMG_LOGO_32']
PLM_LOGO_32 = damg_dirs['PLM_LOGO_32']
BUILD_DIR = damg_dirs['BUILD_DIR']
CORE_DIR = damg_dirs['CORE_DIR']
PLUGIN_DIR = damg_dirs['PLUGIN_DIR']
TEST_DIR = damg_dirs['TEST_DIR']
ASSETS_DIR = damg_dirs['ASSETS_DIR']
ASSETS_CFG_DIR = damg_dirs['ASSETS_CFG_DIR']
PLM_DIR = damg_dirs['PLM_DIR']
PLM_CFG_DIR = damg_dirs['PLM_CFG_DIR']
PLM_CFG_SETTING_DIR = damg_dirs['PLM_CFG_SETTING_DIR']
PLM_CFG_LOG_DIR = damg_dirs['PLM_CFG_LOG_DIR']
PLM_CFG_CACHE_DIR = damg_dirs['PLM_CFG_CACHE_DIR']
PLM_CFG_PREF_DIR = damg_dirs['PLM_CFG_PREF_DIR']
SCENEGRAPH_DIR = damg_dirs['SCENEGRAPH_DIR']
SCENEGRAPH_CFG_DIR = damg_dirs['SCENEGRAPH_CFG_DIR']
SCENEGRAPH_CFG_SETTING_DIR = damg_dirs['SCENEGRAPH_CFG_SETTING_DIR']
SCENEGRAPH_CFG_LOG_DIR = damg_dirs['SCENEGRAPH_CFG_LOG_DIR']
SCENEGRAPH_CFG_CACHE_DIR = damg_dirs['SCENEGRAPH_CFG_CACHE_DIR']
SCENEGRAPH_CFG_PREF_DIR = damg_dirs['SCENEGRAPH_CFG_PREF_DIR']
NODEGRAPH_DIR = damg_dirs['NODEGRAPH_DIR']
NODEGRAPH_CFG_DIR = damg_dirs['NODEGRAPH_CFG_DIR']
NODEGRAPH_CFG_SETTING_DIR = damg_dirs['NODEGRAPH_CFG_SETTING_DIR']
NODEGRAPH_CFG_LOG_DIR = damg_dirs['NODEGRAPH_CFG_LOG_DIR']
NODEGRAPH_CFG_CACHE_DIR = damg_dirs['NODEGRAPH_CFG_CACHE_DIR']
NODEGRAPH_CFG_PREF_DIR = damg_dirs['NODEGRAPH_CFG_PREF_DIR']

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 24/08/2018 - 1:28 AM
# © 2017 - 2018 DAMGteam. All rights reserved