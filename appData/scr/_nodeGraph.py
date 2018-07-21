# -*- coding: utf-8 -*-
"""
Script Name: _setting.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsScene, QGraphicsView, QRubberBand
from PyQt5.QtGui import QPainter, QColor

POSX = 0
POSY = 0

NODE_WIDTH = 200
NODE_ROUND = 10
NODE_BORDER = 2
NODE_REC = 30
NODE_STAMP = 25

NODE_HEADER_HEIGHT = 25
NODE_FOOTER_HEIGHT = 25

ATTR_HEIGHT = 30
ATTR_ROUND = NODE_ROUND/2
ATTR_REC = NODE_REC/2

RADIUS = 10
COL = 10
ROW = 10
GRID_SIZE = 50

FLTR = 'flow_left_to_right'
FRTL = 'flow_right_to_left'

MARGIN = 20
ROUNDNESS = 0
THICKNESS = 1
CURRENT_ZOOM = 1

ASPEC_RATIO = Qt.KeepAspectRatio

# QGraphicsItem - FLAG
ITEMMOVEABLE = QGraphicsItem.ItemIsMovable
ITEMSENDGEOCHANGE = QGraphicsItem.ItemSendsGeometryChanges
ITEMSCALECHANGE = QGraphicsItem.ItemScaleChange
ITEMPOSCHANGE = QGraphicsItem.ItemPositionChange
DEVICECACHE = QGraphicsItem.DeviceCoordinateCache
SELECTABLE = QGraphicsItem.ItemIsSelectable
MOVEABLE = QGraphicsItem.ItemIsMovable
FOCUSABLE = QGraphicsItem.ItemIsFocusable
PANEL = QGraphicsItem.ItemIsPanel

# QPainter
ANTIALIAS = QPainter.Antialiasing
ANTIALIAS_TEXT = QPainter.TextAntialiasing
ANTIALIAS_HIGH_QUALITY = QPainter.HighQualityAntialiasing
SMOOTH_PIXMAP_TRANSFORM = QPainter.SmoothPixmapTransform
NON_COSMETIC_PEN = QPainter.NonCosmeticDefaultPen

# Brush: painter.setBrush()
BRUSH_NONE = Qt.NoBrush

# Pen: painter.setPen()
PEN_NONE = Qt.NoPen

# Pattern
PATTERN_SOLID = Qt.SolidPattern

# Line
LINE_SOLID = Qt.SolidLine

# Cursor
ARROW_NONE = Qt.NoArrow
CURSOR_ARROW = Qt.ArrowCursor
CURSOR_SIZEALL = Qt.SizeAllCursor

# Size
RELATIVE_SIZE = Qt.RelativeSize

# Color
WHITE = Qt.white
LIGHTGRAY = Qt.lightGray
GRAY = Qt.gray
DARKGRAY = Qt.darkGray
BLACK = Qt.black

RED = Qt.red
GREEN = Qt.green
BLUE = Qt.blue

DARKRED = Qt.darkGreen
DARKGREEN = Qt.darkGreen
DARKBLUE = Qt.darkBlue

CYAN = Qt.cyan
MAGENTA = Qt.magenta
YELLOW = Qt.yellow

DARKCYAN = Qt.darkCyan
DARKMAGENTA = Qt.darkMagenta
DARKYELLOW = Qt.darkYellow

# Keyboard
KEYBOARD = Qt.Key
KEY_ALT = Qt.Key_Alt
KEY_DEL = Qt.Key_Delete
KEY_TAB = Qt.Key_Tab
KEY_SHIFT = Qt.Key_Shift
KEY_CTRL = Qt.Key_Control
KEY_BACKSPACE = Qt.Key_Backspace
KEY_F = Qt.Key_F
KEY_S = Qt.Key_S
ALT_MODIFIER = Qt.AltModifier
CTRL_MODIFIER = Qt.ControlModifier
SHIFT_MODIFIER = Qt.ShiftModifier
NO_MODIFIER = Qt.NoModifier
CLOSE_HAND_CUSOR = Qt.ClosedHandCursor

windows = os.name = 'nt'
DMK = Qt.AltModifier if windows else CTRL_MODIFIER

# Mouse button
MOUSEBTN = Qt.MouseButton
MOUSE_LEFT = Qt.LeftButton
MOUSE_RIGHT = Qt.RightButton
MOUSE_MIDDLE = Qt.MiddleButton

# Scrollbar
SCROLLBAROFF = Qt.ScrollBarAlwaysOff
SCROLLBARON = Qt.ScrollBarAlwaysOn
SCROLLBARNEED = Qt.ScrollBarAsNeeded

# Scene Index
NOINDEX = QGraphicsScene.NoIndex

# Viewer
RUBBER_DRAG = QGraphicsView.RubberBandDrag
RUBBER_REC = QRubberBand.Rectangle
POS_CHANGE = QGraphicsItem.ItemPositionChange

NODRAG = QGraphicsView.NoDrag
NOFRAME = QGraphicsView.NoFrame
NOANCHOR = QGraphicsView.NoAnchor

ANCHOR_UNDERMICE = QGraphicsView.AnchorUnderMouse
ANCHOR_VIEWCENTER = QGraphicsView.AnchorViewCenter

CACHE_BG = QGraphicsView.CacheBackground

UPDATE_VIEWRECT = QGraphicsView.BoundingRectViewportUpdate
UPDATE_FULLVIEW = QGraphicsView.FullViewportUpdate
UPDATE_SMARTVIEW = QGraphicsView.SmartViewportUpdate
UPDATE_BOUNDINGVIEW = QGraphicsView.BoundingRectViewportUpdate
UPDATE_MINIMALVIEW = QGraphicsView.MinimalViewportUpdate

# action event
ACTION_MOVE = Qt.MoveAction

NODE = dict(

    width = NODE_WIDTH,
    height= 25,
    radius= 10,
    border= 2,
    attHeight= 30,
    con_width= 2,

    font= 'Arial',
    font_size= 12,
    attFont= 'Arial',
    attFont_size= 10,
    mouse_bounding_box= 80,

    alternate= 20,
    grid_color= [50, 50, 50, 255],
    slot_border= [50, 50, 50, 255],
    non_connectable_color= [100, 100, 100, 255],
    connection_color= [255, 155, 0, 255],
)

SCENE = dict(

    width = 2000,
    height = 2000,
    size = 36,
    antialiasing = True,
    antialiasing_boost = True,
    smooth_pixmap = True,

)

COLOR_CODE = dict(
    blush = QColor(246, 202, 203, 255),
    petal = QColor(247, 170, 189, 255),
    petunia = QColor(231, 62, 151, 255),
    deep_pink = QColor(229, 2, 120, 255),
    melon = QColor(241, 118, 110, 255),
    pomegranate = QColor(178, 27, 32, 255),
    poppy_red = QColor(236, 51, 39, 255),
    orange_red = QColor(240, 101, 53, 255),
    olive = QColor(174, 188, 43, 255),
    spring = QColor(227, 229, 121, 255),
    yellow = QColor(255, 240, 29, 255),
    mango = QColor(254, 209, 26, 255),
    cantaloupe = QColor(250, 176, 98, 255),
    tangelo = QColor(247, 151, 47, 255),
    burnt_orange = QColor(236, 137, 36, 255),
    bright_orange = QColor(242, 124, 53, 255),
    moss = QColor(176, 186, 39, 255),
    sage = QColor(212, 219, 145, 255),
    apple = QColor(178, 215, 140, 255),
    grass = QColor(111, 178, 68, 255),
    forest = QColor(69, 149, 62, 255),
    peacock = QColor(21, 140, 167, 255),
    teal = QColor(24, 157, 193, 255),
    aqua = QColor(153, 214, 218, 255),
    violet = QColor(55, 52, 144, 255),
    deep_blue = QColor(15, 86, 163, 255),
    hydrangea = QColor(150, 191, 229, 255),
    sky = QColor(139, 210, 244, 255),
    dusk = QColor(16, 102, 162, 255),
    midnight = QColor(14, 90, 131, 255),
    seaside = QColor(87, 154, 188, 255),
    poolside = QColor(137, 203, 225, 255),
    eggplant = QColor(86, 5, 79, 255),
    lilac = QColor(222, 192, 219, 255),
    chocolate = QColor(87, 43, 3, 255),
    blackout = QColor(19, 17, 15, 255),
    stone = QColor(125, 127, 130, 255),
    gravel = QColor(181, 182, 185, 255),
    pebble = QColor(217, 212, 206, 255),
    sand = QColor(185, 172, 151, 255),
    )

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 15/06/2018 - 7:50 PM
# © 2017 - 2018 DAMGteam. All rights reserved