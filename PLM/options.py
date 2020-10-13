# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import os, semantic_version, re, sys
from PLM import CFG_DIR, __envKey__

from PySide2.QtWidgets      import (QFrame, QStyle, QAbstractItemView, QSizePolicy, QLineEdit, QPlainTextEdit,
                                    QGraphicsItem, QGraphicsView, QGraphicsScene, QRubberBand, QCalendarWidget, )
from PySide2.QtCore         import QEvent, QSettings, QSize, Qt, QDateTime
from PySide2.QtGui          import QColor, QPainter, QFont, QTextCursor


SingleSelection             = QCalendarWidget.SingleSelection
NoSelection                 = QCalendarWidget.NoSelection
SingleLetterDay             = QCalendarWidget.SingleLetterDayNames
ShortDay                    = QCalendarWidget.ShortDayNames
LongDay                     = QCalendarWidget.LongDayNames
NoHoriHeader                = QCalendarWidget.NoHorizontalHeader
NoVertHeader                = QCalendarWidget.NoVerticalHeader
IsoWeekNum                  = QCalendarWidget.ISOWeekNumbers
SelectMode                  = QCalendarWidget.SelectionMode
HoriHeaderFm                = QCalendarWidget.HorizontalHeaderFormat
VertHeaderFm                = QCalendarWidget.VerticalHeaderFormat

DayOfWeek                   = Qt.DayOfWeek

Sunday                      = Qt.Sunday
Monday                      = Qt.Monday
Tuesday                     = Qt.Tuesday
Wednesday                   = Qt.Wednesday
Thursday                    = Qt.Thursday
Friday                      = Qt.Friday
Saturday                    = Qt.Saturday

ICONSIZE                    = 32
ICONBUFFER                  = -1
BTNTAGSIZE                  = QSize(87, 20)
TAGBTNSIZE                  = QSize(87-1, 20-1)
BTNICONSIZE                 = QSize(ICONSIZE, ICONSIZE)
ICONBTNSIZE                 = QSize(ICONSIZE+ICONBUFFER, ICONSIZE+ICONBUFFER)


DAMG_LOGO_COLOR             = QColor(0, 114, 188, 255)


# Basic color

GlobalColor                 = Qt.GlobalColor

WHITE                       = QColor(Qt.white)
LIGHTGRAY                   = QColor(Qt.lightGray)
GRAY                        = QColor(Qt.gray)
DARKGRAY                    = QColor(Qt.darkGray)
BLACK                       = QColor(Qt.black)
RED                         = QColor(Qt.red)
GREEN                       = QColor(Qt.green)
BLUE                        = QColor(Qt.blue)
DARKRED                     = QColor(Qt.darkRed)
DARKGREEN                   = QColor(Qt.darkGreen)
DARKBLUE                    = QColor(Qt.darkBlue)
CYAN                        = QColor(Qt.cyan)
MAGENTA                     = QColor(Qt.magenta)
YELLOW                      = QColor(Qt.yellow)
DARKCYAN                    = QColor(Qt.darkCyan)
DARKMAGENTA                 = QColor(Qt.darkMagenta)
DARKYELLOW                  = QColor(Qt.darkYellow)

# Dark Palette color
Color_BACKGROUND_LIGHT      = QColor('#505F69')
COLOR_BACKGROUND_NORMAL     = QColor('#32414B')
COLOR_BACKGROUND_DARK       = QColor('#19232D')

COLOR_FOREGROUND_LIGHT      = QColor('#F0F0F0')
COLOR_FOREGROUND_NORMAL     = QColor('#AAAAAA')
COLOR_FOREGROUND_DARK       = QColor('#787878')

COLOR_SELECTION_LIGHT       = QColor('#148CD2')
COLOR_SELECTION_NORMAL      = QColor('#1464A0')
COLOR_SELECTION_DARK        = QColor('#14506E')

# Nice color
blush                       = QColor(246, 202, 203, 255)
petal                       = QColor(247, 170, 189, 255)
petunia                     = QColor(231, 62, 151, 255)
deep_pink                   = QColor(229, 2, 120, 255)
melon                       = QColor(241, 118, 110, 255)
pomegranate                 = QColor(178, 27, 32, 255)
poppy_red                   = QColor(236, 51, 39, 255)
orange_red                  = QColor(240, 101, 53, 255)
olive                       = QColor(174, 188, 43, 255)
spring                      = QColor(227, 229, 121, 255)
yellow                      = QColor(255, 240, 29, 255)
mango                       = QColor(254, 209, 26, 255)
cantaloupe                  = QColor(250, 176, 98, 255)
tangelo                     = QColor(247, 151, 47, 255)
burnt_orange                = QColor(236, 137, 36, 255)
bright_orange               = QColor(242, 124, 53, 255)
moss                        = QColor(176, 186, 39, 255)
sage                        = QColor(212, 219, 145, 255)
apple                       = QColor(178, 215, 140, 255)
grass                       = QColor(111, 178, 68, 255)
forest                      = QColor(69, 149, 62, 255)
peacock                     = QColor(21, 140, 167, 255)
teal                        = QColor(24, 157, 193, 255)
aqua                        = QColor(153, 214, 218, 255)
violet                      = QColor(55, 52, 144, 255)
deep_blue                   = QColor(15, 86, 163, 255)
hydrangea                   = QColor(150, 191, 229, 255)
sky                         = QColor(139, 210, 244, 255)
dusk                        = QColor(16, 102, 162, 255)
midnight                    = QColor(14, 90, 131, 255)
seaside                     = QColor(87, 154, 188, 255)
poolside                    = QColor(137, 203, 225, 255)
eggplant                    = QColor(86, 5, 79, 255)
lilac                       = QColor(222, 192, 219, 255)
chocolate                   = QColor(87, 43, 3, 255)
blackout                    = QColor(19, 17, 15, 255)
stone                       = QColor(125, 127, 130, 255)
gravel                      = QColor(181, 182, 185, 255)
pebble                      = QColor(217, 212, 206, 255)
sand                        = QColor(185, 172, 151, 255)


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

dockL                       = Qt.LeftDockWidgetArea                                             # Docking area
dockR                       = Qt.RightDockWidgetArea
dockT                       = Qt.TopDockWidgetArea
dockB                       = Qt.BottomDockWidgetArea
dockAll                     = Qt.AllDockWidgetAreas


datetTimeStamp               = QDateTime.currentDateTime().toString("hh:mm - dd MMMM yy")             # datestamp


PRS =       dict(password    = QLineEdit.Password,       center = center ,   left  = left   ,    right  = right,
                 spmax       = SiPoMax           ,       sppre  = SiPoPre,   spexp = SiPoExp,    spign  = SiPoIgn,
                 expanding   = QSizePolicy.Expanding,    spmin  = SiPoMin,)


# -------------------------------------------------------------------------------------------------------------
""" Event """

NO_WRAP                      = QPlainTextEdit.NoWrap
NO_FRAME                     = QPlainTextEdit.NoFrame
ELIDE_RIGHT                  = Qt.ElideRight
ELIDE_NONE                   = Qt.ElideNone


# -------------------------------------------------------------------------------------------------------------
""" Window state """

StateNormal                  = Qt.WindowNoState
StateMax                     = Qt.WindowMaximized
StateMin                     = Qt.WindowMinimized
State_Selected               = QStyle.State_Selected

# -------------------------------------------------------------------------------------------------------------
""" Nodegraph setting variables """

ASPEC_RATIO                  = Qt.KeepAspectRatio
SMOOTH_TRANS                 = Qt.SmoothTransformation
SCROLLBAROFF                 = Qt.ScrollBarAlwaysOff                                     # Scrollbar
SCROLLBARON                  = Qt.ScrollBarAlwaysOn
SCROLLBARNEED                = Qt.ScrollBarAsNeeded

WORD_WRAP                    = Qt.TextWordWrap
INTERSECT_ITEM_SHAPE         = Qt.IntersectsItemShape
CONTAIN_ITEM_SHAPE           = Qt.ContainsItemShape
MATCH_EXACTLY                = Qt.MatchExactly
DRAG_ONLY                    = QAbstractItemView.DragOnly

# -------------------------------------------------------------------------------------------------------------
""" UI flags """

ITEMENABLE                   = Qt.ItemIsEnabled
ITEMMOVEABLE                 = QGraphicsItem.ItemIsMovable
ITEMSENDGEOCHANGE            = QGraphicsItem.ItemSendsGeometryChanges
ITEMSCALECHANGE              = QGraphicsItem.ItemScaleChange
ITEMPOSCHANGE                = QGraphicsItem.ItemPositionChange
DEVICECACHE                  = QGraphicsItem.DeviceCoordinateCache
SELECTABLE                   = QGraphicsItem.ItemIsSelectable
MOVEABLE                     = QGraphicsItem.ItemIsMovable
FOCUSABLE                    = QGraphicsItem.ItemIsFocusable
PANEL                        = QGraphicsItem.ItemIsPanel

NOINDEX                      = QGraphicsScene.NoIndex                                    # Scene

RUBBER_DRAG                  = QGraphicsView.RubberBandDrag                              # Viewer
RUBBER_REC                   = QRubberBand.Rectangle
POS_CHANGE                   = QGraphicsItem.ItemPositionChange

NODRAG                       = QGraphicsView.NoDrag
NOFRAME                      = QGraphicsView.NoFrame
ANCHOR_NO                    = QGraphicsView.NoAnchor

ANCHOR_UNDERMICE             = QGraphicsView.AnchorUnderMouse
ANCHOR_CENTER                = QGraphicsView.AnchorViewCenter

CACHE_BG                     = QGraphicsView.CacheBackground

UPDATE_VIEWRECT              = QGraphicsView.BoundingRectViewportUpdate
UPDATE_FULLVIEW              = QGraphicsView.FullViewportUpdate
UPDATE_SMARTVIEW             = QGraphicsView.SmartViewportUpdate
UPDATE_BOUNDINGVIEW          = QGraphicsView.BoundingRectViewportUpdate
UPDATE_MINIMALVIEW           = QGraphicsView.MinimalViewportUpdate

STAY_ON_TOP                  = Qt.WindowStaysOnTopHint
STRONG_FOCUS                 = Qt.StrongFocus
SPLASHSCREEN                 = Qt.SplashScreen
FRAMELESS                    = Qt.FramelessWindowHint
CUSTOMIZE                    = Qt.CustomizeWindowHint
CLOSEBTN                     = Qt.WindowCloseButtonHint
MINIMIZEBTN                  = Qt.WindowMinimizeButtonHint
AUTO_COLOR                   = Qt.AutoColor

# -------------------------------------------------------------------------------------------------------------
""" Drawing """

ANTIALIAS                    = QPainter.Antialiasing                                     # Painter
ANTIALIAS_TEXT               = QPainter.TextAntialiasing
ANTIALIAS_HIGH_QUALITY       = QPainter.HighQualityAntialiasing
SMOOTH_PIXMAP_TRANSFORM      = QPainter.SmoothPixmapTransform
NON_COSMETIC_PEN             = QPainter.NonCosmeticDefaultPen

NO_BRUSH                     = Qt.NoBrush                                                # Brush

NO_PEN                       = Qt.NoPen                                                  # Pen
ROUND_CAP                    = Qt.RoundCap
ROUND_JOIN                   = Qt.RoundJoin

PATTERN_SOLID                = Qt.SolidPattern                                           # Pattern

LINE_SOLID                   = Qt.SolidLine                                              # Line
LINE_DASH                    = Qt.DashLine
LINE_DOT                     = Qt.DotLine
LINE_DASH_DOT                = Qt.DashDotDotLine

TRANSPARENT                  = Qt.transparent
TRANSPARENT_MODE             = Qt.TransparentMode

# -------------------------------------------------------------------------------------------------------------
""" Meta Object """

QUEUEDCONNECTION             = Qt.QueuedConnection


# -------------------------------------------------------------------------------------------------------------
""" Keyboard and cursor """

TEXT_BOLD                   = QFont.Bold
TEXT_NORMAL                 = QFont.Normal
MONO_SPACE                  = QFont.Monospace

TEXT_MENEOMIC               = Qt.TextShowMnemonic


KEY_PRESS                   = QEvent.KeyPress
KEY_RELEASE                 = QEvent.KeyRelease
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
MOVE_OPERATION              = QTextCursor.MoveOperation
MOVE_ANCHOR                 = QTextCursor.MoveMode.MoveAnchor
KEEP_ANCHOR                 = QTextCursor.MoveMode.KeepAnchor

ACTION_MOVE                 = Qt.MoveAction                                             # Action

ignoreARM                   = Qt.IgnoreAspectRatio
# -------------------------------------------------------------------------------------------------------------
""" Set number """

RELATIVE_SIZE               = Qt.RelativeSize                                           # Size

INI                         = QSettings.IniFormat
NATIVE                      = QSettings.NativeFormat
INVALID                     = QSettings.InvalidFormat
SYS_SCOPE                   = QSettings.SystemScope
USER_SCOPE                  = QSettings.UserScope


AUTH_TOKEN_ENVVAR = 'GITHUB_AUTH_TOKEN'

DEFAULT_CONFIG_FILE = os.path.join(CFG_DIR, 'default.cfg')

PROJECT_CONFIG_FILE = os.path.join(DEFAULT_CONFIG_FILE, '.{0}.toml'.format(__envKey__))

DEFAULT_RELEASES_DIRECTORY = 'docs/releases'

IS_WINDOWS = 'win32' in str(sys.platform).lower()

DRAFT_OPTIONS = ['--dry-run', '--verbose', '--no-commit', '--no-tag', '--allow-dirty', ]

STAGE_OPTIONS = ['--verbose', '--allow-dirty', '--no-commit', '--no-tag']

COMMIT_TEMPLATE = 'git commit --message="%s" %s/__init__.py CHANGELOG.md'

TAG_TEMPLATE = 'git tag %s %s --message="%s"'

EXT_TO_MIME_TYPE = {'.gz': 'application/x-gzip', '.whl': 'application/zip', '.zip': 'application/zip', }

ISSUE_ENDPOINT = 'https://api.github.com/repos{/owner}{/repo}/issues{/number}'

LABELS_ENDPOINT = 'https://api.github.com/repos{/owner}{/repo}/labels'

RELEASES_ENDPOINT = 'https://api.github.com/repos{/owner}{/repo}/releases'

VERSION_ZERO = semantic_version.Version('0.0.0')

TOOLS = ['git', 'diff', 'python']

TEST_RUNNERS = ['pytest', 'nose', 'tox']

README_EXTENSIONS = ['.md', '.rst', '.txt', '.wiki', '.rdoc', '.org', '.pod', '.creole', '.textile',]

GITHUB_MERGED_PULL_REQUEST = re.compile(r'^([0-9a-f]{5,40}) Merge pull request #(\w+)')



# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved