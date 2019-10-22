# -*- coding: utf-8 -*-
"""

Script Name: path.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python

import os, re

# PyQt5
from PyQt5.QtCore import Qt, QSettings, QDateTime, QSize
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsView, QGraphicsScene, QRubberBand, QFrame, QSizePolicy

# PLM
from appData.metadatas import __appname__, __groupname__, __envKey__

# -------------------------------------------------------------------------------------------------------------
""" Directory local system """

PROGRAM86                   = os.getenv('PROGRAMFILES(X86)')
PROGRAM64                   = os.getenv('PROGRAMW6432')
LOCALAPPDATA                = os.getenv('LOCALAPPDATA')
PROGRAMDATA                 = os.getenv('PROGRAMDATA')
DESKTOP_DIR                 = os.path.join(os.environ["HOMEPATH"], "desktop")           # Desktop path

# -------------------------------------------------------------------------------------------------------------
""" Name variables """

config                      = 'configuration'
logs                        = 'logs'
cache                       = 'cache'
settings                    = 'settings'
reg                         = 'reg'
nodegraph                   = 'nodegraph'
userPrefs                   = 'userPrefs'
prefs                       = 'prefs'

# -------------------------------------------------------------------------------------------------------------
""" Name variables """

print(os.getenv(__envKey__))

ROOT_DIR                    = os.path.join(os.getenv(__envKey__))

CFG_DIR                     = os.path.join(ROOT_DIR, 'appData', '.config')

CONFIG_LOCAL_DAMG_DIR       = os.path.join(CFG_DIR, __groupname__)                      # DAMG team directory
CONFIG_LOCAL_PLM_DIR        = os.path.join(CFG_DIR, __appname__)                        # Plm directory
CONFIG_DIR                  = os.path.join(CFG_DIR, 'common')                           # Config dir to store config info

SETTING_DIR                 = os.path.join(CONFIG_LOCAL_PLM_DIR, settings)              # Setting dir
LOG_DIR                     = os.path.join(CONFIG_LOCAL_PLM_DIR, logs)                  # Log dir
CACHE_DIR                   = os.path.join(CONFIG_LOCAL_PLM_DIR, cache)                 # Cache dir

NODEGRAPH_DIR               = os.path.join(CONFIG_DIR, nodegraph)                       # Nodegraph dir
PREF_DIR                    = os.path.join(CONFIG_DIR, prefs)                           # Preferences dir
USER_PREF_DIR               = os.path.join(CONFIG_DIR, userPrefs)                       # User preferences dir

# -------------------------------------------------------------------------------------------------------------
""" App (python) """

APP_DATA_DIR                = os.path.join(ROOT_DIR, 'appData')
BUILD_DIR                   = os.path.join(ROOT_DIR, 'build')
CORE_DIR                    = os.path.join(ROOT_DIR, 'appCore')
IMG_DIR                     = os.path.join(ROOT_DIR, 'imgs')
PLUGIN_DIR                  = os.path.join(ROOT_DIR, 'plugins')
UI_DIR                      = os.path.join(ROOT_DIR, 'ui')
TEST_DIR                    = os.path.join(ROOT_DIR, 'test')

# -------------------------------------------------------------------------------------------------------------
""" Dependancies """

DEPENDANCIES_DIR            = os.path.join(CORE_DIR, 'dependencies')

# -------------------------------------------------------------------------------------------------------------
""" App (Non python) """

BIN_DIR                     = os.path.join(ROOT_DIR, 'bin')
SCRIPTS_DIR                 = os.path.join(ROOT_DIR, 'scripts')
QSS_DIR                     = os.path.join(SCRIPTS_DIR, 'qss')
DB_DIR                      = APP_DATA_DIR
APPS_DIR                    = os.path.join(BIN_DIR, 'apps')

# -------------------------------------------------------------------------------------------------------------
""" Image """

APP_ICON_DIR                = os.path.join(IMG_DIR, 'icons')
WEB_ICON_DIR                = os.path.join(IMG_DIR, 'web')
AVATAR_DIR                  = os.path.join(IMG_DIR, 'avatar')
LOGO_DIR                    = os.path.join(IMG_DIR, 'logo')
PIC_DIR                     = os.path.join(IMG_DIR, 'pics')
TAG_DIR                     = os.path.join(IMG_DIR, 'tags')

ICON_DIR_16                 = os.path.join(APP_ICON_DIR, 'x16')
ICON_DIR_24                 = os.path.join(APP_ICON_DIR, 'x24')
ICON_DIR_32                 = os.path.join(APP_ICON_DIR, 'x32')
ICON_DIR_48                 = os.path.join(APP_ICON_DIR, 'x48')
ICON_DIR_64                 = os.path.join(APP_ICON_DIR, 'x64')

WEB_ICON_16                 = os.path.join(WEB_ICON_DIR, 'x16')
WEB_ICON_24                 = os.path.join(WEB_ICON_DIR, 'x24')
WEB_ICON_32                 = os.path.join(WEB_ICON_DIR, 'x32')
WEB_ICON_48                 = os.path.join(WEB_ICON_DIR, 'x48')
WEB_ICON_64                 = os.path.join(WEB_ICON_DIR, 'x64')
WEB_ICON_128                = os.path.join(WEB_ICON_DIR, 'x128')

DAMG_LOGO_DIR               = os.path.join(LOGO_DIR, 'DAMGteam', 'icons')
PLM_LOGO_DIR                = os.path.join(LOGO_DIR, 'Plm', 'icons')

DAMG_LOGO_32                = os.path.join(DAMG_LOGO_DIR, 'logo32')
PLM_LOGO_32                 = os.path.join(PLM_LOGO_DIR, 'logo32')

# -------------------------------------------------------------------------------------------------------------
""" Documentations """

RAWS_DATA_DIR               = os.path.join(APP_DATA_DIR, 'raws')
DOCUMENTATION_DIR           = os.path.join(APP_DATA_DIR, 'documentations')

# -------------------------------------------------------------------------------------------------------------
""" File path configurations """

cfgFile                     = os.path.join(CFG_DIR, 'PLM.cfg')

appIconCfg                  = os.path.join(CONFIG_DIR, 'appIcon.cfg')                   # Config app icon path
webIconCfg                  = os.path.join(CONFIG_DIR, 'webIcon.cfg')                   # Config Web icon path
logoIconCfg                 = os.path.join(CONFIG_DIR, 'logoIcon.cfg')                  # Config logo icon path

pyEnvCfg                    = os.path.join(CONFIG_DIR, 'envKey.cfg')                    # Config python env variables
appConfig                   = os.path.join(CONFIG_DIR, 'main.cfg')                      # Config pipeline soft package
mainConfig                  = os.path.join(CONFIG_DIR, 'PLM.cfg')                       # Master config

# -------------------------------------------------------------------------------------------------------------
""" Settings """

APP_SETTING                 = os.path.join(SETTING_DIR, 'PLM.ini')                      # Pipeline application setting
USER_SETTING                = os.path.join(SETTING_DIR, 'user.ini')                     # User setting
FORMAT_SETTING              = os.path.join(SETTING_DIR, 'format.ini')
UNIX_SETTING                = os.path.join(SETTING_DIR, 'unix.ini')

SETTING_FILEPTH = dict( app = APP_SETTING, user = USER_SETTING, unix = UNIX_SETTING, format = FORMAT_SETTING)

# -------------------------------------------------------------------------------------------------------------
""" File path """

DB_PTH                      = os.path.join(DB_DIR, 'local.db')                          # Local database
LOG_PTH                     = os.path.join(LOG_DIR, 'PLM.logs')                         # Log file

# -------------------------------------------------------------------------------------------------------------
""" Format """

ST_FORMAT = dict(   ini       = QSettings.IniFormat,
                    native    = QSettings.NativeFormat,
                    invalid   = QSettings.InvalidFormat, )

datetTimeStamp = QDateTime.currentDateTime().toString("hh:mm - dd MMMM yy")             # datestamp

IMGEXT = "All Files (*);;Img Files (*.jpg);;Img Files (*.png)"

# -------------------------------------------------------------------------------------------------------------
""" Nodegraph setting variables """

ASPEC_RATIO                 = Qt.KeepAspectRatio

SCROLLBAROFF                = Qt.ScrollBarAlwaysOff                                     # Scrollbar
SCROLLBARON                 = Qt.ScrollBarAlwaysOn
SCROLLBARNEED               = Qt.ScrollBarAsNeeded

# -------------------------------------------------------------------------------------------------------------
""" UI flags """

ITEMMOVEABLE                = QGraphicsItem.ItemIsMovable
ITEMSENDGEOCHANGE           = QGraphicsItem.ItemSendsGeometryChanges
ITEMSCALECHANGE             = QGraphicsItem.ItemScaleChange
ITEMPOSCHANGE               = QGraphicsItem.ItemPositionChange
DEVICECACHE                 = QGraphicsItem.DeviceCoordinateCache
SELECTABLE                  = QGraphicsItem.ItemIsSelectable
MOVEABLE                    = QGraphicsItem.ItemIsMovable
FOCUSABLE                   = QGraphicsItem.ItemIsFocusable
PANEL                       = QGraphicsItem.ItemIsPanel

NOINDEX                     = QGraphicsScene.NoIndex                                    # Scene

RUBBER_DRAG                 = QGraphicsView.RubberBandDrag                              # Viewer
RUBBER_REC                  = QRubberBand.Rectangle
POS_CHANGE                  = QGraphicsItem.ItemPositionChange

NODRAG                      = QGraphicsView.NoDrag
NOFRAME                     = QGraphicsView.NoFrame
NOANCHOR                    = QGraphicsView.NoAnchor

ANCHOR_UNDERMICE            = QGraphicsView.AnchorUnderMouse
ANCHOR_VIEWCENTER           = QGraphicsView.AnchorViewCenter

CACHE_BG                    = QGraphicsView.CacheBackground

UPDATE_VIEWRECT             = QGraphicsView.BoundingRectViewportUpdate
UPDATE_FULLVIEW             = QGraphicsView.FullViewportUpdate
UPDATE_SMARTVIEW            = QGraphicsView.SmartViewportUpdate
UPDATE_BOUNDINGVIEW         = QGraphicsView.BoundingRectViewportUpdate
UPDATE_MINIMALVIEW          = QGraphicsView.MinimalViewportUpdate

# -------------------------------------------------------------------------------------------------------------
""" Drawing """

ANTIALIAS                   = QPainter.Antialiasing                                     # Painter
ANTIALIAS_TEXT              = QPainter.TextAntialiasing
ANTIALIAS_HIGH_QUALITY      = QPainter.HighQualityAntialiasing
SMOOTH_PIXMAP_TRANSFORM     = QPainter.SmoothPixmapTransform
NON_COSMETIC_PEN            = QPainter.NonCosmeticDefaultPen

BRUSH_NONE                  = Qt.NoBrush                                                # Brush

PEN_NONE                    = Qt.NoPen                                                  # Pen
ROUND_CAP                   = Qt.RoundCap
ROUND_JOIN                  = Qt.RoundJoin

PATTERN_SOLID               = Qt.SolidPattern                                           # Pattern

LINE_SOLID                  = Qt.SolidLine                                              # Line

COLOR_LIBS = dict(
    WHITE                   = Qt.white,                                                  # Color
    LIGHTGRAY               = Qt.lightGray,
    GRAY                    = Qt.gray,
    DARKGRAY                = Qt.darkGray,
    BLACK                   = Qt.black,
    RED                     = Qt.red,
    GREEN                   = Qt.green,
    BLUE                    = Qt.blue,
    DARKRED                 = Qt.darkGreen,
    DARKGREEN               = Qt.darkGreen,
    DARKBLUE                = Qt.darkBlue,
    CYAN                    = Qt.cyan,
    MAGENTA                 = Qt.magenta,
    YELLOW                  = Qt.yellow,
    DARKCYAN                = Qt.darkCyan,
    DARKMAGENTA             = Qt.darkMagenta,
    DARKYELLOW              = Qt.darkYellow,

    blush                   = QColor(246, 202, 203, 255),
    petal                   = QColor(247, 170, 189, 255),
    petunia                 = QColor(231, 62, 151, 255),
    deep_pink               = QColor(229, 2, 120, 255),
    melon                   = QColor(241, 118, 110, 255),
    pomegranate             = QColor(178, 27, 32, 255),
    poppy_red               = QColor(236, 51, 39, 255),
    orange_red              = QColor(240, 101, 53, 255),
    olive                   = QColor(174, 188, 43, 255),
    spring                  = QColor(227, 229, 121, 255),
    yellow                  = QColor(255, 240, 29, 255),
    mango                   = QColor(254, 209, 26, 255),
    cantaloupe              = QColor(250, 176, 98, 255),
    tangelo                 = QColor(247, 151, 47, 255),
    burnt_orange            = QColor(236, 137, 36, 255),
    bright_orange           = QColor(242, 124, 53, 255),
    moss                    = QColor(176, 186, 39, 255),
    sage                    = QColor(212, 219, 145, 255),
    apple                   = QColor(178, 215, 140, 255),
    grass                   = QColor(111, 178, 68, 255),
    forest                  = QColor(69, 149, 62, 255),
    peacock                 = QColor(21, 140, 167, 255),
    teal                    = QColor(24, 157, 193, 255),
    aqua                    = QColor(153, 214, 218, 255),
    violet                  = QColor(55, 52, 144, 255),
    deep_blue               = QColor(15, 86, 163, 255),
    hydrangea               = QColor(150, 191, 229, 255),
    sky                     = QColor(139, 210, 244, 255),
    dusk                    = QColor(16, 102, 162, 255),
    midnight                = QColor(14, 90, 131, 255),
    seaside                 = QColor(87, 154, 188, 255),
    poolside                = QColor(137, 203, 225, 255),
    eggplant                = QColor(86, 5, 79, 255),
    lilac                   = QColor(222, 192, 219, 255),
    chocolate               = QColor(87, 43, 3, 255),
    blackout                = QColor(19, 17, 15, 255),
    stone                   = QColor(125, 127, 130, 255),
    gravel                  = QColor(181, 182, 185, 255),
    pebble                  = QColor(217, 212, 206, 255),
    sand                    = QColor(185, 172, 151, 255),
    )

# -------------------------------------------------------------------------------------------------------------
""" Keyboard and cursor """

KEYBOARD                    = Qt.Key                                                    # Keyboard
KEY_ALT                     = Qt.Key_Alt
KEY_DEL                     = Qt.Key_Delete
KEY_TAB                     = Qt.Key_Tab
KEY_SHIFT                   = Qt.Key_Shift
KEY_CTRL                    = Qt.Key_Control
KEY_BACKSPACE               = Qt.Key_Backspace
KEY_F                       = Qt.Key_F
KEY_S                       = Qt.Key_S
ALT_MODIFIER                = Qt.AltModifier
CTRL_MODIFIER               = Qt.ControlModifier
SHIFT_MODIFIER              = Qt.ShiftModifier
NO_MODIFIER                 = Qt.NoModifier
CLOSE_HAND_CUSOR            = Qt.ClosedHandCursor

windows                     = os.name = 'nt'
DMK                         = Qt.AltModifier if windows else CTRL_MODIFIER

MOUSEBTN                    = Qt.MouseButton                                            # Mouse button
MOUSE_LEFT                  = Qt.LeftButton
MOUSE_RIGHT                 = Qt.RightButton
MOUSE_MIDDLE                = Qt.MiddleButton

ARROW_NONE                  = Qt.NoArrow                                                # Cursor
CURSOR_ARROW                = Qt.ArrowCursor
CURSOR_SIZEALL              = Qt.SizeAllCursor

ACTION_MOVE                 = Qt.MoveAction                                             # Action

# -------------------------------------------------------------------------------------------------------------
""" Set number """

RELATIVE_SIZE               = Qt.RelativeSize                                           # Size

POSX                        = 0
POSY                        = 0

NODE_WIDTH                  = 200
NODE_ROUND                  = 10
NODE_BORDER                 = 2
NODE_REC                    = 30
NODE_STAMP                  = 25

NODE_HEADER_HEIGHT          = 25
NODE_FOOTER_HEIGHT          = 25

ATTR_HEIGHT                 = 30
ATTR_ROUND                  = NODE_ROUND/2
ATTR_REC                    = NODE_REC/2

RADIUS                      = 10
COL                         = 10
ROW                         = 10
GRID_SIZE                   = 50

FLTR                        = 'flow_left_to_right'
FRTL                        = 'flow_right_to_left'

MARGIN                      = 20
ROUNDNESS                   = 0
THICKNESS                   = 1
CURRENT_ZOOM                = 1

UNIT                        = 60                                                                # Base Unit
MARG                        = 5                                                                 # Content margin
BUFF                        = 10                                                                # Buffer size
SCAL                        = 1                                                                 # Scale value
STEP                        = 1                                                                 # Step value changing
VAL                         = 1                                                                 # Default value
MIN                         = 0                                                                 # Minimum value
MAX                         = 1000                                                              # Maximum value
WMIN                        = 50                                                                # Minimum width
HMIN                        = 20                                                                # Minimum height
HFIX                        = 80
ICONSIZE                    = 32
ICONBUFFER                  = -1
BTNICONSIZE                 = QSize(ICONSIZE, ICONSIZE)
ICONBTNSIZE                 = QSize(ICONSIZE+ICONBUFFER, ICONSIZE+ICONBUFFER)

keepARM                     = Qt.KeepAspectRatio
ignoreARM                   = Qt.IgnoreAspectRatio

scrollAsNeed                = Qt.ScrollBarAsNeeded
scrollOff                   = Qt.ScrollBarAlwaysOff
scrollOn                    = Qt.ScrollBarAlwaysOn

SiPoMin                     = QSizePolicy.Minimum                                               # Size policy
SiPoMax                     = QSizePolicy.Maximum
SiPoExp                     = QSizePolicy.Expanding
SiPoPre                     = QSizePolicy.Preferred
SiPoIgn                     = QSizePolicy.Ignored

frameStyle                  = QFrame.Sunken | QFrame.Panel

center                      = Qt.AlignCenter                                                    # Alignment
right                       = Qt.AlignRight
left                        = Qt.AlignLeft
hori                        = Qt.Horizontal
vert                        = Qt.Vertical

dockL                       = Qt.LeftDockWidgetArea                                             # Docking area
dockR                       = Qt.RightDockWidgetArea
dockT                       = Qt.TopDockWidgetArea
dockB                       = Qt.BottomDockWidgetArea

# -------------------------------------------------------------------------------------------------------------
""" Node graph pre setting """

# node connection property types
PROPERTY = dict( simple = ['FLOAT', 'STRING', 'BOOL', 'INT'] , arrays  = ['FLOAT2', 'FLOAT3', 'INT2', 'INT3', 'COLOR'],
                 max    = 'maximum value'                    , types   = ['FILE', 'MULTI', 'MERGE', 'NODE', 'DIR']    ,
                 min    = 'minimum value'                    , default = 'default value'                              ,
                 label  = 'node label'                       , private = 'attribute is private (hiddent)'             ,
                 desc   = 'attribute description',)

REGEX   = dict( section        = re.compile(r"^\[[^\]\r\n]+]"),
                section_value  = re.compile(r"\[(?P<attr>[\w]*?) (?P<value>[\w\s]*?)\]$"),
                properties     = re.compile("(?P<name>[\.\w]*)\s*(?P<type>\w*)\s*(?P<value>.*)$"),)

# Default preferences
PREFERENCES = dict(
    ignore_scene_prefs  = {"default": False,     "desc": "Use user prefences instead of scene preferences.", "label": "Ignore scene preferences",    "class": "global"},
    use_gl              = {"default": False,     "desc": "Render graph with OpenGL.",                        "label": "Use OpenGL",                  "class": "scene" },
    edge_type           = {"default": "bezier",  "desc": "Draw edges with bezier paths.",                    "label": "Edge style",                  "class": "scene" },
    render_fx           = {"default": False,     "desc": "Render node drop shadows and effects.",            "label": "render FX",                   "class": "scene" },
    antialiasing        = {"default": 2,         "desc": "Antialiasing level.",                              "label": "Antialiasing",                "class": "scene" },
    logging_level       = {"default": 30,        "desc": "Verbosity level.",                                 "label": "Logging level",               "class": "global"},
    autosave_inc        = {"default": 90000,     "desc": "Autosave delay (seconds x 1000).",                 "label": "Autosave time",               "class": "global"},
    stylesheet_name     = {"default": "default", "desc": "Stylesheet to use.",                               "label": "Stylesheet",                  "class": "global"},
    palette_style       = {"default": "default", "desc": "Color palette to use.",                            "label": "Palette",                     "class": "global"},
    font_style          = {"default": "default", "desc": "font style to use.",                               "label": "Font style",                  "class": "global"},
    viewport_mode       = {"default": "smart",   "desc": "viewport update fm.",                              "label": "Viewport Mode",               "class": "global"}, )

VALID_FONTS = dict( ui   = [ 'Arial', 'Cantarell', 'Corbel', 'DejaVu Sans', 'DejaVu Serif', 'FreeSans', 'Liberation Sans',
                             'Lucida Sans Unicode', 'MS Sans Serif', 'Open Sans', 'PT Sans', 'Tahoma', 'Verdana'],

                    mono = [ 'Consolas', 'Courier', 'Courier 10 Pitch', 'Courier New', 'DejaVu Sans Mono', 'Fixed',
                             'FreeMono', 'Liberation Mono', 'Lucida Console', 'Menlo', 'Monaco'],

                    nodes= [ 'Consolas', 'DejaVu Sans Mono', 'Menlo', 'DejaVu Sans'])

EDGE_TYPES      = dict(bezier = 'bezier'        , polygon = 'polygon'       , )
POS_EVENTS      = dict(change = POS_CHANGE      , )
DRAG_MODES      = dict(none   = NODRAG          , rubber = RUBBER_DRAG)
VIEWPORT_MODES  = dict(full   = UPDATE_FULLVIEW , smart  = UPDATE_SMARTVIEW , minimal = UPDATE_MINIMALVIEW  , bounding = UPDATE_BOUNDINGVIEW, viewrect = UPDATE_VIEWRECT)
FLAG_MODES      = dict(select = SELECTABLE      , move   = MOVEABLE         , focus   = FOCUSABLE           , panel    = PANEL)
ANCHOR_MODES    = dict(none   = NOANCHOR        , under  = ANCHOR_UNDERMICE , center  = ANCHOR_VIEWCENTER   , )


NODE            = dict( width               = NODE_WIDTH            , height       = 25              , radius                 = 10                  , border    = 2 ,
                        attHeight           = 30                    , con_width    = 2               , font                   = 'Arial'             , font_size = 12,
                        attFont             = 'Arial'               , attFont_size = 10              , mouse_bounding_box     = 80                  , alternate= 20,
                        grid_color          = [50, 50, 50, 255]     , slot_border  = [50, 50, 50, 255], non_connectable_color = [100, 100, 100, 255],
                        connection_color    = [255, 155, 0, 255], )

SCENE           = dict( width               = 2000                  , height = 2000                 , size              = 36       , antialiasing = True,
                        antialiasing_boost  = True                  , smooth_pixmap = True, )

# -------------------------------------------------------------------------------------------------------------
""" PLM project base """

PRJ_INFO = dict( APPS               = ["maya", "zbrush", "mari", "nuke", "photoshop", "houdini", "after effects"],
                 MASTER             = ["assets", "sequences", "deliverables", "documents", "editorial", "sound", "resources", "RnD"],
                 TASKS              = ["art", "plt_model", "rigging", "surfacing"],
                 SEQTASKS           = ["anim", "comp", "fx", "layout", "lighting"],
                 ASSETS             = {"heroObj": ["washer", "dryer"], "environment": [], "props": []},
                 STEPS              = ["publish", "review", "work"],
                 MODELING           = ["scenes", "fromZ", "toZ", "objImport", "objExport", "movie"],
                 RIGGING            = ["scenes", "reference"],
                 SURFACING          = ["scenes", "sourceimages", "images", "movie"],
                 LAYOUT             = ["scenes", "sourceimages", "images", "movie", "alembic"],
                 LIGHTING           = ["scenes", "sourceimages", "images", "cache", "reference"],
                 FX                 = ["scenes", "sourceimages", "images", "cache", "reference", "alembic"],
                 ANIM               = ["scenes", "sourceimages", "images", "movie", "alembic"],)

FIX_KEYS = dict( TextEditor         = 'textEditor', NoteReminder = 'noteReminder',  Calculator  = 'calculator',  Calendar  = 'calendar',
                 EnglishDictionary  = 'engDict',    FindFiles    = 'findFile',      ImageViewer = 'imageViewer', NodeGraph = 'nodeGraph',
                 Screenshot         = 'screenShot', )

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 10:45 PM
# Pipeline manager - DAMGteam
