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

# PLM
from .configs            import (__plmWiki__, __localServer__, __pkgsReq__, __homepage__, __appname__, __organization__,
                                 __organizationID__, __organizationName__, __globalServer__, __google__, __plmSlogan__,
                                 __localServerAutho__, __version__, __website__,

                                 ConfigPython, ConfigMachine, ConfigDirectory, ConfigPath, ConfigEnvVar, ConfigIcon,
                                 ConfigMaya, ConfigApps, ConfigPipeline, ConfigUrl, dirInfo, pthInfo,

                                 ignoreIDs, toBuildCmds, toBuildUis,

                                 RAMTYPE, CPUTYPE, FORMFACTOR, DRIVETYPE, DB_ATTRIBUTE_TYPE, actionTypes, layoutTypes,

                                 TRADE_MARK, PLM_ABOUT, WAIT_FOR_UPDATE, WAIT_TO_COMPLETE, WAIT_LAYOUT_COMPLETE,
                                 PASSWORD_FORGOTTON, SIGNUP, DISALLOW, TIT_BLANK, PW_BLANK, PW_WRONG, PW_UNMATCH,
                                 PW_CHANGED, FN_BLANK, LN_BLANK, SEC_BLANK, USER_CHECK_REQUIRED, USER_NOT_CHECK,
                                 USER_BLANK, USER_CHECK_FAIL, USER_NOT_EXSIST, USER_CONDITION, SYSTRAY_UNAVAI,
                                 PTH_NOT_EXSIST, ERROR_OPENFILE, ERROR_QIMAGE, tooltips_present, tooltips_missing,
                                 N_MESSAGES_TEXT, SERVER_CONNECT_FAIL, TEMPLATE_QRC_HEADER, TEMPLATE_QRC_FILE,
                                 TEMPLATE_QRC_FOOTER, HEADER_SCSS, HEADER_QSS,

                                 TRACK_TDS, TRACK_VFX, TRACK_ART, TRACK_PRE, TRACK_TEX, TRACK_POST, LIBRARY_UI_KEYS,
                                 TRACK_OFFICE, TRACK_DEV, TRACK_TOOLS, TRACK_EXTRA, TRACK_SYSTRAY, PLUGIN_UI_KEY,
                                 KEYDETECT, APP_UI_KEYS, KEYPACKAGE, CONFIG_TDS, CONFIG_VFX, FORM_KEY,
                                 CONFIG_ART, CONFIG_PRE, CONFIG_TEX, CONFIG_POST, CONFIG_OFFICE, CONFIG_DEV,
                                 CONFIG_TOOLS, CONFIG_EXTRA, CONFIG_SYSTRAY, ACTIONS_DATA, STYLESHEET_KEYS, OPEN_URL_KEYS,
                                 SHORTCUT_KEYS, QT_BINDINGS, QT_ABSTRACTIONS, QT5_IMPORT_API, QT_API_VALUES, QT_LIB_VALUES,
                                 QT_BINDING, QT_ABSTRACTION, IMAGE_BLACKLIST, PY2, SYS_OPTS, APP_FUNCS_KEYS,
                                 IGNORE_ICONS, notKeys, autodeskVer, PLMAPPID,

                                 QUESTIONS, ABOUT, CREDIT, CODECONDUCT, CONTRIBUTING, REFERENCES, LICENCE, VERSION,

                                 INI, Native, Invalid, LOG_FORMAT, DT_FORMAT, ST_FORMAT, datetTimeStamp, IMGEXT,

                                 SiPoExp, SiPoIgn, SiPoMax, SiPoMin, SiPoPre, right, left, center, bottom, blue,
                                 StateMax, StateMin, StateNormal, dockB, dockL, dockR, dockT, DarkPalette, PRS, FRAMELESS, KEY_RETURN,
                                 SCROLLBAROFF, NO_WRAP, BTNTAGSIZE, TAGBTNSIZE, BTNICONSIZE, ICONBTNSIZE, KEY_RELEASE, BOLD,

                                 AUTO_COLOR, ASPEC_RATIO, SMOOTH_TRANS, IN_PORT, OUT_PORT, ICON_DOWN_ARROW, NODE_PROP, NODE_PROP_QLABEL, NODE_PROP_QLINEEDIT,
                                 NODE_PROP_QCHECKBOX, NODE_PROP_COLORPICKER, NODE_PROP_QTEXTEDIT, NODE_PROP_QCOMBO, Z_VAL_PIPE, NODE_SEL_COLOR,
                                 NODE_SEL_BORDER_COLOR, Z_VAL_NODE, SIZEF_CURSOR, NODE_WIDTH, NODE_HEIGHT, PIPE_DEFAULT_COLOR, PIPE_ACTIVE_COLOR,
                                 PIPE_HIGHLIGHT_COLOR, PIPE_DISABLED_COLOR, PIPE_STYLE_DASHED, PIPE_STYLE_DEFAULT, PIPE_STYLE_DOTTED,
                                 PIPE_LAYOUT_STRAIGHT, PIPE_WIDTH, Z_VAL_PIPE, Z_VAL_NODE_WIDGET, PIPE_LAYOUT_ANGLE, PIPE_LAYOUT_CURVED,
                                 PORT_DEFAULT_COLOR, PORT_DEFAULT_BORDER_COLOR, PORT_DEFAULT_SIZE, PORT_FALLOFF, PORT_HOVER_COLOR,
                                 PORT_HOVER_BORDER_COLOR, PORT_ACTIVE_COLOR, PORT_ACTIVE_BORDER_COLOR, Z_VAL_PORT, NODE_ICON_SIZE, ICON_NODE_BASE,
                                 PIPE_SLICER_COLOR, SCENE_AREA, VIEWER_BG_COLOR, VIEWER_GRID_SIZE, VIEWER_GRID_OVERLAY, VIEWER_GRID_COLOR,
                                 DRAG_DROP_ID, NODE_PROP_QSPINBOX, NODE_PROP_SLIDER, PEN_NONE, MOUSE_LEFT, WORD_WRAP, BRUSH_NONE, INTERSECT_ITEM_SHAPE, CONTAIN_ITEM_SHAPE, ROUND_CAP,
                                 ALT_MODIFIER, LINE_DASH, LINE_SOLID, LINE_DOT, LINE_DASH_DOT, MATCH_EXACTLY, DRAG_ONLY, ITEMENABLE, NO_BUTTON, hori, top, ANTIALIAS, State_Selected,
                                 MOUSE_MIDDLE, MOUSE_RIGHT,

                                 STAY_ON_TOP,

                                 )





iconInfo                        = ConfigIcon()
appInfo                         = ConfigApps()
urlInfo                         = ConfigUrl()
plmInfo                         = ConfigPipeline(iconInfo, appInfo, urlInfo, dirInfo, pthInfo)

LOGO_DIR                        = dirInfo['LOGO_DIR']
WEB_ICON_DIR                    = dirInfo['WEB_ICON_DIR']
TAG_ICON_DIR                    = dirInfo['TAG_ICON_DIR']
AVATAR_DIR                      = dirInfo['AVATAR_DIR']
ICON_DIR                        = dirInfo['ICON_DIR']

SOUND_DIR                       = dirInfo['SOUND_DIR']
TASK_DIR                        = dirInfo['TASK_DIR']
PRJ_DIR                         = dirInfo['PRJ_DIR']
ORG_DIR                         = dirInfo['ORG_DIR']
TEAM_DIR                        = dirInfo['TEAM_DIR']
TMP_DIR                         = dirInfo['TMP_DIR']

QSS_DIR                         = dirInfo['QSS_DIR']

JSON_DIR                        = dirInfo['JSON_DIR']

LOCAL_DB                        = pthInfo['LOCAL_DB']
LOCAL_LOG                       = pthInfo['LOCAL_LOG']
SETTING_FILEPTH                 = pthInfo['SETTING_FILEPTH']

