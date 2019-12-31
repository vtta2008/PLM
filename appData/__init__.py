#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: __init__.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
from __buildtins__ import ROOT, __envKey__
""" import """

import os, subprocess
if os.getenv(__envKey__) != ROOT:
    subprocess.Popen('Set {0} {1}'.format(__envKey__, ROOT), shell=True).wait()

from .configs            import (__plmWiki__, __localServer__, __pkgsReq__, __homepage__, __appname__, __organization__,
                                 __organizationID__, __organizationName__, __globalServer__, __google__, __plmSlogan__,
                                 __localServerAutho__, __version__, __website__,

                                 ConfigPython, ConfigMachine, ConfigDirectory, ConfigPath, ConfigEnvVar, ConfigIcon, ConfigMaya, ConfigApps, ConfigPipeline,

                                 pythonInfo, deviceInfo, dirInfo, pthInfo, envInfo, iconInfo, mayaInfo, appInfo, plmInfo, ignoreIDs, toBuildUis, toBuildCmds,

                                 APPDATA_DAMG, APPDATA_PLM, CFG_DIR, TMP_DIR, SETTING_DIR, LOG_DIR, TASK_DIR, TEAM_DIR, ORG_DIR, APP_DATA_DIR, DB_DIR,
                                 ASSETS_DIR, AVATAR_DIR, FONT_DIR, IMAGE_DIR, LOGO_DIR, DAMG_LOGO_DIR, PLM_LOGO_DIR, PIC_DIR, STYLE_DIR,
                                 STYLE_IMAGE_DIR, STYLE_RC_DIR, STYLE_SVG_DIR, BIN_DIR, DATA_DIR, JSON_DIR, DEPENDANCIES_DIR, DOCS_DIR, RST_DIR,
                                 TXT_DIR, RAWS_DATA_DIR, TEMPLATE_DIR, TEMPLATE_LICENCE, RCS_DIR, CSS_DIR, HTML_DIR, JS_DIR, QSS_DIR, BUILD_DIR,
                                 CORES_DIR, CORES_ASSETS_DIR, CORES_BASE_DIR, DEVKIT_DIR, DEVKIT_CORE, DEVKIT_GUI, DEVKIT_WIDGET, HOOK_DIR, MAYA_DIR,
                                 MARI_DIR, NUKE_DIR, ZBRUSH_DIR, HOUDINI_DIR, ICON_DIR, TAG_ICON_DIR, MAYA_ICON_DIR, NODE_ICON_DIR, WEB_ICON_DIR,
                                 WEB_ICON_16, WEB_ICON_24, WEB_ICON_32, WEB_ICON_48, WEB_ICON_64, WEB_ICON_128, ICON_DIR_12, ICON_DIR_16, ICON_DIR_24,
                                 ICON_DIR_32, ICON_DIR_48, ICON_DIR_64, LIB_DIR, SOUND_DIR, MODULE_DIR, PLUGIN_DIR, NODEGRAPH_DIR, SCRIPT_DIR,
                                 TEST_DIR, UI_DIR, UI_BASE_DIR, UI_ASSET_DIR, BODY_DIR, TABS_DIR, FOOTER_DIR, HEADER_DIR, SUBUI_DIR, FUNCS_DIR,
                                 PRJ_DIR, SETTINGS_DIR, TOOLS_DIR, UTILS_DIR,

                                 evnInfoCfg, iconCfg, avatarCfg, logoCfg, mayaCfg, webIconCfg, nodeIconCfg, picCfg, tagCfg, pythonCfg, plmCfg,
                                 appsCfg, envVarCfg, dirCfg, pthCfg, deviceCfg, userCfg, PLMconfig, sceneGraphCfg, APP_SETTING, USER_SETTING,
                                 FORMAT_SETTING, UNIX_SETTING, LOCAL_DB, LOCAL_LOG, QSS_PATH, MAIN_SCSS_PTH, STYLE_SCSS_PTH, VAR_SCSS_PTH,
                                 SETTING_FILEPTH,

                                 RAMTYPE, CPUTYPE, FORMFACTOR, DRIVETYPE, DB_ATTRIBUTE_TYPE, actionTypes, layoutTypes,

                                 TRADE_MARK, PLM_ABOUT, WAIT_FOR_UPDATE, WAIT_TO_COMPLETE, WAIT_LAYOUT_COMPLETE,
                                 PASSWORD_FORGOTTON, SIGNUP, DISALLOW, TIT_BLANK, PW_BLANK, PW_WRONG, PW_UNMATCH,
                                 PW_CHANGED, FN_BLANK, LN_BLANK, SEC_BLANK, USER_CHECK_REQUIRED, USER_NOT_CHECK,
                                 USER_BLANK, USER_CHECK_FAIL, USER_NOT_EXSIST, USER_CONDITION, SYSTRAY_UNAVAI,
                                 PTH_NOT_EXSIST, ERROR_OPENFILE, ERROR_QIMAGE, tooltips_present, tooltips_missing,
                                 N_MESSAGES_TEXT, SERVER_CONNECT_FAIL, TEMPLATE_QRC_HEADER, TEMPLATE_QRC_FILE,
                                 TEMPLATE_QRC_FOOTER, HEADER_SCSS, HEADER_QSS,

                                 TRACK_TDS, TRACK_VFX, TRACK_ART, TRACK_PRE, TRACK_TEX, TRACK_POST,
                                 TRACK_OFFICE, TRACK_DEV, TRACK_TOOLS, TRACK_EXTRA, TRACK_SYSTRAY,
                                 KEYDETECT, FIX_KEY, APP_UI_KEYS, KEYPACKAGE, CONFIG_TDS, CONFIG_VFX,
                                 CONFIG_ART, CONFIG_PRE, CONFIG_TEX, CONFIG_POST, CONFIG_OFFICE, CONFIG_DEV,
                                 CONFIG_TOOLS, CONFIG_EXTRA, CONFIG_SYSTRAY, ACTIONS_DATA, SHOWLAYOUT_KEY,
                                 RESTORE_KEY, SHOWMAX_KEY, SHOWMIN_KEY, STYLESHEET_KEYS, OPEN_URL_KEYS,
                                 START_FILE, SHORTCUT_KEYS, START_FILE_KEY, EXECUTING_KEY, IGNORE_ICON_NAME,
                                 QT_BINDINGS, QT_ABSTRACTIONS, QT5_IMPORT_API, QT_API_VALUES, QT_LIB_VALUES,
                                 QT_BINDING, QT_ABSTRACTION, IMAGE_BLACKLIST, PY2, SYS_OPTS, APP_FUNCS_KEYS,
                                 notKeys, autodeskVer,

                                 QUESTIONS, ABOUT, CREDIT, CODECONDUCT, CONTRIBUTING, REFERENCE, LICENCE, VERSION,

                                 INI, Native, Invalid, LOG_FORMAT, DT_FORMAT, ST_FORMAT, datetTimeStamp, IMGEXT,

                                 SiPoExp, SiPoIgn, SiPoMax, SiPoMin, SiPoPre, right, left, center, StateMax, StateMin,
                                 StateNormal, dockB, dockL, dockR, dockT, DarkPalette, PRS, FRAMELESS, KEY_RETURN,
                                 SCROLLBAROFF, NO_WRAP, BTNTAGSIZE, TAGBTNSIZE, BTNICONSIZE, ICONBTNSIZE, KEY_RELEASE,

                                 AUTO_COLOR, ASPEC_RATIO, IN_PORT, OUT_PORT, ICON_DOWN_ARROW, NODE_PROP, NODE_PROP_QLABEL, NODE_PROP_QLINEEDIT,
                                 NODE_PROP_QCHECKBOX, NODE_PROP_COLORPICKER, NODE_PROP_QTEXTEDIT, NODE_PROP_QCOMBO, Z_VAL_PIPE, NODE_SEL_COLOR,
                                 NODE_SEL_BORDER_COLOR, Z_VAL_NODE, SIZEF_CURSOR, NODE_WIDTH, NODE_HEIGHT, PIPE_DEFAULT_COLOR, PIPE_ACTIVE_COLOR,
                                 PIPE_HIGHLIGHT_COLOR, PIPE_DISABLED_COLOR, PIPE_STYLE_DASHED, PIPE_STYLE_DEFAULT, PIPE_STYLE_DOTTED,
                                 PIPE_LAYOUT_STRAIGHT, PIPE_WIDTH, Z_VAL_PIPE, Z_VAL_NODE_WIDGET, PIPE_LAYOUT_ANGLE, PIPE_LAYOUT_CURVED,
                                 PORT_DEFAULT_COLOR, PORT_DEFAULT_BORDER_COLOR, PORT_DEFAULT_SIZE, PORT_FALLOFF, PORT_HOVER_COLOR,
                                 PORT_HOVER_BORDER_COLOR, PORT_ACTIVE_COLOR, PORT_ACTIVE_BORDER_COLOR, Z_VAL_PORT, NODE_ICON_SIZE, ICON_NODE_BASE,
                                 PIPE_SLICER_COLOR, SCENE_AREA, VIEWER_BG_COLOR, VIEWER_GRID_SIZE, VIEWER_GRID_OVERLAY, VIEWER_GRID_COLOR,
                                 DRAG_DROP_ID, NODE_PROP_QSPINBOX, NODE_PROP_SLIDER,






                                 )
