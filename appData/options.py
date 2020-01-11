# -*- coding: utf-8 -*-
"""

Script Name: options.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

""" Import """

#Python
import re, os
from collections import OrderedDict

# PyQt5
from PyQt5.QtCore           import Qt, QSize, QEvent
from PyQt5.QtGui            import QPainter, QFont
from PyQt5.QtWidgets        import (QGraphicsItem, QGraphicsView, QGraphicsScene, QRubberBand, QFrame, QSizePolicy,
                                    QLineEdit, QPlainTextEdit, QAbstractItemView, QStyle)

# -------------------------------------------------------------------------------------------------------------
""" Font """

BOLD                        = QFont.Bold
NORMAL                      = QFont.Normal

# -------------------------------------------------------------------------------------------------------------
""" Event """

NO_WRAP                     = QPlainTextEdit.NoWrap
NO_FRAME                    = QPlainTextEdit.NoFrame
ELIDE_RIGHT                 = Qt.ElideRight
KEY_PRESS                   = QEvent.KeyPress
KEY_RELEASE                 = QEvent.KeyRelease

# -------------------------------------------------------------------------------------------------------------
""" Window state """

StateNormal                 = Qt.WindowNoState
StateMax                    = Qt.WindowMaximized
StateMin                    = Qt.WindowMinimized
State_Selected              = QStyle.State_Selected

# -------------------------------------------------------------------------------------------------------------
""" Nodegraph setting variables """

ASPEC_RATIO                 = Qt.KeepAspectRatio
SMOOTH_TRANS                = Qt.SmoothTransformation
SCROLLBAROFF                = Qt.ScrollBarAlwaysOff                                     # Scrollbar
SCROLLBARON                 = Qt.ScrollBarAlwaysOn
SCROLLBARNEED               = Qt.ScrollBarAsNeeded

WORD_WRAP                   = Qt.TextWordWrap
INTERSECT_ITEM_SHAPE        = Qt.IntersectsItemShape
CONTAIN_ITEM_SHAPE          = Qt.ContainsItemShape
MATCH_EXACTLY               = Qt.MatchExactly
DRAG_ONLY                   = QAbstractItemView.DragOnly

# -------------------------------------------------------------------------------------------------------------
""" UI flags """

ITEMENABLE                  = Qt.ItemIsEnabled
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
ANCHOR_NO                   = QGraphicsView.NoAnchor

ANCHOR_UNDERMICE            = QGraphicsView.AnchorUnderMouse
ANCHOR_CENTER               = QGraphicsView.AnchorViewCenter

CACHE_BG                    = QGraphicsView.CacheBackground

UPDATE_VIEWRECT             = QGraphicsView.BoundingRectViewportUpdate
UPDATE_FULLVIEW             = QGraphicsView.FullViewportUpdate
UPDATE_SMARTVIEW            = QGraphicsView.SmartViewportUpdate
UPDATE_BOUNDINGVIEW         = QGraphicsView.BoundingRectViewportUpdate
UPDATE_MINIMALVIEW          = QGraphicsView.MinimalViewportUpdate

STAY_ON_TOP                 = Qt.WindowStaysOnTopHint
STRONG_FOCUS                = Qt.StrongFocus
FRAMELESS                   = Qt.FramelessWindowHint
AUTO_COLOR                  = Qt.AutoColor

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
LINE_DASH                   = Qt.DashLine
LINE_DOT                    = Qt.DotLine
LINE_DASH_DOT               = Qt.DashDotDotLine

# -------------------------------------------------------------------------------------------------------------
""" Week Day  """

sunday                      = Qt.Sunday
monday                      = Qt.Monday
tuesady                     = Qt.Tuesday
wednesday                   = Qt.Wednesday
thursday                    = Qt.Thursday
friday                      = Qt.Friday
saturday                    = Qt.Saturday

# -------------------------------------------------------------------------------------------------------------
""" Keyboard and cursor """

KEY_ALT                     = Qt.Key_Alt
KEY_DEL                     = Qt.Key_Delete
KEY_TAB                     = Qt.Key_Tab
KEY_SHIFT                   = Qt.Key_Shift
KEY_CTRL                    = Qt.Key_Control
KEY_BACKSPACE               = Qt.Key_Backspace
KEY_ENTER                   = Qt.Key_Enter
KEY_RETURN                  = Qt.Key_Return
KEY_F                       = Qt.Key_F
KEY_S                       = Qt.Key_S
ALT_MODIFIER                = Qt.AltModifier
CTRL_MODIFIER               = Qt.ControlModifier
SHIFT_MODIFIER              = Qt.ShiftModifier
NO_MODIFIER                 = Qt.NoModifier
CLOSE_HAND_CUSOR            = Qt.ClosedHandCursor
SIZEF_CURSOR                = Qt.SizeFDiagCursor

windows                     = os.name = 'nt'
DMK                         = Qt.AltModifier if windows else CTRL_MODIFIER

MOUSE_LEFT                  = Qt.LeftButton
MOUSE_RIGHT                 = Qt.RightButton
MOUSE_MIDDLE                = Qt.MiddleButton
NO_BUTTON                   = Qt.NoButton

ARROW_NONE                  = Qt.NoArrow                                                # Cursor
CURSOR_ARROW                = Qt.ArrowCursor
CURSOR_SIZEALL              = Qt.SizeAllCursor

ACTION_MOVE                 = Qt.MoveAction                                             # Action

# -------------------------------------------------------------------------------------------------------------
""" Set number """

RELATIVE_SIZE               = Qt.RelativeSize                                           # Size

POSX                        = 0
POSY                        = 0


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
BTNTAGSIZE                  = QSize(87, 20)
TAGBTNSIZE                  = QSize(87-1, 20-1)
BTNICONSIZE                 = QSize(ICONSIZE, ICONSIZE)
ICONBTNSIZE                 = QSize(ICONSIZE+ICONBUFFER, ICONSIZE+ICONBUFFER)

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
top                         = Qt.AlignTop
bottom                      = Qt.AlignBottom
hori                        = Qt.Horizontal
vert                        = Qt.Vertical
black                       = Qt.black
blue                        = Qt.blue
darkBlue                    = Qt.darkBlue
cyan                        = Qt.cyan

dockL                       = Qt.LeftDockWidgetArea                                             # Docking area
dockR                       = Qt.RightDockWidgetArea
dockT                       = Qt.TopDockWidgetArea
dockB                       = Qt.BottomDockWidgetArea
dockAll                     = Qt.AllDockWidgetAreas

# === PIPE ===

PIPE_WIDTH = 1.2
PIPE_STYLE_DEFAULT = 'line'
PIPE_STYLE_DASHED = 'dashed'
PIPE_STYLE_DOTTED = 'dotted'
PIPE_DEFAULT_COLOR = (175, 95, 30, 255)
PIPE_DISABLED_COLOR = (190, 20, 20, 255)
PIPE_ACTIVE_COLOR = (70, 255, 220, 255)
PIPE_HIGHLIGHT_COLOR = (232, 184, 13, 255)
PIPE_SLICER_COLOR = (255, 50, 75)
#: Style to draw the connection pipes as straight lines.
PIPE_LAYOUT_STRAIGHT = 0
#: Style to draw the connection pipes as curved lines.
PIPE_LAYOUT_CURVED = 1
#: Style to draw the connection pipes as angled lines.
PIPE_LAYOUT_ANGLE = 2

# === PORT ===

#: Connection type for input ports.
IN_PORT = 'in'
#: Connection type for output ports.
OUT_PORT = 'out'

PORT_DEFAULT_SIZE = 22.0
PORT_DEFAULT_COLOR = (49, 115, 100, 255)
PORT_DEFAULT_BORDER_COLOR = (29, 202, 151, 255)
PORT_ACTIVE_COLOR = (14, 45, 59, 255)
PORT_ACTIVE_BORDER_COLOR = (107, 166, 193, 255)
PORT_HOVER_COLOR = (17, 43, 82, 255)
PORT_HOVER_BORDER_COLOR = (136, 255, 35, 255)
PORT_FALLOFF = 15.0

# === NODE ===

NODE_WIDTH = 170
NODE_HEIGHT = 80
NODE_ICON_SIZE = 24
NODE_SEL_COLOR = (255, 255, 255, 30)
NODE_SEL_BORDER_COLOR = (254, 207, 42, 255)

# === NODE PROPERTY ===

#: Property type will hidden in the properties bin (default).
NODE_PROP = 0
#: Property type represented with a QLabel widget in the properties bin.
NODE_PROP_QLABEL = 2
#: Property type represented with a QLineEdit widget in the properties bin.
NODE_PROP_QLINEEDIT = 3
#: Property type represented with a QTextEdit widget in the properties bin.
NODE_PROP_QTEXTEDIT = 4
#: Property type represented with a QComboBox widget in the properties bin.
NODE_PROP_QCOMBO = 5
#: Property type represented with a QCheckBox widget in the properties bin.
NODE_PROP_QCHECKBOX = 6
#: Property type represented with a QSpinBox widget in the properties bin.
NODE_PROP_QSPINBOX = 7
#: Property type represented with a ColorPicker widget in the properties bin.
NODE_PROP_COLORPICKER = 8
#: Property type represented with a Slider widget in the properties bin.
NODE_PROP_SLIDER = 9

# === NODE VIEWER ===

VIEWER_BG_COLOR = (35, 35, 35)
VIEWER_GRID_COLOR = (45, 45, 45)
VIEWER_GRID_OVERLAY = True
VIEWER_GRID_SIZE = 20

SCENE_AREA = 8000.0

DRAG_DROP_ID = 'n0deGraphQT'

# === PATHS ===

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(BASE_PATH, 'widgets', 'icons')
ICON_DOWN_ARROW = os.path.join(ICON_PATH, 'down_arrow.png')
ICON_NODE_BASE = os.path.join(ICON_PATH, 'node_base.png')

# === DRAW STACK ORDER ===

Z_VAL_PIPE = -1
Z_VAL_NODE = 1
Z_VAL_PORT = 2
Z_VAL_NODE_WIDGET = 3


# -------------------------------------------------------------------------------------------------------------
""" setting """

PRS = dict( password    = QLineEdit.Password,       center = center ,   left  = left   ,    right  = right,
            spmax       = SiPoMax           ,       sppre  = SiPoPre,   spexp = SiPoExp,    spign  = SiPoIgn,
            expanding   = QSizePolicy.Expanding,    spmin  = SiPoMin,)

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
    edge_type           = {"default": "bezier",  "desc": "Draw edges with bezier paths.",                    "label": "Edge name",                  "class": "scene" },
    render_fx           = {"default": False,     "desc": "Render node drop shadows and effects.",            "label": "render FX",                   "class": "scene" },
    antialiasing        = {"default": 2,         "desc": "Antialiasing level.",                              "label": "Antialiasing",                "class": "scene" },
    logging_level       = {"default": 30,        "desc": "Verbosity level.",                                 "label": "Logging level",               "class": "global"},
    autosave_inc        = {"default": 90000,     "desc": "Autosave delay (seconds x 1000).",                 "label": "Autosave time",               "class": "global"},
    stylesheet_name     = {"default": "default", "desc": "Stylesheet to use.",                               "label": "Stylesheet",                  "class": "global"},
    palette_style       = {"default": "default", "desc": "Color palette to use.",                            "label": "Palette",                     "class": "global"},
    font_style          = {"default": "default", "desc": "font name to use.",                               "label": "Font name",                  "class": "global"},
    viewport_mode       = {"default": "smart",   "desc": "viewport update fn.",                              "label": "Viewport Mode",               "class": "global"}, )

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
ANCHOR_MODES    = dict(none   = ANCHOR_NO       , under  = ANCHOR_UNDERMICE , center  = ANCHOR_CENTER, )


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
                 MASTER             = ["assets", "sequences", "deliverables", "docs", "editorial", "sound", "rcs", "RnD"],
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

FIX_KEYS = dict( TextEditor         = 'TextEditor', NoteReminder = 'NoteReminder',  Calculator  = 'Calculator',  Calendar  = 'Calendar',
                 EnglishDictionary  = 'EnglishDictionary',    FindFiles    = 'FindFiles',      ImageViewer = 'ImageViewer', NodeGraph = 'NodeGraph',
                 Screenshot         = 'Screenshot', )


class DarkPalette(object):
    """Theme variables."""

    # Color
    COLOR_BACKGROUND_LIGHT = '#505F69'
    COLOR_BACKGROUND_NORMAL = '#32414B'
    COLOR_BACKGROUND_DARK = '#19232D'

    COLOR_FOREGROUND_LIGHT = '#F0F0F0'
    COLOR_FOREGROUND_NORMAL = '#AAAAAA'
    COLOR_FOREGROUND_DARK = '#787878'

    COLOR_SELECTION_LIGHT = '#148CD2'
    COLOR_SELECTION_NORMAL = '#1464A0'
    COLOR_SELECTION_DARK = '#14506E'

    OPACITY_TOOLTIP = 230

    # Size
    SIZE_BORDER_RADIUS = '4px'

    # Borders
    BORDER_LIGHT = '1px solid $COLOR_BACKGROUND_LIGHT'
    BORDER_NORMAL = '1px solid $COLOR_BACKGROUND_NORMAL'
    BORDER_DARK = '1px solid $COLOR_BACKGROUND_DARK'

    BORDER_SELECTION_LIGHT = '1px solid $COLOR_SELECTION_LIGHT'
    BORDER_SELECTION_NORMAL = '1px solid $COLOR_SELECTION_NORMAL'
    BORDER_SELECTION_DARK = '1px solid $COLOR_SELECTION_DARK'

    # Example of additional widget specific variables
    W_STATUS_BAR_BACKGROUND_COLOR = COLOR_SELECTION_DARK

    # Paths
    PATH_RESOURCES = "':/qss_icons'"

    @classmethod
    def to_dict(cls, colors_only=False):
        """Convert variables to dictionary."""
        order = [
            'COLOR_BACKGROUND_LIGHT',
            'COLOR_BACKGROUND_NORMAL',
            'COLOR_BACKGROUND_DARK',
            'COLOR_FOREGROUND_LIGHT',
            'COLOR_FOREGROUND_NORMAL',
            'COLOR_FOREGROUND_DARK',
            'COLOR_SELECTION_LIGHT',
            'COLOR_SELECTION_NORMAL',
            'COLOR_SELECTION_DARK',
            'OPACITY_TOOLTIP',
            'SIZE_BORDER_RADIUS',
            'BORDER_LIGHT',
            'BORDER_NORMAL',
            'BORDER_DARK',
            'BORDER_SELECTION_LIGHT',
            'BORDER_SELECTION_NORMAL',
            'BORDER_SELECTION_DARK',
            'W_STATUS_BAR_BACKGROUND_COLOR',
            'PATH_RESOURCES',
        ]
        dic = OrderedDict()
        for var in order:
            value = getattr(cls, var)

            if colors_only:
                if not var.startswith('COLOR'):
                    value = None

            if value:
                dic[var] = value

        return dic

    @classmethod
    def color_palette(cls):
        """Return the ordered colored palette dictionary."""
        return cls.to_dict(colors_only=True)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 23/10/2019 - 2:48 AM
# © 2017 - 2018 DAMGteam. All rights reserved