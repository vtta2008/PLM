# -*- coding: utf-8 -*-
"""

Script Name: _pref.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import builtins
import re

# PyQt5
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QWidget, QMainWindow, QSystemTrayIcon, QGridLayout, QApplication

# Plm
from appData.scr._path import APP_SETTING, UNIX_SETTING, USER_SETTING, FORMAT_SETTING
from appData.scr._nodeGraph import (ANCHOR_UNDERMICE, ANCHOR_VIEWCENTER, FOCUSABLE, MOVEABLE, NODRAG, NOANCHOR, PANEL,
                                POS_CHANGE, RUBBERDRAG, SELECTABLE, UPDATE_FULLVIEW, UPDATE_SMARTVIEW, UPDATE_BOUNDINGVIEW,
                                UPDATE_MINIMALVIEW, UPDATE_VIEWRECT, )
from appData.scr._meta import __appname__

# -------------------------------------------------------------------------------------------------------------
""" Python Types """

def get_all_types():
    allTypes = {}
    errorTypes = {}
    normalTypes = {}
    types = [getattr(builtins, d) for d in dir(builtins) if isinstance(getattr(builtins, d), type)]
    keys = [str(t).split("<class '")[-1].split("'>")[0] for t in types]

    for key in keys:
        allTypes[key] = types[keys.index(key)]
        if 'Error' in key:
            errorTypes[key]= types[keys.index(key)]
        else:
            normalTypes[key]= types[keys.index(key)]

    return errorTypes, normalTypes, allTypes

ERROR_TYPES, NORMAL_TYPES, ALL_TYPES = get_all_types()

# -------------------------------------------------------------------------------------------------------------
""" PLM Types """

PLM_TYPES  = dict(base    = 'PLM base object',     config  = 'PLM config ui',       console = 'PLM console',
                  core    = 'PLM core object',     flag    = 'PLM flag',            footer  = 'PLM footer ui',
                  header  = 'PLM header ui',       id      = 'PLM id',              index   = 'PLM index',
                  info    = 'PLM info ui',         layout  = 'PLM ui',              service = 'PLM background service',
                  setting = 'PLM setting ui',      sysTray = 'PLM system tray',     main    = 'PLM main ui',
                  menu    = 'PLM menu bar',        mtd     = 'PLM metadata',        mto     = 'PLM meta object',
                  mtp     = 'PLM meta property',   mts     = 'PLM meta signal',     net     = 'PLM network monitor',
                  tab     = 'PLM tab ui',          tag     = 'PLM tag',             testUI  = 'PLM test ui',
                  toolBar = 'PLM tool bar',        unix    = 'PLM unix',            web     = 'PLM web app', )

# -------------------------------------------------------------------------------------------------------------
""" PLM layout profile """

UI_LVL = dict(st = 'main', nd = 'subMain', rd = 'child', th = 'subChild')

SPECS = dict(about         = {'ordinal': 1,  'objName': 'About',          'type': PLM_TYPES['info'],    'lvl': UI_LVL['nd'], 'title': 'About'              , 'id': 'PAB', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             botTab        = {'ordinal': 2,  'objName': 'botTab',         'type': PLM_TYPES['layout'],  'lvl': UI_LVL['rd'], 'title': None                 , 'id': 'PBT', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             browser       = {'ordinal': 3,  'objName': 'Browser',        'type': PLM_TYPES['web'],     'lvl': UI_LVL['nd'], 'title': 'PLM Browser'        , 'id': 'PBR', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             config        = {'ordinal': 4,  'objName': 'Configuration',  'type': PLM_TYPES['config'],  'lvl': UI_LVL['nd'], 'title': 'Pipeline Config'    , 'id': 'PBR', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             calculator    = {'ordinal': 5,  'objName': 'Calculator',     'type': PLM_TYPES['layout'],  'lvl': UI_LVL['nd'], 'title': 'Calculator'         , 'id': 'PCA', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             calendar      = {'ordinal': 6,  'objName': 'Calendar',       'type': PLM_TYPES['layout'],  'lvl': UI_LVL['nd'], 'title': 'Calendar'           , 'id': 'PCD', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             codeConduct   = {'ordinal': 7,  'objName': 'CodeConduct',    'type': PLM_TYPES['info'],    'lvl': UI_LVL['nd'], 'title': 'Code of Conduct'    , 'id': 'PCC', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             console       = {'ordinal': 8,  'objName': 'PLM',            'type': PLM_TYPES['console'], 'lvl': UI_LVL['st'], 'title': None                 , 'id': 'PLM', 'tag': 'PIPELINE MANAGER'   , 'flag': 'Master console'  , 'cls': QApplication, },
             contributing  = {'ordinal': 9,  'objName': 'Contributing',   'type': PLM_TYPES['info'],    'lvl': UI_LVL['nd'], 'title': 'Contributing'       , 'id': 'PCB', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             core          = {'ordinal': 10, 'objName': 'core',           'type': PLM_TYPES['core'],    'lvl': UI_LVL['st'], 'title': None                 , 'id': 'PCO', 'tag': None                 , 'flag': None              , 'cls': QCoreApplication},
             credit        = {'ordinal': 11, 'objName': 'Credit',         'type': PLM_TYPES['info'],    'lvl': UI_LVL['nd'], 'title': 'Credit'             , 'id': 'PCR', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             engDict       = {'ordinal': 12, 'objName': 'EngDict',        'type': PLM_TYPES['layout'],  'lvl': UI_LVL['nd'], 'title': 'English Dictionary' , 'id': 'PED', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             findFile      = {'ordinal': 13, 'objName': 'FindFile',       'type': PLM_TYPES['layout'],  'lvl': UI_LVL['nd'], 'title': 'File Hunting'       , 'id': 'PFF', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             footer        = {'ordinal': 14, 'objName': 'Footer',         'type': PLM_TYPES['footer'],  'lvl': UI_LVL['rd'], 'title': 'Footer'             , 'id': 'PFT', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             forgotPW      = {'ordinal': 15, 'objName': 'forgotPW',       'type': PLM_TYPES['layout'],  'lvl': UI_LVL['rd'], 'title': 'Password Recovery'  , 'id': 'PPR', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             imageViewer   = {'ordinal': 16, 'objName': 'ImageViewer',    'type': PLM_TYPES['layout'],  'lvl': UI_LVL['nd'], 'title': 'Picture Viewer'     , 'id': 'PIM', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             licenceMIT    = {'ordinal': 17, 'objName': 'LicenceMIT',     'type': PLM_TYPES['info'],    'lvl': UI_LVL['nd'], 'title': 'Licence'            , 'id': 'MIT', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             login         = {'ordinal': 18, 'objName': 'LogIn',          'type': PLM_TYPES['layout'],  'lvl': UI_LVL['st'], 'title': 'Sign In'            , 'id': 'PLI', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             mainUI        = {'ordinal': 19, 'objName': 'MainUI',         'type': PLM_TYPES['main'],    'lvl': UI_LVL['nd'], 'title': __appname__          , 'id': 'PML', 'tag': 'PLM MAIN UI'        , 'flag': 'Master Layout'   , 'cls': QMainWindow, },
             mainMenu      = {'ordinal': 20, 'objName': 'MainUI',         'type': PLM_TYPES['main'],    'lvl': UI_LVL['nd'], 'title': 'Main Menu Bar'      , 'id': 'PML', 'tag': 'PLM MAIN MENU'      , 'flag': 'Master Menu'     , 'cls': QMainWindow, },
             newProj       = {'ordinal': 21, 'objName': 'NewProject',     'type': PLM_TYPES['layout'],  'lvl': UI_LVL['nd'], 'title': 'New Project'        , 'id': 'PNP', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             nodeGraph     = {'ordinal': 22, 'objName': 'NodeGraph',      'type': PLM_TYPES['layout'],  'lvl': UI_LVL['nd'], 'title': 'Note Graph'         , 'id': 'PNR', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             noteReminder  = {'ordinal': 23, 'objName': 'NoteReminder',   'type': PLM_TYPES['layout'],  'lvl': UI_LVL['nd'], 'title': 'Note Reminder'      , 'id': 'PNR', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             notification  = {'ordinal': 24, 'objName': 'Notification',   'type': PLM_TYPES['layout'],  'lvl': UI_LVL['nd'], 'title': 'Notification'       , 'id': 'PNT', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             preferences   = {'ordinal': 25, 'objName': 'Configuration',  'type': PLM_TYPES['config'],  'lvl': UI_LVL['nd'], 'title': 'Pipeline Config'    , 'id': 'PBR', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             quickSetting  = {'ordinal': 26, 'objName': 'QuickSetting',   'type': PLM_TYPES['setting'], 'lvl': UI_LVL['nd'], 'title': None                 , 'id': 'PGS', 'tag': None                 , 'flag': None              , 'cls': QGridLayout, },
             reference     = {'ordinal': 27, 'objName': 'Reference',      'type': PLM_TYPES['info'],    'lvl': UI_LVL['nd'], 'title': 'Reference'          , 'id': 'PRF', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             screenShot    = {'ordinal': 28, 'objName': 'ScreenShot',     'type': PLM_TYPES['layout'],  'lvl': UI_LVL['nd'], 'title': 'Screenshot'         , 'id': 'PSC', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             serverStatus  = {'ordinal': 29, 'objName': 'ServerStatus',   'type': PLM_TYPES['net'],     'lvl': UI_LVL['rd'], 'title': None                 , 'id': 'PSS', 'tag': None                 , 'flag': None              , 'cls': QGridLayout, },
             settingUI     = {'ordinal': 30, 'objName': 'Setting Manager','type': PLM_TYPES['config'],  'lvl': UI_LVL['nd'], 'title': 'Application Setting', 'id': 'PSM', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             signup        = {'ordinal': 31, 'objName': 'SignUp',         'type': PLM_TYPES['layout'],  'lvl': UI_LVL['nd'], 'title': 'Sign Up'            , 'id': 'PLU', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             statusBar     = {'ordinal': 32, 'objName': 'SubMenu',        'type': PLM_TYPES['menu'],    'lvl': UI_LVL['rd'], 'title': None                 , 'id': 'PSU', 'tag': None                 , 'flag': None              , 'cls': QMainWindow},
             subMenu       = {'ordinal': 33, 'objName': 'SubMenu',        'type': PLM_TYPES['menu'],    'lvl': UI_LVL['rd'], 'title': None                 , 'id': 'PSU', 'tag': None                 , 'flag': None              , 'cls': QMainWindow},
             sysTray       = {'ordinal': 34, 'objName': 'SystemTray',     'type': PLM_TYPES['sysTray'], 'lvl': UI_LVL['st'], 'title': None                 , 'id': 'PST', 'tag': None                 , 'flag': None              , 'cls': QSystemTrayIcon, },
             testUI        = {'ordinal': 35, 'objName': 'TestUI',         'type': PLM_TYPES['testUI'],  'lvl': UI_LVL['nd'], 'title': 'Test Layout'        , 'id': 'PTU', 'tag': 'PLM TEST UI'        , 'flag': 'Test Layout'     , 'cls': QMainWindow, },
             textEditor    = {'ordinal': 36, 'objName': 'TextEditor',     'type': PLM_TYPES['layout'],  'lvl': UI_LVL['nd'], 'title': 'Text Editor'        , 'id': 'PTE', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             toolBar       = {'ordinal': 37, 'objName': 'ToolBar',        'type': PLM_TYPES['layout'],  'lvl': UI_LVL['nd'], 'title': None                 , 'id': 'PTB', 'tag': None                 , 'flag': None              , 'cls': QMainWindow, },
             topTab        = {'ordinal': 38, 'objName': 'TopTab',         'type': PLM_TYPES['tab'],     'lvl': UI_LVL['nd'], 'title': None                 , 'id': 'PTT', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             topTab1       = {'ordinal': 39, 'objName': 'TopTab1',        'type': PLM_TYPES['tab'],     'lvl': UI_LVL['rd'], 'title': None                 , 'id': 'TT1', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             topTab2       = {'ordinal': 40, 'objName': 'TopTab2',        'type': PLM_TYPES['tab'],     'lvl': UI_LVL['rd'], 'title': None                 , 'id': 'TT2', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             topTab3       = {'ordinal': 41, 'objName': 'TopTab3',        'type': PLM_TYPES['tab'],     'lvl': UI_LVL['rd'], 'title': None                 , 'id': 'TT3', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             topTab4       = {'ordinal': 42, 'objName': 'TopTab4',        'type': PLM_TYPES['tab'],     'lvl': UI_LVL['rd'], 'title': None                 , 'id': 'TT4', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             topTab5       = {'ordinal': 43, 'objName': 'TopTab5',        'type': PLM_TYPES['tab'],     'lvl': UI_LVL['rd'], 'title': None                 , 'id': 'TT5', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             userSetting   = {'ordinal': 44, 'objName': 'UserSetting',    'type': PLM_TYPES['layout'],  'lvl': UI_LVL['nd'], 'title': 'User Preference'    , 'id': 'PUS', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             version       = {'ordinal': 45, 'objName': 'Version',        'type': PLM_TYPES['info'],    'lvl': UI_LVL['nd'], 'title': 'Version'            , 'id': 'PVS', 'tag': None                 , 'flag': None              , 'cls': QWidget, },
             )

# -------------------------------------------------------------------------------------------------------------
""" PLM object profile """

OBJ_INFO = dict()

# -------------------------------------------------------------------------------------------------------------
""" PLM node graph pre setting """

# node connection property types
PROPERTY = dict(simple  = ['FLOAT', 'STRING', 'BOOL', 'INT'], arrays  = ['FLOAT2', 'FLOAT3', 'INT2', 'INT3', 'COLOR'],
                types   = ['FILE', 'MULTI', 'MERGE', 'NODE', 'DIR'], min = 'minimum value', max = 'maximum value',
                default = 'default value', label = 'node label', private = 'attribute is private (hiddent)', desc = 'attribute descriptiohn',)

REGEX = dict(section        = re.compile(r"^\[[^\]\r\n]+]"),
             section_value  = re.compile(r"\[(?P<attr>[\w]*?) (?P<value>[\w\s]*?)\]$"),
             properties     = re.compile("(?P<name>[\.\w]*)\s*(?P<type>\w*)\s*(?P<value>.*)$"),)

# Default preferences
PREFERENCES = dict(
    ignore_scene_prefs = {"default": False,     "desc": "Use user prefences instead of scene preferences.", "label": "Ignore scene preferences",    "class": "global"},
    use_gl =             {"default": False,     "desc": "Render graph with OpenGL.",                        "label": "Use OpenGL",                  "class": "scene"},
    edge_type =          {"default": "bezier",  "desc": "Draw edges with bezier paths.",                    "label": "Edge style",                  "class": "scene"},
    render_fx =          {"default": False,     "desc": "Render node drop shadows and effects.",            "label": "render FX",                   "class": "scene"},
    antialiasing =       {"default": 2,         "desc": "Antialiasing level.",                              "label": "Antialiasing",                "class": "scene"},
    logging_level =      {"default": 30,        "desc": "Verbosity level.",                                 "label": "Logging level",               "class": "global"},
    autosave_inc =       {"default": 90000,     "desc": "Autosave delay (seconds x 1000).",                 "label": "Autosave time",               "class": "global"},
    stylesheet_name =    {"default": "default", "desc": "Stylesheet to use.",                               "label": "Stylesheet",                  "class": "global"},
    palette_style =      {"default": "default", "desc": "Color palette to use.",                            "label": "Palette",                     "class": "global"},
    font_style =         {"default": "default", "desc": "font style to use.",                               "label": "Font style",                  "class": "global"},
    viewport_mode =      {"default": "smart",   "desc": "viewport update mode.",                            "label": "Viewport Mode",               "class": "global"}
)

VALID_FONTS = dict( ui   = ['Arial', 'Cantarell', 'Corbel', 'DejaVu Sans', 'DejaVu Serif', 'FreeSans', 'Liberation Sans', 'Lucida Sans Unicode', 'MS Sans Serif', 'Open Sans', 'PT Sans', 'Tahoma', 'Verdana'],
                    mono = ['Consolas', 'Courier', 'Courier 10 Pitch', 'Courier New', 'DejaVu Sans Mono', 'Fixed', 'FreeMono', 'Liberation Mono', 'Lucida Console', 'Menlo', 'Monaco'],
                    nodes= ['Consolas', 'DejaVu Sans Mono', 'Menlo', 'DejaVu Sans'])

EDGE_TYPES      = dict(bezier  = 'bezier',       polygon = 'polygon')
POS_EVENTS      = dict(change = POS_CHANGE)
DRAG_MODES      = dict(none   = NODRAG,          rubber = RUBBERDRAG)
VIEWPORT_MODES  = dict(full   = UPDATE_FULLVIEW, smart  = UPDATE_SMARTVIEW,  minimal = UPDATE_MINIMALVIEW, bounding = UPDATE_BOUNDINGVIEW, viewrect = UPDATE_VIEWRECT)
FLAG_MODES      = dict(select = SELECTABLE,      move   = MOVEABLE,          focus   = FOCUSABLE,          panel    = PANEL)
ANCHOR_MODES    = dict(none   = NOANCHOR,        under  = ANCHOR_UNDERMICE,  center  = ANCHOR_VIEWCENTER, )
SETTING_FILEPTH = dict(app    = APP_SETTING,     user   = USER_SETTING,      unix    = UNIX_SETTING,       format   = FORMAT_SETTING)

# -------------------------------------------------------------------------------------------------------------
""" PLM project base """

PRJ_INFO = dict(APPS       = ["maya", "zbrush", "mari", "nuke", "photoshop", "houdini", "after effects"],
                MASTER     = ["assets", "sequences", "deliverables", "documents", "editorial", "sound", "resources", "RnD"],
                TASKS      = ["art", "plt_model", "rigging", "surfacing"],
                SEQTASKS   = ["anim", "comp", "fx", "layout", "lighting"],
                ASSETS     = {"heroObj": ["washer", "dryer"], "environment": [], "props": []},
                STEPS      = ["publish", "review", "work"],
                MODELING   = ["scenes", "fromZ", "toZ", "objImport", "objExport", "movie"],
                RIGGING    = ["scenes", "reference"],
                SURFACING  = ["scenes", "sourceimages", "images", "movie"],
                LAYOUT     = ["scenes", "sourceimages", "images", "movie", "alembic"],
                LIGHTING   = ["scenes", "sourceimages", "images", "cache", "reference"],
                FX         = ["scenes", "sourceimages", "images", "cache", "reference", "alembic"],
                ANIM       = ["scenes", "sourceimages", "images", "movie", "alembic"],)

FIX_KEYS = dict(
    TextEditor = 'textEditor', NoteReminder = 'noteReminder', Calculator = 'calculator', Calendar = 'calendar',
    EnglishDictionary = 'engDict', FindFiles = 'findFile', ImageViewer = 'imageViewer', NodeGraph = 'nodeGraph',
    Screenshot = 'screenShot',
)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 17/06/2018 - 12:51 AM
# © 2017 - 2018 DAMGteam. All rights reserved