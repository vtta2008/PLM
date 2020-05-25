# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
from .Gui import Color, Font, Painter
from .Core import Qt, DateTime
from .Widgets import LineEdit, GraphicsItem, GraphicsScene, GraphicsView, PlainTextEdit, RubberBand
import os


from PyQt5.QtWidgets import QSizePolicy, QFrame, QStyle, QAbstractItemView
from PyQt5.QtCore import QEvent


DAMG_LOGO_COLOR         = Color(0, 114, 188, 255)

# Basic color
WHITE                   = Color(Qt.white)
LIGHTGRAY               = Color(Qt.lightGray)
GRAY                    = Color(Qt.gray)
DARKGRAY                = Color(Qt.darkGray)
BLACK                   = Color(Qt.black)
RED                     = Color(Qt.red)
GREEN                   = Color(Qt.green)
BLUE                    = Color(Qt.blue)
DARKRED                 = Color(Qt.darkRed)
DARKGREEN               = Color(Qt.darkGreen)
DARKBLUE                = Color(Qt.darkBlue)
CYAN                    = Color(Qt.cyan)
MAGENTA                 = Color(Qt.magenta)
YELLOW                  = Color(Qt.yellow)
DARKCYAN                = Color(Qt.darkCyan)
DARKMAGENTA             = Color(Qt.darkMagenta)
DARKYELLOW              = Color(Qt.darkYellow)

# Dark Palette color
COLOR_BACKGROUND_LIGHT = Color('#505F69')
COLOR_BACKGROUND_NORMAL = Color('#32414B')
COLOR_BACKGROUND_DARK = Color('#19232D')

COLOR_FOREGROUND_LIGHT = Color('#F0F0F0')
COLOR_FOREGROUND_NORMAL = Color('#AAAAAA')
COLOR_FOREGROUND_DARK = Color('#787878')

COLOR_SELECTION_LIGHT = Color('#148CD2')
COLOR_SELECTION_NORMAL = Color('#1464A0')
COLOR_SELECTION_DARK = Color('#14506E')

# Nice color
blush               = Color(246, 202, 203, 255)
petal               = Color(247, 170, 189, 255)
petunia             = Color(231, 62, 151, 255)
deep_pink           = Color(229, 2, 120, 255)
melon               = Color(241, 118, 110, 255)
pomegranate         = Color(178, 27, 32, 255)
poppy_red           = Color(236, 51, 39, 255)
orange_red          = Color(240, 101, 53, 255)
olive               = Color(174, 188, 43, 255)
spring              = Color(227, 229, 121, 255)
yellow              = Color(255, 240, 29, 255)
mango               = Color(254, 209, 26, 255)
cantaloupe          = Color(250, 176, 98, 255)
tangelo             = Color(247, 151, 47, 255)
burnt_orange        = Color(236, 137, 36, 255)
bright_orange       = Color(242, 124, 53, 255)
moss                = Color(176, 186, 39, 255)
sage                = Color(212, 219, 145, 255)
apple               = Color(178, 215, 140, 255)
grass               = Color(111, 178, 68, 255)
forest              = Color(69, 149, 62, 255)
peacock             = Color(21, 140, 167, 255)
teal                = Color(24, 157, 193, 255)
aqua                = Color(153, 214, 218, 255)
violet              = Color(55, 52, 144, 255)
deep_blue           = Color(15, 86, 163, 255)
hydrangea           = Color(150, 191, 229, 255)
sky                 = Color(139, 210, 244, 255)
dusk                = Color(16, 102, 162, 255)
midnight            = Color(14, 90, 131, 255)
seaside             = Color(87, 154, 188, 255)
poolside            = Color(137, 203, 225, 255)
eggplant            = Color(86, 5, 79, 255)
lilac               = Color(222, 192, 219, 255)
chocolate           = Color(87, 43, 3, 255)
blackout            = Color(19, 17, 15, 255)
stone               = Color(125, 127, 130, 255)
gravel              = Color(181, 182, 185, 255)
pebble              = Color(217, 212, 206, 255)
sand                = Color(185, 172, 151, 255)



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


datetTimeStamp                              = DateTime.currentDateTime().toString("hh:mm - dd MMMM yy")             # datestamp


PRS =       dict(password    = LineEdit.Password,       center = center ,   left  = left   ,    right  = right,
                 spmax       = SiPoMax           ,       sppre  = SiPoPre,   spexp = SiPoExp,    spign  = SiPoIgn,
                 expanding   = QSizePolicy.Expanding,    spmin  = SiPoMin,)


dockL                       = Qt.LeftDockWidgetArea                                             # Docking area
dockR                       = Qt.RightDockWidgetArea
dockT                       = Qt.TopDockWidgetArea
dockB                       = Qt.BottomDockWidgetArea
dockAll                     = Qt.AllDockWidgetAreas



# -------------------------------------------------------------------------------------------------------------
""" Event """

NO_WRAP                     = PlainTextEdit.NoWrap
NO_FRAME                    = PlainTextEdit.NoFrame
ELIDE_RIGHT                 = Qt.ElideRight
ELIDE_NONE                  = Qt.ElideNone


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
ITEMMOVEABLE                = GraphicsItem.ItemIsMovable
ITEMSENDGEOCHANGE           = GraphicsItem.ItemSendsGeometryChanges
ITEMSCALECHANGE             = GraphicsItem.ItemScaleChange
ITEMPOSCHANGE               = GraphicsItem.ItemPositionChange
DEVICECACHE                 = GraphicsItem.DeviceCoordinateCache
SELECTABLE                  = GraphicsItem.ItemIsSelectable
MOVEABLE                    = GraphicsItem.ItemIsMovable
FOCUSABLE                   = GraphicsItem.ItemIsFocusable
PANEL                       = GraphicsItem.ItemIsPanel

NOINDEX                     = GraphicsScene.NoIndex                                    # Scene

RUBBER_DRAG                 = GraphicsView.RubberBandDrag                              # Viewer
RUBBER_REC                  = RubberBand.Rectangle
POS_CHANGE                  = GraphicsItem.ItemPositionChange

NODRAG                      = GraphicsView.NoDrag
NOFRAME                     = GraphicsView.NoFrame
ANCHOR_NO                   = GraphicsView.NoAnchor

ANCHOR_UNDERMICE            = GraphicsView.AnchorUnderMouse
ANCHOR_CENTER               = GraphicsView.AnchorViewCenter

CACHE_BG                    = GraphicsView.CacheBackground

UPDATE_VIEWRECT             = GraphicsView.BoundingRectViewportUpdate
UPDATE_FULLVIEW             = GraphicsView.FullViewportUpdate
UPDATE_SMARTVIEW            = GraphicsView.SmartViewportUpdate
UPDATE_BOUNDINGVIEW         = GraphicsView.BoundingRectViewportUpdate
UPDATE_MINIMALVIEW          = GraphicsView.MinimalViewportUpdate

STAY_ON_TOP                 = Qt.WindowStaysOnTopHint
STRONG_FOCUS                = Qt.StrongFocus
SPLASHSCREEN                = Qt.SplashScreen
FRAMELESS                   = Qt.FramelessWindowHint
CUSTOMIZE                   = Qt.CustomizeWindowHint
CLOSEBTN                    = Qt.WindowCloseButtonHint
MINIMIZEBTN                 = Qt.WindowMinimizeButtonHint
AUTO_COLOR                  = Qt.AutoColor

# -------------------------------------------------------------------------------------------------------------
""" Drawing """

ANTIALIAS                   = Painter.Antialiasing                                     # Painter
ANTIALIAS_TEXT              = Painter.TextAntialiasing
ANTIALIAS_HIGH_QUALITY      = Painter.HighQualityAntialiasing
SMOOTH_PIXMAP_TRANSFORM     = Painter.SmoothPixmapTransform
NON_COSMETIC_PEN            = Painter.NonCosmeticDefaultPen

NO_BRUSH                    = Qt.NoBrush                                                # Brush

NO_PEN                      = Qt.NoPen                                                  # Pen
ROUND_CAP                   = Qt.RoundCap
ROUND_JOIN                  = Qt.RoundJoin

PATTERN_SOLID               = Qt.SolidPattern                                           # Pattern

LINE_SOLID                  = Qt.SolidLine                                              # Line
LINE_DASH                   = Qt.DashLine
LINE_DOT                    = Qt.DotLine
LINE_DASH_DOT               = Qt.DashDotDotLine

TRANSPARENT                 = Qt.transparent
TRANSPARENT_MODE            = Qt.TransparentMode

# -------------------------------------------------------------------------------------------------------------
""" Meta Object """

QUEUEDCONNECTION            = Qt.QueuedConnection


# -------------------------------------------------------------------------------------------------------------
""" Keyboard and cursor """

TEXT_BOLD                   = Font.Bold
TEXT_NORMAL                 = Font.Normal
MONO_SPACE                  = Font.Monospace

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

ACTION_MOVE                 = Qt.MoveAction                                             # Action

ignoreARM                   = Qt.IgnoreAspectRatio
# -------------------------------------------------------------------------------------------------------------
""" Set number """

RELATIVE_SIZE               = Qt.RelativeSize                                           # Size









# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved