# -*- coding: utf-8 -*-
'''

Script Name: path.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

'''
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import ROOT, __envKey__

''' Import '''

# Python
import os, subprocess
if os.getenv(__envKey__) != ROOT:
    subprocess.Popen('Set {0} {1}'.format(__envKey__, ROOT), shell=True).wait()

# PLM
from .metadatas     import __appname__, __organization__
from bin            import DAMGDICT

# -------------------------------------------------------------------------------------------------------------
''' Local pc '''

APPDATA_DAMG        = os.path.join(os.getenv('APPDATA'), __organization__)
APPDATA_PLM         = os.path.join(APPDATA_DAMG, __appname__)
CFG_DIR             = os.path.join(APPDATA_PLM, '.configs')
TMP_DIR             = os.path.join(APPDATA_PLM, '.tmp')
CACHE_DIR           = os.path.join(APPDATA_PLM, '.cache')
SETTING_DIR         = CFG_DIR
LOG_DIR             = CFG_DIR
PREF_DIR            = CFG_DIR
TASK_DIR            = os.path.join(CFG_DIR, 'task')
TEAM_DIR            = os.path.join(CFG_DIR, 'team')
OJ_DIR              = os.path.join(CFG_DIR, 'project')
ORG_DIR             = os.path.join(CFG_DIR, 'organisation')
USER_LOCAL_DATA     = os.path.join(CFG_DIR, 'userLocal')

# -------------------------------------------------------------------------------------------------------------
''' appData '''

APP_DATA_DIR        = os.path.join(ROOT, 'appData')
DB_DIR              = APP_DATA_DIR

# -------------------------------------------------------------------------------------------------------------
''' assets '''

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
''' bin '''

BIN_DIR             = os.path.join(ROOT, 'bin')
DATA_DIR            = os.path.join(BIN_DIR, 'data')
JSON_DIR            = os.path.join(DATA_DIR, 'json')

DEPENDANCIES_DIR    = os.path.join(BIN_DIR, 'dependencies')

DOCS_DIR            = os.path.join(BIN_DIR, 'docs')
RST_DIR             = os.path.join(DOCS_DIR, 'rst')
TXT_DIR             = os.path.join(DOCS_DIR, 'txt')
RAWS_DATA_DIR       = os.path.join(DOCS_DIR, 'raws')
TEMPLATE_DIR        = os.path.join(DOCS_DIR, 'template')
TEMPLATE_LICENCE    = os.path.join(TEMPLATE_DIR, 'LICENCE')

RCS_DIR             = os.path.join(BIN_DIR, 'rcs')
CSS_DIR             = os.path.join(RCS_DIR, 'css')
HTML_DIR            = os.path.join(RCS_DIR, 'html')
JS_DIR              = os.path.join(RCS_DIR, 'js')
QSS_DIR             = os.path.join(RCS_DIR, 'qss')


# -------------------------------------------------------------------------------------------------------------
''' build '''

BUILD_DIR           = os.path.join(ROOT, 'build')

# -------------------------------------------------------------------------------------------------------------
''' cores '''

CORES_DIR           = os.path.join(ROOT, 'cores')
CORES_ASSETS_DIR    = os.path.join(CORES_DIR, 'assets')
CORES_BASE_DIR      = os.path.join(CORES_DIR, 'base')

# -------------------------------------------------------------------------------------------------------------
''' devkit '''

DEVKIT_DIR          = os.path.join(ROOT, 'devkit')
DEVKIT_CORE         = os.path.join(DEVKIT_DIR, 'Core')
DEVKIT_GUI          = os.path.join(DEVKIT_DIR, 'Gui')
DEVKIT_WIDGET       = os.path.join(DEVKIT_DIR, 'Widgets')

# -------------------------------------------------------------------------------------------------------------
''' hooks '''

HOOK_DIR            = os.path.join(ROOT, 'hooks')
MAYA_DIR            = os.path.join(HOOK_DIR, 'Maya')
MARI_DIR            = os.path.join(HOOK_DIR, 'Mari')
NUKE_DIR            = os.path.join(HOOK_DIR, 'Nuke')
ZBRUSH_DIR          = os.path.join(HOOK_DIR, 'ZBrush')
HOUDINI_DIR         = os.path.join(HOOK_DIR, 'Houdini')

# -------------------------------------------------------------------------------------------------------------
''' icons '''

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
''' libs '''

LIB_DIR             = os.path.join(ROOT, 'libs')
SOUND_DIR           = os.path.join(LIB_DIR, 'sound')

# -------------------------------------------------------------------------------------------------------------
''' modules '''

MODULE_DIR          = os.path.join(ROOT, 'modules')

# -------------------------------------------------------------------------------------------------------------
''' plugins '''

PLUGIN_DIR          = os.path.join(ROOT, 'plugins')
NODEGRAPH_DIR       = os.path.join(PLUGIN_DIR, 'NodeGraph')

# -------------------------------------------------------------------------------------------------------------
''' scripts '''

SCRIPT_DIR          = os.path.join(ROOT, 'scripts')

# -------------------------------------------------------------------------------------------------------------
''' test '''

TEST_DIR            = os.path.join(ROOT, 'test')

# -------------------------------------------------------------------------------------------------------------
''' ui '''

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
''' utils '''

UTILS_DIR           = os.path.join(ROOT, 'utils')

class ConfigDirectory(DAMGDICT):

    key                                 = 'ConfigDirectory'

    def __init__(self):
        super(ConfigDirectory, self).__init__()

        self.add('ROOT', ROOT)
        self.add('APPDATA_DAMG', APPDATA_DAMG)
        self.add('APPDATA_PLM', APPDATA_PLM)
        self.add('TMP_DIR', TMP_DIR)
        self.add('CACHE_DIR', CACHE_DIR)
        self.add('PREF_DIR', PREF_DIR)
        self.add('TASK_DIR', TASK_DIR)
        self.add('TEAM_DIR', TEAM_DIR)
        self.add('OJ_DIR', OJ_DIR)
        self.add('ORG_DIR', ORG_DIR)
        self.add('USER_LOCAL_DATA', USER_LOCAL_DATA)
        self.add('APP_DATA_DIR', APP_DATA_DIR)
        self.add('ASSETS_DIR', ASSETS_DIR)
        self.add('AVATAR_DIR', AVATAR_DIR)
        self.add('FONT_DIR', FONT_DIR)
        self.add('IMAGE_DIR', IMAGE_DIR)
        self.add('LOGO_DIR', LOGO_DIR)
        self.add('DAMG_LOGO_DIR', DAMG_LOGO_DIR)
        self.add('PLM_LOGO_DIR', PLM_LOGO_DIR)
        self.add('PIC_DIR', PIC_DIR)
        self.add('STYLE_DIR', STYLE_DIR)
        self.add('STYLE_IMAGE_DIR', STYLE_IMAGE_DIR)
        self.add('STYLE_RC_DIR', STYLE_RC_DIR)
        self.add('STYLE_SVG_DIR', STYLE_SVG_DIR)
        self.add('BIN_DIR', BIN_DIR)
        self.add('DATA_DIR', DATA_DIR)
        self.add('JSON_DIR', JSON_DIR)
        self.add('DEPENDANCIES_DIR', DEPENDANCIES_DIR)
        self.add('DOCS_DIR', DOCS_DIR)
        self.add('RST_DIR', RST_DIR)
        self.add('TXT_DIR', TXT_DIR)
        self.add('RAWS_DATA_DIR', RAWS_DATA_DIR)
        self.add('TEMPLATE_DIR', TEMPLATE_DIR)
        self.add('TEMPLATE_LICENCE', TEMPLATE_LICENCE)
        self.add('CSS_DIR', CSS_DIR)
        self.add('HTML_DIR', HTML_DIR)
        self.add('JS_DIR', JS_DIR)
        self.add('QSS_DIR', QSS_DIR)
        self.add('BUILD_DIR', BUILD_DIR)
        self.add('CORES_DIR', CORES_DIR)
        self.add('CORES_ASSETS_DIR', CORES_ASSETS_DIR)
        self.add('CORES_BASE_DIR', CORES_BASE_DIR)
        self.add('DEVKIT_DIR', DEVKIT_DIR)
        self.add('DEVKIT_CORE', DEVKIT_CORE)
        self.add('DEVKIT_GUI', DEVKIT_GUI)
        self.add('DEVKIT_WIDGET', DEVKIT_WIDGET)
        self.add('HOOK_DIR', HOOK_DIR)
        self.add('MAYA_DIR', MAYA_DIR)
        self.add('MARI_DIR', MARI_DIR)
        self.add('NUKE_DIR', NUKE_DIR)
        self.add('ZBRUSH_DIR', ZBRUSH_DIR)
        self.add('HOUDINI_DIR', HOUDINI_DIR)
        self.add('ICON_DIR', ICON_DIR)
        self.add('TAG_ICON_DIR', TAG_ICON_DIR)
        self.add('MAYA_ICON_DIR', MAYA_ICON_DIR)
        self.add('NODE_ICON_DIR', NODE_ICON_DIR)
        self.add('WEB_ICON_DIR', WEB_ICON_DIR)
        self.add('WEB_ICON_16', WEB_ICON_16)
        self.add('WEB_ICON_24', WEB_ICON_24)
        self.add('WEB_ICON_32', WEB_ICON_32)
        self.add('WEB_ICON_48', WEB_ICON_48)
        self.add('WEB_ICON_64', WEB_ICON_64)
        self.add('WEB_ICON_128', WEB_ICON_128)
        self.add('ICON_DIR_12', ICON_DIR_12)
        self.add('ICON_DIR_16', ICON_DIR_16)
        self.add('ICON_DIR_24', ICON_DIR_24)
        self.add('ICON_DIR_32', ICON_DIR_32)
        self.add('ICON_DIR_48', ICON_DIR_48)
        self.add('ICON_DIR_64', ICON_DIR_64)
        self.add('LIB_DIR', LIB_DIR)
        self.add('SOUND_DIR', SOUND_DIR)
        self.add('MODULE_DIR', MODULE_DIR)
        self.add('PLUGIN_DIR', PLUGIN_DIR)
        self.add('NODEGRAPH_DIR', NODEGRAPH_DIR)
        self.add('SCRIPT_DIR', SCRIPT_DIR)
        self.add('TEST_DIR', TEST_DIR)
        self.add('UI_DIR', UI_DIR)
        self.add('UI_BASE_DIR', UI_BASE_DIR)
        self.add('UI_ASSET_DIR', UI_ASSET_DIR)
        self.add('BODY_DIR', BODY_DIR)
        self.add('TABS_DIR', TABS_DIR)
        self.add('FOOTER_DIR', FOOTER_DIR)
        self.add('HEADER_DIR', HEADER_DIR)
        self.add('SUBUI_DIR', SUBUI_DIR)
        self.add('FUNCS_DIR', FUNCS_DIR)
        self.add('PRJ_DIR', PRJ_DIR)
        self.add('SETTINGS_DIR', SETTINGS_DIR)
        self.add('TOOLS_DIR', TOOLS_DIR)
        self.add('UTILS_DIR', UTILS_DIR)

        self.add('ConfigDir', CFG_DIR)
        self.add('IconDir', ICON_DIR)
        self.add('SettingDir', SETTING_DIR)
        self.add('AppdataDir', APP_DATA_DIR)
        self.add('PreferenceDir', PREF_DIR)

        mode = 0o770
        for path in self.values():
            if not os.path.exists(path):
                head, tail              = os.path.split(path)
                try:
                    original_umask = os.umask(0)
                    os.makedirs(path, mode)
                finally:
                    os.umask(original_umask)
                os.chmod(path, mode)



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 10:45 PM
# Pipeline manager - DAMGteam
