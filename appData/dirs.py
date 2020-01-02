# -*- coding: utf-8 -*-
"""

Script Name: path.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import ROOT, __envKey__

""" Import """

# Python
import os, subprocess
if os.getenv(__envKey__) != ROOT:
    subprocess.Popen('Set {0} {1}'.format(__envKey__, ROOT), shell=True).wait()

# PLM
from .metadatas import __appname__

# -------------------------------------------------------------------------------------------------------------
""" Local pc """

APPDATA_DAMG        = os.path.join(os.getenv('PROGRAMDATA'), __envKey__)
APPDATA_PLM         = os.path.join(APPDATA_DAMG, __appname__)
CFG_DIR             = os.path.join(APPDATA_PLM, '.configs')
TMP_DIR             = os.path.join(APPDATA_PLM, '.tmp')
CACHE_DIR           = os.path.join(APPDATA_PLM, '.cache')
SETTING_DIR         = CFG_DIR
LOG_DIR             = CFG_DIR
PREF_DIR            = CFG_DIR
TASK_DIR            = os.path.join(CFG_DIR, 'task')
TEAM_DIR            = os.path.join(CFG_DIR, 'team')
OJ_DIR            = os.path.join(CFG_DIR, 'project')
ORG_DIR             = os.path.join(CFG_DIR, 'organisation')
USER_LOCAL_DATA     = os.path.join(CFG_DIR, 'userLocal')

# -------------------------------------------------------------------------------------------------------------
""" appData """

APP_DATA_DIR        = os.path.join(ROOT, 'appData')
DB_DIR              = APP_DATA_DIR

# -------------------------------------------------------------------------------------------------------------
""" assets """

ASSETS_DIR          = os.path.join(ROOT, 'assets')
AVATAR_DIR          = os.path.join(ASSETS_DIR, 'avatar')
FONT_DIR            = os.path.join(ASSETS_DIR, 'fonts')
IMAGE_DIR           = os.path.join(ASSETS_DIR, 'images')

LOGO_DIR            = os.path.join(ASSETS_DIR, 'logo')
DAMG_LOGO_DIR       = os.path.join(LOGO_DIR, 'DAMGTEAM')
PLM_LOGO_DIR        = os.path.join(LOGO_DIR, 'PLM')

PIC_DIR             = os.path.join(ASSETS_DIR, 'pics')
STYLE_DIR           = os.path.join(ASSETS_DIR, 'styles')
STYLE_IMAGE_DIR     = os.path.join(STYLE_DIR, 'images')
STYLE_RC_DIR        = os.path.join(STYLE_DIR, 'rc')
STYLE_SVG_DIR       = os.path.join(STYLE_DIR, 'svg')

# -------------------------------------------------------------------------------------------------------------
""" bin """

BIN_DIR             = os.path.join(ROOT, 'bin')
DATA_DIR            = os.path.join(BIN_DIR, 'data')
JSON_DIR            = os.path.join(DATA_DIR, 'json')

DEPENDANCIES_DIR    = os.path.join(BIN_DIR, 'dependencies')

DOCS_DIR            = os.path.join(BIN_DIR, 'docs')
RST_DIR             = os.path.join(DOCS_DIR, 'rst')
TXT_DIR             = os.path.join(DOCS_DIR, 'txt')
RAWS_DATA_DIR       = os.path.join(DOCS_DIR, 'raw')
TEMPLATE_DIR        = os.path.join(DOCS_DIR, 'template')
TEMPLATE_LICENCE    = os.path.join(TEMPLATE_DIR, 'LICENCE')

RCS_DIR             = os.path.join(BIN_DIR, 'rcs')
CSS_DIR             = os.path.join(RCS_DIR, 'css')
HTML_DIR            = os.path.join(RCS_DIR, 'html')
JS_DIR              = os.path.join(RCS_DIR, 'js')
QSS_DIR             = os.path.join(RCS_DIR, 'qss')


# -------------------------------------------------------------------------------------------------------------
""" build """

BUILD_DIR           = os.path.join(ROOT, 'build')

# -------------------------------------------------------------------------------------------------------------
""" cores """

CORES_DIR           = os.path.join(ROOT, 'cores')
CORES_ASSETS_DIR    = os.path.join(CORES_DIR, 'assets')
CORES_BASE_DIR      = os.path.join(CORES_DIR, 'base')

# -------------------------------------------------------------------------------------------------------------
""" devkit """

DEVKIT_DIR          = os.path.join(ROOT, 'devkit')
DEVKIT_CORE         = os.path.join(DEVKIT_DIR, 'Core')
DEVKIT_GUI          = os.path.join(DEVKIT_DIR, 'Gui')
DEVKIT_WIDGET       = os.path.join(DEVKIT_DIR, 'Widgets')

# -------------------------------------------------------------------------------------------------------------
""" hooks """

HOOK_DIR            = os.path.join(ROOT, 'hooks')
MAYA_DIR            = os.path.join(HOOK_DIR, 'Maya')
MARI_DIR            = os.path.join(HOOK_DIR, 'Mari')
NUKE_DIR            = os.path.join(HOOK_DIR, 'Nuke')
ZBRUSH_DIR          = os.path.join(HOOK_DIR, 'ZBrush')
HOUDINI_DIR         = os.path.join(HOOK_DIR, 'Houdini')

# -------------------------------------------------------------------------------------------------------------
""" icons """

ICON_DIR            = os.path.join(ROOT, 'icons')

TAG_ICON_DIR        = os.path.join(ICON_DIR, 'tags')

MAYA_ICON_DIR       = os.path.join(ICON_DIR, 'maya')

NODE_ICON_DIR       = os.path.join(ICON_DIR, 'node')

WEB_ICON_DIR        = os.path.join(ICON_DIR, 'web')
WEB_ICON_16         = os.path.join(WEB_ICON_DIR, 'x16')
WEB_ICON_24         = os.path.join(WEB_ICON_DIR, 'x24')
WEB_ICON_32         = os.path.join(WEB_ICON_DIR, 'x32')
WEB_ICON_48         = os.path.join(WEB_ICON_DIR, 'x48')
WEB_ICON_64         = os.path.join(WEB_ICON_DIR, 'x64')
WEB_ICON_128        = os.path.join(WEB_ICON_DIR, 'x128')

ICON_DIR_12         = os.path.join(ICON_DIR, 'x12')
ICON_DIR_16         = os.path.join(ICON_DIR, 'x16')
ICON_DIR_24         = os.path.join(ICON_DIR, 'x24')
ICON_DIR_32         = os.path.join(ICON_DIR, 'x32')
ICON_DIR_48         = os.path.join(ICON_DIR, 'x48')
ICON_DIR_64         = os.path.join(ICON_DIR, 'x64')

# -------------------------------------------------------------------------------------------------------------
""" libs """

LIB_DIR             = os.path.join(ROOT, 'libs')
SOUND_DIR           = os.path.join(LIB_DIR, 'sound')

# -------------------------------------------------------------------------------------------------------------
""" modules """

MODULE_DIR          = os.path.join(ROOT, 'modules')

# -------------------------------------------------------------------------------------------------------------
""" plugins """

PLUGIN_DIR          = os.path.join(ROOT, 'plugins')
NODEGRAPH_DIR       = os.path.join(PLUGIN_DIR, 'NodeGraph')

# -------------------------------------------------------------------------------------------------------------
""" scripts """

SCRIPT_DIR          = os.path.join(ROOT, 'scripts')

# -------------------------------------------------------------------------------------------------------------
""" test """

TEST_DIR            = os.path.join(ROOT, 'test')

# -------------------------------------------------------------------------------------------------------------
""" ui """

UI_DIR              = os.path.join(ROOT, 'ui')
UI_BASE_DIR         = os.path.join(UI_DIR, 'base')
UI_ASSET_DIR        = os.path.join(UI_DIR, 'assets')
BODY_DIR            = os.path.join(UI_DIR, 'Body')
TABS_DIR            = os.path.join(BODY_DIR, 'Tabs')
FOOTER_DIR          = os.path.join(UI_DIR, 'Footer')
HEADER_DIR          = os.path.join(UI_DIR, 'Header')

SUBUI_DIR           = os.path.join(UI_DIR, 'SubUi')
FUNCS_DIR           = os.path.join(SUBUI_DIR, 'Funcs')
PRJ_DIR             = os.path.join(SUBUI_DIR, 'Projects')
SETTINGS_DIR        = os.path.join(SUBUI_DIR, 'Settings')
TOOLS_DIR           = os.path.join(SUBUI_DIR, 'Tools')

# -------------------------------------------------------------------------------------------------------------
""" utils """

UTILS_DIR           = os.path.join(ROOT, 'utils')

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 10:45 PM
# Pipeline manager - DAMGteam
